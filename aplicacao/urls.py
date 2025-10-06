from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="url_index"),
    path('produtos', views.produtos, name="url_produtos"),
    path('vendas', views.vendas, name="url_vendas"),
    path('cad_produto', views.cad_produto, name="url_cad_produto"),
    path('cad_clientes', views.cad_clientes, name="url_cad_clientes"),
    path('perfil_cliente', views.perfil_cliente, name="url_perfil_cliente"),
    path('atualizar_produto/<int:id>', views.atualizar_produto, name="url_atualizar_produto"),
    path('apagar_produto/<int:id>', views.apagar_produto, name="url_apagar_produto"),
    path('entrar', views.entrar, name="url_entrar"),
    path('cad_user', views.cad_user, name="url_cad_user"),
    path('sair', views.sair, name="url_sair"),
    path('dashboard/', views.dashboard_view, name='dashboard'),

]