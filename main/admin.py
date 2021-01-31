from django.contrib import admin
from main.models import Producto, EntradaFT, ValeSalida, Vale, SalidaFT, FT, FTS, Final, LastSession, Tipos, CantidadPredefinida
from main.forms import CantidadPredefinidaAdminForm 

# Register your models here.
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('name','precio','last_exit')
    list_filter = ('name','precio','last_exit')
    search_fields = ('name','precio','last_exit')
    prepopulated_fields = {'identificador': ('precio','name')}
    #raw_id_fields = ('name',)
    date_hierarchy = 'created'
    ordering = ('name','precio','last_exit')

@admin.register(EntradaFT)
class EntradaAdmin(admin.ModelAdmin):
    list_display = ('Procedencia','No_documento','dia')
    list_filter = ('producto','Procedencia','No_documento','dia')
    search_fields = ('producto','Procedencia','No_documento','dia')
    ordering = ('dia','No_documento','dia')
    date_hierarchy = 'created'
    prepopulated_fields = {'identificador': ('No_documento','dia')}


@admin.register(SalidaFT)
class SalidaAdmin(admin.ModelAdmin):
    list_display = ('Destino','No_documento','dia')
    list_filter = ('producto','Destino','No_documento','dia')
    search_fields = ('producto','Destino','No_documento','dia')
    ordering = ('dia','No_documento','dia')
    date_hierarchy = 'created' 
    prepopulated_fields = {'identificador': ('No_documento','dia')}



@admin.register(ValeSalida)
class valesalidaAdmin(admin.ModelAdmin):
    list_display = ('dia','No_documento','identificador','created','updated')
    search_fields = ('No_documento','producto')
    date_hierarchy = 'created'
    ordering = ('dia','No_documento')    
    prepopulated_fields = {'identificador': ('No_documento','dia')}   
    
@admin.register(Vale)
class valeAdmin(admin.ModelAdmin):
    list_display = ('tipo_de_produccion','valesalida','producto','cantidad','importe','valesalida_dia')
    list_filter = ('tipo_de_produccion','valesalida','producto','cantidad','importe','valesalida__dia')
    search_fields = ('tipo_de_produccion','valesalida','producto','cantidad','importe','valesalida_dia')
    date_hierarchy = 'created'
    ordering = ('tipo_de_produccion','created','valesalida','valesalida__dia') 
    def valesalida_dia(self,obj):
        return obj.valesalida.dia
    #prepopulated_fields = {'importe': ('cantidad',)}  #no pincha con los float dice q no tienen atributo maxlength
    #raw_id_fields = ('producto',)  #no se que pasa si descomento esto, no veo cambio aparente
    
@admin.register(FT)
class FTAdmin(admin.ModelAdmin):
    list_display = ('entradaFt','producto','cantidad','importe')
    list_filter = ('entradaFt','producto','cantidad','importe')
    search_fields = ('entradaFt','producto','cantidad','importe')
    date_hierarchy = 'created'
    ordering = ('entradaFt','producto','cantidad','importe')

@admin.register(FTS)
class FTSAdmin(admin.ModelAdmin):
    list_display = ('salidaFt','producto','cantidad','importe')
    list_filter = ('salidaFt','producto','cantidad','importe')
    search_fields = ('salidaFt','producto','cantidad','importe')
    date_hierarchy = 'created'
    ordering = ('salidaFt','producto','cantidad','importe')    

@admin.register(Final)
class FinalesAdmin(admin.ModelAdmin):
    list_display = ('dia','producto','cantidad','importe')
    list_filter = ('dia','producto','cantidad','importe')
    search_fields = ('dia','producto','cantidad','importe')
    date_hierarchy = 'created'
    ordering = ('dia','producto','cantidad','importe') 

@admin.register(LastSession)
class LastSessionAdmin(admin.ModelAdmin):
    list_display = ('option','value')

@admin.register(Tipos)
class TiposAdmin(admin.ModelAdmin):
    pass
    
@admin.register(CantidadPredefinida)
class CantidadPredefinidaAdmin(admin.ModelAdmin):
    list_display = ('tipo_de_produccion','producto_name','cantidad')
    list_filter = ('tipo_de_produccion','producto_name','cantidad')
    search_fields = ('tipo_de_produccion','producto_name','cantidad')
    date_hierarchy = 'created'
    ordering = ('tipo_de_produccion','producto_name','cantidad')
    form = CantidadPredefinidaAdminForm