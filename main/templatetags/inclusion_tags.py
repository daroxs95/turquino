from django import template
from main.models import Producto, Vale, ValeSalida, EntradaFT, FT, FTS, Final
from main.templatetags.utils import calc_consumo, calc_consumo_by_type, calc_total_entradas, calc_total_salidas
from main.templatetags.utils import calc_consumo_importes, is_in, calc_total, change_date, make_dict_for_table_render, init_dict_for_table_render
from main.templatetags.simple_tags import get_vervosename_from_tuple

register = template.Library()

sort_criteria = {
	"harina": 1,
	"levadura": 2,
	"azucar": 3,
	"azúcar": 4,
	"azucar refino": 5,
	"azúcar refino": 6,
	"sal": 7,
	"aceite": 8,
	"núcleo": 9,
	"miel de abeja": 10,
	"mejorador": 11,
	"petróleo planta": 9999,
	"petróleo planta (2)": 9999,
	"petróleo regular": 99999,
}
petrol_names = ['petróleo regular', 'petróleo planta', "petróleo planta (2)"]


@register.inclusion_tag('tablas/tabla.html')
def make_consumo_table(desde, hasta, table_type):
		used_products = []
		used_products_verbose_name = []
		prices = []
		vales_salida = []
		table_data = []
	
		query = Vale.objects.filter(tipo_de_produccion = table_type , valesalida__dia__gte = desde , valesalida__dia__lte = hasta)

		a = query.order_by('producto__name')
		for item in a:
			if is_in(item.producto,used_products) == False:
				used_products.append(item.producto)
				#used_products_verbose_name.append(get_vervosename_from_tuple(tipoproducto,item.producto.name))
				used_products_verbose_name.append(item.producto.name)
				prices.append(item.producto.precio)

		a = query.order_by('valesalida__dia')
		for item in a:
			if is_in(item.valesalida.identificador,vales_salida) == False:
				vales_salida.append(item.valesalida.identificador)
		
		sortedRes = sorted(zip(used_products, prices, used_products_verbose_name), key=lambda x: sort_criteria.get(x[0].name, 999))
		used_products = [x for (x, y, z) in sortedRes]
		prices = [y for (x, y, z) in sortedRes]
		used_products_verbose_name = [z for (x, y, z) in sortedRes]

		for i in vales_salida:
			 cached_rows=[]
			 queryset = a.filter(valesalida__identificador = i)
			 cached_rows.append(queryset[0].valesalida.No_documento)#revisar si esto sirve, creo q si pero no estoy seguro
			 
			 for ii in used_products:
					cell_cantidad = 0

					for item in queryset:
						if is_in(item.valesalida.dia,cached_rows) == False:
							cached_rows.append(item.valesalida.dia)
						if item.producto == ii:
							cell_cantidad = cell_cantidad + item.cantidad
							
					if cell_cantidad == 0:
						cached_rows.append('')
					else: 
						cached_rows.append(cell_cantidad)     
			 table_data.append(cached_rows)

		used_products_verbose_name.insert(0,'')
		used_products_verbose_name.insert(0,'')

		prices.insert(0,'')
		prices.insert(0,'')

		totales = ['Totales',''] 
		totales.extend(calc_consumo_by_type(desde,hasta,used_products,table_type))
		table_data.append(totales)

		head = []
		head.append(make_dict_for_table_render(used_products_verbose_name))
		head.append(make_dict_for_table_render(prices))

		return {'data': table_data,'head': head}    

