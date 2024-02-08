"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    # Addressing as a function
    path('', views.all_todos, name='all_todos_view'),
    path('<int:todo_id>', views.todo_detail_view, name='todo_detail_view'),
    # Addressing as a class
    path('cbv/', views.TodosListApiView.as_view(), name='todos_list_api_view'),
    path('cbv/<int:todo_id>', views.TodosDetailApiView.as_view(), name='todos_detail_api_view'),
    # Addressing as a class for mixins
    path('mixins/', views.TodosListMixinApiView.as_view(), name='todos_list_mixin_api_view'),
    path('mixins/<pk>', views.TodosDetailMixinApiView.as_view(), name='todos_detail_mixin_api_view'),
    # Addressing as a class for generic
    path('generics/', views.TodosListGenericApiView.as_view(), name='todos_list_generic_api_view'),
    path('generics/<pk>', views.TodosDetailGenericApiView.as_view(), name='todos_detail_generic_api_view'),
]
