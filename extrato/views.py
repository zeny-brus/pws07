from django.shortcuts import render, redirect
from django.http import FileResponse
from perfil.models import Conta,Categoria
from .models import Valores
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime
from django.template.loader import render_to_string
import os
from io import BytesIO
from django.conf import settings
from weasyprint import HTML

# Create your views here.
def novo_valor(request):
    if request.method == 'GET':
        contas = Conta.objects.all()
        categorias = Categoria.objects.all()
        return render(request, 'novo_valor.html',{'contas':contas, 'categorias':categorias})
    elif request.method == 'POST':
        valor = request.POST.get('valor')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')
        tipo = request.POST.get('tipo')
        conta = request.POST.get('conta')
        
        
        valores = Valores( 
            valor = valor,
            categoria_id = categoria,
            descricao = descricao,
            data = data,
            conta_id = conta,
            tipo = tipo, 
        )

        valores.save()

        conta = Conta.objects.get(id=conta)
        if tipo == 'E':
            conta.valor += int(valor)
        elif tipo == 'S':
            conta.valor -= int(valor)
        conta.save()

        messages.add_message(request, constants.SUCCESS,'entrada/saida cadastrada com sucesso!')
        
        #TODO Mensagem processada de acordo com o tipo 
        return redirect('/extrato/novo_valor/') 

def view_extrato(request):    
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    conta_get = request.GET.get('conta')
    categoria_get = request.GET.get('categoria')

    valores = Valores.objects.filter(data__month=datetime.now().month)

    if conta_get:
        valores = valores.filter(conta__id=conta_get)
    if categoria_get:
        valores = valores.filter(categoria__id=categoria_get)
    
    #TODO: Limpar os filtros
    #TODO: Filtrar por periodo
    return render (request,'view_extrato.html',{'valores':valores,'contas':contas, 'categorias':categorias})

def exportar_pdf(request):
    valores = Valores.objects.filter(data__month=datetime.now().month)
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()

    path_template = os.path.join(settings.BASE_DIR, 'templates/partials/extrato.html')
    path_output = BytesIO()

    template_render = render_to_string(path_template,{'valores':valores, 'contas':contas ,'categorias':categorias})
    HTML(string=template_render).write_pdf(path_output)

    path_output.seek(0)

    return FileResponse(path_output, filename='extrato.pdf')
