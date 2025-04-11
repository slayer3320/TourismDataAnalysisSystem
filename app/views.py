#render函数用于将数据渲染到指定的模板中，并返回生成的HTML内容
#redirect允许你将用户从一个URL重定向到另一个URL，通常用于处理单表提交、用户登录、注册等操作后的页面跳转

import jieba
from django.shortcuts import render,redirect
from django.http import JsonResponse
from app.models import User,TravelInfo
from django.http import HttpResponse
from app.recommdation import getUser_ratings,user_bases_collaborative_filtering
from app.utils import errorResponse,getHomeData,getPublicData,getChangeSelfInfoData,getAddCommentsData,getEchartsData,getRecommendationData

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
    Xdata,Ydata = getEchartsData.cityCharDataOne()
    resultData = getEchartsData.cityCharDataTwo()
    return render(request, 'cityChar.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
        'cityCharOneData':{
            'Xdata':Xdata,
            'Ydata':Ydata
        },
        'cityCharTwoData':resultData
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
    travelList = getPublicData.getAllTravelInfoMapData(selectedCity)
    
    # 计算星级占比数据
    starRatioDic = {}
    for travel in travelList:
        if starRatioDic.get(travel.level, -1) == -1:
            starRatioDic[travel.level] = 1
        else:
            starRatioDic[travel.level] += 1
    
    starRatioData = []
    for key, value in starRatioDic.items():
        starRatioData.append({
            'name': key if key else '未知',
            'value': value
        })
    
    # 计算价格分析数据
    priceAnalysisXData = ['免费', '100元以内', '200元以内', '300元以内', '400元以内', '500元以内', '500元以外']
    priceAnalysisYData = [0 for _ in range(len(priceAnalysisXData))]
    
    for travel in travelList:
        try:
            price = float(travel.price)
            if price <= 10:
                priceAnalysisYData[0] += 1
            elif price <= 100:
                priceAnalysisYData[1] += 1
            elif price <= 200:
                priceAnalysisYData[2] += 1
            elif price <= 300:
                priceAnalysisYData[3] += 1
            elif price <= 400:
                priceAnalysisYData[4] += 1
            elif price <= 500:
                priceAnalysisYData[5] += 1
            elif price > 500:
                priceAnalysisYData[6] += 1
        except ValueError:
            # 处理价格不是数字的情况
            pass
    
    # Prepare word cloud data from attraction titles
    wordCloudData = []
    title_counts = {}
    for travel in travelList:
        title = travel.title
        if title in title_counts:
            title_counts[title] += 1
        else:
            title_counts[title] = 1
    
    for title, count in title_counts.items():
        wordCloudData.append({
            'name': title,
            'value': count * 10  # Scale for better visualization
        })

    # Prepare word cloud data from comments
    commentCloudData = []
    comment_counts = {}
    for travel in travelList:
        try:
            comments = eval(travel.comments) if travel.comments else []
            for comment in comments:
                words = jieba.cut(comment['content'])
                for word in words:
                    if len(word) > 1:  # Only include words with 2+ characters
                        if word in comment_counts:
                            comment_counts[word] += 1
                        else:
                            comment_counts[word] = 1
        except:
            continue
    
    for word, count in comment_counts.items():
        commentCloudData.append({
            'name': word,
            'value': count * 5  # Scale for better visualization
        })

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
    travel = TravelInfo.objects.get(id=id)
    
    # 处理评论数据
    try:
        comments = eval(travel.comments) if travel.comments else []
    except:
        comments = []
    
    # 处理图片列表
    try:
        img_list = eval(travel.img_list) if travel.img_list else []
    except:
        img_list = []
    
    return render(request, 'travelDetail.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
        'travel': {
            'title': travel.title,
            'level': travel.level,
            'score': travel.score,
            'price': travel.price,
            'saleCount': travel.saleCount,
            'province': travel.province,
            'detailAddress': travel.detailAddress,
            'shortIntro': travel.shortIntro,
            'detailIntro': travel.detailIntro,
            'img_list': img_list,
            'comments': comments,
            'commentsLen': travel.commentsLen
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
