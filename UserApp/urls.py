from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, HomeView
from GHQ import settings

app_name = 'user_app'

urlpatterns = [ 
    path('', HomeView.as_view(), name='home'),
    path('accounts/register/', SignUpView.as_view(), name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='new_login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout')
]