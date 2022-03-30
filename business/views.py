from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from.forms import AdminSignupForm, AdminForm, EmployeeSignupForm, EmployeeForm, CategoryForm, ProductForm, CustomerUserForm, CustomerForm, CheckoutForm, ContactusForm, OrderStatusForm
from. models import Admin, Employee, Category, Product, Customer, Cartitem, Order, ShippingAddress, Contact,Mycompany
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User,Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
import stripe
from django.views.generic import View
import os


def general_page(request):
	company=Mycompany.objects.get(company_name='Organic Farm')
	categories=Category.objects.all()
	product=Product.objects.all()
	category=request.GET.get('category')
	if category==None:
		product=Product.objects.all()
	else:
		product=Product.objects.all().filter(category=category)

	paginator = Paginator(product,6)
	page = request.GET.get('page')
	try:
		paginated_queryset = paginator.page(page)
	except PageNotAnInteger:
		paginated_queryset = paginator.page(1)
	except EmptyPage:
		paginated_queryset = paginator.page(paginator.num_pages)


	context={
	'company':company,
	'categories':categories,
	'category':category,
	'product':product,
	'queryset': paginated_queryset,
	'page': page,
	}

	return render(request,'business/general_page.html',context)

def product_detail(request,pk):
	product=Product.objects.get(id=pk)
	context={
	'product':product
	}

	return render(request,'business/product_detail.html',context)

def signup(request):

	return render(request,'business/signup_page.html')


def admin_signup(request):
	form1=AdminSignupForm()
	form2=AdminForm()
	context={'form1':form1,'form2':form2}
	if request.method=='POST':
		form1=AdminSignupForm(request.POST)
		form2=AdminForm(request.POST, request.FILES)
		if form1.is_valid() and form2.is_valid():
			user=form1.save()
			user.set_password(user.password)
			user.save()
			admin=form2.save(commit=False)
			admin.user=user
			admin.save()
			adminGroup=Group.objects.get_or_create(name="ADMIN")
			adminGroup[0].user_set.add(user)
		return redirect('login')

	return render(request, 'business/admin_signup.html',context)



def employee_signup(request):
	form1=EmployeeSignupForm()
	form2=EmployeeForm()
	context={'form1':form1,'form2':form2}
	if request.method=='POST':
		form1=EmployeeSignupForm(request.POST)
		form2=EmployeeForm(request.POST, request.FILES)
		if form1.is_valid() and form2.is_valid():
			user=form1.save()
			user.set_password(user.password)
			user.save()
			employee=form2.save(commit=False)
			employee.user=user
			employee.save()
			employeeGroup=Group.objects.get_or_create(name="EMPLOYEE")
			employeeGroup[0].user_set.add(user)
		return redirect('login')

	return render(request, 'business/employee_signup.html',context)


def admin_assistant_detail(request,pk):
	assistant=Employee.objects.get(id=pk)
	context={
	'assistant':assistant,
	}

	return render(request, 'business/assistant_detail.html',context)


def assistant_employee_detail(request,pk):
	employee=Employee.objects.get(id=pk)
	context={
	'employee':employee,
	}

	return render(request, 'business/employee_detail.html',context)


def assistant_approve_employee(request,pk):
	employee=Employee.objects.get(id=pk)
	employee.status=True
	employee.salary=16
	employee.save()
	return redirect('assistant-page')

def assistant_update_employee(request,pk):
	employee=Employee.objects.get(id=pk)
	user=User.objects.get(id=employee.user_id)
	form1=EmployeeSignupForm(instance=user)
	form2=EmployeeForm(request.FILES, instance=employee)
	context={'form1':form1,'form2':form2}
	if request.method=='POST':
		form1=EmployeeSignupForm(request.POST,instance=user)
		form2=EmployeeForm(request.POST, request.FILES,instance=employee)
		if form1.is_valid() and form2.is_valid():
			user=form1.save()
			user.set_password(user.password)
			user.save()
			employee=form2.save(commit=False)
			employee.user=user
			employee.status=True
			employee.save()
			employeeGroup=Group.objects.get_or_create(name="EMPLOYEE")
			employeeGroup[0].user_set.add(user)
		return redirect('assistant-page')

	return render(request, 'business/assistant_update_employee.html',context)

def assistant_delete_employee(request,pk):
	employee=Employee.objects.get(id=pk)
	user=User.objects.get(id=employee.id)
	user.delete()
	employee.delete()
	return redirect('assistant-page')

