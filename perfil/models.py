from django.db import models
from datetime import datetime

# Create your models here.
class Categoria (models.Model):
    categoria = models.CharField(max_length=50)
    essencial = models.BooleanField(default=False)
    valor_planejamento = models.FloatField(default=0)

    def __str__(self):
        return self.categoria
    
    def total_gasto(self):
        from extrato.models import Valores 
        valores = Valores.objects.filter(categoria__id = self.id).filter(data__month=datetime.now().month).filter(tipo='S')
        
        #TODO criar um arquivo utils para desenvolver regra de negocios
        total_valor = 0
        for valor in valores:
            total_valor += valor.valor
            
        return total_valor
    
    def percentual_gasto_categoria(self):
        return int(self.total_gasto()*100/self.valor_planejamento)

class Conta(models.Model):

    BANCO_CHOICES = (
        ('NU', 'nubank'),
        ('CX', 'caixa'),
    )

    TIPO_CHOICES = (
        ('PF','pessoa fisica'),
        ('PJ', 'pessoa juridica'),
    )

    apelido = models.CharField(max_length=50)
    banco =  models.CharField(max_length=2, choices=BANCO_CHOICES)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES)
    valor = models.FloatField()
    icone = models.ImageField(upload_to="icones")

    def __str__(self):
        return self.apelido