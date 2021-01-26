from django.shortcuts import render
from django.http import Http404, HttpResponseForbidden, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

from . import parser

def index(request):
    items = parser.parse()
    return render(request, 'index.html', {'items_list': items})