def is_admin(user):

	return user.groups.filter(name='ADMIN').exists()


def is_employee(user):

	return user.groups.filter(name='EMPLOYEE').exists()


def customer_signup(request):
	form1=CustomerUserForm()
	form2=CustomerForm()
	context={
	'form1':form1,
	'form2':form2
	}
	if request.method=='POST':
		form1=CustomerUserForm(request.POST)
		form2=CustomerForm(request.POST,request.FILES)
		if form1.is_valid() and form2.is_valid():
			user=form1.save()
			user.set_password(user.password)
			user.save()
			customer=form2.save(commit=False)
			customer.user=user
			customer.save()
			my_customer_group = Group.objects.get_or_create(name='Customer')
			my_customer_group[0].user_set.add(user)
		return HttpResponseRedirect('login')

	return render(request,'business/customer_signup.html',context)


def is_customer(user):
	return user.groups.filter(name='Customer').exists()

def after_login(request):
	if is_admin(request.user):
		adminapproval=Admin.objects.all().filter(user_id=request.user.id, status=True)
		if adminapproval:
			return redirect('admin-page')
		else:
			return render(request,'business/employee_wait_for_approval.html')

	elif is_employee(request.user):
		assistantapproval=Employee.objects.all().filter(user_id=request.user.id, status=True,position='Assistant')
		associateapproval=Employee.objects.all().filter(user_id=request.user.id, status=True,position='Associate')
		employeeapproval=Employee.objects.all().filter(user_id=request.user.id, status=True)
		if assistantapproval:
			return redirect('assistant-page')
		elif associateapproval:
			return redirect('associate-page')
		elif employeeapproval:
			return redirect('employee-page')
		else:
			return render(request,'business/employee_wait_for_approval.html')

	elif is_customer(request.user):
		customerapproval=Customer.objects.all().filter(user_id=request.user.id, status=True)
		
		if customerapproval:
			return redirect('customer-page')
		else:
			return render(request,'business/customer_wait_for_approval.html')
	else:
		return redirect('general-page')

@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_page(request):
	admin=Admin.objects.get(user_id=request.user.id,status=True)
	femployee=Employee.objects.all().filter(company=admin.company, status=False)
	fassistant=Employee.objects.all().filter(company=admin.company, position='Assistant',status=False)
	temployee=Employee.objects.all().filter(company=admin.company, status=True)
	orders=Order.objects.all().filter(status='Inprocess')
	context={
	 'admin':admin,
	 'fassistant':fassistant,
	 'admin':admin,
	 'femployee':femployee,
	 'temployee':temployee,
	 'orders':orders
	}

	return render(request, 'business/admin_page.html',context)

@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_approve_assistant(request,pk):
	employee=Employee.objects.get(id=pk)
	employee.status=True
	employee.save()
	return redirect('admin-page')

