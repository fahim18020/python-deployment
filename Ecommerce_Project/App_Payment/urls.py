from django.urls import path
from App_Payment import views

app_name = "App_Payment"

urlpatterns = [
    path('checkout/',views.Checkout,name="checkout"),
    path('pay/',views.payment,name="payment"),
    path('payment_st/',views.payment_status,name="payment_status"),
    path('purchase/',views.purchase,name='purchase'),
    path('orders/',views.order_view,name="orders"),
    # path('status/',views.complete2,name="complete2")





]
