from app.utils.getPublicData import getAllTravelInfoMapData
import random

def getFilteredTravel(travelList=None, region=None, min_price=None, max_price=None, types=None):
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
            
        # 类型筛选 (需要模型中有type字段)
        # if types and travel.type not in types:
        #    continue
            
        filtered.append(travel)
    
    return filtered

def getAllTravelByTitle(traveTitleList, region=None, min_price=None, max_price=None, types=None):
    resultList = []
    for title in traveTitleList:
        for travel in getFilteredTravel(region=region, min_price=min_price, max_price=max_price, types=types):
            if title == travel.title:
                resultList.append(travel)
    return resultList

def getRandomTravel(region=None, min_price=None, max_price=None, types=None):
    travelList = getFilteredTravel(region=region, min_price=min_price, max_price=max_price, types=types)
    maxLen = len(travelList) - 1
    if maxLen < 0:
        return []
        
    resultList = []
    for i in range(min(10, maxLen + 1)):
        randomNum = random.randint(0, maxLen)
        resultList.append(travelList[randomNum])
    return resultList
