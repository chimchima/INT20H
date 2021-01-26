from django.shortcuts import render
from django.http import Http404, HttpResponseForbidden, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

from . import parser_buckwheat, parser_millet, parser_sugar

def index(request):
    buckwheat = parser_buckwheat.parse()
    sugar = parser_sugar.parse()
    millet = parser_millet.parse()
    return render(request, 'index.html', {'buckwheat_list': buckwheat, 'sugar_list': sugar, 'millet_list': millet})
