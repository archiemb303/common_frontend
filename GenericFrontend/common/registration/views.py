from django.shortcuts import render
from rest_framework.views  import APIView
from rest_framework.response import Response

# Create your views here.


class AuthenticateAPI(APIView):
    def post(self,request,format='json'):
        input_json = request.data
        output_json = {}
        output_json['Status'] = "Success"
        output_json['Message'] = "API authentication done"
        return Response(output_json)
