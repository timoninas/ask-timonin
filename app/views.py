from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

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

def new_questions(request):

    pag_questions = paginate(questions, request)

    return render(request, 'new_questions.html', {
        'questions': pag_questions,
        'tags': tags,
    })

def hot_questions(request):

    pag_questions = paginate(questions, request)

    return render(request, 'hot_questions.html', {
        'questions': pag_questions,
        'tags': tags,
    })

def question_page(request, pk):
    question = questions[pk].copy()

    pag_comments = paginate(question['comments'], request)

    question['comments'] = pag_comments

    return render(request, 'question_page.html', {
        'question': question,
        'tags': tags,
    })

def tag_questions(request):

    pag_questions = paginate(questions, request)

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
    filtered_questions = []

    for question in questions:
        if (has(question['tag'], pk)):
            filtered_questions.append(question)

    tag_questions = paginate(filtered_questions, request)

    return render(request, 'tag_questions.html', {
        'questions': tag_questions,
        'tag': pk,
        'tags': tags,
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
