from django.shortcuts import render
from django.http import Http404, HttpResponseForbidden, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
import threading
import time

from . import parser_buckwheat, parser_millet, parser_sugar

def index(request):
    buckwheat = []
    sugar = []
    millet = []
    task1 = threading.Thread(target=parser_buckwheat.parse, kwargs={'arr': buckwheat})
    task2 = threading.Thread(target=parser_sugar.parse, kwargs={'arr': sugar})
    task3 = threading.Thread(target=parser_millet.parse, kwargs={'arr': millet})
    #started_at = time.time()
    task1.start()
    task2.start()
    task3.start()
    task1.join()
    task2.join()
    task3.join()
    #print(f'Time: {time.time() - started_at}')
    return render(request, 'index.html', {'buckwheat_list': buckwheat, 'sugar_list': sugar, 'millet_list': millet})
