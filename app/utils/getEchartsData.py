from app.utils import getPublicData
import datetime
travelInfoList = getPublicData.getAllTravelInfoMapData()

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
    for travel in travelInfoList:
        if cityDic.get(travel.level, -1) == -1:
            cityDic[travel.level] = 1
        else:
            cityDic[travel.level] += 1
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
