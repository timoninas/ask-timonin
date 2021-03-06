# django
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import  get_object_or_404, render, redirect, reverse
from django.http import HttpResponse
from django.contrib import auth
from django.db.models import F

from django.views.decorators.http import require_POST

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser

# app
from app.models import Profile, Question, Comment, Tag
from app.forms import LoginForm, AskForm, SignupForm, CommentForm, SettingsForm, AvatarForm
from django.contrib import messages


class CreateUserAPIView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

def paginate(objects_list, request, per_page=5):
    limit = request.GET.get('limit', per_page)
    paginator = Paginator(objects_list, limit)
    page = request.GET.get('page')
    objects_page_list = paginator.get_page(page)
    return objects_page_list

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

@require_POST
@login_required
def vote(request):
    data = request.POST
    from pprint import pformat
    print('\n\n', '=' * 100)
    print(f'HERE: {pformat(data)}')
    print('=' * 100, '\n\n')
    return JsonResponse({'question_likes': 42})

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
    next_page = request.GET.get('next', '/')
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                print("\nFEFE\n")
                return redirect('/api/v1/')
        messages.error(request, 'Invalid username or password')
        print("\nKEKE\n")
        return redirect(next_page)


    return render(request, 'signin.html', {
        'tags': Tag.objects.popular(),
        'best_members': Profile.objects.best(),
        'form': form,
        'next': next_page
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
            return redirect('/api/v1/')
        messages.error(request, 'User already exist')
        return redirect('/api/v1/')

    return render(request, 'signup.html', {
        'tags': Tag.objects.popular(),
        'best_members': Profile.objects.best(),
        'form': form
    })

def signout(request):
    auth.logout(request)
    return redirect("signin")


@login_required
def settings(request):
    form_class = AvatarForm
    if request.method == 'GET':
        form = form_class()
    else:
        form = form_class(
            data=request.POST, files=request.FILES,
            instance=request.user.profile
        )
        if form.is_valid():
            form.save()
            return redirect(reverse('settings'))
    return render(request, 'settings.html', {
        'tags': Tag.objects.popular(),
        'best_members': Profile.objects.best(),
        'form': form
    })
