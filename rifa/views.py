from django.shortcuts import render, redirect, get_object_or_404
from .models import Rifa, Numero
from django.contrib import messages

def home(request):
    rifas = Rifa.objects.all()
    return render(request, 'rifa/home.html', {'rifas': rifas})
from django.shortcuts import render, redirect, get_object_or_404
from .models import Rifa, Numero
from django.contrib import messages

def raffle_detail(request, raffle_id):
    rifa = get_object_or_404(Rifa, id=raffle_id)
    return render(request, 'rifa/raffle_detail.html', {'raffle': rifa})

def reservar_numero(request, raffle_id, number_id):
    rifa = get_object_or_404(Rifa, id=raffle_id)
    numero_obj = get_object_or_404(Numero, rifa=rifa, id=number_id)

    if request.method == 'POST':
        if numero_obj.status == 'livre':
            numero_obj.status = 'reservado'
            numero_obj.save()
            messages.success(request, 'Número reservado com sucesso! Envie o pagamento via Pix e aguarde confirmação.')
        else:
            messages.error(request, 'Este número já foi reservado.')
        return redirect('raffle_detail', raffle_id=rifa.id)

    # GET: exibe formulário simples para reservar
    return render(request, 'rifa/reservar_numero.html', {'raffle': rifa, 'numero': numero_obj})