@register.inclusion_tag('tablas/tabla.html')
def make_mov_materias_primas(desde, hasta):
		used_products = []
		prices = []
		vales = []
		vales_verbose_name = []
		vales_salida = []
		table_data_salida = []
		table_data = []
		#tipoproducto = Producto.PRODUCTS
		used_products_verbose_name = []
		exist_inicial = ['existencia inicial','','']

		facturas_traslados = FT.objects.filter(entradaFt__dia__gte = desde , entradaFt__dia__lte = hasta)
		traslados_emitidos = FTS.objects.filter(salidaFt__dia__gte = desde , salidaFt__dia__lte = hasta)

		c = Final.objects.filter(dia = change_date(desde,dia= -1) ).order_by('producto__name')
		d = Vale.objects.filter(valesalida__dia__gte = desde , valesalida__dia__lte = hasta).order_by('producto__name')

		for item in d:
			if is_in(item.producto,used_products) == False:
				used_products.append(item.producto)
				prices.append(item.producto.precio)
				used_products_verbose_name.append(item.producto.name)
		for item in c:
			if is_in(item.producto,used_products) == False:
				used_products.append(item.producto)
				prices.append(item.producto.precio)
				used_products_verbose_name.append(item.producto.name)
		
		a = facturas_traslados.order_by('producto__name')
		for item in a:
			if is_in(item.producto,used_products) == False:
				used_products.append(item.producto)
				prices.append(item.producto.precio)
				used_products_verbose_name.append(item.producto.name)

		a = facturas_traslados.order_by('entradaFt__dia')
		for item in a:
			if is_in(item.entradaFt.identificador,vales) == False:
				vales.append(item.entradaFt.identificador)  
				vales_verbose_name.append(item.entradaFt.tipo +" "+ item.entradaFt.No_documento)
	
		b = traslados_emitidos.order_by('producto__name')  
		for item in b:
			if is_in(item.producto,used_products) == False:
				used_products.append(item.producto)
				prices.append(item.producto.precio)
				used_products_verbose_name.append(item.producto.name)

		b = traslados_emitidos.order_by('salidaFt__dia')  
		for item in b:
			if is_in(item.salidaFt.identificador,vales_salida) == False:
				vales_salida.append(item.salidaFt.identificador)  

		sortedRes = sorted(zip(used_products, prices, used_products_verbose_name), key=lambda x: sort_criteria.get(x[0].name, 999))
		used_products = [x for (x, y, z) in sortedRes]
		prices = [y for (x, y, z) in sortedRes]
		used_products_verbose_name = [z for (x, y, z) in sortedRes]

		for i in vales_salida:
			 cached_rows=[]
			 queryset = b.filter(salidaFt__identificador = i)
			 cached_rows.append(queryset[0].salidaFt.No_documento)#revisar si esto sirve, creo q si pero no estoy seguro
			 for ii in used_products:
					cell_cantidad = 0

					for item in queryset:
						if is_in(item.salidaFt.dia,cached_rows) == False:
							cached_rows.append(item.salidaFt.dia)
							cached_rows.append(item.salidaFt.Destino)
						if item.producto == ii:
							cell_cantidad = cell_cantidad + item.cantidad
							
					if cell_cantidad == 0:
						cached_rows.append('')
					else: 
						cached_rows.append(cell_cantidad)     
			 table_data_salida.append(cached_rows)

		for item in used_products:
			cell_cantidad = 0
			for ii in c:
				if ii.producto == item:
						cell_cantidad = cell_cantidad + ii.cantidad
			exist_inicial.append(cell_cantidad)      
		
		table_data.append(exist_inicial)

		for i,isal in zip(vales,vales_verbose_name):
			 cached_rows=[]
			 queryset = a.filter(entradaFt__identificador = i)
			 cached_rows.append(queryset[0].entradaFt)
			 
			 for ii in used_products:
					cell_cantidad = 0

					for item in queryset:
						if is_in(item.entradaFt.dia,cached_rows) == False:
							cached_rows.append(item.entradaFt.dia)
							cached_rows.append(item.entradaFt.Procedencia)
						if item.producto == ii:
							cell_cantidad = cell_cantidad + item.cantidad
							
					if cell_cantidad == 0:
						cached_rows.append('')
					else: 
						cached_rows.append(cell_cantidad)     
			 table_data.append(cached_rows) 

		prices.insert(0,'')
		prices.insert(0,'')
		prices.insert(0,'')

		used_products_verbose_name.insert(0,'')
		used_products_verbose_name.insert(0,'')
		used_products_verbose_name.insert(0,'')

		head = []
		head.append(make_dict_for_table_render(used_products_verbose_name))
		head.append(make_dict_for_table_render(prices))

		totales = ['Disponible','',''] 
		temp_totales = calc_total_entradas(desde, hasta, used_products)
		real_totales = []
		for index, item in enumerate(temp_totales,3):
			real_totales.append(round(item + exist_inicial[index], 3)) 
		totales.extend(real_totales)
		table_data.append(totales)

		totales_descontar = ['Total Enviado','',''] 
		totales_descontar.extend(calc_total_salidas(desde, hasta, used_products))

		consumo_row = ['Consumo','','']
		consumo_row.extend(calc_consumo(desde, hasta, used_products))
		table_data.append(consumo_row)
		
		saldo_final = ['Saldo Final','','']
		for i in range(3,len(totales)):
			saldo_final.append(round(totales[i] - consumo_row[i] - totales_descontar[i],3))
		table_data_salida.append(saldo_final)
		
		importe = ['Importe','','']
		for i in range(3,len(saldo_final)):
			importe.append(round(saldo_final[i] * prices[i],2))
		table_data_salida.append(importe)

		for i in table_data_salida:
			table_data.append(i)   
		
		return {'data': table_data,'head': head,'a':len(a),'b':len(b),'c':len(c),'d':len(d)}

