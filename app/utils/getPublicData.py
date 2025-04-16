from app.models import TravelInfo,User
import json
import os
from pypinyin import pinyin, Style

monthList = ['January','February','March','April','May','June','July','August','Suptember','October','November','December']

from .fetchCityJson import fetch_cities_from_mysql

# 初始化时从MySQL获取城市数据
cityList = []
try:
    from .fetchCityJson import get_city_data
    data = get_city_data()
    if data:
        # 转换新格式数据为旧格式兼容结构
        provinces = {}
        for city, province in data.items():
            if province not in provinces:
                provinces[province] = []
            provinces[province].append({'name': city, 'url': ''})
        
        cityList = [{'province': p, 'city': c} for p, c in provinces.items()]
except Exception as e:
    print(f"初始化城市数据失败: {str(e)}")
    cityList = []

def getProvinceList():
    """获取省份列表并按拼音排序"""
    try:
        from .fetchCityJson import get_city_data
        data = get_city_data()
        if not data:
            return []
            
        # 从数据获取不重复的省份列表
        province_list = list(set(data.values()))
        province_list.sort(key=lambda x: pinyin(x, style=Style.FIRST_LETTER)[0][0].lower())
        return province_list
    except Exception as e:
        print(f"获取省份列表出错: {str(e)}")
        return []

def getCityList(province_name=None):
    """获取城市列表，可按省份筛选并按拼音排序"""
    try:
        from .fetchCityJson import get_city_data
        data = get_city_data()
        if not data:
            return []
            
        if province_name:
            # 获取指定省份的城市
            city_list = [city for city, province in data.items() if province == province_name]
            city_list.sort(key=lambda x: pinyin(x, style=Style.FIRST_LETTER)[0][0].lower())
            return city_list
        else:
            # 获取所有城市
            city_list = list(data.keys())
            city_list.sort(key=lambda x: pinyin(x, style=Style.FIRST_LETTER)[0][0].lower())
            return city_list
    except Exception as e:
        print(f"获取城市列表出错: {str(e)}")
        return []

def getAllTravelInfoMapData(province=None):
    def map_fn(item):
        item.img_list = json.loads(item.img_list) #在数据库表中的img_list是json形式，这里使用同样需要转换回来成python字典
        item.comments = json.loads(item.comments)
        return item
    if province:
        travelList = TravelInfo.objects.filter(province=province)
    else:
        travelList = TravelInfo.objects.all()
    travelListMap = list(map(map_fn,travelList))
    return travelListMap

def getAllUsersInfoData():
    return User.objects.all()

def getAllCommentsData():
    travelList = getAllTravelInfoMapData()
    commentsList = []
    for travel in travelList:
        for comment in travel.comments:
            commentsList.append(comment)
    return commentsList
