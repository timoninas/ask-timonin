from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout

from .models import *
from .forms import *


def paginate(objects, page, limit=10):
    if limit > 100:
        limit = 10

    paginator = Paginator(objects, limit)
    page = paginator.page(page)
    return page


def new_questions_case(page, limit):
    questions = Question.objects.newest()
    return paginate(questions, page, limit)


def create_question_case(data, user):
    form = AskForm(data)
    if form.is_valid():
        q = form.save(user.profile.id)
    else:
        q = form.errors
    return q


def hot_questions_case(page, limit):
    questions = Question.objects.hottest()
    return paginate(questions, page, limit)

def questions_by_tag_case(tag_title, page, limit):
    questions = Tag.objects.by_tag(tag_title)
    return paginate(questions, page, limit)


def question_by_id_case(qid, page, limit):
    question = Question.objects.by_id(qid)
    return question, paginate(question.answer.all(), page, limit)


def answer_list_case(qid, page, limit):
    answers = Comment.objects.filter(question_id=qid)
    return paginate(answers, page, limit)


def create_answer_case(data, user, qid):
    form = AnswerForm(data)
    if form.is_valid():
        a = form.save(qid, user.profile.id)
    else:
        a = form.errors
    return a


def users_list_case(page, limit):
    users = Profile.objects.all()
    return paginate(users, page, limit)


def user_id_case(uid):
    return get_object_or_404(Profile, id=uid)


def delete_user_case(uid):
    user = get_object_or_404(Profile, id=uid)
    Profile.objects.delete(user)


def settings_case(uid, data=None, files=None):
    if data is None:
        return SettingsForm().fields

    form = SettingsForm(data, files)
    if form.is_valid():
        user = form.save(uid)
    else:
        user = form.errors
    return user


def tags_list_case(page, limit):
    tags = Tag.objects.all()
    return paginate(tags, page, limit)


def create_user_case(request=None):
    if request is None:
        return SignupForm().fields

    form = SignupForm(request.POST, request.FILES)
    if form.is_valid():
        user = form.save()
        login(request, user)
    else:
        user = form.errors
    return user.profile

def login_user_case(request=None, data=None):
    if data is None:
        return LoginForm().fields

    form = LoginForm(data)
    if form.is_valid():
        user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(request, user)
    else:
        user = form.errors
    return user.profile

def logout_user_case(data):
    logout(data)