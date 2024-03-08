# from django.urls import path
# from .import views
from django.urls import path
from .views import RegisterView, SuccessView, IndexView, LoginView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('success/', SuccessView.as_view(), name='success'),
]