from django.shortcuts import render
from django.http import HttpRequest, JsonResponse, HttpResponse


# Function_base_view for home page
def index_page_view(request: HttpRequest):
    context = {}
    return render(request, 'base/index.html', context=context)
