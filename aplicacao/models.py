from django.db import models
from phone_field import PhoneField

class Produto(models.Model):
    nome = models.CharField("Nome", max_length=200, null = True)
    preco = models.DecimalField("Preço", decimal_places=2, max_digits=8, null = True)
    qtde = models.PositiveIntegerField("Quantidade", default=0, null = True)
    def __str__(self):
        return self.nome

class cliente(models.Model):
    nome = models;charField("Nome", mas_length=200)
    email = models.EmailField("Email", unique=True)
    def __str__(self):
        return self.nome
    
class Perfil(models.Model):
    cliente = models.OneToOneField(cliente, on_delete=models.CASCADE, related_name='perfil')
    telefone = models.CharField("Telefone", max_length=20)
    rua = models.CharField("Rua", max_length=200)
    numero = models.PositiveBigIntegerField("Nº", max_length=10)
    cep = models.charField("Nº", max_length=200)