# Generated by Django 4.2.7 on 2023-11-13 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuario', '0003_alter_usuario_foto'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='cedula',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='direccion',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='telefono',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]