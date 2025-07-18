from django.contrib import admin
from .models import Rifa, Numero

class NumeroInline(admin.TabularInline):
    model = Numero
    extra = 10

@admin.register(Rifa)
class RifaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'preco_por_numero')
    inlines = [NumeroInline]

@admin.register(Numero)
class NumeroAdmin(admin.ModelAdmin):
    list_display = ('rifa', 'numero', 'status', 'comprador_nome')
    list_filter = ('rifa', 'status')
    search_fields = ('comprador_nome', 'comprador_email')
