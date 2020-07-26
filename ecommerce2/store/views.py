from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json,datetime
from .utils import cookieCart,cartData,guestOrder
from .forms import UserForm,UserFormLogin


from django.contrib.auth import authenticate, login,logout
from django.shortcuts import redirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View
# Create your views here.


def store(request):
	data=cartData(request)
	cartItems=data['cartItems']
	order=data['order']
	items=data['items']


	products=Product.objects.all()
	context={'products':products,'cartItems':cartItems}
	return render(request,'store/store.html',context)

def cart(request):
	data=cartData(request)
	cartItems=data['cartItems']
	order=data['order']
	items=data['items']


	context={'items':items,'order':order,'cartItems':cartItems}
	return render(request,'store/cart.html',context)

def checkout(request):
	data=cartData(request)
	cartItems=data['cartItems']
	order=data['order']
	items=data['items']

	context={'items':items,'order':order,'cartItems':cartItems}
	return render(request,'store/checkout.html',context)

def updateItem(request):
	data=json.loads(request.body)
	productId=data['productId']
	action=data['action']
	print('Action:'+action)
	print('Product:'+productId)
	customer=request.user.customer
	product=Product.objects.get(id=productId)
	order,created=Order.objects.get_or_create(customer=customer,complete=False)
	orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)	
	if action=='add':
		print('adding now')
		orderItem.quantity=(orderItem.quantity+1)
	elif action=='remove':
		orderItem.quantity-=1
	orderItem.save()
	if orderItem.quantity<=0:
		orderItem.delete()
	return JsonResponse('Item was added',safe=False)


def processOrder(request):
	transaction_id=datetime.datetime.now().timestamp()
	data=json.loads(request.body)

	if request.user.is_authenticated:
		customer=request.user.customer
		order,created=Order.objects.get_or_create(customer=customer,complete=False)
		

	else:
		customer,order=guestOrder(request,data)

	total=float(data['form']['total'])
	order.transaction_id=transaction_id
	if total==order.get_cart_total:
		order.complete=True
	order.save()

	if order.shipping==True:
		ShippingAddress.objects.create(
										customer=customer,
										order=order,
										address=data['shipping']['address'],
										city=data['shipping']['city'],
										state=data['shipping']['state'],
										zipcode=data['shipping']['zipcode'],
				                      )


	return JsonResponse('Payment submitted',safe=False)

def noSuchPage(request):
	return render(request,'store/404page.html',{"msg":"You Seem Lost"})
	# return JsonResponse({"message":"No such Page Man"})


#FORMS FOR LOGIN AND REGISTER
class LoginFormView(View):
    form_class=UserFormLogin
    template_name = 'store/register_login.html'
    def get(self, request):
        form = self.form_class(None)
        if request.session.has_key('askedfor'):
            return render(request, self.template_name, {'form': form,'title':'Login','err':'You have to Login First'})    
        return render(request, self.template_name, {'form': form,'title':'Login'})

    def post(self,request):
        form=self.form_class(request.POST)        
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username,password=password)
            
            if user is not None and user.is_active:
                login(request,user)
                if request.session.has_key('askedfor'):
                    x=request.session['askedfor']
                    del request.session['askedfor']
                    return redirect(x)
                return redirect('store')
            return render(request, self.template_name, {'form': form,'title':'Login','error_message':'Wrong credentials'})
        
        return render(request, self.template_name, {'form': form,'title':'Login'})

class UserFormView(View):
    form_class = UserForm
    template_name = 'store/register_login.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form,'title':'Register'})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # cleaned and normalized data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user.is_active:
                # thats it.... User is logged in now, we can now refer to the user as request.user.username.etc
                login(request, user)
                if request.session.has_key('askedfor'):
                    x=request.session['askedfor']
                    del request.session['askedfor']
                    return redirect(x)
                return redirect('store:store')
            return render(request, self.template_name, {'form': form,'title':'Register','error_message':'Wrong credentials'})
        return render(request, self.template_name, {'form': form,'title':'Register','error_message':'LOGIN FAILED'})

def logout_user(request):
    logout(request)
    return redirect('login')