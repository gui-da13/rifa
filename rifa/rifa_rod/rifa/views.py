from django.shortcuts import render, redirect, get_object_or_404
from .models import Rifa, Numero
from django.contrib import messages

def rifa_detail(request):
    rifa = Rifa.objects.first()  # só uma rifa
    numeros = Numero.objects.filter(rifa=rifa).order_by('numero')
    return render(request, 'rifa/rifa_detail.html', {'rifa': rifa, 'numeros': numeros})

def reservar_numero(request):
    if request.method == 'POST':
        numero_id = request.POST.get('numero_id')
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')

        numero = get_object_or_404(Numero, id=numero_id)

        if numero.status == 'livre':
            numero.status = 'reservado'
            numero.comprador_nome = nome
            numero.comprador_email = email
            numero.comprador_telefone = telefone
            numero.save()
            messages.success(request, 'Número reservado com sucesso! Envie o pagamento via Pix e aguarde confirmação.')
        else:
            messages.error(request, 'Este número já foi reservado.')

        return redirect('rifa:rifa_detail')
    else:
        return redirect('rifa:rifa_detail')
