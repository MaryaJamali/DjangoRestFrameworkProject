# DjangoRestFrameworkProject 🌐
If you're a techie or have been in the development industry for a while, you've probably heard the term REST API.<br> `API or Application Programming Interfaces`
For anyone looking to get into web API development or loves building APIs in Python, the Django REST framework is the go-to tool.
This project is very useful and great for learning Django Rest framework.💻
### Instructions
___
1. ***Prerequisites***<br>
Download and install the latest version of Python and start the Django installation process<br>
It's time to install the relevant packages from inside the "req.text" file. The first real step is to start the Django Rest framework, which is installed with the command<br>
`pip install django_rest_framework` <br><br>
Note 📝: To separate dependencies, you can create a virtual environment, this is great, but you can skip this step <br><br>
2. ***Simulate your repository***<br>
`git clone https://github.com/MaryaJamali/DjangoRestFrameworkProject.git` <br><br>
3. ***Run the program***
### Description
___
🌟 Creating a Model for the App<br>
`models.py` file <br>

```python
from django.db import models
from django.contrib.auth import get_user_model

# Calling the user model and storing it in the variable
user = get_user_model()


# Create model for todo
class Todo(models.Model):
    title = models.CharField(max_length=300, verbose_name='title')
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name='todos', verbose_name='user')
    content = models.TextField(verbose_name='text')
    priority = models.IntegerField(default=1, verbose_name='Display priority:')
    is_done = models.BooleanField(default=False, verbose_name='done/not done')

    def __str__(self) -> str:
        return f'{self.title} / Is Done: {self.is_done}'

    class Meta:
        # Set the desired table name
        db_table = 'todos'
```
`admin.py` file <br>
```python
from django.contrib import admin
from . import models


# Admin panel customization for the TodoAdmin
@admin.register(models.Todo)
class TodoAdmin(admin.ModelAdmin):
    # Display fields on the Admin page
    list_display = ['title', 'user', 'content', 'priority', 'is_done']
```
🌟 Migrating the App &  Set up the Django admin interface<br>
`python manage.py makemigrations`<br>
`python manage.py migrate`<br>
`python manage.py createsuperuser`<br><br>
<img src="https://github.com/MaryaJamali/DjangoRestFrameworkProject/blob/main/img/admin.png?raw=true" width="1000" height="500" alt="admin"/><br><br>
🌟 to enable APIs to read data more easily, serializers transform complex Django models into JSON objects.So we need to create a file called `serializers.py‍`<br>
```python
from rest_framework import serializers
from .models import Todo
from django.contrib.auth import get_user_model


User = get_user_model()


class TodoSerializer(serializers.ModelSerializer):

    # Setting up the validation system personal
    # def validate_..... --> The name of the field we want to validate
    def validate_priority(self, priority):
        if priority < 10 or priority > 20:
            raise serializers.ValidationError('priority is not ok')
        return priority

    class Meta:
        model = Todo
        # fields = ['id', 'title', 'content']
        fields = '__all__'


# fetch the user list and in addition to serializing the user information,
# it displays the serializing todos list of each user.
class UserSerialzier(serializers.ModelSerializer):
    # The name of the 'todos' is taken from the 'user' field model of 'related_name' part
    todos = TodoSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = '__all__'

```
🌟 Using the serializers and Data models, we now have to update the API view<br>
Note 📝: Importing the entire package that must be done in the `views.py` file<br>
```python
from django.shortcuts import render
# The Request, Response is the same as the HttpRequest, HttpResponse but with more features
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer, UserSerialzier
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

User = get_user_model()
```
<br>
🖥 Adding data list with GET as a Function<br>
<img src="https://github.com/MaryaJamali/DjangoRestFrameworkProject/blob/main/img/function-list.png?raw=true" width="1000" height="500" alt="function-list"/><br>
🖥 Adding data list with POST as a Function<br>
<img src="https://github.com/MaryaJamali/DjangoRestFrameworkProject/blob/main/img/function%20&%20class%20-%20post.png?raw=true" width="1000" height="500" alt="function-list"/>
<br><br>

```python
# Function_base_view in api view
# The type of requests we want it to process ( we have 4 request models in API: 1. Get (read), 2. Post (create),
# 3. Delete (delete), 4. Put (update) )
@api_view(['GET', 'POST'])
def all_todos(request: Request):
    if request.method == 'GET':
        # Fetch all information
        todos = Todo.objects.order_by('priority').all()
        # An instance of the serializer is created and stored in a variable
        # The first input: the data that wants to be converted into, for example, Json
        # The second input: the number of data (many or single)
        todo_serializer = TodoSerializer(todos, many=True)
        # We pass the data in the response
        return Response(todo_serializer.data, status.HTTP_200_OK)
    elif request.method == 'POST':
        # The de-serializer is created and stored in a variable
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(None, status.HTTP_400_BAD_REQUEST)

    return Response(None, status.HTTP_400_BAD_REQUEST)
```
<br>
🖥 Adding, Deleting and Editing the data detail with GET,DELETE,PUT as a Function<br>
<img src="https://github.com/MaryaJamali/DjangoRestFrameworkProject/blob/main/img/function-detail.png?raw=true" width="1000" height="500" alt="function-detail"/><br><br>

