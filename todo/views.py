from django.shortcuts import render
# The Request, Response is the same as the HttpRequest, HttpResponse but with more features
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer
from rest_framework import status
from rest_framework.decorators import api_view


# Function_base_view in api view
# The type of requests we want it to process ( we have 4 request models in API: 1. Get, 2. Post, 3. Delete, 4. Put )
@api_view(['GET'])
def all_todos(request: Request):
    # Fetch all information
    todos = Todo.objects.order_by('priority').all()
    # An instance of the serializer is created and stored in a variable
    # The first input: the data that wants to be converted into, for example, Json
    # The second input: the number of data (many or single)
    todo_serializer = TodoSerializer(todos, many=True)
    # We pass the data in the response
    return Response(todo_serializer.data, status.HTTP_200_OK)
