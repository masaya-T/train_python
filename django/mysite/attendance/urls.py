from django.urls import path

from . import views

urlpatterns = [
    path('', views.WorkerListView.as_view(), name='list'),
    path('<int:pk>/', views.PersonView.as_view(), name='person'),
]