```python
@api_view(['GET', 'PUT', 'DELETE'])
def todo_detail_view(request: Request, todo_id: int):
    try:
        todo = Todo.objects.get(pk=todo_id)
    except Todo.DoesNotExist:
        return Response(None, status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_202_ACCEPTED)
        return Response(None, status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        todo.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)
  ```
🌟 Addressing in the `urls.py` file <br>
```python
from django.urls import path, include
from . import views
urlpatterns = [
    # Addressing as a function
    path('', views.all_todos, name='all_todos_view'),
    path('<int:todo_id>', views.todo_detail_view, name='todo_detail_view'),
]
```
<br>
🖥 Adding data list with GET as a Class<br>
<img src="https://github.com/MaryaJamali/DjangoRestFrameworkProject/blob/main/img/class-list.png?raw=true" width="1000" height="500" alt="class-list"/><br>
🖥 Adding data list with POST as a Class<br>
<img src="https://github.com/MaryaJamali/DjangoRestFrameworkProject/blob/main/img/function%20&%20class%20-%20post.png?raw=true" width="1000" height="500" alt="class-list"/>
<br><br>

```python
# Class_base_view in api view
class TodosListApiView(APIView):
    def get(self, request: Request):
        todos = Todo.objects.order_by('priority').all()
        todo_serializer = TodoSerializer(todos, many=True)
        return Response(todo_serializer.data, status.HTTP_200_OK)

    def post(self, request: Request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(None, status.HTTP_400_BAD_REQUEST)
```
<br>
🖥 Adding, Deleting and Editing the data detail with GET,DELETE,PUT as a Class<br>
<img src="https://github.com/MaryaJamali/DjangoRestFrameworkProject/blob/main/img/class-detail.png?raw=true" width="1000" height="500" alt="class-detail"/><br><br>

```python
class TodosDetailApiView(APIView):
    def get_object(self, todo_id: int):
        try:
            todo = Todo.objects.get(pk=todo_id)
            return todo
        except Todo.DoesNotExist:
            return Response(None, status.HTTP_404_NOT_FOUND)

    def get(self, request: Request, todo_id: int):
        todo = self.get_object(todo_id)
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request: Request, todo_id: int):
        todo = self.get_object(todo_id)
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_202_ACCEPTED)
        return Response(None, status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, todo_id: int):
        todo = self.get_object(todo_id)
        todo.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)
  ```
🌟 Addressing in the `urls.py` file <br>
```python
from django.urls import path, include
from . import views
urlpatterns = [
    # Addressing as a class
    path('cbv/', views.TodosListApiView.as_view(), name='todos_list_api_view'),
    path('cbv/<int:todo_id>', views.TodosDetailApiView.as_view(), name='todos_detail_api_view'),
]
```
<br>
🖥 Adding data list with GET as a Mixins<br>
<img src="https://github.com/MaryaJamali/DjangoRestFrameworkProject/blob/main/img/mixins-list.png?raw=true" width="1000" height="500" alt="mixins-list"/><br>
🖥 Adding data list with POST as a Mixins<br>
<img src="https://github.com/MaryaJamali/DjangoRestFrameworkProject/blob/main/img/mixins%20&%20generics%20&%20viewsets%20-%20post.png?raw=true" width="1000" height="500" alt="mixins-list"/>
<br><br>

```python
# Class_base_view in api view with Mixins
# mixins.ListModelMixin ---> GET command
# mixins.CreateModelMixin ---> POST command
# generics.GenericAPIView ---> To become an API View
class TodosListMixinApiView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer

    def get(self, request: Request):
        return self.list(request)

    def post(self, request: Request):
        return self.create(request)
```
<br>
🖥 Adding, Deleting and Editing the data detail with GET,DELETE,PUT as a Mixins<br>
<img src="https://github.com/MaryaJamali/DjangoRestFrameworkProject/blob/main/img/mixins-detail.png?raw=true" width="1000" height="500" alt="mixins-detail"/><br><br>

```python
# mixins.RetrieveModelMixin ---> GET command
# mixins.UpdateModelMixin ---> PUT command
# mixins.DestroyModelMixin ---> DELETE command
class TodosDetailMixinApiView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                              generics.GenericAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer

    def get(self, request: Request, pk):
        return self.retrieve(request, pk)

    def put(self, request: Request, pk):
        return self.update(request, pk)

    def delete(self, request: Request, pk):
        return self.destroy(request, pk)
  ```
🌟 Addressing in the `urls.py` file <br>
```python
from django.urls import path, include
from . import views
urlpatterns = [
    # Addressing as a class for mixins
    path('mixins/', views.TodosListMixinApiView.as_view(), name='todos_list_mixin_api_view'),
    path('mixins/<pk>', views.TodosDetailMixinApiView.as_view(), name='todos_detail_mixin_api_view'),
]
```
<br>
🖥 Adding data list with GET as a generics<br>
<img src="https://github.com/MaryaJamali/DjangoRestFrameworkProject/blob/main/img/generics-list.png?raw=true" width="1000" height="500" alt="generics-list"/><br>
🖥 Adding data list with POST as a generics<br>
<img src="https://github.com/MaryaJamali/DjangoRestFrameworkProject/blob/main/img/mixins%20&%20generics%20&%20viewsets%20-%20post.png?raw=true" width="1000" height="500" alt="generics-list"/>
<br><br>

