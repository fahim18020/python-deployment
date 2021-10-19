from django.shortcuts import render,HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
#models and forms

from App_Order.models import Order,Cart
from App_Payment.models import BillingAddress
from App_Payment.forms import BillingForm
from django.contrib.auth.models import User
from App_Login.models import UserProfile
from django.views.decorators.csrf import csrf_exempt


from django.contrib.auth.decorators import login_required
from django.urls import reverse

import requests
import razorpay


@login_required
def Checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    print(saved_address)
    saved_address = saved_address[0]
    print(saved_address)
    form = BillingForm(instance=saved_address)
    if request.method == "POST":
        form = BillingForm(request.POST,instance=saved_address)

        if form.is_valid():
            form.save()
            form = BillingForm(instance=saved_address)
            messages.success(request,f"Shipping Address Saved!")
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    order_items = order_qs[0].orderitems.all()
    print(order_items[0])
    order_total = order_qs[0].get_totals()
    return render(request,'App_Payment/checkout.html',context={"form":form,"order_items":order_items,"order_total":order_total,"saved_address":saved_address})

# @login_required
# def payment2(request):
#     saved_address = BillingAddress.objects.get_or_create(user=request.user)
#     if not saved_address[0].is_fully_filled():
#         messages.info(request,f"Please complete shipping address!")
#         return redirect("App_Payment:checkout")
#     # store_id = 'mbstu616a62f185233'
#     # API_key = 'mbstu616a62f185233@ssl'
#     settings = { 'store_id': 'mbstu616a62f185233', 'store_pass': 'mbstu616a62f185233@ssl', 'issandbox': True }
#     sslcommez = SSLCOMMERZ(settings)
#     status_url = request.build_absolute_uri(reverse("App_Payment:complete2"))
#     print(status_url)
#     order_qs = Order.objects.filter(user=request.user,ordered=False)
#     order_items = order_qs[0].orderitems.all()
#     order_items_count = order_qs[0].orderitems.count()
#     order_total = order_qs[0].get_totals()
#
#     post_body = {}
#     post_body['total_amount']= Decimal(order_total)
#     post_body['currency'] = "BDT"
#     post_body['tran_id'] = "12345"
#     post_body['success_url'] = status_url
#     post_body['fail_url'] = "your fail url"
#     post_body['cancel_url'] = "your cancel url"
#     post_body['ship_name'] = current_user.user_profile.full_name
#     post_body['sessionkey'] =
#     current_user = request.user
#     post_body['cus_name'] = current_user.user_profile.full_name
#     post_body['cus_email'] = current_user.email
#     post_body['cus_phone'] = current_user.user_profile.phone
#     post_body['cus_add1'] = current_user.user_profile.address_1
#     post_body['cus_city'] = current_user.user_profile.city
#     post_body['cus_country'] = current_user.user_profile.country
#     post_body['shipping_method'] = "Courier"
#     post_body['product_name'] = order_items
#     post_body['num_of_item']= order_items_count
#
#     response = sslcommez.createSession(post_body)
#     print(response)
#     from django.shortcuts import redirect
#     return redirect(response['GatewayPageURL'])
#
#
#
#
#
#
#
#
#
#
#
#
#     # mypayment=(success_url=status_url,fail_url=status_url,cancel_url=status_url,ipn_url=status_url)
#     #
#     #
#     # mypayment.set_product_integration(total_amount=Decimal(order_total),currency='BDT',product_category='Mixed',product_name=order_items,num_of_item=order_items_count,shipping_method='Courier',product_profile='None')
#     # current_user = request.user
#     # mypayment.set_customer_info(name='current_user.user_profile.full_name',email='current_user.email',address1='current_user.user_profile.address_1',address2='current_user.user_profile.address_1',city='current_user.user_profile.city',postcode='current_user.user_profile.zipcode',country='current_user.user_profile.country',phone='current_user.user_profile.phone')
#     #
#     # mypayment.set_shipping_info(shipping_to='current_user.user_profile.full_name',address='saved_address.address_1',city='saved_address.city',postcode='saved_address.zipcode',country='saved_address.country')
#
#
#     # response_data = mypayment.init_payment()
#     # return redirect(response_data['GatewayPageURL'])
#
#     # return render(request,"App_Payment/payment2.html",context={})
#
#
#
# @login_required
# def complete2(request):
#     # if request.method == 'POST' or request.method == 'post':
#     #     payment_data =request.POST
#     #     status = payment_data['status']
#
#     render(request,"App_Payment/complete2.html",context={})
#
#







# ----------------------------------------------------










@login_required
def payment(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    if not saved_address[0].is_fully_filled():
        messages.info(request,f"Please complete shipping address!")
        return redirect("App_Payment:checkout")




    order_qs = Order.objects.filter(user=request.user,ordered=False)
    order_items = order_qs[0].orderitems.all()
    order_item_count = order_qs[0].orderitems.count()
    order_total = order_qs[0].get_totals()
    current_user = request.user
    email = current_user.email
    name = current_user.username
    phone = current_user.user_profile.phone

    order_id = order_qs[0].orderedId
    address = current_user.user_profile.address_1


    keyid = 'rzp_test_dFzwZJbvSrqAVx'

    keysecret = 'CQFSkjVl8lYMi8OAfByV18jp'

    client = razorpay.Client(auth=(keyid,keysecret))

    order_qs = Order.objects.filter(user=request.user,ordered=False)
    order_total = order_qs[0].get_totals()
    order_amount = order_total * 100
    order_currency ='BDT'
    order_receipt = 'order_rcptid_11'
    notes = {'Shipping address' : address}

    order_data = client.order.create(dict(amount=order_amount,currency=order_currency,receipt=order_receipt,notes=notes))
    print(order_data)
    order_id = order_data['id']
    order_status = order_data['status']

    return render(request,"App_Payment/payment.html",context={'order_items':order_items,'order_items_count':order_item_count,'order_amount':order_amount,'current_user':current_user,'name':name,'email':email,'order_id':order_id,'phone':phone,'keyid':keyid,'payment_st':order_data})





@login_required
def payment_status(request):
    response = request.POST
    status = True
    if status == True:
        messages.success(request,f"Your Payment Completed Successfully!")
        return HttpResponseRedirect(reverse("App_Payment:purchase"))
    else:
        messages.warning(request,f"Your Payment Failed! Please Try Again!")

    return render(request,'App_Payment/payment_status.html')

@login_required
def purchase(request):
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    order = order_qs[0]
    order.ordered = True
    order.save()
    cart_items = Cart.objects.filter(user=request.user,purchased=False)
    for item in cart_items:
        item.purchased = True
        item.save()
    return HttpResponseRedirect(reverse("App_Shop:home"))

# @login_required
# def order_view(request):
#     try:
#         orders = Order.objects.filter(user=request.user,ordered=True)
#         context = {"orders": orders}
#     except:
#         messages.warning(request,"You do no have an active order")
#         return redirect("App_Shop:home")
#     return render(request,"App_Payment/order.html",context={})

@login_required
def order_view(request):
    print(request.POST)
    return render(request,"App_Payment/order.html")
