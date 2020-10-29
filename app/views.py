from django.http import HttpResponse
from django.shortcuts import render

questions = [
    {
        'id': idx,
        'title': f'title {idx}',
        'text': 'text text',
    } for idx in range(5)
]

def new_questions(request):
    return render(request, 'new_questions.html', {
        'questions': questions,
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
    return render(request, 'tag_questions.html', {})

def settings(request):
    return render(request, 'settings.html', {})

def question_page(request, pk):
    question = questions[pk];
    return render(request, 'question_page.html', {
        'question': question,
    })
