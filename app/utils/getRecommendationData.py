from app.utils.getPublicData import getAllTravelInfoMapData
import random

def getFilteredTravel(travelList=None, region=None, min_price=None, max_price=None, score=None, level=None, types=None):
    if travelList is None:
        travelList = getAllTravelInfoMapData()
    
    filtered = []
    for travel in travelList:
        # 地区筛选
        if region and travel.province != region:
            continue
            
        # 价格筛选
        try:
            price = float(travel.price)
            if min_price is not None and price < min_price:
                continue
            if max_price is not None and price > max_price:
                continue
        except ValueError:
            continue
            
        # 评分筛选
        try:
            travel_score = float(travel.score)
            if score is not None and travel_score < float(score):
                continue
        except ValueError:
            continue
            
        # 等级筛选（支持"5A"和"5A级"等格式）
        if level:
            if not travel.level or level not in travel.level:
                continue
            
        # 类型筛选 (需要模型中有type字段)
        # if types and travel.type not in types:
        #    continue
            
        filtered.append(travel)
    
    return filtered

def getAllTravelByTitle(traveTitleList, region=None, min_price=None, max_price=None, score=None, level=None, types=None):
    resultList = []
    for title in traveTitleList:
        for travel in getFilteredTravel(region=region, min_price=min_price, max_price=max_price, score=score, level=level, types=types):
            if title == travel.title:
                resultList.append(travel)
    return resultList

def getRandomTravel(region=None, min_price=None, max_price=None, score=None, level=None, types=None):
    travelList = getFilteredTravel(region=region, min_price=min_price, max_price=max_price, score=score, level=level, types=types)
    maxLen = len(travelList) - 1
    if maxLen < 0:
        return []
        
    resultList = []
    for i in range(min(10, maxLen + 1)):
        randomNum = random.randint(0, maxLen)
        resultList.append(travelList[randomNum])
    return resultList
