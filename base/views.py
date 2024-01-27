from django.shortcuts import render
from django.http import HttpRequest
from todo.models import Todo


# Function_base_view for home page
def index_page_view(request: HttpRequest):
    context = {
        'todos': Todo.objects.order_by('priority').all()
    }
    return render(request, 'base/index.html', context=context)
