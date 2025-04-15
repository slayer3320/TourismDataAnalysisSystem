#render函数用于将数据渲染到指定的模板中，并返回生成的HTML内容
#redirect允许你将用户从一个URL重定向到另一个URL，通常用于处理单表提交、用户登录、注册等操作后的页面跳转

import jieba
from django.shortcuts import render,redirect
from django.http import JsonResponse
from app.models import User,TravelInfo
from django.http import HttpResponse
from app.recommdation import getUser_ratings,user_bases_collaborative_filtering
from app.utils import errorResponse,getHomeData,getPublicData,getChangeSelfInfoData,getAddCommentsData,getEchartsData,getRecommendationData,check_tables

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            User.objects.get(username=username, password=password)
            request.session['username'] = username
            return redirect('/app/home')

        except:
            return errorResponse.errorResponse(request,'账号或密码错误')


def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        try:
            User.objects.get(username=username)
        except:
            if not username or not password or not confirmPassword:return errorResponse.errorResponse(request,'不允许为空值')
            if  password != confirmPassword:return errorResponse.errorResponse(request,'两次密码不一致')
            User.objects.create(username=username,password=password)
            return redirect('/app/login')

        return errorResponse.errorResponse(request,'该账号已存在')

def logOut(request):
    request.session.clear() #退出登录时，清除request.session
    return redirect('/app/login') #退出登录 转到登陆页面

