# Generated by Django 3.0.4 on 2020-05-09 03:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ausers', '0004_remove_aluno_conquistas'),
        ('progame', '0013_auto_20200430_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='conquista',
            name='aluno',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conquistas', to='ausers.Aluno'),
        ),
        migrations.AddField(
            model_name='conquista',
            name='turma',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conquistas', to='progame.Turma'),
        ),
        migrations.AddField(
            model_name='itemconquista',
            name='descricao',
            field=models.TextField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='itemconquista',
            name='slug',
            field=models.SlugField(editable=False, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='conquista',
            name='item_conquista',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='progame.ItemConquista'),
        ),
    ]