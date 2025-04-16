from app.models import TravelInfo,User
import json
import os
from pypinyin import pinyin, Style

monthList = ['January','February','March','April','May','June','July','August','Suptember','October','November','December']

def load_city_json():
    """从city.json加载城市数据"""
    try:
        with open(os.path.join(os.path.dirname(__file__), 'city.json'), 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载city.json失败: {str(e)}")
        return {}

# 初始化城市数据
city_data = load_city_json()
cityList = []
if city_data:
    # 转换数据格式
    provinces = {}
    for city, province in city_data.items():
        if province not in provinces:
            provinces[province] = []
        provinces[province].append({'name': city, 'url': ''})
    
    cityList = [{'province': p, 'city': c} for p, c in provinces.items()]

def getProvinceList():
    """获取省份列表并按拼音排序"""
    global city_data
    if not city_data:
        city_data = load_city_json()
    
    if not city_data:
        return []
        
    # 从数据获取不重复的省份列表
    province_list = list(set(city_data.values()))
    province_list.sort(key=lambda x: pinyin(x, style=Style.FIRST_LETTER)[0][0].lower())
    return province_list

def getCityList(province_name=None):
    """获取城市列表，可按省份筛选并按拼音排序"""
    global city_data
    if not city_data:
        city_data = load_city_json()
    
    if not city_data:
        return []
        
    if province_name:
        # 获取指定省份的城市
        city_list = [city for city, province in city_data.items() if province == province_name]
    else:
        # 获取所有城市
        city_list = list(city_data.keys())
    
    city_list.sort(key=lambda x: pinyin(x, style=Style.FIRST_LETTER)[0][0].lower())
    return city_list

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