```python
# Custom paging system settings with class definition
class TodosGenericApiViewPagination(PageNumberPagination):
    page_size = 3


# Class_base_view in api view with Generic
class TodosListGenericApiView(generics.ListCreateAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    pagination_class = TodosGenericApiViewPagination
    # Authentication system with basic authentication
    authentication_classes = [BasicAuthentication]
    # Access level
    permission_classes = [IsAuthenticated]
```
<br>
🖥 Adding, Deleting and Editing the data detail with GET,DELETE,PUT as a generics<br>
<img src="https://github.com/MaryaJamali/DjangoRestFrameworkProject/blob/main/img/generics-detail.png?raw=true" width="1000" height="500" alt="generics-detail"/><br><br>

```python
class TodosDetailGenericApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
  ```
🌟 Addressing in the `urls.py` file <br>
```python
from django.urls import path, include
from . import views
urlpatterns = [
    # Addressing as a class for generic
    path('generics/', views.TodosListGenericApiView.as_view(), name='todos_list_generic_api_view'),
    path('generics/<pk>', views.TodosDetailGenericApiView.as_view(), name='todos_detail_generic_api_view'),
]
```
<br>
🖥 Adding data list with GET as a viewsets<br>
<img src="https://github.com/MaryaJamali/DjangoRestFrameworkProject/blob/main/img/viewsets-list.png?raw=true" width="1000" height="500" alt="viewsets-list"/><br>
🖥 Adding data list with POST as a viewsets<br>
<img src="https://github.com/MaryaJamali/DjangoRestFrameworkProject/blob/main/img/mixins%20&%20generics%20&%20viewsets%20-%20post.png?raw=true" width="1000" height="500" alt="viewsets-list"/>
🖥 Adding, Deleting and Editing the data detail with GET,DELETE,PUT as a viewsets<br>
<img src="https://github.com/MaryaJamali/DjangoRestFrameworkProject/blob/main/img/viewsets-detail.png?raw=true" width="1000" height="500" alt="viewsets-detail"/><br><br>

```python
# Class_base_view in api view with Viewsets
class TodosViewSetApiView(viewsets.ModelViewSet):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    # Paging system settings specifically directly
    pagination_class = LimitOffsetPagination
```
<br>

🌟 Addressing in the `urls.py` file <br>

```python
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# Basic settings for addressing viewsets
router = DefaultRouter()
router.register('', views.TodosViewSetApiView)
urlpatterns = [
    # Addressing as a class for viewsets
    path('viewsets/', include(router.urls), name='todos_viewsets_api_view'),
]
```
<br>
🖥 Display general user information <br>
<img src="https://github.com/MaryaJamali/DjangoRestFrameworkProject/blob/main/img/user-1.png?raw=true" width="1000" height="500" alt="user"/><br>
<img src="https://github.com/MaryaJamali/DjangoRestFrameworkProject/blob/main/img/user-2.png?raw=true" width="1000" height="500" alt="user"/>
<br>

```python
# Class_base_view in api view with Generic for user
class UsersGenericApiView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerialzier
```
<br>

🌟 Addressing in the `urls.py` file <br>

```python
from django.urls import path, include
from . import views

urlpatterns = [
   # Addressing as a class for user
    path('users/', views.UsersGenericApiView.as_view(), name='user_list_generic_api_view'),
]
```
<br>
🖥 Settings related to the authentication system in three ways and Use standard appearance with swagger <br>

 `settings.py` file <br>

```python
# Note: These settings are global and only applies to viewsets and generics
# Paging system settings related to the framework
REST_FRAMEWORK = {
    # The address of the desired class + the name of the desired class
    # Note: If we use " PageNumberPagination " , it uses ?page=... , and if we use " LimitOffsetPagination " ,
    # it uses ?limit=... ( page number ) & offset=... ( Step value )
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 2,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.BasicAuthentication'
        # 'rest_framework.authentication.TokenAuthentication'
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# Setting the drf_spectacular
SPECTACULAR_SETTINGS = {
    'TITLE': 'Your Project API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}

# Setting the updateing time
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}
```
<br>

🌟 `urls.py` file <br>
 
```python
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Addressing App
urlpatterns = [
    path('', include('base.urls')),
    path('todos/', include('todo.urls')),
    # Addresses related to BasicAuthentication
    path('api-auth/', include('rest_framework.urls')),
    # Addresses related to TokenAuthentication
    path('auth-token/', obtain_auth_token, name='generate_auth_token'),
    # Addresses related to djangorestframework-simplejwt
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Addresses related to drf_spectacular
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  # YOUR PATTERNS
    path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # Optional UI
    path('admin/', admin.site.urls),
]
```

### Author
___
Maryam Jamali 😘
