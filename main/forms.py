from django import forms
from main.models import Vale, ValeSalida, Tipos
from djangoformsetjs.utils import formset_media_js
from .templatetags.utils import initWithData
from .django_extensions.formsets import formsets_factory


class GetModelForm(forms.Form):
    desde = forms.DateField(label='desde', widget = forms.TextInput(attrs={'class':'datepicker w3-input w3-border',
                                                                           'placeholder':'Desde',"style":""}))
    hasta = forms.DateField(label='hasta', widget = forms.TextInput(attrs={'class':'datepicker w3-input w3-border',
                                                                           'placeholder':'Hasta',"style":""}))


class ValeSalidaForm(forms.ModelForm):
    class Meta:
            model = ValeSalida
            fields = ['No_documento', 'dia']
            widgets = {'No_documento': forms.TextInput(attrs={'class':'w3-input w3-border',
                                                              'placeholder':'Número de documento'}),
                       'dia': forms.TextInput(attrs={'class':'datepicker w3-input w3-border','placeholder':'Día'})}

class PickProductForm(forms.Form):
    tipo = forms.ModelChoiceField(queryset=Tipos.objects.all(),
                                  empty_label='Tipo de Producción',
                                  widget = forms.Select(attrs={'class':'w3-select w3-border w3-margin-bottom'}))

class ValeForm(forms.ModelForm):
    class Meta:
            model = Vale
            fields = ['producto', 'cantidad']
            widgets = {'producto': forms.Select(attrs={'class':'w3-select w3-border w3-margin-bottom','placeholder':'Producto',
                                                "required":""}),
                       'cantidad': forms.TextInput(attrs={'class':'w3-input w3-border w3-margin-bottom','placeholder':'Cantidad',
                                                   "required":""})}          
    def __init__(self, *args, **kwargs):
        super(ValeForm, self).__init__(*args, **kwargs)
        self.fields['producto'].empty_label = 'Producto'


ValeFormset = forms.modelformset_factory(Vale, form = ValeForm)
ValeFormsets = formsets_factory(ValeFormset)
PickProductFormset = forms.formset_factory(PickProductForm)




    
