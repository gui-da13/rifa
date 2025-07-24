from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('rifa', '0006_alter_numero_options_numero_comprador_cpf_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_social', models.CharField(max_length=150, blank=True, verbose_name='Nome Social')),
                ('cpf', models.CharField(max_length=14, unique=True, verbose_name='CPF')),
                ('data_nascimento', models.CharField(max_length=10, verbose_name='Data de nascimento')),
                ('telefone', models.CharField(max_length=20, verbose_name='Telefone')),
                ('cep', models.CharField(max_length=9, verbose_name='CEP')),
                ('logradouro', models.CharField(max_length=100, verbose_name='Logradouro')),
                ('numero', models.CharField(max_length=10, verbose_name='Número')),
                ('bairro', models.CharField(max_length=100, verbose_name='Bairro')),
                ('complemento', models.CharField(max_length=100, blank=True, verbose_name='Complemento')),
                ('uf', models.CharField(max_length=2, verbose_name='UF')),
                ('cidade', models.CharField(max_length=100, verbose_name='Cidade')),
                ('referencia', models.CharField(max_length=100, blank=True, verbose_name='Ponto de referência')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='auth.user')),
            ],
        ),
    ]
