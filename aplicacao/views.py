from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto
from django.http.response import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def index(request):
    context = {
        'texto': "Olá mundo!",
    }
    return render(request, 'index.html', context)

@login_required(login_url="url_entrar")
def produtos(request):
    produtos = Produto.objects.all()
    context = {
        'produtos' : produtos,
    }
    return render(request, 'produtos.html', context)

def cad_produto(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, 'cad_produto.html')
        elif request.method == "POST":
            nome = request.POST.get('nome')
            preco = request.POST.get('preco').replace(',', '.')
            qtde = request.POST.get('qtde')
            produto = Produto(
            nome = nome,
            preco = preco,
            qtde = qtde
            )
            produto.save()
            return redirect('url_produtos')
        else:
            messages.error(request, "precisa estar logado para visualizar")
            return redirect('url_entrar')
    
def atualizar_produto(request, id):
    #prod = Produto.objects.get(id=id)
    prod = get_object_or_404(Produto, id=id)
    if request.method == "GET":
        context = {
            'prod': prod,
        }
        return render(request, 'atualizar_produto.html', context)
    elif request.method == "POST":
        nome = request.POST.get('nome')
        preco = request.POST.get('preco').replace(',', '.')
        qtde = request.POST.get('qtde')

        prod.nome = nome
        prod.preco = preco
        prod.qtde = qtde
        prod.save()

    return redirect('url_produtos')

def apagar_produto(request, id):
    prod = get_object_or_404(Produto, id=id)
    prod.delete()
    return redirect('url_produtos')

def entrar(request):
    if request.method == "GET":
        return render(request, 'entrar.html')
    else:
        username = request.POST.get('nome')
        password = request.POST.get('senha')
        user = authenticate(username = username, password = password)

        if user:
            login(request, user)
            return redirect("url_produtos")
        else:
            return HttpResponse("Falha no login")
def cad_user(request):
    if request.method == 'POST':
        nome = request.POST('nome')
        senha = request.POST('senha')
        email = request.POST('email')

        user = User.objects.filter(username=nome).first

        if user:
            return HttpResponse("usuário já existe")
        
        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        return HttpResponse("usuário criado")
    else:
        return render(request, "cad_user.html")

def sair(request):
    logout(request)
    return redirect('url_entrar')

