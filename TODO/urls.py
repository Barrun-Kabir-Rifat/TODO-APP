from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('done/<int:task_id>/', views.mark_done, name='mark_done'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
]
