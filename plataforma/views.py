from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from plataforma.models import Imovel, Cidade, Visitas
from django.shortcuts import get_object_or_404


@login_required
def home(request):
    if request.method == "GET":
        cidades = Cidade.objects.all()
        imoveis = Imovel.objects.all()
    elif request.method == "POST":
        preco_minimo = request.POST.get('preco_minimo')
        preco_maximo = request.POST.get('preco_maximo')
        cidade = request.POST.get('cidade')
        tipo = request.POST.getlist('tipo')
        cidades = Cidade.objects.all()
        if preco_minimo or preco_maximo or cidade or tipo:
            
            if not preco_minimo:
                preco_minimo = 0
            if not preco_maximo:
                preco_maximo = 999999999
            if not tipo:
                tipo = ['A', 'C']

            if not cidade:
                imoveis = Imovel.objects\
                .filter(valor__gte=preco_minimo)\
                .filter(valor__lte=preco_maximo)\
                .filter(tipo_imovel__in=tipo)
            else:
                imoveis = Imovel.objects\
                .filter(valor__gte=preco_minimo)\
                .filter(valor__lte=preco_maximo)\
                .filter(tipo_imovel__in=tipo)\
                .filter(cidade=cidade)
        else:
            imoveis = Imovel.objects.all()

    return render(request, 'home.html', {'imoveis': imoveis, 'cidades': cidades})


@login_required
def imovel(request, id):
    imovel = get_object_or_404(Imovel, id=id)
    sugestoes = Imovel.objects.filter(cidade=imovel.cidade).exclude(id=id)[:2]
    return render(request, 'imovel.html', {'imovel': imovel, 'sugestoes': sugestoes, 'id': id})


@login_required
def agendar_visitas(request):
    usuario = request.user
    dia = request.POST.get('dia')
    horario = request.POST.get('horario')
    id_imovel = request.POST.get('id_imovel')

    visita = Visitas(
        imovel_id=id_imovel,
        usuario=usuario,
        dia=dia,
        horario=horario
    )
    visita.save()

    return redirect('/plataforma/agendamentos/')


@login_required
def agendamentos(request):
    visitas = Visitas.objects.filter(usuario=request.user)
    return render(request, "agendamentos.html", {'visitas': visitas})


@login_required
def cancelar_agendamento(request, id):
    visitas = get_object_or_404(Visitas, id=id)
    visitas.status = "C"
    visitas.save()
    return redirect('/plataforma/agendamentos/')


@login_required
def finalizar_agendamento(request, id):
    visitas = get_object_or_404(Visitas, id=id)
    visitas.status = "F"
    visitas.save()
    return redirect('/plataforma/agendamentos/')
