# Generated by Django 5.2.4 on 2025-07-16 21:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rifa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('descricao', models.TextField()),
                ('imagem', models.ImageField(upload_to='rifas/')),
                ('preco_por_numero', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Numero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('livre', 'Livre'), ('reservado', 'Reservado'), ('pago', 'Pago')], default='livre', max_length=10)),
                ('comprador_nome', models.CharField(blank=True, max_length=100)),
                ('comprador_email', models.EmailField(blank=True, max_length=254)),
                ('comprador_telefone', models.CharField(blank=True, max_length=20)),
                ('rifa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='numeros', to='rifa.rifa')),
            ],
        ),
    ]
