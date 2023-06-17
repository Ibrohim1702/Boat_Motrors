from django.shortcuts import redirect
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from register.models import User
from sayt.base.format import basketFormat
from sayt.models import Product, Basket


# class BasketView(GenericAPIView):
#     authentication_classes = TokenAuthentication,
#     permission_classes = IsAuthenticated,
#
#     def post(self, requests, *args, **kwargs):
#         data = requests.data
#
#         if "prod_id" not in data:
#             return Response({
#                 "Error": "Prod id berilmagan"
#             })
#
#         prod = Product.objects.filter(pk=data['prod_id']).first()
#
#         if prod:
#             baskett = Basket.objects.get_or_create(
#                 user=requests.user,
#                 product=prod,
#             )[0]
#
#             baskett.quantity = data.get('quantity', baskett.quantity)
#             baskett.save()
#
#             return Response({
#                 "result": basketFormat(baskett)
#             })
#
#         else:
#             return Response({
#                 "Error": "Noto'gri prod berilgan"
#             })
class BasketView(GenericAPIView):
    authentication_classes = TokenAuthentication,
    permission_classes = IsAuthenticated,

    def post(self, requests, *args, **kwargs):
        data = requests.data

        if "prod_id" not in data:
            return Response({
                "Error": "Prod id berilmagan"
            })

        prod = Product.objects.filter(pk=data['prod_id']).first()

        if prod:
            baskett = Basket.objects.get_or_create(
                user=requests.user,
                product=prod,
            )[0]

            baskett.quantity = data.get('quantity', baskett.quantity)
            baskett.save()

            return Response({
                "result": basketFormat(baskett)
            })

        else:
            return Response({
                "Error": "Noto'gri prod berilgan"
            })
