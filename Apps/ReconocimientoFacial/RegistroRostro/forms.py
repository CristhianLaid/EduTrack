from django .forms import ModelForm
from .models import RegistroRostro

class CapturaRostroForm(ModelForm):
    class Meta:
        model = RegistroRostro
        fields = ['foto_rostro']