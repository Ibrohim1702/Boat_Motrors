from django.urls import path

from api.v1.auth.views import RegisView, StepOne, StepTwo, LoginView, ChangePass
from api.v1.category.views import CategoryView
from api.v1.delivery.views import Saler
from api.v1.product.views import ProductView, LikeDislike, LikeDis, Commentview
from api.v1.subctg.views import SubCtgView
from api.v1.basket.views import BasketView




urlpatterns = [
        path('category/', CategoryView.as_view()),
        path('category/<int:pk>/', CategoryView.as_view()),
        path('subctg/', SubCtgView.as_view()),
        path('subctg/<int:pk>/',SubCtgView.as_view()),
        path('register/', RegisView.as_view()),
        path('login/', LoginView.as_view()),
        path('likes/', LikeDislike.as_view()),
        path('like/', LikeDis.as_view()),

        path('product/', ProductView.as_view()),
        path('product/<int:pk>/', ProductView.as_view()),

        path('product/s/<int:sub>/', ProductView.as_view()),
        path('product/c/<int:ctg>/', ProductView.as_view()),


        path("add_pro/<int:pk>/", BasketView.as_view()),

        path('stepone/', StepOne.as_view()),
        path('steptwo/', StepTwo.as_view()),
        path('basket/', BasketView.as_view()),
        path('change/', ChangePass.as_view()),
        path('comment/', Commentview.as_view()),
        path('comment/<int:pk>/', Commentview.as_view()),

        path('saler/', Saler.as_view())

]
