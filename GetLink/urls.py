from django.urls import include, path
from . import views


urlpatterns=[
    path('',views.index,name='index'),
    path('api/v1/listFile/',views.listFile),
    path('api/v1/listFile/<str:fileId>',views.viewFile),
    path('form-redirect/',views.formHandle,name='redirect'),
]