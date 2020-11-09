from main.models import Tipos

def agregar_tipos_consumo(request):
    tipos = Tipos.as_list()
    context_data = dict()    
    context_data['tipos'] = tipos 
    return context_data
