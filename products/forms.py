from django import forms
from .models import Product, Category, Manufacturer, TyreSize


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        brands = Manufacturer.objects.all().order_by('display_name', )
        sizes = TyreSize.objects.all().order_by('rim_size', 'width',)
        display_name_categories = [(c.id, c.get_display_name()) for c in categories]
        full_size_display = [(s.id, s.get_display_name()) for s in sizes]
        display_names_brands = [(b.id, b.get_display_name()) for b in brands]

        self.fields['category'].choices = display_name_categories
        self.fields['manufacturer'].choices = display_names_brands
        self.fields['size'].choices = full_size_display
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'rounded-0'
