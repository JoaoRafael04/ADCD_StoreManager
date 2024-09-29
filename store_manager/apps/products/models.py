from django.db import models

# Create your models here.
from django.db import models


class Produtos(models.Model):
    nome = models.CharField(max_length=200, null=False)
    marca = models.CharField(max_length=200, null=False)
    producao = models.CharField(max_length=200, null=False)
    frete_gratis = models.BooleanField(default=False)
    altura = models.IntegerField(default=0)
    largura = models.IntegerField(default=0)
    profundidade = models.IntegerField(default=0)
    itens_para_caixa = models.BooleanField(default=False)

    medida_1 = 'mm'
    medida_2 = 'cm'
    medida_3 = 'm'

    opcoes_medidas = [
        # 1º Parâm. armazena no BD, o 2º é o mostrado no formulário.
        (medida_1, 'mm'),
        (medida_2, 'cm'),
        (medida_3, 'm'),
    ]

    unidade_medida = models.CharField(
        max_length=2,
        choices=opcoes_medidas,
        default=medida_1
    )
    
    validade = models.DateField()

    def __str__(self):
        return self.nome