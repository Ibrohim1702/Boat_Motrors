import datetime
import random
import uuid

from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from register.models import User
# from sayt.base.helper import code_decoder
from sayt.models import OTP

from django.core.mail import send_mail
from django.http import HttpResponse


class RegisView(GenericAPIView):

    def post(self, requests, *args, **kwargs):
        data = requests.data

        nott = ["first_name", "last_name", "phone", "password", 'email']
        s = ''

        for i in nott:
            if i not in data:
                s += f" {i} "

        if s:
            return Response({
                "Error": f" Datada {s}  to`ldirilmagan"

            })

        if len(data['phone']) != 12:
            return Response({"Error": "Telefon raqam  12 tadan iborat bo`lishi kerak !"})

        if not data['phone'].isdigit():
            return Response({"Error": "Raqamlarni sonlarda kiriting"})

        if len(data['password']) < 6:
            return Response({"Error": "Parol juda oddiy"})

        user = User.objects.create_user(
            phone=data['phone'],
            email=data['email'],
            password=data.get('password', ''),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            region=data.get('region', ''),
        )

        token = Token.objects.get_or_create(user=user)[0]

        return Response({
            "Success": token.key,

        })


class LoginView(GenericAPIView):
    def post(self,  requests, *args, **kwargs):
        data = requests.data

        if data is None:
            return Response({
                "error": "data to'ldirilmagan"
            })

        nott = 'email' if 'email' not in data else 'password' if "password" not in data else None
        if nott:
            return Response({
                "Error": f"{nott} to`ldirilmagan"
            })
        user = User.objects.filter(email=data['email']).first()

        if not user:
            return Response({
                "Error": "Bunday foydalanuvchi afsuski yo`q."
            })
        if not user.check_password(data['password']):
            return Response({
                "Error": "Parol xato"
            })

        token = Token.objects.get_or_create(user=user)[0]

        return Response({
            "Success": token.key,
            "user": user.format()
        })


class StepOne(GenericAPIView):


    def post(self, requests, ):
        data = requests.data

        if "email" not in data:
            return Response({
                "Error": "Email kiritilmagan"
            })

        parol = random.randint(100000, 999999)
        # try:
        #     res = send_mail("Hacker", f"Maxfiy kalit: {parol}", settings.EMAIL_HOST_USER, [data['email']])
        # except Exception as e:
        #     return Response({
        #         "Error": e.__str__()
        #     })

        tokenn = uuid.uuid4().str() + uuid.uuid4().str() + str(parol)

        # shifr = code_decoder(tokenn)
        otp_token = OTP.objects.create(
            key=tokenn,
            email=data["email"],
            state="step-one",

        )

        return Response({
            "parol": parol,
            # "tokenn": tokenn,
            "otp_token": otp_token.key,

        })


class StepTwo(GenericAPIView):
    def post(self, requests, *args, **kwargs):
        data = requests.data

        if "token" not in data:
            return Response({
                "Error": "Token kiritilmagan"
            })

        elif "code" not in data:
            return Response({
                "Error": "Code kiritilmagan"
            })

        otp = OTP.objects.filter(key=data['token']).first()

        if not otp:
            return Response({
                "Error": "Bunaqa token mavjud emas"
            })

        if otp.is_expired:
            return Response({
                "Error": "Otp eskirgan"
            })

        now = datetime.datetime.now(datetime.timezone.utc)
        cr = otp.create_at

        if (now - cr).total_seconds() >= 120:
            otp.is_expired = True
            otp.save()
            return Response({
                "Error": "Yuborilgan raqam 2 daqiqa ichida kiritilishi kerak"
            })

        if otp.key[-6:] != str(data['code']):
            return Response({
                "Error": "Xato raqam kiritildi"
            })

        user = User.objects.filter(email=otp.email).first()
        return Response({
            "is_register": user is not None
        })



class ChangePass(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)  # ikkalasi userni ro'yhatdan o'tganligini tekshiradi

    def post(self, requests, *args, **kwargs):
        user = requests.user
        data = requests.data

        if "old" not in data:
            return Response({
                "Error": "eski parol kiritlmagan"
            })

        if not user.check_password(data['old']):
            return Response({
                "Error": "eski parol noto`g`ri kiritlgan"
            })

        if "new" not in data:
            return Response({
                "Error": "yangi qoymoqchi bo`lingan parol kiritilmagan"
            })


        user.set_password(data['new'])
        user.save()

        return Response({
            "Success": "parol o`zgartirildi"
        })

# like -> product->comment->post









