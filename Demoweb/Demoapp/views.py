from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


# Create your views here.S
def page(request):
    return render(request, "page.html")
