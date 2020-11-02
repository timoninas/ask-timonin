from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

questions = [
    {
        'id': idx,
        'title': f'title {idx}',
        'text': 'text text',
        'tag': ['bender', 'cpp', 'bla', 'raytrace'],
    } for idx in range(15)
]

questions[0]['tag'].append('kke')
questions[1]['tag'].append('NoKke')

def new_questions(request):
    paginator = Paginator(questions, 5)
    page = request.GET.get('page')
    pag_questions = paginator.get_page(page)

    return render(request, 'new_questions.html', {
        'questions': pag_questions,
    })

def ask_question(request):
    return render(request, 'ask_question.html', {})

def signin(request):
    return render(request, 'signin.html', {})

def signup(request):
    return render(request, 'signup.html', {})

def answer_question(request):
    return render(request, 'answer_question.html', {})

def tag_questions(request):
    return render(request, 'tag_questions.html', {
        'questions': questions,
        'tag': 'All tags'
    })

def settings(request):
    return render(request, 'settings.html', {})

def question_page(request, pk):
    question = questions[pk];
    return render(request, 'question_page.html', {
        'question': question,
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

    return render(request, 'tag_questions.html', {
        'questions': filtered_questions,
        'tag': pk,
    })
