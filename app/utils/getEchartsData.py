from app.utils import getPublicData
import datetime
import json
import csv
from pathlib import Path
travelInfoList = getPublicData.getAllTravelInfoMapData()

def provinceCharDataOne():
    # Read city to province mapping
    city_json_path = Path(__file__).parent / 'city.json'
    with open(city_json_path, 'r', encoding='utf-8') as f:
        city_to_province = json.load(f)
    
    # Read city sights data
    csv_path = Path(__file__).parent / 'city_sights_counts_5A_4A.csv'
    province_data = {}
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            city = row['city']
            count = int(row['sights_count_5A_4A'])
            
            # Map city to province
            province = city_to_province.get(city)
            if not province:
                continue
                
            # Aggregate by province
            if province not in province_data:
                province_data[province] = 0
            province_data[province] += count
    
    # Convert to list of dicts sorted by count
    result = [{'name': k, 'value': v} for k, v in province_data.items()]
    result.sort(key=lambda x: x['value'], reverse=True)
    
    return result

def cityCharDataOne():
    import csv
    from pathlib import Path
    
    # Read data from city_sights_counts_5A_4A.csv
    csv_path = Path(__file__).parent / 'city_sights_counts_5A_4A.csv'
    city_data = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            city_data.append({
                'city': row['city'],
                'count': int(row['sights_count_5A_4A'])
            })
    
    # Sort by count in descending order first
    city_data.sort(key=lambda x: x['count'], reverse=True)
    
    # Then sort by city name pinyin first letter
    from pypinyin import lazy_pinyin
    city_data.sort(key=lambda x: lazy_pinyin(x['city'])[0][0])
    
    # Extract top 100 cities for better visualization
    top_cities = city_data[:100]
    
    return [x['city'] for x in top_cities], [x['count'] for x in top_cities]

def cityCharDataTwo():
    cityDic = {}
    other_levels = set()  # 记录所有非标准等级
    
    for travel in travelInfoList:
        # 标准化景点等级名称
        level = travel.level
        if level == '5A景区' or level == '5A':
            level = '5A'
        elif level == '4A景区' or level == '4A':
            level = '4A'
        elif level == '3A景区' or level == '3A':
            level = '3A'
        elif not level or level.strip() == '':
            level = '未评价'
        else:
            other_levels.add(level)  # 收集非标准等级
            level = '其他'
            
        if cityDic.get(level, -1) == -1:
            cityDic[level] = 1
        else:
            cityDic[level] += 1
    
    # 打印非标准等级信息
    if other_levels:
        print(f"其他类包含以下非标准等级: {', '.join(other_levels)}")
    
    resultData = []
    for key,value in cityDic.items():
        resultData.append({
            'name':key,
            'value':value
        })
    return resultData

def getRateCharDataOne(travelList):
    startDic = {}
    for travel in travelList:
        if startDic.get(travel.star, -1) == -1:
            startDic[travel.star] = 1
        else:
            startDic[travel.star] += 1
    resultData = []
    for key, value in startDic.items():
        resultData.append({
            'name': key,
            'value': value
        })
    return resultData


def getRateCharDataTwo(travelList):
    startDic = {}
    for travel in travelList:
        if startDic.get(travel.score, -1) == -1:
            startDic[travel.score] = 1
        else:
            startDic[travel.score] += 1
    resultData = []
    for key, value in startDic.items():
        resultData.append({
            'name': key,
            'value': value
        })
    return resultData

def getPriceCharDataOne(traveList):
    xData = ['免费','100元以内','200元以内','300元以内','400元以内','500元以内','500元以外']
    yData = [0 for x in range(len(xData))]
    for travel in traveList:
        price = float(travel.price)
        if price <= 10:
            yData[0] += 1
        elif price <= 100:
            yData[1] += 1
        elif price <= 200:
            yData[2] += 1
        elif price <= 300:
            yData[3] += 1
        elif price <= 400:
            yData[4] += 1
        elif price <= 500:
            yData[5] += 1
        elif price > 500:
            yData[6] += 1
    return xData,yData

def getPriceCharDataTwo(traveList):
    xData = [str(x * 300) + '份以内' for x in range(1,15)]
    yData = [0 for x in range(len(xData))]
    for travel in traveList:
        saleCount = float(travel.saleCount)
        for x in range(1,15):
            count = x * 300
            if saleCount <= count:
                yData[x - 1] += 1
                break

    return xData,yData


def getPriceCharDataThree(travelList):
    startDic = {}
    for travel in travelList:
        if startDic.get(travel.discount, -1) == -1:
            startDic[travel.discount] = 1
        else:
            startDic[travel.discount] += 1
    resultData = []
    for key, value in startDic.items():
        resultData.append({
            'name': key,
            'value': value
        })
    return resultData

def getCommentsCharDataOne():
    commentsList = getPublicData.getAllCommentsData()
    xData = []
    def get_list(date):
        return datetime.datetime.strptime(date,'%Y-%m-%d').timestamp()
    for comment in commentsList:
        xData.append(comment['date'])
    xData = list(set(xData))
    xData = list(sorted(xData,key=lambda x: get_list(x),reverse=True))
    yData = [0 for x in range(len(xData))]
    for comment in commentsList:
        for index,date in enumerate(xData):
            if comment['date'] == date:
                yData[index] += 1
    return xData,yData

def getCommentsCharDataTwo():
    commentsList = getPublicData.getAllCommentsData()
    startDic = {}
    for travel in commentsList:
        if startDic.get(travel['score'], -1) == -1:
            startDic[travel['score']] = 1
        else:
            startDic[travel['score']] += 1
    resultData = []
    for key, value in startDic.items():
        resultData.append({
            'name': key,
            'value': value
        })
    return resultData

def getCommentsCharDataThree():
    travelList = getPublicData.getAllTravelInfoMapData()
    xData = [str(x * 1000) + '条以内' for x in range(1, 20)]
    yData = [0 for x in range(len(xData))]
    for travel in travelList:
        saleCount = int(travel.commentsLen)
        for x in range(1, 20):
            count = x * 1000
            if saleCount <= count:
                yData[x - 1] += 1
                break
    return xData, yData
