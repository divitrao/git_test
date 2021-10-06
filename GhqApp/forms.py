from django import forms
from django.forms import widgets
from django.forms.widgets import RadioSelect
from .models import Options, QuizAttemptAnswer
# from django import template
# register = template.library()

class AnswerForm(forms.ModelForm):
    user_answer = forms.ModelChoiceField(queryset=Options.objects.none(),
                                    widget=RadioSelect,
                                    required=True,
                                    label="")

    class Meta:
        model = QuizAttemptAnswer
        fields = ('user_answer',)

    def __init__(self, question, *args, **kwargs):
        super(AnswerForm,self).__init__(*args, **kwargs)
        self.fields['user_answer'] = forms.ChoiceField(choices=Options.objects.filter(question = question.id).\
                                                    values_list('id','option'),
                                                    widget=RadioSelect,
                                                    required=True,
                                              label="")
  


 
        