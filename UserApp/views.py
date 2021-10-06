from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from .models import CustomUser
from GhqApp.models import QuizTaken
import uuid


class HomeView(TemplateView):
    template_name = 'home.html'
    def dispatch(self, request, *args, **kwargs):
        user_session = self.request.session.get('ghq_user_session_id',None)
        if request.user.is_authenticated:
            print( self.request.session.get('ghq_user_session_id',None))
            if user_session is not None:
                if QuizTaken.objects.filter(id=uuid.UUID(user_session)).exists():
                    quiz_attempt = QuizTaken.objects.get(id=uuid.UUID(user_session))
                    quiz_attempt.user_id = request.user.id
                    quiz_attempt.save()
                    del self.request.session['ghq_user_session_id']

        elif request.GET.get('retest')=='True':
            user_session = self.request.session.get('ghq_user_session_id',None)
            if user_session is not None:
                del request.session['ghq_user_session_id']
            else:
                return redirect('user_app:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            attempted_quiz = QuizTaken.objects.filter(user=self.request.user.id).values('id')
            if len(attempted_quiz)>=1:
                context['result'] = attempted_quiz.first()['id']
            else:
                context['result'] = 0
        return context
        
        

class SignUpView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'new_signup.html'
    success_url = reverse_lazy('user_app:login')

    def form_valid(self, form):
        form.save()
        user_session = self.request.session.get('ghq_user_session_id',None)
        user_name = form.cleaned_data['username']
        if user_session is not None:
                if QuizTaken.objects.filter(id=uuid.UUID(user_session)).exists():
                    quiz_attempt = QuizTaken.objects.get(id=uuid.UUID(user_session))
                    quiz_attempt.user_id = CustomUser.objects.get(username=user_name).id
                    quiz_attempt.save()
                    del self.request.session['ghq_user_session_id']

        
        return super().form_valid(form)
