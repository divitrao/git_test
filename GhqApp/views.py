from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from UserApp.models import CustomUser
from .models import Options, QuizTaken, QuizAttemptAnswer, Question
from django.urls import reverse_lazy
from .forms import AnswerForm
import uuid
import json
from django.db.models import Sum



class QuestionDisplayView(FormView):
    form_class = AnswerForm
    template_name = 'question.html'

    def unanswered_question(self, session_id):
        self.answered_question = QuizAttemptAnswer.objects.filter(
                                                                quiz_taken=uuid.UUID(session_id)
                                                                ).values_list('question')
        return Question.objects.filter().exclude(id__in=self.answered_question)


    def dispatch(self, request, *args, **kwargs ):
        self.get_session = self.request.session.get('ghq_user_session_id',None)
        if request.user.is_authenticated:
                if self.get_session is None:
                    
                    new_test = QuizTaken.objects.create(user_id=self.request.user.id)
                    self.request.session['ghq_user_session_id'] = str(new_test.id)
                else:
                    if len(self.unanswered_question(self.get_session)) == 0:
                        return redirect('ghq_app:result',quiz_taken=self.request.session.get('ghq_user_session_id',None))
        
        else:
                
                if self.get_session is None:
                    new_test = QuizTaken.objects.create(user_id=CustomUser.objects.get(username='anonymous_user').id)
                    self.request.session['ghq_user_session_id'] = str(new_test.id)
                else:
                    if len(self.unanswered_question(self.get_session)) == 0:
                        return redirect('ghq_app:result',quiz_taken=self.request.session.get('ghq_user_session_id',None))
        
                

        return super().dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        
        self.question = self.unanswered_question(self.request.session.get('ghq_user_session_id',None))[0]
        return self.form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return dict(kwargs, question=self.question)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['total_questions'] = Question.objects.all().count()
        context['current_question_number'] = self.answered_question.count() + 1
        if context['current_question_number'] == 12:
            context['submit_button_name'] = 'Submit'
        else:
            context['submit_button_name'] = 'Next'
        context['question'] = self.question
        return context

    def form_valid(self, form):
        choosed_option = form.cleaned_data['user_answer']
        QuizAttemptAnswer.objects.create(
                            quiz_taken_id=QuizTaken.objects.get(id=uuid.UUID(self.request.session.get('ghq_user_session_id'))).id,
                            question_id = Question.objects.get(question=self.question).id,
                            answer_id = Options.objects.get(id=choosed_option).id,
                            user_answer =  Options.objects.get(id=choosed_option).option)


        
        return super().form_valid(form)

    def get_success_url(self):
        
        return reverse_lazy('ghq_app:questions')



class ResultView(TemplateView):
    template_name = 'result.html'

    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        data = {}
        data['current_result'] = []
        data['other_result'] = []
        if self.request.user.is_authenticated:
            quiz_taken = QuizTaken.objects.filter(user=self.request.user.id)\
                                                .exclude(id__in=[uuid.UUID(self.kwargs.get('quiz_taken'))])\
                                                .values_list('id','date_test_given')
            for j,k in quiz_taken:
                selected_options = QuizAttemptAnswer.objects.filter(quiz_taken=j).values('answer')
                marks_achieved = Options.objects.filter(id__in=selected_options).aggregate(Sum('marks'))['marks__sum']
                                                                
               
                data['other_result'].append([str(j),{'year':k.timetuple()[0],'month':k.timetuple()[1],
                                                     'day':k.timetuple()[2],'hour':k.timetuple()[3],'minute':k.timetuple()[4]},
                                                    {'marks_achieved':marks_achieved}])
            for i in range(1):
                user_result = QuizAttemptAnswer.objects.filter(quiz_taken=uuid.UUID(self.kwargs.get('quiz_taken')))\
                                                                .values_list('question','user_answer','answer')
                for j in user_result:
                    results = {}
                    results['question'] = Question.objects.get(id=j[0]).question
                    results['user_answer'] = j[1]
                    results['marks'] = Options.objects.get(id=j[2]).marks
                    data['current_result'].append(results)
                    
                
                
            


        else:
            data = {}
            data['current_result'] = []
            user_result = QuizAttemptAnswer.objects.filter(quiz_taken=uuid.UUID(self.kwargs.get('quiz_taken')))\
                                                                .values_list('question','user_answer','answer')
            for j in user_result:
                    results = {}
                    results['question'] = Question.objects.get(id=j[0]).question
                    results['user_answer'] = j[1]
                    results['marks'] = Options.objects.get(id=j[2]).marks
                    data['current_result'].append(results)
        current_username = QuizTaken.objects.get(id=uuid.UUID(self.kwargs.get('quiz_taken'))).user.username
        if  current_username=='anonymous_user'\
                and self.kwargs.get('quiz_taken')==self.request.session.get('ghq_user_session_id',None):
            context['save'] = True
        else:
            context['save'] = False
        context['data'] = json.dumps(data)
        context['username'] = QuizTaken.objects.get(id=uuid.UUID(self.kwargs.get('quiz_taken'))).user.username
        selected_options = QuizAttemptAnswer.objects.filter(
                                    quiz_taken=uuid.UUID(self.kwargs.get('quiz_taken'))).values('answer')
        context['marks_achieved'] = Options.objects.filter(id__in=selected_options).aggregate(Sum('marks'))['marks__sum']
        return context
        
