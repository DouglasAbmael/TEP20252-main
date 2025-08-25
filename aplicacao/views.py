from django.shortcuts import render
from .models import Produto
from django.http.response import HttpResponse

def index(request):
    context = {
        'texto': "Olá mundo!",
    }
    return render(request, 'index.html', context)

def produto(request):
    produtos = Produto.objects.all()
    # produtos = get_objects_or_404()
    context = {
        'produtos': produtos,
    }
    return render(request, 'produto.html', context)

def cad_produto(request):
    return HttpResponse("tela de cadastro de produto")