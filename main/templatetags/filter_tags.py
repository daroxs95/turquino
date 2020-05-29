from django import template

register = template.Library()

@register.filter(name='zip')# ver si puedo regresar algo con algun item por defecto para poder iterar por la list mayor, actualmente solo itera en la plantilla la cantidad de veces = size del menor iterable
def zip_lists(a, b):
  return zip(a, b)