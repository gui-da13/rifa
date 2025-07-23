from django.contrib import admin
from .models import Rifa, Numero, NumeroRifa
from .admin_numero import NumeroAdmin
from django.utils.html import format_html
import csv
from django.http import HttpResponse

 # Removido registro duplicado para evitar AlreadyRegistered

@admin.register(Rifa)
class RifaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'preco', 'encerrada', 'imagem_tag', 'data_encerramento', 'ganhador_nome', 'ganhador_numero')
    actions = ['sortear_ganhador']

    def get_actions(self, request):
        actions = super().get_actions(request)
        # Renomear ação para aparecer como 'Sortear' no painel
        if 'sortear_ganhador' in actions:
            actions['sortear_ganhador']['short_description'] = 'Sortear'
        return actions

    def sortear_ganhador(self, request, queryset):
        if not request.user.is_superuser:
            from django.contrib import messages
            messages.error(request, 'Ação permitida apenas para administradores.')
            return
        from .models import Numero
        from django.core.mail import send_mail
        import random
        for rifa in queryset:
            if rifa.encerrada and not rifa.ganhador_nome:
                bilhetes = Numero.objects.filter(rifa=rifa, status='pago')
                if bilhetes.exists():
                    sorteado = random.choice(list(bilhetes))
                    user = sorteado.reservado_por
                    rifa.ganhador_nome = user.get_full_name() or user.username if user else sorteado.comprador_nome
                    rifa.ganhador_numero = sorteado.numero
                    if hasattr(user, 'profile') and user.profile.foto:
                        rifa.ganhador_foto = user.profile.foto
                    rifa.save()
                    # Enviar e-mail
                    email = user.email if user else sorteado.comprador_email
                    if email:
                        from django.template.loader import render_to_string
                        html_message = render_to_string('emails/ganhador_rifa.html', {
                            'nome_ganhador': rifa.ganhador_nome,
                            'titulo_rifa': rifa.titulo,
                            'numero_bilhete': rifa.ganhador_numero,
                            'valor_premio': rifa.preco,
                        })
                        send_mail(
                            '🎉 Parabéns! Você venceu a rifa',
                            '',
                            'Rifa Online <noreply@rifa.com>',
                            [email],
                            fail_silently=True,
                            html_message=html_message
                        )
        self.message_user(request, 'Ganhador sorteado e notificado por e-mail!')
    sortear_ganhador.short_description = 'Sortear ganhador e enviar e-mail'
    list_filter = ('encerrada', 'data_encerramento')
    search_fields = ('titulo', 'descricao')
    fields = ('titulo', 'descricao', 'preco', 'imagem', 'encerrada', 'data_encerramento')

    def imagem_tag(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" style="max-height:40px;max-width:60px;" />', obj.imagem.url)
        return "-"
    imagem_tag.short_description = 'Imagem'

    # Exportação CSV
    actions = ['exportar_csv']
    def exportar_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=rifas.csv'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Título', 'Descrição', 'Preço', 'Encerrada', 'Data Encerramento'])
        for rifa in queryset:
            writer.writerow([rifa.id, rifa.titulo, rifa.descricao, rifa.preco, rifa.encerrada, getattr(rifa, 'data_encerramento', '')])
        return response
    exportar_csv.short_description = "Exportar selecionadas para CSV"

    # Dashboard avançado
    change_list_template = "admin/rifa_dashboard.html"

    def changelist_view(self, request, extra_context=None):
        from .models import Numero
        queryset = self.get_queryset(request)
        total_bilhetes = Numero.objects.count()
        valor_total_vendido = sum([n.rifa.preco for n in Numero.objects.filter(status='pago')])
        rifas = queryset
        nomes_rifas = [r.titulo for r in rifas]
        bilhetes_por_rifa = [Numero.objects.filter(rifa=r).count() for r in rifas]
        extra_context = extra_context or {}
        rifas_ativas = queryset.filter(encerrada=False).count()
        rifas_encerradas = queryset.filter(encerrada=True).count()
        extra_context.update({
            'rifas_ativas': rifas_ativas,
            'rifas_encerradas': rifas_encerradas,
            'total_bilhetes': total_bilhetes,
            'valor_total_vendido': f'{valor_total_vendido:,.2f}'.replace('.',','),
            'nomes_rifas': nomes_rifas,
            'bilhetes_por_rifa': bilhetes_por_rifa,
        })
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Numero)
class NumeroAdmin(admin.ModelAdmin):
    list_display = ('numero', 'rifa', 'status', 'comprador_nome', 'comprador_email', 'comprador_telefone')
    list_filter = ('status', 'rifa')
    search_fields = ('comprador_nome', 'comprador_email', 'comprador_telefone', 'numero')
    actions = ['exportar_csv']

    def exportar_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=numeros.csv'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Número', 'Rifa', 'Status', 'Nome', 'Email', 'Telefone'])
        for n in queryset:
            writer.writerow([n.id, n.numero, n.rifa.titulo, n.status, n.comprador_nome, n.comprador_email, n.comprador_telefone])
        return response
    exportar_csv.short_description = "Exportar selecionados para CSV"

@admin.register(NumeroRifa)
class NumeroRifaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'rifa', 'reservado_por', 'reservado_em')
    list_filter = ('rifa',)
    search_fields = ('numero', 'rifa__titulo', 'reservado_por__username')
