from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from phone_field import PhoneField
from django_countries.fields import CountryField
import json

class Mycompany(models.Model):
	company_name=models.CharField(max_length=200)
	overview=models.TextField()
	pic= models.ImageField(upload_to='companyPic',null=True,blank=True)
	location=models.CharField(max_length=200, blank=True,null=True)
	address = models.CharField(max_length=40,blank=True,null=True)
	postal_code=models.CharField(max_length=20,blank=True,null=True)
	skey=models.CharField(max_length=300, blank=True,null=True)
	pkey=models.CharField(max_length=300, blank=True,null=True)

	def __str__(self):
		return self.company_name



class Admin(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	profile_pic= models.ImageField(upload_to='profile_pic/EmployeePic/',null=True,blank=True)
	overview=RichTextField(null=True,blank=True)
	address = models.CharField(max_length=40)
	email=models.EmailField(max_length=50, null=True)
	phone = models.CharField(max_length=40,null=True)
	company= models.ForeignKey(Mycompany, on_delete=models.CASCADE)
	resume= models.FileField(upload_to='EmpoResume', null=True, blank=True)
	salary= models.FloatField(null=True,blank=True)
	status=models.BooleanField(default=False)

	@property
	def get_name(self):
		return self.user.first_name+" "+self.user.last_name
	@property
	def get_id(self):
		return self.user.id

	def __str__(self):
		return "{} ({})".format(self.user.username, self.company)




positions=[('Assistant','Assistant'),
('Doctor','Doctor'),
('Accountant','Accountant'),
('Associate','Associate'),
('Pharmasist','Pharmasist'),
('Nurse','Nurse'),
('Cleaner','Cleaner'),
]


class Employee(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	profile_pic= models.ImageField(upload_to='profile_pic/EmployeePic/',null=True,blank=True)
	overview=RichTextField(null=True,blank=True)
	address = models.CharField(max_length=40)
	email=models.EmailField(max_length=50, null=True)
	phone = models.CharField(max_length=40,null=True)
	company= models.ForeignKey(Mycompany, on_delete=models.CASCADE)
	position= models.CharField(max_length=50,choices=positions,default='Assistant',null=True)
	resume= models.FileField(upload_to='EmpoResume', null=True, blank=True)
	salary= models.FloatField(null=True,blank=True)
	status=models.BooleanField(default=False)

	@property
	def get_name(self):
		return self.user.first_name+" "+self.user.last_name
	@property
	def get_id(self):
		return self.user.id

	def __str__(self):
		return "{} ({})".format(self.user.username, self.position)


class Category(models.Model):
	company=models.ForeignKey(Mycompany,on_delete=models.CASCADE, related_name='categories', blank=True, null=True)
	category_name=models.CharField(max_length=200)

	def __str__(self):
		return self.category_name

class Product(models.Model):
	category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products', blank=True, null=True)
	company=models.ForeignKey(Mycompany,on_delete=models.CASCADE, related_name='prods', blank=True, null=True)
	name=models.CharField(max_length=200)
	overview=models.TextField()
	pic= models.ImageField(upload_to='productPic', null=True, blank=True)
	description=RichTextField(blank=True, null=True)
	vfile= models.FileField(upload_to='productVideo', null=True, blank=True)
	reg_price=models.FloatField()
	sale_price=models.FloatField(null=True, blank=True)
	stock=models.PositiveIntegerField(default=0,null=True, blank=True)
	mft_date=models.DateField(null=True, blank=True)
	exp_date=models.DateField(null=True, blank=True)
	
	def __str__(self):
		return "{} ({})".format(self.category, self.name)


genders=[('Male','Male'),('Femele','Femele'),('Other','Other')]

class Customer(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	mobile=PhoneField(null=False, help_text='Contact phone number')
	email=models.EmailField(max_length=50)
	profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
	address = models.CharField(max_length=40)
	gender=models.CharField(max_length=50,choices=genders,default='Femele', null=True, blank=True)
	age=models.PositiveIntegerField(null=True,blank=True)
	info=RichTextField(blank=True, null=True)
	status=models.BooleanField(default=False)
	

	@property
	def get_name(self):
		return self.user.first_name+" "+self.user.last_name
	@property
	def get_id(self):
		return self.user.id
	def __str__(self):
		return "{} ({})".format(self.user.first_name,self.user.last_name)


class Cartitem(models.Model):
	product=models.ForeignKey(Product, on_delete=models.CASCADE)
	qty=models.IntegerField(default=1)
	sugar=models.IntegerField(default=0,blank=True,null=True)
	milk=models.IntegerField(default=0,blank=True,null=True)
	buyer=models.ForeignKey(Customer, on_delete=models.CASCADE)
	ordered=models.BooleanField(default=False)
	
	def __str__(self):
		return f"{self.product.name} of {self.qty}"

	def total_price(self):
		if self.product.sale_price:
			return self.product.sale_price * self.qty
		else:
			return self.product.reg_price * self.qty

process=[('Inprocess','Inprocess'),('Confirmed','Confirmed'),('On The Way','On The Way'),('Delivered','Delivered')]
class Order(models.Model):
	products=models.ManyToManyField(Cartitem)
	buyer=models.ForeignKey(Customer, on_delete=models.CASCADE)
	ordered=models.BooleanField(default=False)
	order_date=models.DateField()
	update_date=models.DateField(blank=True,null=True)
	status=models.CharField(max_length=50,choices=process, default='Inprocess')
	
	def __str__(self):
		return f"{self.buyer} of {self.order_date}"

	def order_total(self):
			total=0
			for prod in self.products.all():
				total+=prod.total_price()
			return total

	@property
	def get_address(self):
		return self.myorder.all()

class ShippingAddress(models.Model):
	order=models.ForeignKey(Order, on_delete=models.CASCADE,related_name='myorder',null=True)
	email=models.EmailField(max_length=50)
	phone=PhoneField(blank=True, help_text='Contact phone number')
	street_name=models.CharField(max_length=50)
	apartment_num=models.PositiveIntegerField(null=True,blank=True)
	city=models.CharField(max_length=50,blank=True,null=True)
	country = CountryField(multiple=False)
	postal_code=models.CharField(max_length=20)
	
	
	def __str__(self):
		return f"{self.order} of {self.street_name}"

# class StripePayment(models.Model):
# 	order=models.ForeignKey(Order, on_delete=models.CASCADE,related_name='mypayment',null=True)
# 	stripe_charge_id = models.CharField(max_length=50)
# 	amount = models.FloatField()
# 	timestamp = models.DateTimeField(auto_now_add=True)

# 	def __str__(self):
# 		return f"{self.order} of {self.amount}"

class Contact(models.Model):
	name=models.CharField(max_length=200)
	email=models.EmailField(max_length=50)
	message=models.TextField()

	def __str__(self):
		return f"{self.name} of {self.email}"