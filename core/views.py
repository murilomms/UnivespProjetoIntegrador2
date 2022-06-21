import asyncio
from unicodedata import category
from django.db import models
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from .forms import AttemptForm, ContactForm , QuestionForm, ThemeForm
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View, TemplateView, CreateView, DetailView, ListView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Question, Theme, Attempt, Category
from Include import TextToSpeachConverter
from django.utils.encoding import uri_to_iri
import urllib

User = get_user_model()

class IndexView(TemplateView):
    template_name = 'index.html'
index = IndexView.as_view()


@login_required
def contact(request):
    success = False        
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.send_mail()
        success = True

    context = {
        'form': form,
        'success': success
    }
    return render(request, 'contact.html', context)

def help(request):
    return render(request, 'help.html')

def file(request):
    return render(request, 'file.html')

def project(request):
    user  = request.user
    user_id = user.id
    current_user= User.objects.get(id=user_id)
    user_themes = current_user.theme_set.all()
    return render(request, 'project.html', {'themes': user_themes})

##Classe para acesso as informações da tabela Theme
# class ThemeListView(ListView):
#     model = Theme

# class ThemeDetailView(DetailView):
#     model = Theme

def list_theme(request):
    themes = Theme.objects.all()
    user  = request.user
    user_id = user.id
    current_user= User.objects.get(id=user_id)
    user_themes = current_user.theme_set.all()
    return render(request, 'themes.html', {'themes': user_themes})


def create_theme(request):
    form = ThemeForm(request.POST or None)
    user  = request.user
    user_id = user.id
    form.initial["user"] = user_id
    if form.is_valid():
        form.initial["user"] = user_id
        form.save()
        return redirect('list_theme')

    return render(request, 'themes-form.html', {'form': form})


def update_theme(request, id):
    theme = Theme.objects.get(id=id)
    form = ThemeForm(request.POST or None, instance=theme)
    user  = request.user
    user_id = user.id
    form.initial["user"] = user_id
    if form.is_valid():
        form.initial["user"] = user_id
        form.save()
        return redirect('list_theme')

    return render(request, 'themes-form.html', {'form': form, 'theme': theme})


def delete_theme(request, id):
    theme = Theme.objects.get(id=id)
    if request.method == 'POST':
        theme.delete()
        return redirect('list_theme')

    return render(request, 'theme-delete-form.html', {'theme': theme})


##Classe para acesso as informações da tabela Question
# class QuestionListView(ListView):
#     model = Question

# class QuestionDetailView(DetailView):
#     model = Question

def list_question(request):
    questions = Question.objects.all()
    user  = request.user
    user_id = user.id
    current_user= User.objects.get(id=user_id)
    user_questions = current_user.question_set.all()
    return render(request, 'questions.html', {'questions': user_questions})


def create_question(request):
    form = QuestionForm(request.POST or None)
    user  = request.user
    user_id = user.id
    form.initial["user"] = user_id
    if form.is_valid():
        form.initial["user"] = user_id
        form.save()
        return redirect('core:list_question')

    return render(request, 'questions-form.html', {'form': form})


def update_question(request, id):
    question = Question.objects.get(id=id)
    form = QuestionForm(request.POST or None, instance=question)
    user  = request.user
    user_id = user.id
    form.initial["user"] = user_id
    if form.is_valid():
        form.initial["user"] = user_id
        form.save()
        return redirect('core:list_question')

    return render(request, 'questions-form.html', {'form': form, 'question': question})


def delete_question(request, id):
    question = Question.objects.get(id=id)

    if request.method == 'POST':
        question.delete()
        return redirect('core:list_question')

    return render(request, 'question-delete-form.html', {'question': question})

##Classe para acesso as informações da tabela Attempt
# class AttemptListView(ListView):
#     model = Attempt

# class AttemptDetailView(DetailView):
#     model = Attempt

