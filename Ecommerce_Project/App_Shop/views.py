from django.shortcuts import render

from django.views.generic import ListView,DetailView

from App_Shop.models import Product

from App_Login import views

from django.contrib.auth.mixins import LoginRequiredMixin

class Home(ListView):
    model = Product
    template_name = 'App_Shop/home.html'


class ProductDetail(DetailView):
    model = Product
    template_name ='App_Shop/product_detail.html'
