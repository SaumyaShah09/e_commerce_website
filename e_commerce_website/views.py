from django.shortcuts import render


def Master(request):
    return render(request,"masters.html")


def Index(request):
    return render(request,"index.html")