from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nome_social = models.CharField('Nome Social', max_length=150, blank=True)
    cpf = models.CharField('CPF', max_length=14, unique=True)
    data_nascimento = models.CharField('Data de nascimento', max_length=10)
    telefone = models.CharField('Telefone', max_length=20)
    cep = models.CharField('CEP', max_length=9)
    logradouro = models.CharField('Logradouro', max_length=100)
    numero = models.CharField('Número', max_length=10)
    bairro = models.CharField('Bairro', max_length=100)
    complemento = models.CharField('Complemento', max_length=100, blank=True)
    uf = models.CharField('UF', max_length=2)
    cidade = models.CharField('Cidade', max_length=100)
    referencia = models.CharField('Ponto de referência', max_length=100, blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"
