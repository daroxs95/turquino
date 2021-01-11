from main.models import Producto, Vale, ValeSalida, EntradaFT, FT, FTS , CantidadPredefinida
from datetime import datetime, timedelta
from calendar import monthrange

def calc_consumo(desde, hasta, productos):
    used_products = productos
    table_data = [] 
    queryset = Vale.objects.filter(valesalida__dia__gte = desde , valesalida__dia__lte = hasta);

    for ii in used_products:
      cell_cantidad = 0

      for item in queryset.filter(producto = ii):
        cell_cantidad = cell_cantidad + item.cantidad
                    
      table_data.append(round(cell_cantidad, 3))

    return table_data 

def calc_consumo_by_type(desde, hasta, productos,table_type):
    used_products = productos
    table_data = [] 
    queryset = Vale.objects.filter(tipo_de_produccion = table_type,valesalida__dia__gte = desde , valesalida__dia__lte = hasta);

    for ii in used_products:
      cell_cantidad = 0

      for item in queryset.filter(producto = ii):
        cell_cantidad = cell_cantidad + item.cantidad
                    
      table_data.append(round(cell_cantidad, 3))

    return table_data

def calc_total_entradas(desde, hasta, productos):
    used_products = productos
    table_data = [] 
    queryset = FT.objects.filter(entradaFt__dia__gte = desde , entradaFt__dia__lte = hasta);

    for ii in used_products:
      cell_cantidad = 0

      for item in queryset.filter(producto = ii):
        cell_cantidad = cell_cantidad + item.cantidad
                    
      table_data.append(cell_cantidad)

    return table_data 

def calc_total_salidas(desde, hasta, productos):
    used_products = productos
    table_data = [] 
    queryset = FTS.objects.filter(salidaFt__dia__gte = desde , salidaFt__dia__lte = hasta);

    for ii in used_products:
      cell_cantidad = 0

      for item in queryset.filter(producto = ii):
        cell_cantidad = cell_cantidad + item.cantidad
                    
      table_data.append(cell_cantidad)

    return table_data 

def calc_consumo_importes(desde, hasta, productos):
    used_products = productos
    table_data = [] 
    queryset = Vale.objects.filter(valesalida__dia__gte = desde , valesalida__dia__lte = hasta)
    for ii in used_products:
      cell_cantidad = 0

      for item in queryset.filter(producto = ii ):
        cell_cantidad = cell_cantidad + item.importe
                    
      table_data.append(cell_cantidad)

    return table_data 

def max_len_of_filas(lista):
  max_len = 0
  for i in range(0,len(lista)):
    if len(lista[i]) > max_len:
      max_len = len(lista[i])
  return max_len

def is_in(objeto,lista):
  for i in lista:
    if i == objeto:
      return True
  return False             

def calc_total(tabla): 
  total=[]
  if len(tabla) == 0:
    return None
  for i in range(0,len(tabla[0])):
    total.append(0)
  for i in range(0,len(tabla)):
    for ii in range(0,len(tabla[i])):
      if type(tabla[i][ii]) == int or type(tabla[i][ii]) == float:
        total[ii] = round(total[ii] + tabla[i][ii],2)
  return total      

def change_date(fecha ,anno = 0 , mes = 0, dia = 0 ):
  fechaf = fecha.split('-')
  current_date = datetime(int(fechaf[0]),int(fechaf[1]),int(fechaf[2]))
  result = current_date.replace(year= current_date.year + anno)
  dt= timedelta(days= mes*30 + dia )
  result = result + dt
  return result.date().__str__()

def make_dict_for_table_render(values,colspan=1,rowspan=1):
    keys = ['value' , 'colspan', 'rowspan']
    a=[]
    for value in values:
      cell_dict = {}
      for key in keys:
        cell_dict[key]=eval(key)
      a.append(cell_dict)
    return a

def init_dict_for_table_render(values,colspans,rowspans):
    keys = ['value' , 'colspan', 'rowspan']
    a=[]
    for value,colspan,rowspan in zip(values,colspans,rowspans):
      cell_dict = {}
      for key in keys:
        cell_dict[key]=eval(key)
      a.append(cell_dict)
    return a

def retrive_lst(place,field):
  try:
    result = place.objects.filter(option = field)[0]
  except:
    result = place(option = field,value = defLST[field] or 0)
    result.save()
  return result

def retrieve_predefined_production(production_type, amount):
  items = CantidadPredefinida.objects.filter(tipo_de_produccion = production_type)
  result = []
  for item in items:
    result.append({'producto':Producto.objects.filter(name = item.producto_name).order_by('-last_exit')[0],'cantidad':round(float(amount)*item.cantidad,3)})
  return result

def create_DATA_for_formset_with_custom_forms(prefix, list_of_Dict_of_fields):#list_of_Dict_of_fields is the returned object of retrieve_predefined_production
  DATA = {}
  total_forms = 0
  initial_forms = 0
  for dict_of_fields in list_of_Dict_of_fields:
    for key in dict_of_fields:
      DATA[prefix+'-'+str(total_forms)+'-'+key] = dict_of_fields[key]
    total_forms = total_forms + 1
  DATA[prefix+'-'+'TOTAL_FORMS'] = total_forms
  DATA[prefix+'-'+'INITIAL_FORMS'] = initial_forms

  return DATA

defLST = {'actual_type': 'PN', 'desde': '2010-10-10','hasta': '2020-10-10'}