# Generated by Django 3.0.4 on 2020-04-15 02:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ausers', '0002_auto_20200402_0253'),
        ('progame', '0004_auto_20200404_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questao',
            name='nivel',
            field=models.CharField(choices=[(0, 'Nenhum'), (1, '1 - Lembrar'), (2, '2 - Entender'), (3, '3 - Aplicar'), (4, '4 - Analisar'), (5, '5 - Avaliar'), (6, '6 - Criar')], max_length=50, null=True, verbose_name='nível'),
        ),
        migrations.CreateModel(
            name='NivelAlunoTurma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nivel', models.CharField(choices=[(0, 'Nenhum'), (1, '1 - Lembrar'), (2, '2 - Entender'), (3, '3 - Aplicar'), (4, '4 - Analisar'), (5, '5 - Avaliar'), (6, '6 - Criar')], default=0, max_length=50)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='niveis_turmas', to='ausers.Aluno')),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='niveis_alunos', to='progame.Turma')),
            ],
        ),
        migrations.CreateModel(
            name='NivelAlunoModulo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nivel', models.CharField(choices=[(0, 'Nenhum'), (1, '1 - Lembrar'), (2, '2 - Entender'), (3, '3 - Aplicar'), (4, '4 - Analisar'), (5, '5 - Avaliar'), (6, '6 - Criar')], default=0, max_length=50)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='niveis_modulos', to='ausers.Aluno')),
                ('modulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='niveis_alunos', to='progame.Modulo')),
            ],
        ),
    ]
