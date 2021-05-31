from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from SUNOSab.models import Register
from SUNOSab.serializers import RegisterSerializer
from rest_framework import status
# Create your views here.


@csrf_exempt
def registerApi(request,Id=0):
    if request.method=='GET':
        register = Register.objects.all()
        register_serializer = RegisterSerializer(register, many=True)
        return JsonResponse(register_serializer.data, safe=False)

    elif request.method=='POST':
        register_data=JSONParser().parse(request)
        register_serializer = RegisterSerializer(data=register_data)
        if register_serializer.is_valid():
            register_serializer.save()
            return JsonResponse("Added Successfully!!" , safe=False)
        return JsonResponse("Failed to Add.",safe=False)
    
    elif request.method=='PUT':
        register_data = JSONParser().parse(request)
        register=RegisterSerializer.objects.get(UserID=register_data['UserID'])
        register_serializer=RegisterSerializer(register,data=register_data)
        if register_serializer.is_valid():
            register_serializer.save()
            return JsonResponse("Updated Successfully!!", safe=False)
        return JsonResponse("Failed to Update.", safe=False)

    elif request.method == 'DELETE':
        count = Register.objects.get(UserID=Id).delete()
        return JsonResponse({'message': '{} Enteries were deleted successfully!'.format(count[0])})
 


