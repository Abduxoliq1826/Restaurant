from django.urls import path
from .views import *
from .cashierviews import *
from .directorviews import *
from .managerviews import *
urlpatterns = [
    # waiter
    path('menu/', GetMenyu.as_view()),
    path('orderitem_create/', OrderItemcreate),
    path('order_create/', Ordercreated),
    path('update/<int:pk>/', Update),
    path('myaccaunt/', Myaccaunt),
    # cashier
    path('getall/<int:pk>/', GetAll.as_view()),
    path('close_order/<int:pk>/', CloseOrder),
    # manager
    path('register/', Register_waiters),
    path('login/', login_waiters),
    path('waiters/', all_waiters),
    path('cashiers/', all_cashiers),
    path('deletew/', delete_workers),
    path('statisticday/', statistic_day),
    path('statisticmonth/', statistic_month),
    path('statisticyear/', statistic_year),
    path('add_product/', AddProduct),
    # director

    path('delete/', delete_workers_director),
    path('money/', Spentmoney),
    path('allmoney/', all_money),
    path('registerwaiterd/', Register_waiters_for_director),
    path('loginwaitersd/', login_waiters_for_director),
    path('allwaitersd/', all_waiters_for_director),
    path('allcashiersd/', all_cashiers_for_director),
    path('allmanagersd/', all_managers),
    path('statisticdaydirector/', statistic_day_director),
    path('statisticmonthdirector/', statistic_month_director),
    path('statisticyeardirector/', statistic_year_director),
    path('give_me/', Quit),

]