from django.db import models
from accounts.models import User

# Create your models here.

class Category(models.Model):
    description = models.CharField(max_length=60, verbose_name='Categoria')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.description

class Theme(models.Model):
    description = models.CharField(max_length=250,verbose_name='Tema')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoria', default=0)

    class Meta:
        db_table = 'theme'
    
    def __str__(self):
        return self.description

    # def __init__(self, *args, **kwargs):
    #     super(Theme, self).__init__(*args, **kwargs)
    #     #self.fields["user"].value = 2
    #     print(User.id)

class Question(models.Model):
    description = models.CharField(max_length=250, null=False, verbose_name='Questão')
    answer = models.CharField(max_length=500, verbose_name='Resposta')
    image = models.TextField(null=True, verbose_name='Imagem')
    public = models.BooleanField(verbose_name='Publica')
    created_at = models.DateTimeField(auto_now_add=True)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, verbose_name='Tema')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='usuários')

    class Meta:
        db_table = 'questions'
    
    def __str__(self):
        return self.description

class Difficults_options(models.IntegerChoices):
    EASY = 1
    MEDIUM = 2
    DIFFICULT = 3 

class Attempt(models.Model):
    attempt_number = models.IntegerField(null=False)
    attempt_date = models.DateTimeField(auto_now_add=True)
    got_it_right = models.BooleanField(verbose_name='acertou')
    difficult = models.IntegerField(choices=Difficults_options.choices, verbose_name='Dificuldade')
    question = models.ForeignKey(Question, on_delete=models.CASCADE,verbose_name='Questão')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='usuários')
    
    class Meta:
        db_table = 'attempts'

    def __str__(self):
        return self.question.description        
    


