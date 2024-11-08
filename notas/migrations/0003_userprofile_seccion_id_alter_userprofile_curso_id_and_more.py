# Generated by Django 5.1.1 on 2024-11-08 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notas', '0002_userprofile_grado_id_alter_userprofile_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='seccion_id',
            field=models.ManyToManyField(blank=True, to='notas.secciones', verbose_name='secciones'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='curso_id',
            field=models.ManyToManyField(blank=True, to='notas.cursos', verbose_name='cursos'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='grado_id',
            field=models.ManyToManyField(blank=True, to='notas.grados', verbose_name='grados'),
        ),
    ]
