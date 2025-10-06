from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto, Cliente, Vendas, ItensVenda, PerfilClientes, Avaliacao
from django.http.response import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import pandas as pd
import matplotlib.pyplot as plt
import io, base64
import matplotlib
matplotlib.use('Agg')

# Create your views here.

def index(request):
    context = {
        'texto': "Olá mundo!",
    }
    return render(request, 'index.html', context)

@login_required(login_url='url_entrar')
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
        messages.error(request, "Precisa...")
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
            return redirect('url_index')
        else:
            return HttpResponse("Falha no login")
        
def cad_user(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        email = request.POST.get('email')

        user = User.objects.filter(username=nome).first()
        if user:
            return HttpResponse("Usuário já existe...")
        
        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        messages.success(request, "Usuario cadastrado")
        return render(request, "index.html")
    else:
        return render(request, "cad_user.html")
    
def sair(request):
    logout(request)
    return redirect('url_entrar')

def cad_clientes(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, 'cad_clientes.html')
        elif request.method == "POST":
            nome = request.POST.get('nome')
            email = request.POST.get('email')

            clientes = Cliente(
                nome = nome,
                email = email,
            )
            clientes.save()
            return redirect('url_perfil_cliente')
    else:
        messages.error(request, "Precisa...")
        return redirect('url_entrar')

def perfil_cliente(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            clientes = Cliente.objects.all()
            return render(request, 'cad_perfil_clientes.html', {'clientes': clientes})
        elif request.method == "POST":
            cliente_id = request.POST.get("cliente_id")
            telefone = request.POST.get('telefone')
            rua = request.POST.get('rua')
            numero = request.POST.get('numero')
            cep = request.POST.get('cep')
            bairro = request.POST.get('bairro')
            cidade = request.POST.get('cidade')
            complemento = request.POST.get('complemento')

            cliente_obj = get_object_or_404(Cliente, id=cliente_id)

            perfil_cliente = PerfilClientes.objects.create(
                cliente= cliente_obj,
                telefone = telefone,
                rua = rua,
                numero = numero,
                cep = cep,
                bairro = bairro,
                cidade = cidade,
                complemento = complemento,
            )
            perfil_cliente.save()
            return redirect('url_index')
    else:
        messages.error(request, "Precisa...")
        return redirect('url_entrar')

def vendas(request):
    if not request.user.is_authenticated:
        messages.error(request, "Você precisa estar logado.")
        return redirect('url_entrar')
    if request.method == "GET":
        clientes = Cliente.objects.all()
        produtos = Produto.objects.all()
        return render(request, 'vendas.html', {'clientes': clientes, 'produtos': produtos})
    elif request.method == "POST":
        cliente_id = request.POST.get("cliente")
        if not cliente_id:
            messages.error(request, "Selecione um cliente.")
            return redirect('url_vendas')
        
        cliente = get_object_or_404(Cliente, id=cliente_id)
        venda = Vendas.objects.create(cliente=cliente)

        for produto in Produto.objects.all():
            if request.POST.get(f"produto_{produto.id}"):
                quantidade = int(request.POST.get(f"quantidade_{produto.id}", 0))
                
                if quantidade > produto.qtde:
                    messages.error(request, f"Estoque insuficiente para {produto.nome}.")
                    return redirect('url_vendas')
                
                ItensVenda.objects.create(
                    venda=venda,
                    produto=produto,
                    quantidade=quantidade,
                    preco_unitario=produto.preco)
                
                produto.qtde -= quantidade
                produto.save
        
        messages.success(request, "Venda cadastrada com sucesso!")
        return redirect('url_index')
    
# --- Funções auxiliares ---
def get_dataframe():
    # Troque o caminho abaixo pelo seu arquivo CSV
    df = pd.read_csv('books-15k.csv')
    return df

def plot_to_base64():
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return f"data:image/png;base64,{base64.b64encode(buf.read()).decode()}"

def dashboard_view(request):
    df = get_dataframe()

    def gerar_grafico(figura):
        """Função auxiliar para salvar o gráfico atual como base64 e limpar o plt."""
        img = plot_to_base64()
        plt.close(figura)
        return img

    # --- Gráfico 1: Usuários mais ativos ---
    top15 = df['profile_name'].dropna().value_counts().nlargest(15).sort_values()
    fig, ax = plt.subplots(figsize=(10, 5))
    top15.plot.barh(ax=ax, color='steelblue')
    ax.set(title='Top 15 Usuários Mais Ativos', xlabel='Número de Avaliações')
    grafico_usuarios = gerar_grafico(fig)

    # --- Gráfico 2: Evolução das avaliações ---
    df['data'] = pd.to_datetime(df['review_time'], unit='s', errors='coerce')
    contagem = df['data'].dt.year.value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    contagem.plot(marker='o', ax=ax)
    ax.set(title='Evolução do Número de Avaliações por Ano', xlabel='Ano', ylabel='Qtd de Avaliações')
    grafico_evolucao = gerar_grafico(fig)

    # --- Gráfico 3: Preço vs Nota ---
    df_precos = df.query('0 < price < 100')
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.scatter(df_precos['price'], df_precos['review_score'], alpha=0.3)
    ax.set(title='Correlação entre Preço e Nota', xlabel='Preço', ylabel='Nota')
    grafico_preco = gerar_grafico(fig)

    # --- Gráfico 4: Sentimento ---
    positivos = ['good', 'great', 'excellent', 'love', 'recommend']
    negativos = ['bad', 'terrible', 'disappoint', "didn't like"]

    def sentimento(texto):
        texto = str(texto).lower()
        if any(p in texto for p in positivos): return 'Positivo'
        if any(n in texto for n in negativos): return 'Negativo'
        return 'Neutro'

    df['sentimento'] = df['review_summary'].apply(sentimento)
    fig, ax = plt.subplots()
    df['sentimento'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
    ax.set(title='Distribuição de Sentimentos', ylabel='')
    grafico_sentimento = gerar_grafico(fig)

    # --- Retorno para o template ---
    context = {
        'grafico_usuarios_ativos': grafico_usuarios,
        'grafico_evolucao_reviews': grafico_evolucao,
        'grafico_preco_score': grafico_preco,
        'grafico_sentimento': grafico_sentimento,
    }

    return render(request, 'dashboard.html', context)

    