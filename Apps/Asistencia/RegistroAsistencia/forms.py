from django import forms
from .models import RegistroAsistencia

class RegistroAsistenciaForm(forms.ModelForm):
    class Meta:
        model = RegistroAsistencia
        fields = ['tipo', 'estado_asistencia']

    def __init__(self, *args, **kwargs):
        super(RegistroAsistenciaForm, self).__init__(*args, **kwargs)
        # Deshabilitar el campo 'tipo' para los estudiantes
        self.fields['tipo'].widget.attrs['readonly'] = True
        self.fields['estado_asistencia'].widget.attrs['readonly'] = True