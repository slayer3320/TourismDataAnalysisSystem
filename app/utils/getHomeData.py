from app.utils import getPublicData
import random
import time

travelMapData = getPublicData.getAllTravelInfoMapData()
userData = getPublicData.getAllUsersInfoData()

#获取三个数据特征：”5A级景点的个数””评论最多的景区“”拥有景点最多的省份“
def getHomeTagData():
    a5Len = 0
    a4Len = 0
    commentsLenMax = 0
    commentsLenTitle = ''
    provienceDic = {}
    for travel in travelMapData:
        level = travel.level.replace('景区', '级')  # 统一转换为"5A级"格式
        if '5A' in level: a5Len += 1
        if '4A' in level: a4Len += 1
        comments_len = int(travel.commentsLen) if travel.commentsLen else 0
        if comments_len > commentsLenMax:
            commentsLenMax = comments_len
            commentsLenTitle = travel.title
        if provienceDic.get(travel.province,-1) == -1 : provienceDic[travel.province] = 1
        else:provienceDic[travel.province] += 1

    provienceDicSort = list(sorted(provienceDic.items(),key=lambda x:x[1],reverse=True))[0][0]

    return {'5A': a5Len, '4A': a4Len}, commentsLenTitle, provienceDicSort

def getAnthorData():
    scoreTop10 = []  #应该不止有10个，所以取随机
    for travel in travelMapData:
        if travel.score == '5':
            scoreTop10.append(travel)
    
    maxLen = len(scoreTop10)
    scoreTop10Data = []
    #random.randint(start, stop)返回在start和stop之间的随机整数
    for i in range(10):
        randomIndex = random.randint(0, maxLen - 1)
        scoreTop10Data.append(scoreTop10[randomIndex])

    saleCountTop10 = list(sorted(travelMapData,key=lambda x:int(x.saleCount) if x.saleCount else 0,reverse=True))[:10]

    return scoreTop10Data,saleCountTop10

#获取即时时间
def getNowTime():
    timeFormat = time.localtime()  #格式化时间戳为本地的时间，没有返回值
    year = timeFormat.tm_year
    mon = timeFormat.tm_mon
    day = timeFormat.tm_mday
    return year,mon,day

def getGeoData():
    import csv
    from pathlib import Path
    
    # Read data from province_sights_counts.csv
    csv_path = Path(__file__).parent / 'province_sights_counts.csv'
    geo_data = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            geo_data.append({
                'name': row['province'],
                'value': int(row['sights_count'])
            })
    
    return geo_data

def getUserCreateTimeData():
    dataDic = {}
    for user in userData:
        if dataDic.get(str(user.createTime),-1) == -1:
            dataDic[str(user.createTime)] = 1
        else:
            dataDic[str(user.createTime)] += 1

    resutData = []
    for key, value in dataDic.items():
        resutData.append({
            'name': key,
            'value': value
        })
    return resutData

def getProvince5ACount():
    provinceCount = {}
    for travel in travelMapData:
        level = travel.level.replace('景区', '级')
        if '5A' in level:
            if travel.province not in provinceCount:
                provinceCount[travel.province] = 0
            provinceCount[travel.province] += 1
    
    # 转换为前端需要的格式
    result = []
    for province, count in provinceCount.items():
        result.append({
            'name': province,
            'value': count
        })
    return sorted(result, key=lambda x: x['value'], reverse=True)
