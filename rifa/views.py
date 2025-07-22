from .models import Rifa

def sorteio_detail(request, id):
    rifa = get_object_or_404(Rifa, id=id)
    qtde_list = ['1', '2', '5', '10', '25', '50']
    numeros_list = [str(i).zfill(6) for i in range(1, 21)]
    return render(request, 'rifa/raffle_detail.html', {
        'rifa': rifa,
        'qtde_list': qtde_list,
        'numeros_list': numeros_list
    })
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'rifa/login.html', {'form': form})

def cadastro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'rifa/cadastro.html', {'form': form})
from .models import Rifa
from django.contrib.auth.decorators import login_required

@login_required
def premios(request):
    rifas = Rifa.objects.all()
    return render(request, 'rifa/premios.html', {'rifas': rifas})
from django.shortcuts import render, redirect, get_object_or_404
from .models import Rifa, Numero
from django.contrib import messages

def home(request):
    rifas = Rifa.objects.all()
    return render(request, 'rifa/home.html', {'rifas': rifas, 'user': request.user})
from django.shortcuts import render, redirect, get_object_or_404
from .models import Rifa, Numero, NumeroRifa
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
def sorteios(request):
    rifas = Rifa.objects.all()
    return render(request, 'rifa/sorteios.html', {'rifas': rifas})

# View para busca de números pelo telefone
@csrf_exempt
def buscar_numeros_por_telefone(request):
    if request.method == 'POST':
        telefone = request.POST.get('telefone')
        numeros = Numero.objects.filter(comprador_telefone=telefone).values_list('numero', flat=True)
        numeros = list(numeros)
        if numeros:
            return JsonResponse({'status': 'ok', 'numeros': numeros})
        else:
            return JsonResponse({'status': 'notfound'})
    return JsonResponse({'status': 'error'})
from django.contrib import messages

@login_required
def raffle_detail(request, raffle_id):
    rifa = get_object_or_404(Rifa, id=raffle_id)
    numeros = NumeroRifa.objects.filter(rifa=rifa).order_by('numero')
    if request.method == 'POST':
        numero_id = request.POST.get('numero')
        numero_obj = get_object_or_404(NumeroRifa, id=numero_id, rifa=rifa)
        if not numero_obj.reservado_por:
            numero_obj.reservado_por = request.user
            from django.utils import timezone
            numero_obj.reservado_em = timezone.now()
            numero_obj.save()
            messages.success(request, f'Número {numero_obj.numero} reservado com sucesso!')
        else:
            messages.error(request, f'O número {numero_obj.numero} já está reservado.')
        return redirect('raffle-detail', raffle_id=rifa.id)
    return render(request, 'rifa/raffle_detail.html', {
        'raffle': rifa,
        'numeros': numeros,
        'user': request.user
    })

@login_required
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
    return render(request, 'rifa/reservar_numero.html', {'raffle': rifa, 'numero': numero_obj, 'user': request.user})
