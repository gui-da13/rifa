from django import forms
from .models import Numero

class NumeroForm(forms.ModelForm):
    class Meta:
        model = Numero
        fields = ['rifa', 'numero', 'status', 'comprador_nome', 'comprador_email', 'comprador_telefone', 'comprador_cpf']
        widgets = {
            'comprador_telefone': forms.TextInput(attrs={
                'placeholder': '(99) 99999-9999',
                'class': 'form-control',
                'data-mask': '(00) 00000-0000',
            }),
            'comprador_cpf': forms.TextInput(attrs={
                'placeholder': '000.000.000-00',
                'class': 'form-control',
            }),
            'comprador_nome': forms.TextInput(attrs={
                'placeholder': 'Nome completo',
                'class': 'form-control',
            }),
            'comprador_email': forms.EmailInput(attrs={
                'placeholder': 'email@exemplo.com',
                'class': 'form-control',
            }),
        }
    def clean_comprador_telefone(self):
        telefone = self.cleaned_data.get('comprador_telefone')
        import re
        telefone_regex = r'^\(\d{2}\) \d{4,5}-\d{4}$'
        if telefone and not re.match(telefone_regex, telefone):
            raise forms.ValidationError('Telefone deve estar no formato (99) 99999-9999.')
        return telefone
    def clean_comprador_cpf(self):
        cpf = self.cleaned_data.get('comprador_cpf')
        import re
        if cpf:
            cpf_num = re.sub(r'\D', '', cpf)
            if len(cpf_num) != 11 or not cpf_num.isdigit() or cpf_num == cpf_num[0]*11:
                raise forms.ValidationError('CPF inválido.')
            def cpf_valido(cpf):
                def calc_digito(cpf, peso):
                    soma = sum(int(d)*p for d, p in zip(cpf, peso))
                    resto = soma % 11
                    return '0' if resto < 2 else str(11-resto)
                d1 = calc_digito(cpf[:9], range(10,1,-1))
                d2 = calc_digito(cpf[:10], range(11,1,-1))
                return cpf[-2:] == d1+d2
            if not cpf_valido(cpf_num):
                raise forms.ValidationError('CPF inválido.')
        return cpf
    def clean(self):
        cleaned = super().clean()
        status = cleaned.get('status')
        nome = cleaned.get('comprador_nome')
        if status in ['reservado', 'pago'] and not nome:
            self.add_error('comprador_nome', 'Nome do comprador é obrigatório para bilhetes reservados ou pagos.')
        return cleaned