def list_attempt(request):
    questionCount = 0
    user  = request.user
    user_id = user.id
    current_user = User.objects.get(id=user_id)
    # attempts = Attempt.objects.filter(attempt_number=1,user=user_id)
    lastAttempt = current_user.attempt_set.order_by('-attempt_number')[0]
    attempts = Attempt.objects.filter(attempt_number=lastAttempt.attempt_number,user=user_id)
    Convert = TextToSpeachConverter.TextToSpeachConverterPyttsx3()

    # attempts = AttemptForm(request.POST or None, instance=antes)
    if request.POST:
        for value in request.POST:

            if (value != 'csrfmiddlewaretoken'):
                x = value.split("_")
                id = x[1]
                updateAttempt = Attempt.objects.get(id=id)
                #Ao salvar (finalizar a tentativa) fala a pergunta e as respostas.
                #Convert.ConvertAndPlay('Pergunta: ' + updateAttempt.question.description)
                #Convert.ConvertAndPlay('Resposta: ' + updateAttempt.question.answer)
             
                if (value == 'got-it-right_'+id):
                    updateAttempt.got_it_right = 1
                    updateAttempt.save()
                if (value == 'difficult_'+id):
                    updateAttempt.difficult = int(request.POST[value])
                    updateAttempt.save()

        return render(request, 'alert.html', {'no_record_check': 1})

    # Falar as perguntas geradas
    for attempt in attempts:
        Convert.ConvertAndPlay('Pergunta ' + str(questionCount) + ':' +  attempt.question.description)
        questionCount += 1

    return render(request, 'attempts.html', {'attempts': attempts})


def create_attempt(request):
    user  = request.user
    user_id = user.id

    current_user = User.objects.get(id=user_id)
    user_themes = current_user.theme_set.all()
    categories = Category.objects.all()
    if request.POST:
        quantidade_select = request.POST['quantidade_perguntas']
        themeId = request.POST['decks']
        categoryId = request.POST['categoria']
        publicQuestionsOn = 'aceita_publica' in request.POST
        theme = Theme.objects.get(id=themeId)
        themeCategory = Theme.objects.filter(category = categoryId)
        
        #verifica quantas tentativas (quiz) já foram geradas para este usuário, para pegar o valor da nova tentativa.
        if current_user.attempt_set.count() > 0:
            lastAttempt = current_user.attempt_set.order_by('-attempt_number')[0]
            if lastAttempt.attempt_number :
                thisAttempt = lastAttempt.attempt_number + 1
        else:
            thisAttempt = 1

        #Verifica se no formulário o usuário marcou que irá usar as perguntas publicas para querar seu quiz de estudo
        if publicQuestionsOn:
            questions = current_user.question_set.all().filter(theme=theme).order_by('?') | Question.objects.filter(public = 1).filter(theme__in=themeCategory).order_by('?')
            questions = questions.order_by('?')[:int(quantidade_select)]
        else:
            questions = current_user.question_set.all().filter(theme=theme).order_by('?')[:int(quantidade_select)]
        count = 0
        length = questions.count()
        if length <= 0:
            return render(request,'alert.html', {'no_record_check': 0})       
        
        for question in questions:
            attempt = Attempt(attempt_number = int(thisAttempt), got_it_right=0 , difficult=0,question=question, user = current_user)
            attempt.save()
            count += 1
            if count == length:
                return redirect('list_attempt') 

    return render(request, 'create_attempts.html', {'themes': user_themes, 'categories': categories})

def readText(request):
   # print (request.GET)
    decodeTextUrl = urllib.parse.unquote(str(request.GET['text']))
    Convert = TextToSpeachConverter.TextToSpeachConverterPyttsx3()
    #print('----------------------------+++++++++------------------')
    #print(urllib.parse.unquote(str(request.GET['text'])))
    Convert.ConvertAndPlay(decodeTextUrl)
    data={'valor':'teste'}
    return JsonResponse(data)


