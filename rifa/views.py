from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .models import Rifa, Numero, NumeroRifa
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# View protegida para sortear rifa pelo painel do site
@login_required
def sortear_rifa(request, rifa_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden('Apenas o administrador pode sortear a rifa.')
    rifa = get_object_or_404(Rifa, id=rifa_id)
    if rifa.encerrada:
        messages.warning(request, 'Esta rifa já está encerrada.')
        return redirect('raffle-detail', raffle_id=rifa.id)
    bilhetes = Numero.objects.filter(rifa=rifa, status='pago')
    if not bilhetes.exists():
        messages.warning(request, 'Nenhum bilhete pago para esta rifa.')
        return redirect('raffle-detail', raffle_id=rifa.id)
    import random
    sorteado = random.choice(list(bilhetes))
    user = getattr(sorteado, 'reservado_por', None)
    rifa.ganhador_nome = user.get_full_name() if user and user.get_full_name() else (user.username if user else sorteado.comprador_nome)
    rifa.ganhador_numero = sorteado.numero
    if user and hasattr(user, 'profile') and hasattr(user.profile, 'foto') and user.profile.foto:
        rifa.ganhador_foto = user.profile.foto
    rifa.encerrada = True
    rifa.save()
    # Enviar e-mail (opcional)
    email = user.email if user else sorteado.comprador_email
    if email:
        from django.template.loader import render_to_string
        from django.core.mail import send_mail
        html_message = render_to_string('emails/ganhador_rifa.html', {
            'nome_ganhador': rifa.ganhador_nome,
            'titulo_rifa': rifa.titulo,
            'numero_bilhete': rifa.ganhador_numero,
            'valor_premio': rifa.preco,
        })
        send_mail(
            '🎉 Parabéns! Seu bilhete foi sorteado. Receba o seu prêmio.',
            '',
            'Vipebook <noreply@rifa.com>',
            [email],
            fail_silently=True,
            html_message=html_message
        )
    messages.success(request, f'Ganhador sorteado "{rifa.titulo}"!')
    return redirect('raffle-detail', raffle_id=rifa.id)
# --- IMPORTS ---
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .models import Rifa, Numero, NumeroRifa
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def meus_numeros(request):
    return render(request, 'rifa/meus_numeros.html')
# --- VIEWS ---
def meus_numeros(request):
    return render(request, 'rifa/meus_numeros.html')

def ganhadores(request):
    rifas_encerradas = Rifa.objects.filter(encerrada=True).order_by('-data_encerramento')
    return render(request, 'rifa/ganhadores.html', {'rifas_encerradas': rifas_encerradas})

@login_required
def sorteio_detail(request, id):
    rifa = get_object_or_404(Rifa, id=id)
    qtde_list = ['10', '20', '50', '100', '200', '500']  # Sugestão de quantidades para compra
    numeros_list = Numero.objects.filter(rifa=rifa).order_by('numero')
    return render(request, 'rifa/raffle_detail.html', {
        'rifa': rifa,
        'qtde_list': qtde_list,
        'numeros_list': numeros_list
    })

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
    from .forms_user import CustomUserCreationForm
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Save extra fields to user model (first_name, email, etc.)
            user.first_name = form.cleaned_data.get('nomeCompleto')
            user.email = form.cleaned_data.get('email')
            user.save()
            # Optionally, save extra info to a profile model or another table
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'rifa/cadastro.html', {'form': form})

@login_required
def premios(request):
    rifas = Rifa.objects.all()
    return render(request, 'rifa/premios.html', {'rifas': rifas})

def home(request):
    rifas = Rifa.objects.all()
    return render(request, 'rifa/home.html', {'rifas': rifas, 'user': request.user})
# View para busca de pedidos por telefone
@csrf_exempt
def buscar_pedidos(request):
    if request.method == 'POST':
        telefone = request.POST.get('telefone', '').strip()
        cpf = request.POST.get('cpf', '').strip().replace('.', '').replace('-', '')
        numeros = []
        if telefone:
            numeros = Numero.objects.filter(comprador_telefone=telefone).values_list('numero', flat=True)
        elif cpf and len(cpf) == 11 and cpf.isdigit():
            numeros = Numero.objects.filter(comprador_cpf=cpf).values_list('numero', flat=True)
        numeros = list(numeros)
        if numeros:
            return JsonResponse({'status': 'ok', 'numeros': numeros})
        else:
            return JsonResponse({'status': 'notfound'})
    return JsonResponse({'status': 'error', 'msg': 'Método inválido'})
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

def raffle_detail(request, raffle_id):
    rifa = get_object_or_404(Rifa, id=raffle_id)
    qtde_list = ['10', '20', '50', '100', '200', '500']  # Sugestão de quantidades para compra
    numeros_list = Numero.objects.filter(rifa=rifa).order_by('numero')
    if request.method == 'POST':
        numero_id = request.POST.get('numero')
        numero_obj = get_object_or_404(Numero, id=numero_id, rifa=rifa)
        if numero_obj.status == 'livre':
            numero_obj.status = 'reservado'
            from django.utils import timezone
            numero_obj.save()
            messages.success(request, f'Número {numero_obj.numero} reservado com sucesso!')
        else:
            messages.error(request, f'O número {numero_obj.numero} já está reservado.')
        return redirect('raffle-detail', raffle_id=rifa.id)
    return render(request, 'rifa/raffle_detail.html', {
        'rifa': rifa,
        'qtde_list': qtde_list,
        'numeros_list': numeros_list,
        'user': request.user
    })

@login_required
def reservar_numero(request, raffle_id, number_id):
    rifa = get_object_or_404(Rifa, id=raffle_id)
    from .models import Numero
    numero_obj = Numero.objects.filter(rifa=rifa, id=number_id).first()
    if not numero_obj:
        # Cria novo bilhete se não existir
        numero_obj = Numero.objects.create(rifa=rifa, numero=number_id, status='livre')

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
