from django.db import models

STATUS_CHOICES = [
    ('livre', 'Livre'),
    ('reservado', 'Reservado'),
    ('pago', 'Pago'),
]

class Rifa(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='rifas/')
    preco_por_numero = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.titulo

class Numero(models.Model):
    rifa = models.ForeignKey(Rifa, on_delete=models.CASCADE, related_name='numeros')
    numero = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='livre')
    comprador_nome = models.CharField(max_length=100, blank=True)
    comprador_email = models.EmailField(blank=True)
    comprador_telefone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.numero} - {self.rifa.titulo} ({self.status})"
