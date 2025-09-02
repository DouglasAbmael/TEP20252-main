from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto
from django.http.response import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ClienteForm, PerfilForm

def index(request):
    context = {
        'texto': "Olá mundo!",
    }
    return render(request, 'index.html', context)

@login_required(login_url="url_entrar")
def produto(request):
    produtos = Produto.objects.all()
    # produtos = get_objects_or_404()
    context = {
        'produtos': produtos,
    }
    return render(request, 'produto.html', context)

def cad_produto(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, 'cad_produto.html')
        elif request.method == "POST":
            nome = request.POST.get('nome')
            preco = request.POST.get('preco').replace(',', '.')
            qtde = request.POST.get('qtde')

            produto  = Produto(
                nome = nome,
                preco = preco,
                qtde = qtde,
            )
            produto.save()
            return redirect('url_produto')
    else:
        messages.error(request, "Precisa estar logado para acessar o produto")
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
    return redirect('url_produto')

def apagar_produto(request, id):
    prod = get_object_or_404(Produto, id=id)
    prod.delete()
    return redirect('url_produto')

def entrar(request):
    if request.method == "GET":
        return render(request, "entrar.html")
    else:
        username = request.POST.get('nome')
        password = request.POST.get('senha')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('url_produto')
        else:
            return HttpResponse("Falha no login")

def cad_user(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        email = request.POST.get('email')

        user = User.objects.filter(username=nome).first()

        if user:
            return HttpResponse("Usuário já existe")

        user = User.objects.create_user(username=nome, email=email, password=senha)

        user.save()
        messages.success(request, "Usuário cadastrado")
        return render(render, "cad_user.html")
    else:
        return render(request, "cad_user.html")
    
def sair(request):
    logout(request)
    return redirect('url_entrar')

def cad_cliente(request):
    if request.method == "POST":
        form_cliente = ClienteForm(request.POST, request.FILES)
        form_perfil = PerfilForm(request.POST, request.FILES)
        if form_cliente.is_valid() and form_perfil.is_valid():
            cliente = form_cliente.save()
            perfil = form_perfil.save(commit=False)
            perfil.cliente = cliente
            perfil.save()
    
    form = ClienteForm()
    context = {
        'form_cliente': form_cliente,
        'form_perfil': form_perfil
        }
    return render(request, "cad_cliente.html", context)