@register.inclusion_tag('tablas/tabla.html')
def make_mov_materias_primas_en_valores(desde, hasta):
		used_products = []
		prices = []
		table_data = []
		tipoEntrada = EntradaFT.TIPOS
		used_products_verbose_name = []

		head=[]
		colspans=[1,1,2,4,4,2]
		rowspans=[3,3,2,1,1,2]
		headrow = init_dict_for_table_render(['Producto','Precio','Existencia Inicial','Entradas','Salidas','Existencia Final'],colspans,rowspans)
		head.append(headrow)
		colspans=[2,2,2,2]
		rowspans=[1,1,1,1]
		headrow = init_dict_for_table_render(['Facturas','Traslados','Consumo','Traslado'],colspans,rowspans)
		head.append(headrow)
		headrow = []
		for i in range(0,6):
				headrow.extend(make_dict_for_table_render(['Fisico']))
				headrow.extend(make_dict_for_table_render(['Valor']))
		head.append(headrow)


		a = FT.objects.filter(entradaFt__dia__gte = desde , entradaFt__dia__lte = hasta).order_by('producto__name')
		b = FTS.objects.filter(salidaFt__dia__gte = desde , salidaFt__dia__lte = hasta).order_by('producto__name')
		c = Final.objects.filter(dia = change_date(desde,dia= -1) ).order_by('producto__name')
		d = Vale.objects.filter(valesalida__dia__gte = desde , valesalida__dia__lte = hasta).order_by('producto__name')
		
		for item in c:
			if is_in(item.producto,used_products) == False:
				used_products.append(item.producto)
				prices.append(item.producto.precio)
				used_products_verbose_name.append(item.producto.name)

		for item in d:
			if is_in(item.producto,used_products) == False:
				used_products.append(item.producto)
				prices.append(item.producto.precio)
				used_products_verbose_name.append(item.producto.name)
		
		for item in a:
			if is_in(item.producto,used_products) == False:
				used_products.append(item.producto)
				prices.append(item.producto.precio)
				#used_products_verbose_name.append(get_vervosename_from_tuple(tipoproducto,item.producto.name))
				used_products_verbose_name.append(item.producto.name)
		 
		for item in b:
			if is_in(item.producto,used_products) == False:
				used_products.append(item.producto)
				prices.append(item.producto.precio)
				used_products_verbose_name.append(item.producto.name)  
		
		sortedRes = sorted(zip(used_products, prices, used_products_verbose_name), key=lambda x: sort_criteria.get(x[0].name, 999))
		used_products = [x for (x, y, z) in sortedRes]
		prices = [y for (x, y, z) in sortedRes]
		used_products_verbose_name = [z for (x, y, z) in sortedRes]
		
		exist_inicial=[]
		exist_inicial_valor=[]
		for item in used_products:
			cell_cantidad = 0
			cell_cantidad_valor = 0
			for ii in c:
				if ii.producto == item:
						cell_cantidad = cell_cantidad + ii.cantidad
						cell_cantidad_valor += ii.importe
			exist_inicial.append(cell_cantidad) 
			exist_inicial_valor.append(cell_cantidad_valor) 
		
		temp_totales = calc_total_entradas(desde, hasta, used_products)
		totales = []
		for index, item in enumerate(temp_totales):
			totales.append(item + exist_inicial[index]) 
			
		totales_descontar = calc_total_salidas(desde, hasta, used_products)
		consumo = calc_consumo(desde, hasta, used_products)
		
		saldo_final = []
		saldo_final_importes = []
		for i in range(0,len(totales)):
			saldo_final.append( round(totales[i] - consumo[i] - totales_descontar[i] , 3))
			saldo_final_importes.append(round(saldo_final[i] * prices[i],2))

		for i,product,price,inicio,inicio_valor,consumo,importe,final,final_importe in zip(used_products,used_products_verbose_name,prices,exist_inicial,exist_inicial_valor,consumo,calc_consumo_importes(desde, hasta, used_products),saldo_final,saldo_final_importes):
			cached_rows=[]
			cached_rows.append(product)
			cached_rows.append(price)
			cached_rows.append(inicio)
			cached_rows.append(inicio_valor)
			importe_entrada = 0
			importe_salida = 0

			for tipo in tipoEntrada:
				cell_cantidad=0
				cell_importe=0
				queryset = a.filter(entradaFt__tipo = tipo[0])
				for ii in queryset:
					if ii.producto == i:
						cell_cantidad = cell_cantidad + ii.cantidad
						cell_importe = cell_importe + ii.importe
						importe_entrada += ii.importe
				
				if cell_cantidad == 0:
						cached_rows.append('')
				else: 
						cached_rows.append(cell_cantidad)
				
				if cell_importe == 0:
						cached_rows.append('')
				else: 
						cached_rows.append(round(cell_importe, 2))

			cached_rows.append(consumo)
			
			cell_cantidad=0
			cell_importe=0
			for ii in b.filter(producto = i):
				cell_cantidad = cell_cantidad + ii.cantidad
				cell_importe = cell_importe + ii.importe
				importe_salida += ii.importe
				
			cached_rows.append(round(inicio_valor + importe_entrada -final_importe - cell_importe,3))#calcula el valor de los consumos

			if cell_cantidad == 0:
					cached_rows.append('')
			else: 
					cached_rows.append(cell_cantidad)
				
			if cell_importe == 0:
					cached_rows.append('')
			else: 
					cached_rows.append(round(cell_importe,3))    

			cached_rows.append(final)
			cached_rows.append(final_importe)

			table_data.append(cached_rows)
		
		index_of_first_petrol = 0
		temp_table_data_product_names = [x[0] for x in table_data ]

		no_petrol_table_data = table_data[:]
		#petrol_table_data = [no_petrol_table_data.pop(i) for i,x in enumerate(no_petrol_table_data) if x[0] in petrol_names ]
		petrol_table_data = []
		for x in table_data:
			if x[0] in petrol_names:
				petrol_table_data.append(x)
				no_petrol_table_data.remove(x)

		no_petrol_table_data.append(calc_total(no_petrol_table_data))
		try:
			no_petrol_table_data[-1][0] = 'Totales'
		except:
			pass

		petrol_table_data.append(calc_total(petrol_table_data))
		try:
		 	petrol_table_data[-1][0] = 'Totales'
		except:
			pass
		
		table_data = no_petrol_table_data + petrol_table_data

		return {'data': table_data, 'head': head}

