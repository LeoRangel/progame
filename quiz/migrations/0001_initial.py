# Generated by Django 3.0.4 on 2020-04-19 01:12

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ausers', '0002_auto_20200402_0253'),
        ('progame', '0007_auto_20200416_0049'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tentativa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('numero', models.PositiveIntegerField()),
                ('nivel', models.CharField(choices=[(0, 'Nenhum'), (1, '1 - Lembrar'), (2, '2 - Entender'), (3, '3 - Aplicar'), (4, '4 - Analisar'), (5, '5 - Avaliar'), (6, '6 - Criar')], default=0, max_length=50)),
                ('aluno', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tentativas', to='ausers.Aluno')),
                ('modulo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tentativas', to='progame.Modulo')),
                ('respostas', models.ManyToManyField(blank=True, to='progame.Resposta')),
            ],
            options={
                'verbose_name': 'Tentativa',
                'verbose_name_plural': 'Tentativas',
            },
        ),
    ]
