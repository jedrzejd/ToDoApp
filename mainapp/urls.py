from django.urls import path

from . import views


urlpatterns = [
    path('', views.ListListView.as_view(), name='index'),
    path('register', views.register_request, name='register'),
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('list/<int:list_id>/', views.TaskListView.as_view(), name='list'),
    path('list/add/', views.ListCreate.as_view(), name='list-add'),
    path('list/<int:list_id>/item/add/', views.TaskCreate.as_view(), name='task-add'),
    path('list/<int:list_id>/item/<int:pk>/', views.TaskUpdate.as_view(), name='task-update'),
    path('list/<int:pk>/delete/', views.ListDelete.as_view(), name='list-delete'),
    path('list/<int:list_id>/item/<int:pk>/delete/', views.TaskDelete.as_view(), name="task-delete"),
    path('password_reset/', views.password_reset_request, name="password_reset"),
]