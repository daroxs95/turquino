from django import template
from main.models import Producto, Vale, ValeSalida, EntradaFT, FT, FTS

register = template.Library()


@register.simple_tag
def get_value_of_cell(cell):
  return get_value_from_key(cell,'value')

@register.simple_tag
def get_colspan_of_cell(cell):
  return get_value_from_key(cell,'colspan')

@register.simple_tag
def get_rowspan_of_cell(cell):
  return get_value_from_key(cell,'rowspan')

@register.simple_tag
def get_value_from_key(object, key):
    if key == 'producto':
        return object.producto
    if key == 'valesalida':
        return object.valesalida
    if type(object) == dict:
        return object[key]
    else:
        return object.__dict__[key]  

@register.simple_tag
def get_vervosename_from_tuple(object, key):
    for i in object:
      if i[0] == key:
        return i[1]
    return 'BASE DE DATOS VACIA'

@register.simple_tag
def get_verbose_model_type(tipos, actual_type):
  if actual_type == 'MMP':
    return 'Movimiento de materias primas'
  if actual_type == 'MMPV':
    return 'Movimiento de materias primas en valores'
  if actual_type == 'IC':
    return 'Indices de Consumo'
  else:
    return 'Consumo de ' + get_vervosename_from_tuple(tipos,actual_type)

@register.simple_tag
def get_value_from_index(object, index):
    return object[index]

