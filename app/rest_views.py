from rest_framework import status, decorators, response, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

from .use_cases import *
from .serializers import ProfileSerializer

@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def login_view(request):
    if request.method == 'GET':
        user = login_user_case()
        serializer = ProfileSerializer(user, many=True)
        st = status.HTTP_200_OK
    elif request.method == 'POST':
        user = login_user_case(request, request.POST)
        serializer = ProfileSerializer(data=request.POST, many=True)
        if serializer.is_valid():
            st = status.HTTP_200_OK
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response('Error', status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data, status=st)

@api_view(['GET'])
def logout_view(request):
    logout_user_case(request)
    return Response('Logout', status=status.HTTP_202_ACCEPTED)