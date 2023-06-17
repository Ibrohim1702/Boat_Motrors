from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

# ctg bn, sub_ctg, product bn
from register.models import User
from sayt.base.format import productFormat, subctgFormat, commentFormat
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from sayt.models import Sub_ctg, Category, Product, Likes, Comment


class ProductView(GenericAPIView):

    def get(self, requests, sub=None, ctg=None, pk=None, *args, **kwargs):
        prod = Product.objects.all()
        l = []
        for i in prod:
            l.append(productFormat(i))


        if ctg:
            ctg_one = Category.objects.filter(pk=ctg).first()

            if not ctg_one:
                return Response({
                    "Error": "Bunaqa id li ctg topilmadi"
                })

            prod = Product.objects.filter(pk=ctg)
            l = []

            for i in prod:
                l.append(productFormat(i))

            return Response({
                "result": l
            })


        elif sub:

            subcategory = Sub_ctg.objects.filter(pk=sub).first()

            if not subcategory:
                return Response({
                    "Error": "Bunaqa id li subctg topilmadi"
                })

            subprod = Product.objects.filter(pk=sub)

            l = []
            for i in subprod:
                l.append(productFormat(i))

            return Response({
                "result": l
            })


        elif pk:
            product = Product.objects.filter(pk=pk).first()

            if not product:
                return Response({
                    "Error": "Bunaqa id li product topilmadi"
                })

            return Response({
                "result": productFormat(product)
            })
        else:


            return Response({
                "result": l
            })


class LikeDislike(GenericAPIView):
    authentication_classes = TokenAuthentication,
    permission_classes = IsAuthenticated,

    def post(self, requests, *args, **kwargs):
        data = requests.data

        if ('like' not in data and 'dislike' not in data) or "product_id" not in data:
            return Response({"error": "data to'lliq emas"})

        pro = Product.objects.filter(pk=data['product_id']).first()
        if not pro:
            return Response({'error': "bunaqa product yo'"})

        likes = Likes.objects.get_or_create(product=pro, user=requests.user)[0]

        if 'like' in data and 'dislike' in data:
            return Response({"error": "xato data"})

        like = likes.like
        dislike = likes.dislike

        if 'dislike' in data and data['dislike']:
            like = False
            dislike = True

        if 'like' in data and data['like']:
            like = True
            dislike = False

        likes.like = like
        likes.dislike = dislike
        likes.save()

        return Response({
            "tog'ri": likes.res()
        })


class LikeDis(GenericAPIView):
    authentication_classes = TokenAuthentication,
    permission_classes = IsAuthenticated,  # user -> requests.user

    def post(self, requests):
        data = requests.data
        if 'product_id' not in data or 'status' not in data:
            return Response({'error': "data tto'llimas"})

        pro = Product.objects.filter(pk=data['product_id']).first()
        if not pro:
            return Response({'error': "bunaqa product yo'"})

        likes = Likes.objects.get_or_create(product=pro, user=requests.user)[0]
        if data['status'] == 'like':
            likes.like = not likes.like
            likes.dislike = False
        if data['status'] == 'dislike':
            likes.like = False
            likes.dislike = not likes.dislike  # bazadagini teskarisiga alamshtiradi like->dis, dis->like
        likes.save()

        liked = Likes.objects.filter(like=True).count()
        dis = Likes.objects.filter(dislike=True).count()

        return Response({
            "tog'ri": likes.res(),
            "likes": liked,
            "dis": dis

        })


class Commentview(GenericAPIView):
    authentication_classes = TokenAuthentication,
    permission_classes = IsAuthenticated,

    def post(self, requests, *args, **kwargs):
        data = requests.data

        if "prod_id" not in data or 'comment' not in data:
            return Response({"Error:Product/Comment id berilmagan"})

        prod = Product.objects.filter(pk=data.get("prod_id")).first()

        if not prod:
            return Response({"Error": "Bunaqa id bn product topilmadi"})

        root = Comment.objects.create(user=requests.user, product=prod, text=data['comment'])
        root.save()
        return Response({"Success":"Kommentariya qo'shildi"})

    def get(self, requests, pk=None, *args, **kwargs):
        prod_id = Product.objects.filter(pk=pk).first()

        if not prod_id:
            return Response({"Error":"Bunaqa id li product topilmadi"})

        root = Comment.objects.filter(product=prod_id)
        l=[]
        for i in root:
            l.append(commentFormat(i))

        return Response({"Result": l})

