from django.shortcuts import render, HttpResponse


def Index(request):
    return render(request, 'index.html')
