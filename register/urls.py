# from django.urls import path
# from .import views
from django.urls import path
from .views import RegisterView, IndexView, LoginView, ProductListView, \
                    AddProductView, ProductUpdateView, DeleteItemView, \
                    ProductDetailView, CustomLogoutView, ProfileDetailView, ProfileEditView
from django.conf.urls import handler404

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('product_list/', ProductListView.as_view(), name='product_list'),
    path('add_product', AddProductView.as_view(), name='add_product'),
    path("product_edit/<str:pk>/", ProductUpdateView.as_view(), name="product_edit"),
    path("delete_items/<str:pk>/", DeleteItemView.as_view(), name="delete_items"),
    path("product_detail/<pk>", ProductDetailView.as_view(), name="product_detail"),
    path('profile/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
]

handler404 = 'register.views.custom_404_view'  # Specify the view function for rendering 404 errors