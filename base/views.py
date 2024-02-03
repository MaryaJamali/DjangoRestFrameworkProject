from django.shortcuts import render
from django.http import HttpRequest
from todo.models import Todo
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


# Function_base_view for home page
def index_page_view(request: HttpRequest):
    context = {
        'todos': Todo.objects.order_by('priority').all()
    }
    return render(request, 'base/index.html', context=context)


# Function_base_view in api view
# The type of requests we want it to process ( we have 4 request models in API: 1. Get, 2. Post, 3. Delete, 4. Put )
@api_view(['GET'])
def todos_json(request: Request):
    # Fetch all information and display desired values
    # Note: This information must be converted into a list to access, otherwise we need a for loop to access
    todos = list(Todo.objects.order_by('priority').all().values('title', 'content', 'is_done'))
    return Response({'todos': todos}, status.HTTP_200_OK)
