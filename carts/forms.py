# from django import forms
# from .models import Product

# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = '__all__'  # Nếu Product không có image_url, fields này sẽ không bao gồm image_url
#         exclude = ['image_url']  # Loại bỏ image_url nếu nó tồn tại trong model Product
#         widgets = {
#             'product_name': forms.TextInput(attrs={'placeholder': 'Product Name', 'class': 'form-control here slug-title'}),
#             'slug': forms.TextInput(attrs={'placeholder': 'Slug', 'class': 'form-control here slug'}),
#             'category_main': forms.Select(attrs={'class': 'form-control form-control-sm'}),
#             'sub_category': forms.Select(attrs={'class': 'form-control form-control-sm'}),
#             'mrp_price': forms.NumberInput(attrs={'placeholder': 'MRP Price', 'class': 'form-control here'}),
#             'price': forms.NumberInput(attrs={'placeholder': 'Price', 'class': 'form-control here'}),
#             'short_desp': forms.TextInput(attrs={'placeholder': 'Short Description', 'class': 'form-control here'}),
#             'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
#             'stock': forms.NumberInput(attrs={'placeholder': 'Stock', 'class': 'form-control here'}),
#             'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super(ProductForm, self).__init__(*args, **kwargs)
#         from category.models import CategoryMain
#         self.fields['category_main'].queryset = CategoryMain.objects.all()
# carts/forms.py
from django import forms
from store.models import Product, ProductImage
from django.forms import inlineformset_factory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['image_url', 'rating', 'created_date', 'modified_date']  # Loại bỏ rating và các trường không cần thiết
        widgets = {
            'product_name': forms.TextInput(attrs={'placeholder': 'Product Name', 'class': 'form-control here slug-title'}),
            'slug': forms.TextInput(attrs={'placeholder': 'Slug', 'class': 'form-control here slug'}),
            'category_main': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'sub_category': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'mrp_price': forms.NumberInput(attrs={'placeholder': 'MRP Price', 'class': 'form-control here'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Price', 'class': 'form-control here'}),
            'short_desp': forms.TextInput(attrs={'placeholder': 'Short Description', 'class': 'form-control here'}),
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'stock': forms.NumberInput(attrs={'placeholder': 'Stock', 'class': 'form-control here'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'brand_name': forms.TextInput(attrs={'placeholder': 'Brand Name', 'class': 'form-control here'}),
            'gender': forms.TextInput(attrs={'placeholder': 'Gender', 'class': 'form-control here'}),
            'season': forms.TextInput(attrs={'placeholder': 'Season', 'class': 'form-control here'}),
            'year': forms.NumberInput(attrs={'placeholder': 'Year', 'class': 'form-control here'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        from category.models import CategoryMain
        self.fields['category_main'].queryset = CategoryMain.objects.all()

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'image_type']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image_type': forms.Select(attrs={'class': 'form-control form-control-sm'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProductImageForm, self).__init__(*args, **kwargs)
        self.fields['image_type'].required = False  # Không bắt buộc

ProductImageFormSet = inlineformset_factory(
    Product,
    ProductImage,
    form=ProductImageForm,
    fields=['image', 'image_type'],
    extra=3,
    can_delete=True
)