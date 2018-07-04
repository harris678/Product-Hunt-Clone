from django import forms

from .models import Product


class ProductCreateForm(forms.ModelForm):
	class Meta:
		model = RestaurantLocation
		fields = [
			'name',
			'location',
			'category',
			'slug'
		]
	def clean_name(self):
		name = self.cleaned_data.get('name')
		if(name == 'Hello'):
			raise forms.ValidationError("not a valid name")
		return name
