from django.contrib import admin
from .models import Produto, Cliente, Vendas, ItensVenda

# Register your models here.
class ProdutoAdm(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'qtde')

admin.site.register(Produto, ProdutoAdm)
admin.site.register(Cliente)
admin.site.register(Vendas)
admin.site.register(ItensVenda)
