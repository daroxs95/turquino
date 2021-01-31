from django.db import models
from django.utils import timezone
from datetime import date , datetime
# Create your models here.

class LastSession(models.Model):
    option = models.CharField(max_length=80)
    value = models.CharField(max_length=80)
    
    objects = models.Manager()

class Producto(models.Model):
    name = models.CharField(max_length=80)

    precio = models.FloatField() #no se si usar decimalfield instead
    identificador = models.CharField(max_length=80,primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    last_exit = models.DateTimeField(default = datetime.now, editable = False)#0,0 if never used, check if on editable = false, it can be edited outside the django admin 

    objects = models.Manager()
    
    class Meta:
       ordering=("name","precio")
    
    @classmethod
    def names_as_list(self):       
        allPRODUCTS = self.objects.all()
        productlist = []
        try:
            for product in allPRODUCTS:
                if [product.name,product.name] not in productlist:
                    productlist.append([product.name,product.name])
        except: return []
        return productlist

    def __str__(self):
        return self.name+" "+str(self.precio)

class EntradaFT(models.Model):
    TIPOS = (('F', 'Factura'),('T', 'Traslado'))
    tipo = models.CharField(max_length=20,choices=TIPOS)
    Procedencia = models.CharField(max_length=80)
    No_documento = models.CharField(max_length=80)
    producto = models.ManyToManyField(Producto,through='FT',verbose_name="Producto que entra")
    dia = models.DateField(default=datetime.now)
    
    identificador = models.CharField(max_length=80,primary_key=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.tipo + ':' + self.No_documento    

class SalidaFT(models.Model):
    Destino = models.CharField(max_length=80)
    No_documento = models.CharField(max_length=80)
    producto = models.ManyToManyField(Producto,through='FTS',verbose_name="Producto que sale")
    dia = models.DateField(default=datetime.now)

    identificador = models.CharField(max_length=80,primary_key=True)

    created = models.DateTimeField(auto_now_add=True,null=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()    
    def __str__(self):
        return self.No_documento

class ValeSalida(models.Model):
    No_documento = models.CharField(max_length=80)
    dia = models.DateField(default=date.today)
    producto = models.ManyToManyField(Producto,through='Vale')

    identificador = models.CharField(max_length=80,primary_key=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager() 
    def __str__(self):
        return self.No_documento   

class Tipos(models.Model):
    key = models.CharField(max_length=50,primary_key=True)
    verbose_name = models.CharField(max_length=50)
    
    objects = models.Manager()
    
    def __str__(self):
        return self.verbose_name
    
    @classmethod
    def as_list(self):       
        allPRODUCTS = self.objects.all()
        productlist =[]
        for product in allPRODUCTS:
            productlist.append([product.key,product.verbose_name])
        return productlist

class Vale(models.Model):
    valesalida = models.ForeignKey(ValeSalida, on_delete=models.CASCADE)
    tipo_de_produccion = models.ForeignKey(Tipos, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE,verbose_name="Producto usado")
    cantidad = models.FloatField(default = 0)
    importe = models.FloatField(default = 0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    def save(self, *args, **kwargs):
        self.producto.last_exit = datetime.now()
        super(Vale,self).save( *args, **kwargs)
    
    @staticmethod
    def fields(self):
        return ('valesalida', 'producto','cantidad', 'importe',)

class FT(models.Model):
    entradaFt = models.ForeignKey(EntradaFT, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  
    cantidad = models.FloatField(default = 0)
    importe = models.FloatField(default = 0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class FTS(models.Model):
    salidaFt = models.ForeignKey(SalidaFT, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  
    cantidad = models.FloatField(default = 0)
    importe = models.FloatField(default = 0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Final(models.Model):
    dia = models.DateField(default=datetime.now)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.FloatField(default = 0)
    importe = models.FloatField(default = 0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['dia', 'producto'], name='unique_final')
        ]

class CantidadPredefinida(models.Model):
    identificador = models.AutoField(primary_key=True)
    tipo_de_produccion = models.ForeignKey(Tipos, on_delete=models.CASCADE)
    producto_name = models.CharField(max_length=80)
    cantidad = models.FloatField(default = 0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tipo_de_produccion', 'producto_name'], name='unique_cantidad_predefinida')
        ]

