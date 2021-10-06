from django.contrib import admin
from .models import QuizTaken, Question, Options, QuizAttemptAnswer

@admin.register(QuizTaken)
class QuizTakenAdmin(admin.ModelAdmin):
    pass

class OptionAdmin(admin.TabularInline):
    model = Options

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionAdmin]

@admin.register(Options)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['option', 'question', 'marks']

@admin.register(QuizAttemptAnswer)
class AttemptedAnswerAdmin(admin.ModelAdmin):
    pass

