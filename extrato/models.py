from django.db import models
from perfil.models import Categoria, Conta


# Create your models here.
class Valores(models.Model):
    CHOICE_TIPO = (
        ('E', 'Entrada'),
        ('S', 'Saída'),
    )

    valor = models.FloatField()
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    descricao = models.TextField()
    data = models.DateField()
    conta = models.ForeignKey(Conta, on_delete=models.DO_NOTHING)
    tipo = models.CharField(max_length=1, choices=CHOICE_TIPO)

    def __str__(self):
        return self.descricao