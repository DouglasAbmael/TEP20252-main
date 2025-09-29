from django.db import models

class Avaliacao(models.Model):
    id_evaluation = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    user_id = models.CharField(max_length=100, null=True, blank=True)
    profile_name = models.CharField(max_length=255, null=True, blank=True)
    review_helpfulness = models.CharField(max_length=20, null=True, blank=True)
    review_score= models.FloatField()
    review_time = models.IntegerField()
    review_summary = models.CharField(max_length=255, null=True, blank=True)
    review_text = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - Score: {self.review_score}"
    

class Produto(models.Model):
    nome = models.CharField("Nome", max_length=200, null = True)
    preco = models.DecimalField("Preço", decimal_places=2, max_digits=8, null = True)
    qtde = models.PositiveIntegerField("Quantidade", default=0, null = True)
    def __str__(self):
        return self.nome
    
class Cliente(models.Model):
    nome = models.CharField("Nome", max_length=200)
    email = models.EmailField("Email", unique=True)
    def __str__(self):
        return self.nome
    
class Perfil(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='perfil')
    telefone = models.CharField("Telefone", max_length=20)
    rua = models.CharField("Rua", max_length=200)
    numero = models.PositiveIntegerField("Nº")
    cep = models.CharField("CEP", max_length=20)
    bairro = models.CharField("Bairro", max_length=50)
    cidade = models.CharField("Cidade", max_length=50)
    complemento = models.CharField("Complemento", max_length=200)
    def __str__(self):
        #return self.rua
        return f'{self.rua}, {self.numero} - {self.bairro}'