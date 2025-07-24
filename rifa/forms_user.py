from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    nomeCompleto = forms.CharField(label='Nome completo', max_length=150, required=True)
    nomeSocial = forms.CharField(label='Nome Social', max_length=150, required=False)
    cpf = forms.CharField(label='CPF', max_length=14, required=True)
    dataNascimento = forms.CharField(label='Data de nascimento', max_length=10, required=True)
    email = forms.EmailField(label='E-mail', required=True)
    telefone = forms.CharField(label='Telefone', max_length=20, required=True)
    confirmaTelefone = forms.CharField(label='Confirmar telefone', max_length=20, required=True)
    cep = forms.CharField(label='CEP', max_length=9, required=True)
    logradouro = forms.CharField(label='Logradouro', max_length=100, required=True)
    numero = forms.CharField(label='Número', max_length=10, required=True)
    bairro = forms.CharField(label='Bairro', max_length=100, required=True)
    complemento = forms.CharField(label='Complemento', max_length=100, required=False)
    uf = forms.CharField(label='UF', max_length=2, required=True)
    cidade = forms.CharField(label='Cidade', max_length=100, required=True)
    referencia = forms.CharField(label='Ponto de referência', max_length=100, required=False)

    class Meta:
        model = User
        fields = ('username', 'nomeCompleto', 'nomeSocial', 'cpf', 'dataNascimento', 'email', 'telefone', 'confirmaTelefone', 'cep', 'logradouro', 'numero', 'bairro', 'complemento', 'uf', 'cidade', 'referencia', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('Nome de usuário já cadastrado.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('E-mail já cadastrado.')
        return email

    def clean_nomeCompleto(self):
        nome = self.cleaned_data['nomeCompleto']
        if User.objects.filter(first_name=nome).exists():
            raise ValidationError('Nome completo já cadastrado.')
        return nome

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        from rifa.models_profile import UserProfile
        if UserProfile.objects.filter(cpf=cpf).exists():
            raise ValidationError('CPF já cadastrado.')
        return cpf

    def clean(self):
        cleaned = super().clean()
        telefone = cleaned.get('telefone')
        confirma = cleaned.get('confirmaTelefone')
        if telefone and confirma and telefone != confirma:
            self.add_error('confirmaTelefone', 'Os telefones não coincidem.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('nomeCompleto')
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
            from rifa.models_profile import UserProfile
            profile = UserProfile.objects.create(
                user=user,
                nome_social=self.cleaned_data.get('nomeSocial', ''),
                cpf=self.cleaned_data.get('cpf'),
                data_nascimento=self.cleaned_data.get('dataNascimento'),
                telefone=self.cleaned_data.get('telefone'),
                cep=self.cleaned_data.get('cep'),
                logradouro=self.cleaned_data.get('logradouro'),
                numero=self.cleaned_data.get('numero'),
                bairro=self.cleaned_data.get('bairro'),
                complemento=self.cleaned_data.get('complemento', ''),
                uf=self.cleaned_data.get('uf'),
                cidade=self.cleaned_data.get('cidade'),
                referencia=self.cleaned_data.get('referencia', ''),
            )
        return user
