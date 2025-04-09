from app.utils import getPublicData
import random
import time

travelMapData = getPublicData.getAllTravelInfoMapData()
userData = getPublicData.getAllUsersInfoData()

#获取三个数据特征：”5A级景点的个数””评论最多的景区“”拥有景点最多的省份“
def getHomeTagData():
    a5Len = 0
    commentsLenMax = 0
    commentsLenTitle = ''
    provienceDic = {}
    for travel in travelMapData:
        if travel.level == '5A景区':a5Len += 1
        if int(travel.commentsLen) > commentsLenMax:
            commentsLenMax = int(travel.commentsLen)
            commentsLenTitle = travel.title
        if provienceDic.get(travel.province,-1) == -1 : provienceDic[travel.province] = 1
        else:provienceDic[travel.province] += 1

    provienceDicSort = list(sorted(provienceDic.items(),key=lambda x:x[1],reverse=True))[0][0]

    return a5Len,commentsLenTitle,provienceDicSort

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

    saleCountTop10 = list(sorted(travelMapData,key=lambda x:int(x.saleCount),reverse=True))[:10]

    return scoreTop10Data,saleCountTop10

#获取即时时间
def getNowTime():
    timeFormat = time.localtime()  #格式化时间戳为本地的时间，没有返回值
    year = timeFormat.tm_year
    mon = timeFormat.tm_mon
    day = timeFormat.tm_mday
    return year,mon,day

def getGeoData():
    provinceAttractions = {}  # {province: set(attraction_names)}
    
    # First collect all unique attraction names per province
    for travel in travelMapData:
        if travel.province not in provinceAttractions:
            provinceAttractions[travel.province] = set()
        provinceAttractions[travel.province].add(travel.title)
    
    # Map provinces to their cityList provinces and count unique attractions
    dataDic = {}
    for province, attractions in provinceAttractions.items():
        for j in getPublicData.cityList:
            for city in j['city']:
                if city.find(province) != -1:
                    if j['province'] not in dataDic:
                        dataDic[j['province']] = 0
                    dataDic[j['province']] += len(attractions)
                    break  # Found matching city, move to next province

    return [{'name': province, 'value': count} for province, count in dataDic.items()]

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
