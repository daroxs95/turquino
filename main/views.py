import io
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from main.models import Producto, Vale, ValeSalida,LastSession, Tipos
from .forms import GetModelForm, ValeForm, ValeSalidaForm, PickProductFormset, ValeFormsets
from main.templatetags.utils import retrive_lst, initWithData

from django.shortcuts import render
from django.views.generic import ListView

# Create your views here.
def NuevoVale(request):
    DATA = {
        'formsets-TOTAL_FORMSETS':'2',
        'formsets0-TOTAL_FORMS': '2',
        'formsets0-INITIAL_FORMS': '0',
        'formsets1-TOTAL_FORMS': '2',
        'formsets1-INITIAL_FORMS': '0',
        'pickPFormset-TOTAL_FORMS': '2',
        'pickPFormset-INITIAL_FORMS': '0',
        }

    valeSalidaForm = ValeSalidaForm(request.POST or None)
    #valeFormSet = ValeFormset(request.POST or initWithData(DATA,"formset1"), prefix='formset1')#revisar si se inicializan bien ambos
#    formsets = ValeFormsets(ValeFormset,request.POST , DATA)
    formsets = ValeFormsets(request.POST or DATA, prefix='formsets')

    #formsets = ValeFormsets(ValeFormset, DATA)

    pickProductFormset = PickProductFormset(request.POST or DATA,prefix='pickPFormset')

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
                    vale2save.valesalida = valesalida
                    vale2save.tipo_de_produccion = tipo_de_produccion
                    vale2save.save()
    tipos = Tipos.as_list()

    return render(request,'vale.html',{'pickProductFormset':pickProductFormset,
                                       'valesalidaform':valeSalidaForm,
                                       #'tipos': Tipos.as_list(),
                                       'formsets':formsets,
                                       'tipos': tipos,
                                       })
        

def MainFunc(request,actual_type = 'PN', desde = '2019-10-05', hasta ='2020-10-05'):
    #lsActualType = LastSession.objects.filter(option = 'actual_type')[0]
    #lstdesde = LastSession.objects.filter(option = 'desde')[0]
    #lsthasta = LastSession.objects.filter(option = 'hasta')[0]

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
    
    tipos = Tipos.as_list()
    
    return render(request, 'Main.html', {'tipos': tipos,
                                         'actual_type':actual_type,
                                         'desde':desde,
                                         'hasta':hasta,
                                         'form':form})

