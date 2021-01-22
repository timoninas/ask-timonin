from rest_framework import status, decorators, response, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

from .use_cases import *
from .serializers import *

@api_view(['GET', 'POST'])
def index_view(request):
    if request.method == 'GET':
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        questions = new_questions_case(page, limit)
        serializer = QuestionSerializer(questions, many=True)
        st = status.HTTP_200_OK
    elif request.method == 'POST':
        question = create_question_case(request.POST, request.user)
        serializer = QuestionSerializer(question)
        if serializer.is_valid():
            st = status.HTTP_201_CREATED
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response('Error', status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data, status=st)

@api_view(['GET'])
def hot_view(request):
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    questions = hot_questions_case(page, limit)
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def question_id_view(request, qid):
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    question, answers = question_by_id_case(qid, page, limit)
    print(question)
    print(answers)
    if question is None:
        return Response('Error', status=status.HTTP_400_BAD_REQUEST)
    qserializer = QuestionSerializer(question)
    aserializer = AnswerSerializer(answers, many=True)
    data = {"question": qserializer.data, "answers": aserializer.data }
    return Response(data)

@api_view(['GET', 'POST'])
def question_answer_view(request, qid):
    if request.method == 'GET':
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        answers = answer_list_case(qid, page, limit)
        serializer = AnswerSerializer(answers, many=True)
        st = status.HTTP_200_OK
    elif request.method == 'POST':
        answer = create_answer_case(request.POST, request.user, qid)
        serializer = AnswerSerializer(answer)
        if serializer.is_valid():
            st = status.HTTP_201_CREATED
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response('Error', status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data, status=st)

@api_view(['GET'])
def users_view(request):
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    users = users_list_case(page, limit)
    serializer = ProfileSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET', 'DELETE'])
def user_id_view(request, uid):
    if request.method == 'GET':
        user = user_id_case(uid)
        serializer = ProfileSerializer(user)
        st = status.HTTP_200_OK
    elif request.method == 'DELETE':
        delete_user_case(uid)
        return Response('Deleted', status=status.HTTP_204_NO_CONTENT)
    else:
        return Response('Error', status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data, status=st)

@api_view(['GET', 'POST', 'PATCH'])
def settings_view(request):
    uid = request.user.id
    if request.method == 'GET':
        user = settings_case(uid)
        serializer = ProfileSerializer(user)
        st = status.HTTP_200_OK
    elif request.method == 'POST' or request.method == 'PATCH':
        user = settings_case(uid, request.POST, request.FILES)
        serializer = ProfileSerializer(user)
        if serializer.is_valid():
            st = status.HTTP_202_ACCEPTED
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response('Error', status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data, status=st)

@api_view(['GET'])
def tags_view(request):
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    tags = tags_list_case(page, limit)
    serializer = TagSerializer(tags, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def question_tag_view(request, slug):
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    questions = questions_by_tag_case(slug, page, limit)
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def signup_view(request):
    if request.method == 'GET':
        user = create_user_case()
        serializer = ProfileSerializer(user)
        st = status.HTTP_200_OK
    elif request.method == 'POST':
        user = create_user_case(request)
        serializer = ProfileSerializer(user)
        if serializer.is_valid():
            st = status.HTTP_201_CREATED
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response('Error', status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data, status=st)

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