def home(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    a5Len,commentsLenTitle,provienceDicSort = getHomeData.getHomeTagData()
    scoreTop10Data,saleCountTop10 = getHomeData.getAnthorData()
    year,mon,day = getHomeData.getNowTime()
    geoData = getHomeData.getGeoData()
    userBarCharData = getHomeData.getUserCreateTimeData()
    #字典
    return render(request,'home.html',{
        'userInfo':userInfo,
        'a5Len':a5Len,
        'commentsLenTitle':commentsLenTitle,
        'provienceDicSort':provienceDicSort,
        'scoreTop10Data':scoreTop10Data,
        'nowTime':{
            'year':year,
            'mon':getPublicData.monthList[mon - 1],
            'day':day
        },
        'geoData':geoData,
        'userBarCharData':userBarCharData,
        'saleCountTop10':saleCountTop10
    })

def changeSelfInfo(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year,mon,day = getHomeData.getNowTime()
    if request.method == 'POST':
        getChangeSelfInfoData.changeSelfInfo(username,request.POST,request.FILES)
        userInfo = User.objects.get(username=username)

    return render(request,'changeSelfInfo.html',{
        'userInfo':userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
    })

def changePassword(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    if request.method == 'POST':
        res = getChangeSelfInfoData.getChangePassword(userInfo,request.POST)
        if res != None:
            return errorResponse.errorResponse(request,res)

    return render(request, 'changePassword.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
    })

def tableData(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    talbeData = getPublicData.getAllTravelInfoMapData()
    return render(request, 'tableData.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
        'talbeData':talbeData
    })

def addComments(request,id):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    travelInfo = getAddCommentsData.getTravelById(id)
    if request.method == 'POST':
        getAddCommentsData.addComments({
            'id':id,
            'rate':int(request.POST.get('rate')),
            'content':request.POST.get('content'),
            'userInfo':userInfo,
            'travelInfo':travelInfo
        })
        return redirect('/app/tableData')
    return render(request, 'addComments.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
        'travelInfo':travelInfo,
        'id':id
    })

def cityChar(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    cities, counts = getEchartsData.cityCharDataOne()
    resultData = getEchartsData.cityCharDataTwo()
    return render(request, 'cityChar.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
        'city_data': {
            'cities': cities,
            'counts': counts
        },
        'cityCharTwoData': resultData
    })

def rateChar(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    provinceList = getPublicData.getProvinceList()
    cityList = getPublicData.getCityList(provinceList[0])
    travelList = getPublicData.getAllTravelInfoMapData(cityList[0] if cityList else None)
    charOneData = getEchartsData.getRateCharDataOne(travelList)
    charTwoData = getEchartsData.getRateCharDataTwo(travelList)
    if request.method == 'POST':
        travelList = getPublicData.getAllTravelInfoMapData(request.POST.get('province'))
        charOneData = getEchartsData.getRateCharDataOne(travelList)
        charTwoData = getEchartsData.getRateCharDataTwo(travelList)


    return render(request, 'rateChar.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
        'cityList':cityList,
        'charOneData':charOneData,
        'charTwoData':charTwoData
    })

def priceChar(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    provinceList = getPublicData.getProvinceList()
    cityList = getPublicData.getCityList()
    travelList = getPublicData.getAllTravelInfoMapData()
    xData,yData = getEchartsData.getPriceCharDataOne(travelList)
    x1Data,y1Data = getEchartsData.getPriceCharDataTwo(travelList)
    disCountPieData = getEchartsData.getPriceCharDataThree(travelList)
    return render(request, 'priceChar.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
        'cityList': cityList,
        'echartsData':{
            'xData':xData,
            'yData':yData,
            'x1Data':x1Data,
            'y1Data':y1Data,
            'disCountPieData':disCountPieData
        }
    })

def commentsChar(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    xData,yData = getEchartsData.getCommentsCharDataOne()
    commentsScorePieData = getEchartsData.getCommentsCharDataTwo()
    x1Data,y1Data = getEchartsData.getCommentsCharDataThree()
    return render(request, 'commentsChar.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
        'echartsData':{
            'xData':xData,
            'yData':yData,
            'commentsScorePieData':commentsScorePieData,
            'x1Data':x1Data,
            'y1Data':y1Data
        }
    })

def recommendation(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    
    # 获取筛选参数
    region = request.GET.get('region') or request.POST.get('region')
    min_price = request.GET.get('min_price') or request.POST.get('min_price')
    max_price = request.GET.get('max_price') or request.POST.get('max_price')
    score = request.GET.get('score') or request.POST.get('score')
    level = request.GET.get('level') or request.POST.get('level')
    
    try:
        min_price = float(min_price) if min_price else None
        max_price = float(max_price) if max_price else None
    except (ValueError, TypeError):
        min_price = max_price = None
    
    try:
        user_ratings = getUser_ratings()
        recommended_items = user_bases_collaborative_filtering(userInfo.id, user_ratings)
        resultDataList = getRecommendationData.getAllTravelByTitle(
            recommended_items,
            region=region,
            min_price=min_price,
            max_price=max_price,
            score=score,
            level=level
        )
    except:
        resultDataList = getRecommendationData.getRandomTravel(
            region=region,
            min_price=min_price,
            max_price=max_price,
            score=score,
            level=level
            # types=types
        )

    # 获取地区列表用于下拉框
    provinceList = getPublicData.getProvinceList()
    cityList = getPublicData.getCityList()

    return render(request, 'recommendation.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
        'resultDataList': resultDataList,
        'cityList': cityList,
        'filter_params': {
            'region': region,
            'min_price': min_price,
            'max_price': max_price,
            'score': score,
            'level': level
        }
    })

def detailIntroCloud(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    return render(request, 'detailIntroCloud.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        }
    })

def commentContentCloud(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    return render(request, 'commentContentCloud.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        }
    })

def citySidebarAnalysis(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    
    # 获取城市列表
    provinceList = getPublicData.getProvinceList()
    if not provinceList:  # 如果省份列表为空
        provinceList = ['直辖市', '港澳台', '海南', '浙江', '广东']  # 默认省份列表
    cityList = getPublicData.getCityList(provinceList[0]) if provinceList else []
    
    # 确保provinceList和cityList不为None
    provinceList = provinceList or []
    cityList = cityList or []
    
    # 默认选择第一个城市
    selectedCity = request.GET.get('city', cityList[0] if cityList else '北京')
    
    # 获取选定城市的景点数据
    from app.utils.fetch_data import fetch_scenic_spots_by_city

    # 获取选定城市的景点列表(只包含景区名、等级、评分和价格)
    travelList = check_tables.get_scenic_spots_list(selectedCity)
    travelList = [{
        'id': travel[0],
        'name': travel[1], 
        'grade': travel[2], 
        'score': travel[3], 
        'ticket_price': travel[4],
        'image_url': travel[5],
        'address': travel[6],
        'type': travel[7],
        'intro': travel[8],
        'heat': travel[9],
        'comments': travel[10],
    } for travel in travelList]
    
    # 获取星级占比数据
    starRatioData = check_tables.get_star_ratio(selectedCity)
    
    # 获取价格分析数据
    priceAnalysisData = check_tables.get_price_analysis(selectedCity)
    priceAnalysisXData = [str(price) for price, _ in priceAnalysisData]
    priceAnalysisYData = [count for _, count in priceAnalysisData]
    
    # 生成景点词云数据
    wordCloudData = []
    if travelList:
        # 计算各指标的最大值用于标准化
        max_heat = max(travel['heat'] for travel in travelList if travel['heat']) or 1
        max_comments = max(travel['comments'] for travel in travelList if travel['comments']) or 1
        max_score = 5  # 评分最大为5分
        
        for travel in travelList:
            # 计算综合评分
            grade_weight = 0
            if travel['grade'] == '5A':
                grade_weight = 1.0
            elif travel['grade'] == '4A':
                grade_weight = 0.7
            else:
                grade_weight = 0.3
                
            # 标准化处理各指标
            normalized_heat = (travel['heat'] or 0) / max_heat
            normalized_comments = (travel['comments'] or 0) / max_comments
            normalized_score = (travel['score'] or 0) / max_score
            
            # 综合评分 = 热度*0.4 + 评论数*0.3 + 评分*0.2 + 等级*0.1
            composite_score = (
                normalized_heat * 0.4 + 
                normalized_comments * 0.3 + 
                normalized_score * 0.2 + 
                grade_weight * 0.1
            ) * 100
            
            # 确保评分在10-100范围内
            composite_score = max(10, min(100, composite_score))
            
            wordCloudData.append({
                'name': travel['name'],
                'value': composite_score,
                'itemStyle': {
                    'color': f'rgb({int(255 * (1 - composite_score/100))}, {int(255 * (composite_score/100))}, 150)'
                }
            })

    # 评论词云数据暂时为空
    commentCloudData = []
    
    # 调试信息
    print(f"景点数量: {len(travelList)}")
    print(f"词云数据数量: {len(wordCloudData)}")
    if wordCloudData:
        print(f"示例词云数据: {wordCloudData[0]}")

    print(f"词云数据: {wordCloudData}")  # 添加调试信息
    return render(request, 'citySidebarAnalysis.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
        'provinceList': provinceList,
        'cityList': cityList,
        'selectedCity': selectedCity,
        'travelList': travelList,
        'starRatioData': starRatioData,
        'priceAnalysisXData': priceAnalysisXData,
        'priceAnalysisYData': priceAnalysisYData,
        'wordCloudData': wordCloudData,
        'commentCloudData': commentCloudData
    })

def travelDetail(request, id):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    
    # 获取景点详细信息
    travel = check_tables.get_scenic_spots_list_by_id(id)
    travelList = [{
        'id': travel[0],
        'name': travel[1], 
        'grade': travel[2], 
        'score': travel[3], 
        'ticket_price': travel[4],
        'image_url': travel[5],
        'address': travel[6],
        'type': travel[7],
        'intro': travel[8],
        'heat': travel[9],
        'comments': travel[10],
    }]
    
    # 这里应该取列表中的第一个元素（字典）
    travel_data = travelList[0]
    
    return render(request, 'travelDetail.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
        'travel': {
            'id': travel_data['id'],
            'name': travel_data['name'],
            'grade': travel_data['grade'],
            'score': travel_data['score'],
            'ticket_price': travel_data['ticket_price'],
            'image_url': travel_data['image_url'],
            'address': travel_data['address'],
            'type': travel_data['type'],
            'intro': travel_data['intro'],
            'heat': travel_data['heat'],
            'comments': travel_data['comments'],
        }
    })

