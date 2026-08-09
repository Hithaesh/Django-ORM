from django import forms

from core.models import Order, Staff

class ProductStockException(Exception):
  pass
 

class ProductOrderForm(forms.ModelForm):
  class Meta:
    model = Order 
    fields = ('product', 'number_of_items')

  def save(self, commit=True):
    """ Check to see if the product has enough items in stock"""
    order = super().save(commit=False)

    if order.product.number_in_stocks < order.number_of_items:
      raise ProductStockException(f"no enough items in stock for product: {order.product}")
    
    if commit is True:
      order.save()
      
    return order


class StaffDetailsForm(forms.ModelForm):
  class Meta:
    model = Staff
    fields = ('name',)