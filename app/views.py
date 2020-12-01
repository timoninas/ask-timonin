from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from app.models import Profile, Question, Comment, Tag
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import F

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
<<<<<<< HEAD
    db_question = Question.objects.get(id=pk)
    comments = Comment.objects.newest(db_question.id)
    pag_comments = paginate(comments, request)

    # question['comments'] = pag_comments

    return render(request, 'question_page.html', {
        'question': db_question,
        'comments': pag_comments,
        'tags': Tag.objects.popular(),
        'best_members': Profile.objects.best()
    })

def tag_questions(request):

    pag_questions = paginate(questions, request)
=======
    question = questions[pk].copy()
>>>>>>> d24bf1c17df477c7adbb9252259ed7cc5befd1fd

    return render(request, 'tag_questions.html', {
        'questions': pag_questions,
        'tag': 'All tags',
        'tags': Tag.objects.popular(),
        'best_members': Profile.objects.best()
    })

def tag_questions(request):
    limit = request.GET.get('limit', 5)
    paginator = Paginator(questions, limit)
    page = request.GET.get('page')
    pag_questions = paginator.get_page(page)

    return render(request, 'tag_questions.html', {
        'questions': pag_questions,
        'tag': 'All tags',
        'tags': tags,
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

    limit = request.GET.get('limit', 5)
    paginator = Paginator(filtered_questions, limit)
    page = request.GET.get('page')
    tag_questions = paginator.get_page(page)

    return render(request, 'tag_questions.html', {
<<<<<<< HEAD
        'questions': questions,
        'tag': tag.title,
        'tags': Tag.objects.popular(),
        'best_members': Profile.objects.best()
    })

def ask_question(request):
    return render(request, 'ask_question.html', {
        'tags': Tag.objects.popular(),
        'best_members': Profile.objects.best()
    })

def signin(request):
    return render(request, 'signin.html', {
        'tags': Tag.objects.popular(),
        'best_members': Profile.objects.best()
    })

def signup(request):
    return render(request, 'signup.html', {
        'tags': Tag.objects.popular(),
        'best_members': Profile.objects.best()
    })


def settings(request):
    return render(request, 'settings.html', {
        'tags': Tag.objects.popular(),
        'best_members': Profile.objects.best()
=======
        'questions': tag_questions,
        'tag': pk,
        'tags': tags,
>>>>>>> d24bf1c17df477c7adbb9252259ed7cc5befd1fd
    })

def ask_question(request):
    return render(request, 'ask_question.html', {
        'tags': tags,
    })

def signin(request):
    return render(request, 'signin.html', {
        'tags': tags,
    })

def signup(request):
    return render(request, 'signup.html', {
        'tags': tags,
    })


def settings(request):
    return render(request, 'settings.html', {
        'tags': tags,
    })