def ai_chat(request):
    return render(request, 'ai_chat.html')

def ai_chat_api(request):
    if request.method == 'POST':
        try:
            import json
            from django.http import JsonResponse, StreamingHttpResponse
            from time import sleep
            
            data = json.loads(request.body)
            message = data.get('message', '')
            
            def generate_response():
                if "北京" in message and "日游" in message:
                    days = message.split("日游")[0].split("北京")[1].strip()
                    content = f"为您推荐北京{days}日游行程：\n\n第一天：\n- 上午：天安门广场、故宫\n- 下午：景山公园俯瞰故宫全景\n- 晚上：王府井步行街\n\n第二天：\n- 上午：颐和园\n- 下午：圆明园\n- 晚上：三里屯酒吧街\n\n第三天：\n- 上午：长城一日游（推荐八达岭或慕田峪）\n- 下午：返回市区，参观鸟巢、水立方\n\n小贴士：\n1. 故宫需提前预约门票\n2. 长城较远，建议包车或参加一日游\n3. 北京交通拥堵，请预留充足时间"
                else:
                    content = f"您好！我是SightSeekAI旅游助手。\n\n关于'{message}'，我可以为您提供以下帮助：\n1. 目的地推荐\n2. 行程规划\n3. 景点介绍\n4. 当地美食推荐\n5. 交通指南\n\n请告诉我您更具体的需求，例如：\n- '上海3日游推荐'\n- '北京必去景点'\n- '成都美食攻略'"
                
                for i in range(0, len(content), 10):
                    chunk = content[i:i+10]
                    yield json.dumps({
                        "choices": [{
                            "message": {
                                "content": chunk,
                                "role": "assistant"
                            }
                        }]
                    })
                    sleep(0.1)  # 模拟流式输出延迟

            return StreamingHttpResponse(generate_response(), content_type='application/json')
            
        except Exception as e:
            return JsonResponse({
                "error": str(e)
            }, status=500)
    
    return JsonResponse({
        "error": "只支持POST请求"
    }, status=405)

def get_cities(request):
    province = request.GET.get('province')
    city_list = getPublicData.getCityList(province)
    return JsonResponse(city_list, safe=False)

def debug_province_list(request):
    province_list = getPublicData.getProvinceList()
    return JsonResponse({
        'provinceList': province_list,
        'source': 'city.json' if province_list else 'default'
    }, safe=False)
