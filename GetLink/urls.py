from django.urls import include, path
from . import views


urlpatterns=[
    path('listFile/',views.listFile),
    path('listFile/<str:fileId>',views.viewFile),
]