import io
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils import timezone
import json
from datetime import datetime

from main.models import Producto, Vale, ValeSalida,LastSession, Tipos, CantidadPredefinida, Final
from .forms import GetModelForm, ValeFormset, ValeSalidaForm, PickProductFormset, CantidadPredefinidaFormset
from .forms import ValeFormsets, PickProductForm, CantidadPredefinidaFillForm, ProduccionForm
from .forms import FTEntradaFormset, EntradaFTForm, ProductoForm, FTSalidaFormset, SalidaFTForm
from main.templatetags.utils import retrive_lst , retrieve_predefined_production, create_DATA_for_formset_with_custom_forms, get_message_of_db_adding

from django.shortcuts import render
from django.views.generic import ListView

# Create your views here.
def MainFunc(request,actual_type = 'PN', desde = '2019-10-05', hasta ='2020-10-05'):
    lsActualType = retrive_lst(LastSession,'actual_type')
    lstdesde = retrive_lst(LastSession,'desde')
    lsthasta = retrive_lst(LastSession,'hasta')


    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GetModelForm(request.POST)
        
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            cd = form.cleaned_data
            # redirect to a new URL:
            return HttpResponseRedirect('/'+'?desde='+str(cd['desde'])+'&hasta='+str(cd['hasta']))

            # if a GET (or any other method) we'll create a blank form
    else:
        form = GetModelForm()
        desde = request.GET.get('desde') or lstdesde.value
        hasta = request.GET.get('hasta') or lsthasta.value
        actual_type = request.GET.get('actualtype') or lsActualType.value


        lsthasta.value = hasta
        lstdesde.value = desde
        lsActualType.value = actual_type

        lsActualType.save()
        lstdesde.save()
        lsthasta.save()
    
    return render(request, 'Main.html', {'actual_type':actual_type,
                                         'desde':desde,
                                         'hasta':hasta,
                                         'form':form})

def GetProductionFormset(request):
    DATA = {
        'formsets-0-TOTAL_FORMS': '5',
        'formsets-0-INITIAL_FORMS': '0',
        #'formsets-0-0-cantidad': 355
        }
    formset_prefix = 'formsets-0'
    formset = ValeFormset(DATA, prefix = formset_prefix)

    if request.method =='POST':
        producto = request.POST.get('producto','none')
        cantidad = request.POST.get('cantidad', 0 )

        PPForm = PickProductForm({'pickPFormset-0-tipo':producto}, prefix='pickPFormset-0')#aqui tiene el prefijo para q jquery pueda encontrarlo y actualizar los indices, para poder usarlo correctamente en el formset de nuevo vale
        
        DATA = create_DATA_for_formset_with_custom_forms(formset_prefix,retrieve_predefined_production(producto , cantidad))
        formset = ValeFormset(DATA, prefix = formset_prefix)

    return render(request,'production_formset.html',{'formset':formset,
                                    'products':PPForm,
                                    })

def AddProduct(request):
    form = ProductoForm(request.POST or None)
    status = 'idle'

    if request.method =='POST':
        if form.is_valid():
            form2save = form.save(commit=False)
            form2save.created = timezone.now()
            form2save.identificador = str(form2save.precio) + '-'+ form2save.name
            form2save.save()
            status = 'success'
        if status != 'success':
            status = 'error'
    
    message = get_message_of_db_adding(status)
    
    if request.is_ajax():
        return render(request,'message.html',{'title':message['title'],
                                       'content':message['content'],
                                       'color':message['color'],
                                       })
    else:
        return render(request,'addProduct_form.html',{'form':form,
                                                    'message': message,
                                                    })

def AddFinals(request):
    status = 'idle'

    if request.method =='POST':
        json_data = json.loads(request.POST.get('dataJSON'))
        for item in json_data['finals']:
            product = Producto.objects.get(name = item['name'], precio = item['price'])
            try:
                final2save = Final.objects.get(dia = json_data['date'] , producto = product)
            except:
                final2save = Final(dia = json_data['date'], producto = product)

            final2save.cantidad= item['amount']
            final2save.importe= item['value']

            final2save.save()
            status = 'success'
        if status != 'success':
            status = 'error'

        message = get_message_of_db_adding(status)

    return render(request,'message.html',{'title':message['title'],
                                       'content':message['content'],
                                       'color':message['color'],
                                       })

