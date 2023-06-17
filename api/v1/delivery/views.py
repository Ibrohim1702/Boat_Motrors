from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from register.models import User
from sayt.models import Delivery


class Saler(GenericAPIView):
    authentication_classes = TokenAuthentication,
    permission_classes = IsAuthenticated,

    def post(self, requests, *args, **kwargs):
        data = requests.data

        nott = ["first_name", "last_name", "phone", "email", "signed_up", "agreement"]
        s = ''

        for i in nott:
            if i not in data:
                s += f",{i},"
        if s:
            return Response({
                "Error": f" There is no {s} in data "})

        if len(data['phone']) != 12:
            return Response({"Error": "Mobile phone must contain minimum 12 digits"})

        if not data['phone'].isdigit():
            return Response({"Error": "Mobile number must be in digits ! "})

        user = Delivery.objects.create(
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            email=data.get('email', ''),
            phone=data['phone'],
            signed_up=data.get("signed_up", False),
            agreement=data.get("agreement", False)

        )

        return Response({
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,

        })
