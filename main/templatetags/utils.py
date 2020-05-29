from main.models import Producto, Vale, ValeSalida, EntradaFT, FT, FTS

def calc_consumo(desde, hasta, productos):
    used_products = productos
    table_data = [] 

    for ii in used_products:
      cell_cantidad = 0

      for item in Vale.objects.filter(valesalida__dia__gte = desde , valesalida__dia__lte = hasta):
        if item.producto == ii:
          cell_cantidad = cell_cantidad + item.cantidad
                    
      table_data.append(cell_cantidad)

    return table_data 

def calc_consumo_by_type(desde, hasta, productos,table_type):
    used_products = productos
    table_data = [] 

    for ii in used_products:
      cell_cantidad = 0

      for item in Vale.objects.filter(tipo_de_produccion = table_type,valesalida__dia__gte = desde , valesalida__dia__lte = hasta):
        if item.producto == ii:
          cell_cantidad = cell_cantidad + item.cantidad
                    
      table_data.append(cell_cantidad)

    return table_data

def calc_total_entradas(desde, hasta, productos):
    used_products = productos
    table_data = [] 

    for ii in used_products:
      cell_cantidad = 0

      for item in FT.objects.filter(entradaFt__dia__gte = desde , entradaFt__dia__lte = hasta):
        if item.producto == ii:
          cell_cantidad = cell_cantidad + item.cantidad
                    
      table_data.append(cell_cantidad)

    return table_data 

def calc_total_salidas(desde, hasta, productos):
    used_products = productos
    table_data = [] 

    for ii in used_products:
      cell_cantidad = 0

      for item in FTS.objects.filter(salidaFt__dia__gte = desde , salidaFt__dia__lte = hasta):
        if item.producto == ii:
          cell_cantidad = cell_cantidad + item.cantidad
                    
      table_data.append(cell_cantidad)

    return table_data 

def calc_consumo_importes(desde, hasta, productos):
    used_products = productos
    table_data = [] 

    for ii in used_products:
      cell_cantidad = 0

      for item in Vale.objects.filter(valesalida__dia__gte = desde , valesalida__dia__lte = hasta):
        if item.producto == ii:
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
  result = str(int(fechaf[0]) + anno)+'-'+ str(int(fechaf[1]) + mes)+'-' + str(int(fechaf[2]) + dia)
  
  return result

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

def initWithData(DATA, prefix):#this is for initing(and needed in a list of formsets) a formset with a DATA dict, appending the formset prefix,
  initializedDATA = {}

  for key in DATA.keys():
    initializedDATA[prefix +"-"+ key] = DATA[key]
    
  return initializedDATA

defLST = {'actual_type': 'PN', 'desde': '2010-10-10','hasta': '2020-10-10'}