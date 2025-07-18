from django.shortcuts import render, redirect, get_object_or_404
from .models import Rifa, Numero
from django.contrib import messages

def rifa_detail(request, rifa_id=None):
    if rifa_id:
        rifa = get_object_or_404(Rifa, id=rifa_id)
    else:
        rifa = Rifa.objects.first()
    if not rifa:
        messages.error(request, 'Nenhuma rifa encontrada.')
        return redirect('/')
    numeros = Numero.objects.filter(rifa=rifa).order_by('numero')
    return render(request, 'rifa/rifa_detail.html', {'rifa': rifa, 'numeros': numeros})

def reservar_numero(request, rifa_id, numero):
    rifa = get_object_or_404(Rifa, id=rifa_id)
    numero_obj = get_object_or_404(Numero, rifa=rifa, numero=numero)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')

        if numero_obj.status == 'disponivel':
            numero_obj.status = 'reservado'
            numero_obj.comprador_nome = nome
            numero_obj.comprador_email = email
            numero_obj.comprador_telefone = telefone
            numero_obj.save()
            messages.success(request, 'Número reservado com sucesso! Envie o pagamento via Pix e aguarde confirmação.')
        else:
            messages.error(request, 'Este número já foi reservado.')
        return redirect('rifa_detail', rifa_id=rifa.id)

    # GET: exibe formulário simples para reservar
    return render(request, 'rifa/reservar_numero.html', {'rifa': rifa, 'numero': numero_obj})
