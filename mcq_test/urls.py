from django.urls import path
from . import views 

app_name='mcq_test'
urlpatterns = [
    # path('/', views.login_view, name='login'), 
    path('create/name', views.create_test_page1, name='create_test_page1'), 
    path('create/ques/<int:tid>/', views.create_test_page2, name='create_test_page2'), 
    # path('logout/', views.logout_view, name='logout'), 
    # path('display/', views.display_test, name='display_test'), 
    # path('test/', include('mcq_test.urls')),
]