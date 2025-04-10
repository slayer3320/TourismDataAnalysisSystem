#主路由配置文件不处理用户具体路由，只做请求的分发，即分布式请求处理。具体的请求由各自应用进行处理
from django.urls import path
from app import views

urlpatterns = [
    path('login/',views.login, name='login'),
    path('register/',views.register, name='register'),
    path('logOut/',views.logOut, name='logOut'),
    path('home/',views.home, name='home'),
    path('changeSelfInfo/',views.changeSelfInfo, name='changeSelfInfo'),
    path('changePassword/',views.changePassword, name='changePassword'),
    path('tableData/',views.tableData, name='tableData'),
    path('addComments/<int:id>/',views.addComments, name='addComments'),
    path('cityChar/',views.cityChar, name='cityChar'),
    path('rateChar/',views.rateChar, name='rateChar'),
    path('priceChar/',views.priceChar, name='priceChar'),
    path('commentsChar/',views.commentsChar, name='commentsChar'),
    path('recommendation/',views.recommendation, name='recommendation'),
    path('detailIntroCloud/',views.detailIntroCloud, name='detailIntroCloud'),
    path('commentContentCloud/',views.commentContentCloud, name='commentContentCloud'),
    path('citySidebarAnalysis/',views.citySidebarAnalysis, name='citySidebarAnalysis'),
    path('travelDetail/<int:id>/',views.travelDetail, name='travelDetail'),
    path('ai/', views.ai_chat, name='ai_chat'),
]
