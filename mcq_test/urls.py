from django.urls import path
from . import views 

app_name='mcq_test'
urlpatterns = [
    path('', views.login_view, name='login_view'), 
    path('logout/', views.logout_view, name='logout'), 
    path('faculty/', views.dashboard_faculty, name='dashboard_faculty'),
    path('faculty/test/<int:tid>/', views.display_test_faculty, name='display_test_faculty'),
    path('test/leaderboard/<int:tid>/', views.leaderboard, name='leaderboard'),
    path('student/', views.dashboard_student, name='dashboard_student'),
    path('create/name/', views.create_test_page1, name='create_test_page1'), 
    path('create/ques/<int:tid>/', views.create_test_page2, name='create_test_page2'), 
    path('test/<int:tid>/', views.test_view, name='test_view'), 
    # path('display/', views.display_test, name='display_test'), 
]