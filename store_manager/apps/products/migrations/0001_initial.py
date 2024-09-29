# Generated by Django 5.1.1 on 2024-09-28 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Produtos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('marca', models.CharField(max_length=200)),
                ('producao', models.CharField(max_length=200)),
                ('frete_gratis', models.BooleanField(default=False)),
                ('altura', models.IntegerField(default=0)),
                ('largura', models.IntegerField(default=0)),
                ('profundidade', models.IntegerField(default=0)),
                ('itens_para_caixa', models.BooleanField(default=False)),
                ('unidade_medida', models.CharField(choices=[('mm', 'mm'), ('cm', 'cm'), ('m', 'm')], default='mm', max_length=2)),
                ('validade', models.DateField()),
            ],
        ),
    ]
