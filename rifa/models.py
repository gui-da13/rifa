from django.db import models

STATUS_CHOICES = [
    ('livre', 'Livre'),
    ('reservado', 'Reservado'),
    ('pago', 'Pago'),
]

class Rifa(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    imagem = models.ImageField(upload_to='rifas/', blank=True, null=True)
    encerrada = models.BooleanField(default=False, help_text='Marque como encerrada para tornar os bilhetes indisponíveis.')
    data_encerramento = models.DateTimeField(null=True, blank=True, help_text='Data e hora de encerramento da rifa.')

    def __str__(self):
        return self.titulo

from django.contrib.auth.models import User

class NumeroRifa(models.Model):
    numero = models.IntegerField()
    rifa = models.ForeignKey('Rifa', on_delete=models.CASCADE)
    reservado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reservado_em = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.numero} - {self.rifa.titulo}"
class Numero(models.Model):
    rifa = models.ForeignKey(Rifa, on_delete=models.CASCADE, related_name='numeros')
    numero = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='livre')
    comprador_nome = models.CharField(max_length=100, blank=True)
    comprador_email = models.EmailField(blank=True)
    comprador_telefone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.numero} - {self.rifa.titulo} ({self.status})"
