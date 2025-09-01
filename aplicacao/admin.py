from django.contrib import admin
from .models import Produto, cliente, Perfil

class ProdutoAdm(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'qtde')

admin.site.register(Produto, ProdutoAdm)
admin.site.register(Produto, ProdutoAdm)

