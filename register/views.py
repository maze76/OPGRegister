from django.shortcuts import render, redirect
from django.views import View
from .forms import CompanyForm, UserForm
from django.views.generic import TemplateView, FormView
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

class IndexView(TemplateView):
    template_name = "index.html"

class RegisterView(View):
    def get(self, request):
        company_form = CompanyForm()
        user_form = UserForm()
        return render(request, 'register.html', {'company_form': company_form, 'user_form': user_form})

    def post(self, request):
        company_form = CompanyForm(request.POST)
        user_form = UserForm(request.POST)
        
        if user_form.is_valid() and company_form.is_valid():
            # Save user data
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            user.save()

            # Save company data
            company = company_form.save(commit=False)
            company.user = user
            company.save()
            
            return redirect('login')  # Redirect to login page
        else:
            return render(request, 'register.html', {'company_form': company_form, 'user_form': user_form})

                                           
class SuccessView(TemplateView):
    template_name = 'success.html'

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = 'product_list'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request, "Korisničko ime i/ili lozinka su pogrešni! Molimo pokušajte ponovo.")
            return super().form_invalid(form)

    def get_success_url(self):
        return self.success_url

