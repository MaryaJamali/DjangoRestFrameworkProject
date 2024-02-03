from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer
from rest_framework import status
from rest_framework.decorators import api_view


# Function_base_view in api view
@api_view(['GET'])
def all_todos(request: Request):
    todos = Todo.objects.order_by('priority').all()
    todo_serializer = TodoSerializer(todos, many=True)
    return Response(todo_serializer.data, status.HTTP_202_ACCEPTED)
