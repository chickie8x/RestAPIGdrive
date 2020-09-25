from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/v1/listFile/', views.listFile),
    path('api/v1/listFile/<str:fileId>', views.viewFile),
    path('explorer/', views.explorer, name='explorer'),
    path('file/<str:fileId>/', views.getById, name='getById'),
    path('register/', views.register, name='register'),
    path('accounts/login/', views.loginView, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('ajax_post/', views.ajax_post, name='ajax_post'),
    path('sublist/', views.subList, name='sublist'),
    path('changepw/', views.pwchange, name='pwchange'),
    path('deleteFile/', views.deleteFile, name='deleteFile'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('user/forgot_password/', views.passwordReset, name='forgotpw'),
    path('user/password_reset/done/', views.passwordResetDone, name='pw_reset_done'),
]
