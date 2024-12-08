from django import forms    
from .models import Aduan

# Form untuk mengubah status aduan
class AduanStatusForm(forms.ModelForm):
    class Meta:
        model = Aduan
        fields = ['status'] 

    STATUS_CHOICES = [
        ('Baru', 'Baru'),
        ('Diproses', 'Diproses'),
        ('Selesai', 'Selesai'),
    ]
    
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
