from django.shortcuts import render, redirect
from django.views import View
from .forms import CompanyForm, UserForm, ProductForm
from django.views.generic import TemplateView, FormView, UpdateView, DeleteView, DetailView
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
        

class LoginView(FormView):
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
                print("User is authenticated:", self.request.user.username)
                return super().form_valid(form)
        else:
            messages.error(self.request, "Korisničko ime i/ili lozinka su pogrešni! Molimo pokušajte ponovo.")
            return super().form_invalid(form)

    def get_success_url(self):
        return self.success_url


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(creator=self.request.user)
    
    
class AddProductView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'add_product.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    
    
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_update.html'
    success_url = reverse_lazy('product_list')

    def get_queryset(self):
        return super().get_queryset().filter(creator=self.request.user)
    

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'product_id.html'

    def get_queryset(self):
        return super().get_queryset().filter(creator=self.request.user)
    

# class DeleteItemView(LoginRequiredMixin, DeleteView):
#     model = Product
#     template_name = 'delete_items.html'
#     success_url = reverse_lazy('product_list')

#     # def get_queryset(self):
#     #     # Return an empty queryset since we don't need it
#     #     return self.model.objects.none()

#     def get_object(self):
        
#         # return super().get_queryset().filter(creator=self.request.user)
#         # return self.model.objects.filter(creator=self.request.user)
#         return self.model.objects.get(pk=self.kwargs['pk'])

#     def delete(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         self.object.delete()
#         # return HttpResponseRedirect(self.get_success_url())
#         return super().delete(request, *args, **kwargs)
    
    
class DeleteItemView(LoginRequiredMixin, View):
    def get(self, request, pk):
        # Retrieve the specific object to be deleted
        item = get_object_or_404(Product, pk=pk)

        # Check if the user has permission to delete the object
        if item.creator == request.user:
            # Delete the object
            item.delete()
        
            # Add a success message
            messages.success(request, 'The item was successfully deleted.')

        # Redirect to the success URL (product_list in this case)
        return redirect('product_list')


class CustomLogoutView(View):
    redirect_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(self.redirect_url)


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        form = CompanyForm(instance=request.user.company)  # Assuming Company model has a ForeignKey to User model
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CompanyForm(request.POST, instance=request.user.company)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after saving
        return render(request, self.template_name, {'form': form})

