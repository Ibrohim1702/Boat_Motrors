from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from sayt.base.format import subctgFormat
from sayt.models import Sub_ctg



class SubCtgView(GenericAPIView):

    def get(self, requests, pk=None, *args, **kwargs):
        subctg = ''

        if pk:
            subctg = subctgFormat(Sub_ctg.objects.filter(pk=pk).first())

        if pk is None:
            l = Sub_ctg.objects.all()
            subctg = []
            for i in l:
                subctg.append(subctgFormat(i))

        return Response({
            "result": subctg
        })
