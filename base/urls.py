from django.urls import path
from. import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('', views.home, name='home'),
    path('create-account/', views.CreateAccount, name='create-acc'),
    path('transaction/<str:ak>', views.Transactions, name='transaction'),
    path('transfer/<str:ak>/<str:pk>', views.Transfer, name='transfer'),
    path('transactions/', views.Transactionss, name='transactions')

]
