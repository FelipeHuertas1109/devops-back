# Generated manually to add timestamps to Asistencia model

from django.db import migrations, models
from django.utils import timezone


def set_timestamps_for_existing_asistencias(apps, schema_editor):
    """Asignar timestamps a las asistencias existentes"""
    Asistencia = apps.get_model('example', 'Asistencia')
    now = timezone.now()
    Asistencia.objects.filter(created_at__isnull=True).update(created_at=now)
    Asistencia.objects.filter(updated_at__isnull=True).update(updated_at=now)


class Migration(migrations.Migration):

    dependencies = [
        ('example', '0006_configuracionsistema'),
    ]

    operations = [
        migrations.AddField(
            model_name='asistencia',
            name='created_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='asistencia',
            name='updated_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.RunPython(set_timestamps_for_existing_asistencias),
        migrations.AlterField(
            model_name='asistencia',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Fecha y hora de creación'),
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='Fecha y hora de última modificación'),
        ),
    ]

