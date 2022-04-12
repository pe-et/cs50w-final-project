from django.urls import path

from . import views

urlpatterns = [
    path('', views.market, name='market'),
    path('buy', views.buy, name='buy'),
    path('sell', views.sell, name='sell'),
    path('analysis', views.analysis, name='analysis'),
    path('transactions', views.transactions, name='transactions'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
]
