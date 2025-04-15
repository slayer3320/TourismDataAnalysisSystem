import pandas as pd
from sqlalchemy import create_engine, text
from snownlp import SnowNLP
from datetime import datetime, timedelta
import jieba.analyse

# 1. 数据库连接配置
engine = create_engine(
    "mysql+pymysql://root:tqkzT4olfaRImhlwgDiQZSiqwVNQDfZSOuyKwsGOvQc@47.109.193.153:8673/data"
)


# 2. 情感分析函数（优化异常处理）
def sentiment_analysis(text):
    try:
        return SnowNLP(text).sentiments if isinstance(text, str) else 0.5
    except:
        return 0.5  # 默认中性值


# 3. 核心推荐函数（完整修复版）
def recommend_attractions(params):
    """参数示例
    params = {
        'province': '广东',
        'city': '广州',
        'min_score': 4.0,
        'grade': '5A',
        'price_range': (0, 200),
        'travel_month': 7  # 需要确保是整数类型
    }
    """

    # 基础筛选SQL（使用参数化防止SQL注入）
    base_query = text(f"""
    SELECT s.*, c.province, c.city_name 
    FROM scenic_spots s
    JOIN city c ON s.city_id = c.id
    WHERE 
        (c.province = :province OR c.city_name = :city)
        AND s.score >= :min_score
        {"AND s.grade = :grade" if params.get('grade') else ''}
        AND s.ticket_price BETWEEN :price_low AND :price_high
    """)

    # 执行查询
    with engine.connect() as conn:
        df_base = pd.read_sql(
            base_query, conn,
            params={
                'province': params.get("province", ""),
                'city': params.get("city", ""),
                'min_score': params.get("min_score", 3.0),
                'grade': params.get("grade"),
                'price_low': params['price_range'][0],
                'price_high': params['price_range'][1]
            }
        )

    # 无结果时提前返回
    if df_base.empty:
        return []

    # 获取评论数据（使用chunk优化大数据量）
    spot_ids = tuple(df_base['id'].unique())
    reviews_query = text("""
    SELECT scenic_id, content, time, likes 
    FROM reviews 
    WHERE scenic_id IN :spot_ids
    """)

    df_reviews = pd.read_sql(
        reviews_query, engine,
        params={'spot_ids': spot_ids},
        chunksize=5000  # 分块读取优化内存
    )
    df_reviews = pd.concat(df_reviews) if df_reviews else pd.DataFrame()

    # 特征计算函数（全面异常处理）
    def calculate_features(group):
        # 时间分析
        try:
            time_series = pd.to_datetime(group['time'], errors='coerce')
            time_counts = time_series.dt.month.value_counts()
            peak_months = time_counts.nlargest(2).index.astype(int).tolist()
        except:
            peak_months = []

        # 情感分析（向量化优化）
        sentiments = group['content'].apply(
            lambda x: sentiment_analysis(x) if pd.notna(x) else 0.5
        )

        # 关键词提取（处理空内容）
        try:
            valid_content = group['content'].dropna().astype(str)
            keywords = jieba.analyse.extract_tags(
                ' '.join(valid_content),
                topK=5,
                withWeight=False
            ) if not valid_content.empty else []
        except:
            keywords = []

        # 近期评论量（时区敏感处理）
        try:
            time_threshold = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            recent_reviews = group[group['time'] > time_threshold].shape[0]
        except:
            recent_reviews = 0

        return pd.Series({
            'recent_reviews': recent_reviews,
            'avg_sentiment': sentiments.mean(),
            'peak_months': peak_months,
            'total_likes': group['likes'].sum(),
            'keywords': keywords
        })

    # 聚合特征（处理空评论数据）
    if not df_reviews.empty:
        df_features = df_reviews.groupby('scenic_id').apply(calculate_features).reset_index()
    else:
        df_features = pd.DataFrame(
            columns=['scenic_id', 'recent_reviews', 'avg_sentiment', 'peak_months', 'total_likes', 'keywords'])

    # 合并数据（处理可能的缺失）
    df_merged = df_base.merge(
        df_features,
        left_on='id',
        right_on='scenic_id',
        how='left'
    ).fillna({
        'recent_reviews': 0,
        'avg_sentiment': 0.5,
        'total_likes': 0
    })  # 不再填充列表类型字段

    # 强制类型转换（关键修复点）
    def ensure_list_type(series):
        return series.apply(
            lambda x: x.tolist() if isinstance(x, pd.Series)  # 处理合并产生的Series
            else (x if isinstance(x, list)  # 已有列表保持不变
                  else [])  # 其他类型转为空列表
        )

    df_merged['peak_months'] = ensure_list_type(df_merged['peak_months'])
    df_merged['keywords'] = ensure_list_type(df_merged['keywords'])

    # 时间匹配得分（类型安全校验）
    if params.get('travel_month'):
        try:
            target_month = int(params['travel_month'])
            df_merged['time_match'] = df_merged['peak_months'].apply(
                lambda x: 1.0 if target_month in x else 0.2
            )
        except:
            df_merged['time_match'] = 1.0
    else:
        df_merged['time_match'] = 1.0

    # 综合评分计算（动态权重）
    weights = {
        'heat': 0.3,
        'score': 0.25,
        'sentiment': 0.2,
        'time_match': 0.15,
        'price_ratio': 0.1
    }

    # 价格标准化
    max_price = df_merged['ticket_price'].max() or 1  # 避免除零错误
    df_merged['price_ratio'] = 1 - (df_merged['ticket_price'] / max_price)

    # 计算综合得分（处理NaN）
    df_merged['composite_score'] = (
            df_merged['heat'].fillna(0) * weights['heat'] +
            df_merged['score'].fillna(0) * weights['score'] +
            df_merged['avg_sentiment'].fillna(0.5) * weights['sentiment'] +
            df_merged['time_match'].fillna(1) * weights['time_match'] +
            df_merged['price_ratio'].fillna(0) * weights['price_ratio']
    )

    # 结果格式化
    final_columns = [
        'name', 'grade', 'score', 'ticket_price', 'address',
        'composite_score', 'keywords', 'peak_months', 'avg_sentiment'
    ]

    return (
        df_merged.sort_values('composite_score', ascending=False)
        .head(20)
        [final_columns]
        .assign(
            # 安全处理列表类型（二次校验）
            keywords=lambda df: df['keywords'].apply(
                lambda x: x[:3] if isinstance(x, list) else []
            ),
            peak_months=lambda df: df['peak_months'].apply(
                lambda x: sorted(x) if isinstance(x, list) else []
            )
        )
        .to_dict('records')
    )


# 使用示例
# if __name__ == "__main__":
#     params = {
#         'province': '广东',
#         'city': '广州',
#         'min_score': 4.0,
#         'grade': '5A',
#         'price_range': (0, 200),
#         'travel_month': 5  # 必须为整数
#     }

#     recommendations = recommend_attractions(params)
#     print("推荐结果：")
#     for idx, item in enumerate(recommendations, 1):
#         print(f"{idx}. {item['name']} | 综合评分：{item['composite_score']:.2f}")
#         print(
#             f"   关键词：{', '.join(item['keywords'][:3]) if item['keywords'] else '无'} | 最佳月份：{item['peak_months']}")
#         print(f"   情感得分：{item['avg_sentiment']:.2f} | 门票：{item['ticket_price']}元\n")