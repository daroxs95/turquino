from django import forms
from main.models import Vale, ValeSalida, Tipos, Producto, CantidadPredefinida, FT, EntradaFT, SalidaFT, FTS
#from djangoformsetjs.utils import formset_media_js
from .django_extensions.formsets import formsets_factory


class GetModelForm(forms.Form):
    desde = forms.DateField(label='desde', widget = forms.DateInput(attrs={'class':'datepicker w3-input w3-border',
                                                                           'placeholder':'Desde',"style":""}))
    hasta = forms.DateField(label='hasta', widget = forms.DateInput(attrs={'class':'datepicker w3-input w3-border',
                                                                           'placeholder':'Hasta',"style":""}))

class ValeSalidaForm(forms.ModelForm):
    class Meta:
            model = ValeSalida
            fields = ['No_documento', 'dia']
            widgets = {'No_documento': forms.TextInput(attrs={'class':'w3-input w3-border',
                                                              'placeholder':'Número de documento'}),
                       'dia': forms.DateInput(attrs={'class':'datepicker w3-input w3-border','placeholder':'Día'})}

class PickProductForm(forms.Form):
    tipo = forms.ModelChoiceField(queryset=Tipos.objects.all(),
                                  empty_label='Tipo de Producción',
                                  widget = forms.Select(attrs={'class':'w3-select w3-border'}))

PickProductFormset = forms.formset_factory(PickProductForm)

class ValeForm(forms.ModelForm):
    class Meta:
            model = Vale
            fields = ['producto', 'cantidad']
            widgets = {'producto': forms.Select(attrs={'class':'w3-select w3-border','placeholder':'Producto',
                                                "required":""}),
                       'cantidad': forms.NumberInput(attrs={'class':'w3-input w3-border','placeholder':'Cantidad',
                                                   "required":""})}          
    def __init__(self, *args, **kwargs):
        super(ValeForm, self).__init__(*args, **kwargs)
        self.fields['producto'].empty_label = 'Producto'

ValeFormset = forms.modelformset_factory(Vale, form = ValeForm)
ValeFormsets = formsets_factory(ValeFormset)

class CantidadPredefinidaAdminForm(forms.ModelForm):#esto es para guardar una cantidad predefinida en el admin de django
    producto_name = forms.ChoiceField(choices=Producto.names_as_list())#esto esta mal aqui, solo funciona cuando se inicia el server 

class CantidadPredefinidaFillForm(forms.Form):#esto es para el form de rellenar el vale con una cantidad predefinida
    producto_name = forms.ModelChoiceField(queryset=Tipos.objects.all(),
                                  empty_label='Tipo de Producción',
                                  widget = forms.Select(attrs={'class':'w3-select w3-border'}))
    cantidad = forms.FloatField(widget = forms.NumberInput(attrs={'class':'w3-input w3-border','placeholder':'Cantidad',
                                                "required":""}))


class ProduccionForm(forms.ModelForm):
    class Meta:
            model = Tipos
            fields = ['verbose_name']
            widgets = {'verbose_name': forms.TextInput(attrs={'class':'w3-input w3-border',
                                                              'placeholder':'Nombre del tipo de producción'})}

class CantidadPredefinidaForm(forms.ModelForm):
    class Meta:
            model = CantidadPredefinida
            fields = [ 'cantidad']
            widgets = {'cantidad': forms.NumberInput(attrs={'class':'w3-input w3-border','placeholder':'Cantidad',
                                                   "required":""})}

    producto_name = forms.ChoiceField(choices=Producto.names_as_list(),
                                  widget = forms.Select(attrs={'class':'w3-select w3-border',"required":""}))     
    def __init__(self, *args, **kwargs):
        super(CantidadPredefinidaForm, self).__init__(*args, **kwargs)
        self.fields['producto_name'].empty_label = 'Producto'

CantidadPredefinidaFormset = forms.modelformset_factory(CantidadPredefinida, form = CantidadPredefinidaForm)

class FTEntradaForm(forms.ModelForm):
    class Meta:
            model = FT
            fields = ['producto', 'cantidad','importe']
            widgets = {'producto': forms.Select(attrs={'class':'w3-select w3-border','placeholder':'Producto',
                                                "required":""}),
                       'cantidad': forms.NumberInput(attrs={'class':'w3-input w3-border','placeholder':'Cantidad',
                                                   "required":""}),
                        'importe':forms.NumberInput(attrs={'class':'w3-input w3-border','placeholder':'Importe',
                                                   "required":""})
                                                   }        
    def __init__(self, *args, **kwargs):
        super(FTEntradaForm, self).__init__(*args, **kwargs)
        self.fields['producto'].empty_label = 'Producto'

FTEntradaFormset = forms.modelformset_factory(FT, form = FTEntradaForm)

class EntradaFTForm(forms.ModelForm):
    class Meta:
            model = EntradaFT
            fields = ['tipo','Procedencia','No_documento', 'dia']
            widgets = {'tipo': forms.Select(attrs={'class':'w3-select w3-border',
                                                              'placeholder':'Tipo de documento'}),
                        'dia': forms.DateInput(attrs={'class':'datepicker w3-input w3-border','placeholder':'Día'}),
                        'No_documento': forms.TextInput(attrs={'class':'w3-input w3-border',
                                                              'placeholder':'Número de documento'}),
                        'Procedencia': forms.TextInput(attrs={'class':'w3-input w3-border',
                                                              'placeholder':'Procedencia'})
                       }
    def __init__(self, *args, **kwargs):
        super(EntradaFTForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].empty_label = 'Tipo de documento'


class ProductoForm(forms.ModelForm):
    class Meta:
            model = Producto
            fields = ['name', 'precio']
            widgets = {'name': forms.TextInput(attrs={'class':'w3-input w3-border','placeholder':'Nombre',
                                                   "required":""}),
                        'precio':forms.NumberInput(attrs={'class':'w3-input w3-border','placeholder':'Precio',
                                                   "required":""})
                                                   }   

class FTSalidaForm(forms.ModelForm):
    class Meta:
            model = FTS
            fields = ['producto', 'cantidad','importe']
            widgets = {'producto': forms.Select(attrs={'class':'w3-select w3-border','placeholder':'Producto',
                                                "required":""}),
                       'cantidad': forms.NumberInput(attrs={'class':'w3-input w3-border','placeholder':'Cantidad',
                                                   "required":""}),
                        'importe':forms.NumberInput(attrs={'class':'w3-input w3-border','placeholder':'Importe',
                                                   "required":""})
                                                   }
    def __init__(self, *args, **kwargs):
        super(FTSalidaForm, self).__init__(*args, **kwargs)
        self.fields['producto'].empty_label = 'Producto'

FTSalidaFormset = forms.modelformset_factory(FTS, form = FTSalidaForm)

class SalidaFTForm(forms.ModelForm):
    class Meta:
            model = SalidaFT
            fields = ['Destino','No_documento', 'dia']
            widgets = { 'dia': forms.DateInput(attrs={'class':'datepicker w3-input w3-border','placeholder':'Día'}),
                        'No_documento': forms.TextInput(attrs={'class':'w3-input w3-border',
                                                              'placeholder':'Número de documento'}),
                        'Destino': forms.TextInput(attrs={'class':'w3-input w3-border',
                                                              'placeholder':'Destino'})
                       }     