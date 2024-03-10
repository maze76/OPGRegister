# from django.urls import path
# from .import views
from django.urls import path
from .views import RegisterView, IndexView, LoginView, ProductListView, \
                        AddProductView, ProductUpdateView, DeleteItemView, ProductDetailView, CustomLogoutView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('product_list/', ProductListView.as_view(), name='product_list'),
    path('add_product', AddProductView.as_view(), name='add_product'),
    path("product_update/<str:pk>/", ProductUpdateView.as_view(), name="product_update"),
    path("delete_items/<str:pk>/", DeleteItemView.as_view(), name="delete_items"),
    path("product_id/<pk>", ProductDetailView.as_view(), name="product_id"),

    # path("profile/", views.profile, name="profile"),
    # path("edit_profile/<str:pk>/", views.edit_profile, name="edit_profile"),
]