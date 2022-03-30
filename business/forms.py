from django import forms
from django.contrib.auth.models import User
from . models import Admin, Employee, Category, Product, Customer, ShippingAddress, Order

class EmployeeSignupForm(forms.ModelForm):
	class Meta:
		model=User
		fields=['first_name', 'last_name', 'username','password']
		widgets = {
		'password': forms.PasswordInput()
		}

class EmployeeForm(forms.ModelForm):
	class Meta:
		model=Employee
		fields=['profile_pic','overview','address','phone','email','position','company','resume','status']


class AdminSignupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name', 'last_name', 'username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class AdminForm(forms.ModelForm):
    class Meta:
        model=Admin
        fields=['profile_pic','overview','address','phone','email','company','resume','status']

class CategoryForm(forms.ModelForm):
    class Meta:
        model= Category
        fields=['category_name']

class ProductForm(forms.ModelForm):
    overview=forms.CharField(widget=forms.Textarea(attrs=
            {'class':'form-control','placeholder':'Highlight Product Summary','rows':'4'}))
    class Meta:
        model= Product
        fields=['name','category','pic','vfile','stock', 'overview','reg_price','sale_price','description','mft_date','exp_date']

class CustomerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class CustomerForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['gender','address','mobile','email','age','status','profile_pic','info']

class CheckoutForm(forms.ModelForm):
    class Meta:
        model=ShippingAddress
        fields=['phone','email','country','city','street_name','apartment_num','postal_code']

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['status']