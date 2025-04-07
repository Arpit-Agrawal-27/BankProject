from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login_view,name='login'),
    path('signup/',views.register_user,name='signup'),
    path('register/', views.register_user, name='register_user'),
    path('registration-success/', views.registration_success, name='registration_success'),
    path('user-login/', views.create_userlogin_view, name='userlogin'),
    path('dashboard/', views.bank_dashboard, name='bank_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('withdraw/', views.withdraw_view, name='withdraw'),
    path('transactions/', views.transaction_history, name='transaction_history'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('fund-transfer/', views.fund_transfer, name='fund_transfer'),
    path('delete-account/', views.delete_account, name='delete_account'),





    
    
]