def NuevoVale(request):
    DATA = {
        'formsets-TOTAL_FORMSETS':'2',
        'formsets-0-TOTAL_FORMS': '5',
        'formsets-0-INITIAL_FORMS': '0',
        'formsets-1-TOTAL_FORMS': '5',
        'formsets-1-INITIAL_FORMS': '0',
        'pickPFormset-TOTAL_FORMS': '2',
        'pickPFormset-INITIAL_FORMS': '0',
        }

    valeSalidaForm = ValeSalidaForm(request.POST or None)
    formsets = ValeFormsets(request.POST or DATA, prefix='formsets')
    pickProductFormset = PickProductFormset(request.POST or DATA,prefix='pickPFormset')
    status = 'idle'

    cantidadPredefinidaForm = CantidadPredefinidaFillForm()
    if request.method =='POST':
            if valeSalidaForm.is_valid() and formsets.is_valid() and pickProductFormset.is_valid():
                valesalida = valeSalidaForm.save(commit=False)
                valesalida.identificador = valesalida.No_documento + '-'+ str(valesalida.dia)
                try:
                    valesalida.created = ValeSalida.objects.get(identificador=valesalida.identificador).created
                except:
                    pass
                valesalida.save()

                for formset, pickProductForm in zip(formsets,pickProductFormset):
                    tipo_de_produccion = pickProductForm.cleaned_data['tipo']
                    for vale in formset:
                        vale2save = vale.save(commit=False)
                        print(vale2save.producto.identificador)
                        Producto.objects.filter(identificador = vale2save.producto.identificador).update(last_exit = datetime.now())

                        vale2save.valesalida = valesalida
                        vale2save.tipo_de_produccion = tipo_de_produccion
                        vale2save.save()
                status = 'success'

            if status != 'success':
                status = 'error'

    return render(request,'nuevo_vale.html',{'pickProductFormset':pickProductFormset,
                                       'valesalidaform':valeSalidaForm,
                                       #'tipos': Tipos.as_list(),
                                       'formsets':formsets,
                                       'cantidadPredefinidaForm':cantidadPredefinidaForm,
                                       'message': get_message_of_db_adding(status),
                                       })

def NuevaProduccion(request):
    DATA = {
        'formset-TOTAL_FORMS': '5',
        'formset-INITIAL_FORMS': '0',
        }

    produccionForm = ProduccionForm(request.POST or None)
    formset = CantidadPredefinidaFormset(request.POST or DATA, prefix='formset')
    status = 'idle'
    
    for form in formset:
        form.fields['producto_name'].choices = Producto.names_as_list()

    if request.method =='POST':
        if produccionForm.is_valid() and formset.is_valid():
            produccion = produccionForm.save(commit=False)
            produccion.key = produccion.verbose_name.replace(" ", "_")
            try:
                produccion.created = Tipos.objects.get(key=produccion.key).created#no se si sea necesario hacerlo aqui
            except:
                pass    
            produccion.save()
            for CantidadPredefinidaItem in formset:
                CantidadPredefinida2save = CantidadPredefinidaItem.save(commit=False)
                CantidadPredefinida2save.tipo_de_produccion = produccion
                CantidadPredefinida2save.producto_name = CantidadPredefinidaItem.cleaned_data['producto_name']
                try:
                    CantidadPredefinida2save.created = CantidadPredefinida.objects.get(producto_name=CantidadPredefinida2save.producto_name).created#no se si sea necesario hacerlo aqui
                except:
                    pass
                CantidadPredefinida2save.save()
            status = 'success'

        if status != 'success':
            status = 'error'

    return render(request,'nueva_produccion.html',{'produccionForm':produccionForm,
                                       'formset':formset,
                                       'message': get_message_of_db_adding(status),
                                       })

def NuevoTrasladoEmitido(request):
    DATA = {
        'formset-TOTAL_FORMS': '1',
        'formset-INITIAL_FORMS': '0',
        }

    salidaFTForm = SalidaFTForm(request.POST or None)
    formset = FTSalidaFormset(request.POST or DATA, prefix='formset')
    productoForm = ProductoForm(request.POST or None)
    status = 'idle'

    if request.method =='POST':
        if salidaFTForm.is_valid() and formset.is_valid():
            salidaFT = salidaFTForm.save(commit=False)
            salidaFT.identificador = salidaFT.No_documento + '-'+ str(salidaFT.dia)
            try:
                salidaFT.save()
            except:
                pass

            for FTform in formset:
                FTform2save = FTform.save(commit=False)
                FTform2save.salidaFt = salidaFT
                FTform2save.created = timezone.now()
                FTform2save.save()
            status = 'success'

        if status != 'success':
            status = 'error'

    return render(request,'nuevo_traslado_emitido.html',{'salidaFTForm':salidaFTForm,
                                       'formset':formset,
                                       'productoForm':productoForm,
                                       'message': get_message_of_db_adding(status),
                                       })

def NuevaFT(request):
    DATA = {
        'formset-TOTAL_FORMS': '1',
        'formset-INITIAL_FORMS': '0',
        }
    status = 'idle'

    entradaFTForm = EntradaFTForm(request.POST or None)
    formset = FTEntradaFormset(request.POST or DATA, prefix='formset')
    productoForm = ProductoForm(request.POST or None)

    if request.method =='POST':
        if entradaFTForm.is_valid() and formset.is_valid():
            entradaFT = entradaFTForm.save(commit=False)
            entradaFT.identificador = entradaFT.No_documento + '-'+ str(entradaFT.dia)
            try:
                entradaFT.save()
            except:
                pass

            for FTform in formset:
                FTform2save = FTform.save(commit=False)
                FTform2save.entradaFt = entradaFT
                FTform2save.created = timezone.now()
                FTform2save.save()
            status = 'success'

        if status != 'success':
            status = 'error'


    return render(request,'nueva_ft.html',{'entradaFTForm':entradaFTForm,
                                       'formset':formset,
                                       'productoForm':productoForm,
                                       'message': get_message_of_db_adding(status),
                                       })