# django
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import  get_object_or_404, render, redirect, reverse
from django.http import HttpResponse
from django.contrib import auth
from django.db.models import F

# app
from app.models import Profile, Question, Comment, Tag
from app.forms import LoginForm, AskForm, SignupForm, CommentForm

comment1 = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, ' \
           'sed do eiusmod tempor incididunt ut labore et dolore magna aliqua'

comment2 = 'incididunt ut labore et dolore magna aliqua. ' \
           'Ut enim ad minim veniam, quis nostrud exercitation ullamco'

comment3 = 'Lorem ipsum dolor sit amet, consectetur adipiscing ' \
           'elit, sed do eiusmod tempor incididunt ut labore et ' \
           'dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco'

questions = [
    {
        'id': idx,
        'title': f'title {idx}',
        'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et',
        'tag': ['bender', 'cpp', 'bla', 'raytrace'],
        'comments': [comment1, comment2, comment3, comment1, comment2, comment3]
    } for idx in range(25)
]

# (some request).filter(status='Pending').count()
tags = ['cpp', 'c#', 'bender', 'kke', 'bla', 'python', 'django', 'ruby', 'swift']

questions[0]['tag'].append('kke')
questions[2]['tag'].append('kke')
questions[1]['tag'].append('NoKke')



def paginate(objects_list, request, per_page=5):
    limit = request.GET.get('limit', per_page)
    paginator = Paginator(objects_list, limit)
    page = request.GET.get('page')
    objects_page_list = paginator.get_page(page)
    return objects_page_list


# Question.objects.order_by(F('data_create').desc())     - new
# Question.objects.order_by(F('data_create').asc())      - old
def new_questions(request):

    db_question = Question.objects.newest()
    pag_questions = paginate(db_question, request)

    return render(request, 'new_questions.html', {
        'questions': pag_questions,
        'tags': Tag.objects.popular(),
        'best_members': Profile.objects.best()
    })

def hot_questions(request):

    db_question = Question.objects.hottest()
    pag_questions = paginate(db_question, request)

    return render(request, 'hot_questions.html', {
        'questions': pag_questions,
        'tags': Tag.objects.popular(),
        'best_members': Profile.objects.best()
    })

def question_page(request, pk):
    db_question = Question.objects.get(id=pk)
    comments = Comment.objects.newest(db_question.id)
    pag_comments = paginate(comments, request)

    if request.method == "GET":
        form = CommentForm()
    else:
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user.profile
            comment.question = db_question
            comment.save()
            return redirect(reverse('selectedquestion', kwargs={'pk': db_question.pk}))

    return render(request, 'question_page.html', {
        'question': db_question,
        'comments': pag_comments,
        'tags': Tag.objects.popular(),
        'best_members': Profile.objects.best(),
        'form': form
    })

def tag_questions(request):

    pag_questions = paginate(questions, request)

    return render(request, 'tag_questions.html', {
        'questions': pag_questions,
        'tag': 'All tags',
        'tags': Tag.objects.popular(),
        'best_members': Profile.objects.best()
    })

def has(array, element):
    for item in array:
        if (item == element):
            return True
    return False

def tag_page(request, pk):
    questions = Question.objects.filter(tags__title=pk)
    tag = Tag.objects.get(title=pk)

    # for question in questions:
    #     if (has(question['tag'], pk)):
    #         filtered_questions.append(question)
    #
    # tag_questions = paginate(filtered_questions, request)

    return render(request, 'tag_questions.html', {
        'questions': questions,
        'tag': tag.title,
        'tags': Tag.objects.popular(),
        'best_members': Profile.objects.best()
    })

@login_required
def ask_question(request):
    if request.method == "GET":
        form = AskForm()
    else:
        form = AskForm(data=request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user.profile
            question.save()
            return redirect(reverse('selectedquestion', kwargs={'pk': question.pk}))
    return render(request, 'ask_question.html', {
        'tags': Tag.objects.popular(),
        'best_members': Profile.objects.best(),
        'form': form
    })

def signin(request):
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect("/") # Нужен правильный редирект

    return render(request, 'signin.html', {
        'tags': Tag.objects.popular(),
        'best_members': Profile.objects.best(),
        'form': form
    })

def signup(request):
    if request.method == 'GET':
        form = SignupForm()
    else:
        form = SignupForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            auth.authenticate(request, **form.cleaned_data)
            profile = Profile(name=request.POST['username'], user=user)
            profile.save()
            return redirect("/")
            # return redirect(request.POST.get('next', '/'))


    return render(request, 'signup.html', {
        'tags': Tag.objects.popular(),
        'best_members': Profile.objects.best(),
        'form': form
    })

def signout(request):
    auth.logout(request)
    return redirect("signin")


def settings(request):
    return render(request, 'settings.html', {
        'tags': Tag.objects.popular(),
        'best_members': Profile.objects.best()
    })
