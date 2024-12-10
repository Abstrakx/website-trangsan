from django import forms    
from .models import Aduan, User

# Form untuk menambahkan data user di dashboard user
class UserForm(forms.ModelForm):
    # Field password untuk form user
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label="Konfirmasi Password"
    )

    class Meta:
        model = User
        fields = ['id_user', 'nama_user','username', 'jabatan', 'status', 'profile_picture']

    # Hanya menerima akun ketika password dan konfirmasi password cocok
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password dan Konfirmasi Password tidak cocok.")
        return cleaned_data


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
