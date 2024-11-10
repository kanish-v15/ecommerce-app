"""Urls.py"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (IndexView, SignUpView, LoginView, LogoutView, ProfileView, AdminDashboardView,
AdminAddProductView, AdminProductDetailView, AdminDeleteProductView, AdminManageCategoriesView,
AdminDeleteCategoryView, SuperAdminDashboardView, SuperAdminAddAdminView, SuperAdminUserDetailView,
SuperAdminEditUserView, SuperAdminDeleteUserView, AddMoneyToWalletView, ProductListView,
ProductDetailView, AddToCartView, CartView, UpdateCartView, RemoveFromCartView, CheckoutView,
OrderConfirmationView, OrdersDashboardView, WalletDashboardView)

urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', LoginView.as_view(), name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin/add-product/', AdminAddProductView.as_view(), name='admin_add_product'),
    path('admin/product/<int:product_id>/', AdminProductDetailView.as_view(),
name='admin_product_detail'),
    path('admin/delete-product/<int:product_id>/', AdminDeleteProductView.as_view(),
name='admin_delete_product'),
    path('admin/manage-categories/', AdminManageCategoriesView.as_view(),
name='admin_manage_categories'),
    path('admin/delete-category/<int:category_id>/', AdminDeleteCategoryView.as_view(),
name='admin_delete_category'),
    path('superadmin/', SuperAdminDashboardView.as_view(), name='superadmin_dashboard'),
    path('superadmin/add-admin/', SuperAdminAddAdminView.as_view(), name='superadmin_add_admin'),
    path('superadmin/user/<int:user_id>/', SuperAdminUserDetailView.as_view(),
name='superadmin_user_detail'),
    path('superadmin/user/<int:user_id>/edit/', SuperAdminEditUserView.as_view(),
name='superadmin_edit_user'),
    path('superadmin/user/<int:user_id>/delete/', SuperAdminDeleteUserView.as_view(),
name='superadmin_delete_user'),

    path('add-money/', AddMoneyToWalletView.as_view(), name='add_money_to_wallet'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('update-cart/<int:item_id>/', UpdateCartView.as_view(), name='update_cart'),
    path('remove-from-cart/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-confirmation/<int:order_id>/', OrderConfirmationView.as_view(),
name='order_confirmation'),
    path('orders/', OrdersDashboardView.as_view(), name='orders_dashboard'),
    path('wallet/', WalletDashboardView.as_view(), name='wallet_dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
