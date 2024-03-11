from django.shortcuts import render, redirect
from django.views import View
from .forms import CompanyForm, UserForm, ProductForm
from django.views.generic import TemplateView, FormView, UpdateView, DetailView
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Company
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User



class IndexView(TemplateView):
    """
    Welcome, login or register page.
    """
    template_name = "index.html"


class RegisterView(View):
    """
    Register view to register company and the user.
    """
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
        

class LoginView(FormView):
    """
    Login view - form after retistration form
    """
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            if self.request.user.is_authenticated:
                return super().form_valid(form)
        else:
            error_message = _("Invalid username or password. Please try again.")
            return self.render_to_response(self.get_context_data(form=form, error_message=error_message))

    def get_success_url(self):
        return self.success_url


class ProductListView(LoginRequiredMixin, ListView):
    """
    View for displaying list of products
    """
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(creator=self.request.user)
    
    
class AddProductView(LoginRequiredMixin, CreateView):
    """
    View to add product
    """
    model = Product
    form_class = ProductForm
    template_name = 'add_product.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    
    
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update data of the product
    """    
    model = Product
    form_class = ProductForm
    template_name = 'product_edit.html'
    success_url = reverse_lazy('product_list')

    def get_queryset(self):
        return super().get_queryset().filter(creator=self.request.user)
    

class ProductDetailView(LoginRequiredMixin, DetailView):
    """
    View for displaying product details
    """
    model = Product
    template_name = 'product_detail.html'

    def get_queryset(self):
        return super().get_queryset().filter(creator=self.request.user)
    
    
class DeleteItemView(LoginRequiredMixin, View):
    """
    Delete item view, deleting from product detail page
    """
    def get(self, request, pk):
        item = get_object_or_404(Product, pk=pk)

        # Check if the user has permission to delete the object
        if item.creator == request.user:
            item.delete()

        # Redirect to the success URL (product_list in this case)
        return redirect('product_list')


class CustomLogoutView(View):
    """
    User logout view, logout from navbar
    """
    redirect_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(self.redirect_url)
    

class ProfileDetailView(LoginRequiredMixin, DetailView):
    """
    Details of the user profile
    """
    model = Company 
    template_name = 'profile_detail.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.company
    

class ProfileEditView(LoginRequiredMixin, UpdateView):
    """
    View for user profile editing
    """
    model = Company  
    form_class = CompanyForm
    template_name = 'profile_edit.html'
    success_url = '/profile/'

    def get_object(self):
        return self.request.user.company

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    
class DeleteUserView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        user_id = kwargs.get('user_id')
        
        if user_id and user_id != user.id:
            # If the user_id in the URL doesn't match the logged-in user's ID,
            return redirect('profile_edit')
        
        # Delete related products
        Product.objects.filter(creator=user).delete()

        # Delete related company
        company = Company.objects.get(user=user).delete()

        # Delete the user
        user.delete()

        # Redirect to login page
        return redirect('login')


def custom_404_view(request, exception):
    """
    custom 404 page
    """
    return render(request, '404.html', status=404)



