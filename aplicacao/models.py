from django.db import models

# Create your models here.
class Produto(models.Model):
    nome = models.CharField("Nome", max_length=200, null= True)
    preco = models.DecimalField("Preço", decimal_places=2, max_digits=8, null= True)
    qtde = models.PositiveIntegerField("Quantidade", default=0, null = True)
    def __str__(self):
        return self.nome
    
class Vendas(models.Model):
    cliente = models.ForeignKey("Cliente", on_delete=models.CASCADE, related_name="vendas", null=True)
    data = models.DateTimeField("Data", auto_now_add=True)

    def __str__(self):
        return f"Venda {self.id} - {self.cliente.nome}"

    def total(self):
        return sum(item.subtotal() for item in self.itens.all())

class ItensVenda(models.Model):
    quantidade = models.IntegerField("Quantidade", default=0, null=True)
    venda = models.ForeignKey(Vendas, on_delete=models.CASCADE, related_name="itens", null=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} (Venda {self.venda.id})"

class Cliente(models.Model):
    nome = models.CharField("Nome", max_length=200, null= True)
    email = models.CharField("Email", max_length=200, unique= True)

    def __str__(self):
        return self.nome
   

class PerfilClientes(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    telefone = models.CharField("Telefone", max_length=20, null=True)
    rua = models.CharField("Rua", max_length=200)
    numero = models.PositiveIntegerField("Número")
    cep = models.CharField("CEP", max_length=20)
    bairro = models.CharField("Bairro", max_length=50)
    cidade = models.CharField("Cidade", max_length=50)
    complemento = models.CharField("Complemento", max_length=200)

    def __str__(self):
        return self.telefone, self.rua, self.numero, self.cep, self.bairro, self.cidade, self.complemento

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
