from app.models import TravelInfo,User
import json
import os
from pypinyin import pinyin, Style

monthList = ['January','February','March','April','May','June','July','August','Suptember','October','November','December']

cityList = []
with open(os.path.join(os.path.dirname(__file__), 'city.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)
    for province in data['city']:
        cities = [{'name': city['name'], 'url': city['url']} for city in province['city']]
        cityList.append({'province': province['name'], 'city': cities})

def getProvinceList():
    """获取省份列表并按拼音排序"""
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'city.json')
        print(f"尝试读取文件: {file_path}")  # 调试信息
        
        if not os.path.exists(file_path):
            print("city.json文件不存在")
            return []
            
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            province_list = [province['name'] for province in data['city']]
            province_list.sort(key=lambda x: pinyin(x, style=Style.FIRST_LETTER)[0][0].lower())
            return province_list
    except Exception as e:
        print(f"获取省份列表出错: {str(e)}")
        return []

def getCityList(province_name=None):
    """获取城市列表，可按省份筛选并按拼音排序"""
    with open(os.path.join(os.path.dirname(__file__), 'city.json'), 'r', encoding='utf-8') as f:
        data = json.load(f)
        if province_name:
            # 获取指定省份的城市
            for province in data['city']:
                if province['name'] == province_name:
                    city_list = [city['name'] for city in province['city']]
                    city_list.sort(key=lambda x: pinyin(x, style=Style.FIRST_LETTER)[0][0].lower())
                    return city_list
            return []
        else:
            # 获取所有城市
            city_list = [city['name'] for province in data['city'] for city in province['city']]
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
