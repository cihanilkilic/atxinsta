from django.shortcuts import render
from product_packages.models import ProductPackage
# Create your views here.
def index(request):
    """Ana sayfa render edilir ve ProductPackage verileri gönderilir"""
    packages = ProductPackage.objects.all()
    return render(request, "atxaisoft/index.html", {"packages": packages})