from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from sayt.base.format import categoryFormat
from sayt.models import Category


class CategoryView(GenericAPIView):
    def get(self, requests, pk=None, *args, **kwargs):
        category = ''
        if pk:
            category = categoryFormat(Category.objects.filter(pk=pk).first())
        if pk is None:
            l = Category.objects.all()
            category = []
            for i in l:
                category.append(categoryFormat(i))

        return Response({
            "result": category
        })

