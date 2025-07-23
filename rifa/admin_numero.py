from django.contrib import admin
from .models import Numero
from .forms import NumeroForm

class NumeroAdmin(admin.ModelAdmin):
    form = NumeroForm
    list_display = ('numero', 'rifa', 'status', 'comprador_nome', 'comprador_telefone', 'comprador_cpf')
    list_filter = ('status', 'rifa')
    search_fields = ('numero', 'comprador_nome', 'comprador_telefone', 'comprador_cpf')
    fieldsets = (
        (None, {
            'fields': ('rifa', 'numero', 'status')
        }),
        ('Dados do comprador', {
            'fields': ('comprador_nome', 'comprador_email', 'comprador_telefone', 'comprador_cpf'),
            'description': 'Preencha corretamente os dados do comprador. O telefone deve estar no formato (99) 99999-9999 e o CPF deve ser válido.'
        }),
    )
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['comprador_telefone'].widget.attrs['placeholder'] = '(99) 99999-9999'
        form.base_fields['comprador_cpf'].widget.attrs['placeholder'] = '000.000.000-00'
        form.base_fields['comprador_nome'].widget.attrs['placeholder'] = 'Nome completo'
        form.base_fields['comprador_email'].widget.attrs['placeholder'] = 'email@exemplo.com'
        return form

 # Removido registro duplicado para evitar AlreadyRegistered