@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_employee(request):
	admin=Admin.objects.get(user_id=request.user.id,status=True)
	femployee=Employee.objects.all().filter(company=admin.company, status=False)
	temployee=Employee.objects.all().filter(company=admin.company, status=True)
	context={
	 'admin':admin,
	 'femployee':femployee,
	 'temployee':temployee,
	}

	return render(request, 'business/admin_employee.html',context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_employee_detail(request,pk):
	employee=Employee.objects.get(id=pk)
	context={
	'employee':employee,
	}

	return render(request, 'business/employee_detail.html',context)

@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_approve_employee(request,pk):
	employee=Employee.objects.get(id=pk)
	employee.status=True
	employee.save()
	return redirect('admin-employee')

@login_required(login_url='login')
@user_passes_test(is_employee)
def assistant_page(request):
	assistant=Employee.objects.get(user_id=request.user.id,status=True)
	femployee=Employee.objects.all().filter(company=assistant.company, status=False).exclude(position='Assistant')
	temployee=Employee.objects.all().filter(company=assistant.company, status=True)
	orders=Order.objects.all().filter(status='Inprocess')
	context={
	 'assistant':assistant,
	 'femployee':femployee,
	 'temployee':temployee,
	 'orders':orders
	}

	return render(request, 'business/assistant_page.html',context)

@login_required(login_url='login')
@user_passes_test(is_employee)
def assistant_employee(request):
	assistant=Employee.objects.get(user_id=request.user.id,status=True)
	femployee=Employee.objects.all().filter(company=assistant.company, status=False)
	temployee=Employee.objects.all().filter(company=assistant.company, status=True)
	context={
	 'assistant':assistant,
	 'femployee':femployee,
	 'temployee':temployee
	}

	return render(request, 'business/assistant_employee.html',context)

@login_required(login_url='login')
@user_passes_test(is_employee)
def associate_page(request):
	associate=Employee.objects.get(user_id=request.user.id,status=True)
	temployee=Employee.objects.all().filter(company=associate.company, status=True)
	context={
	 'temployee':temployee
	}

	return render(request, 'business/associate_page.html',context)

def employee_page(request):
	employee=Employee.objects.get(user_id=request.user.id,status=True)
	context={
	 'employee':employee
	}

	return render(request, 'business/employee_page.html',context)

@login_required(login_url='login')
@user_passes_test(is_customer)
def customer_page(request):
	customer=Customer.objects.get(user_id=request.user.id,status=True)
	context={
	 'customer':customer
	}

	return render(request, 'business/customer_page.html',context)


def assistant_category(request):
	assistant=Employee.objects.get(user_id=request.user.id,status=True)
	categories=Category.objects.all().filter(company=assistant.company)
	context={
	'assistant':assistant,
	'categories':categories
	}

	return render(request, 'business/assistant_category.html',context)


@login_required(login_url='login')
@user_passes_test(is_employee)
def assistant_add_category(request):
	assistant=Employee.objects.get(user_id=request.user.id,status=True)
	form=CategoryForm()
	if request.method=='POST':
		form=CategoryForm(request.POST)
		if form.is_valid():
			cat=form.save(commit=False)
			cat.company=assistant.company
			cat.save()
		return redirect('assistant-category')
	context={
	'assistant':assistant,
	'form':form
	}

	return render(request, 'business/assistant_add_category.html',context)

def assistant_delete_category(request,pk):
	category=Category.objects.get(id=pk)
	category.delete()
	return redirect('assistant-category')


def assistant_product(request):
	assistant=Employee.objects.get(user_id=request.user.id,status=True)
	products=Product.objects.all().filter(company=assistant.company)
	context={
	'assistant':assistant,
	'products':products
	}

	return render(request, 'business/assistant_product.html',context)

def assistant_add_product(request):
	assistant=Employee.objects.get(user_id=request.user.id,status=True)
	form=ProductForm()
	if request.method=='POST':
		form=ProductForm(request.POST, request.FILES)
		if form.is_valid():
			prod=form.save(commit=False)
			prod.company=assistant.company
			prod.save()
		return redirect('assistant-product')
	context={
	'assistant':assistant,
	'form':form
	}

	return render(request, 'business/assistant_add_product.html',context)



def assistant_update_product(request,pk):
	assistant=Employee.objects.get(user_id=request.user.id,status=True)
	product=Product.objects.get(id=pk)
	form=ProductForm(instance=product)
	if request.method=='POST':
		form=ProductForm(request.POST,request.FILES,instance=product)
		if form.is_valid():
			prod=form.save(commit=False)
			prod.company=assistant.company
			prod.save()
		return redirect('assistant-product')
	context={
	'assistant':assistant,
	'form':form
	}

	return render(request, 'business/assistant_update_product.html',context)

def assistant_delete_product(request,pk):
	product=Product.objects.get(id=pk)
	product.delete()
	return redirect('assistant-product')

def add_product_to_cart(request,pk):
	buyer=Customer.objects.get(user_id=request.user.id)
	product=get_object_or_404(Product,id=pk)
	cartitem, created=Cartitem.objects.get_or_create(product=product, buyer=buyer, ordered=False)
	order=Order.objects.filter(ordered=False, buyer=buyer)
	if order.exists():
		order=order[0]
		if order.products.filter(product__id=product.id).exists():
			cartitem.qty+=1
			cartitem.save()
			return redirect("order-summary")
		else:
			order.products.add(cartitem)
			return redirect("order-summary")
	else:
		order_date=timezone.now()
		order=Order.objects.create(order_date=order_date, buyer=buyer)
		order.products.add(cartitem)
		return redirect("order-summary")

def order_summary(request):
	buyer=Customer.objects.get(user_id=request.user.id)
	order=Order.objects.get(ordered=False, buyer=buyer)
	
	context={
	'order':order,
	}

	return render(request,'business/order_summary.html',context)

def order_checkout(request):
	buyer=Customer.objects.get(user_id=request.user.id)
	order=Order.objects.get(ordered=False, buyer=buyer)
	form=CheckoutForm()
	if request.method=="POST":
		form=CheckoutForm(request.POST)
		if form.is_valid():
			address=form.save()
			address.order=order
			address.save()
		return redirect('general-page')
	
	context={
	'order':order,
	'form':form,
	}

	return render(request,'business/order_checkout.html',context)


# class stripe_payment(View):
# 	def get(self, *args, **kwargs):
# 		buyer=Customer.objects.get(user_id=self.request.user.id)
# 		order=Order.objects.filter(ordered=False, buyer=buyer)[0]
		
# 		context = {
# 			'order':order,
# 			}
			
# 		return render(self.request, "business/stripe_payment.html", context)

# 	def post(self, *args, **kwargs):
# 		buyer=Customer.objects.get(user_id=self.request.user.id)
# 		order=Order.objects.filter(ordered=False, buyer=buyer)[0]
		
# 		token = self.request.POST.get('stripeToken')
# 		amount = int(order.order_total() * 100)

# 		try:
# 			charge = stripe.Charge.create(
# 				amount=amount,  
# 				currency="usd",
# 				source=token
# 				)


# 			# create the payment
# 			payment = StripePayment()
# 			payment.stripe_charge_id = charge['id']
# 			payment.order = order
# 			payment.amount = amount
# 			payment.save()
			
# 				# assign the payment to the order
# 			if order:
# 				order_items = order.products.all()
# 				order_items.update(ordered=True)
# 				for item in order_items:
# 					item.save()
# 					product=Product.objects.get(id=item.product.id)
# 					product.stock-=item.qty
# 					product.save()

# 				order.ordered = True
# 				order.save()
# 				buyer.status=True
# 				buyer.save()
				
# 				messages.success(self.request, "Your order was successful!")
# 				return redirect("customer-page")
# 			# return redirect("/")
		
# 		except stripe.error.CardError as e:
# 			body = e.json_body
# 			err = body.get('error', {})
# 			messages.warning(self.request, f"{err.get('message')}")
# 			return redirect("/")

# 		except stripe.error.RateLimitError as e:
# 				# Too many requests made to the API too quickly
# 			messages.warning(self.request, "Rate limit error")
# 			return redirect("/")

# 		except stripe.error.InvalidRequestError as e:
# 				# Invalid parameters were supplied to Stripe's API
# 			print(e)
# 			messages.warning(self.request, "Invalid parameters")
# 			return redirect("/")

# 		except stripe.error.AuthenticationError as e:
# 				# Authentication with Stripe's API failed
# 				# (maybe you changed API keys recently)
# 			messages.warning(self.request, "Not authenticated")
# 			return redirect("/")

# 		except stripe.error.APIConnectionError as e:
# 				# Network communication with Stripe failed
# 			messages.warning(self.request, "Network error")
# 			return redirect("/")

# 		except stripe.error.StripeError as e:
# 				# Display a very generic error to the user, and maybe send
# 				# yourself an email
# 			messages.warning(
# 			self.request, "Something went wrong. You were not charged. Please try again.")
# 			return redirect("/")

# 		except Exception as e:
# 				# send an email to ourselves
# 			messages.warning(
# 			self.request, "A serious error occurred. We have been notifed.")
# 			return redirect("/")

def contactus_view(request):
    sub = ContactusForm()
    if request.method == 'POST':
        sub = ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            contact=Contact()
            contact.name=name
            contact.email=email
            contact.message=message
            contact.save()
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'business/contactussuccess.html')
    return render(request, 'business/contactus.html', {'form':sub})

def my_order(request):
	customer=Customer.objects.get(user_id=request.user.id,status=True)
	order=Order.objects.all().filter(buyer=customer)[0]
	address=ShippingAddress.objects.get(order=order)
	context={
	'order':order,
	'address':address
	}

	return render(request, 'business/my_order.html',context)

def assistant_update_order_status(request, pk):
	form=OrderStatusForm()
	assistant=Employee.objects.get(user_id=request.user.id,status=True)
	order=Order.objects.get(id=pk)
	context={
		'form':form,
	}
	if request.method == 'POST':
		form = OrderStatusForm(request.POST)
		if form.is_valid():
			order.status=form.cleaned_data['status']
			order.save()
			return redirect('assistant-view-order')

	return render(request, 'business/assistant_update_order.html',context)

def assistant_view_order(request):
	assistant=Employee.objects.get(user_id=request.user.id,status=True)
	orders=Order.objects.all().filter(status='Confirmed')
	context={
	'orders':orders,
	}

	return render(request, 'business/assistant_view_order.html',context)