@register.inclusion_tag('tablas/tabla.html')
def make_indice_consumo(desde,hasta):
	pass

@register.inclusion_tag('tablas/tabla.html')
def show_table(data, head=[]):
		return {'data': data,'head': head}     

@register.inclusion_tag('tablas/tabla.html')
def show_table_type(desde, hasta ,table_type):
	if table_type == 'MMP':
		return make_mov_materias_primas(desde, hasta)
	if table_type == 'MMPV':
		return make_mov_materias_primas_en_valores(desde, hasta)
	if table_type == 'IC':
		return make_indice_consumo(desde, hasta)
	else:
		return make_consumo_table(desde, hasta ,table_type)

@register.inclusion_tag("fieldTooltip.html")
def renderFieldTooltiped(field, style="", css_class=""):
		
		return {
			"style":style,
			"field":field,
			"class":css_class
				
		}

@register.inclusion_tag("forms/basicForm.html")
def renderTooltipedModalForm(form, modal_name="", modal = False, action = ""):
		return {
			"form":form,
			"modal_name":modal_name,
			"modal": modal,
			"action": action
		}

@register.inclusion_tag("message.html")
def renderMessage(title, content, color="green"):#por ahora message_type no hace nada solo salen success
		return {
			"title":title,
			"content":content,
			"color": color,
		}