from django import forms    
from .models import Aduan, User, PeminjamanBarang

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

# Form untuk meminjam barang dari user
class PeminjamanForm(forms.ModelForm):
    class Meta:
        model = PeminjamanBarang
        fields = ['user', 'barang', 'jumlah_pinjam', 'kondisi_awal']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}), 
            'barang': forms.Select(attrs={'class': 'form-control'}), 
            'kondisi_awal': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'jumlah_pinjam': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Jumlah barang', 'min': '1'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        barang = cleaned_data.get('barang')
        jumlah_pinjam = cleaned_data.get('jumlah_pinjam')

        if barang and jumlah_pinjam:
            if jumlah_pinjam > barang.jumlah:
                raise forms.ValidationError("Jumlah barang yang diminta melebihi stok tersedia.")
        return cleaned_data
    
# Form untuk mengubah status peminjaman
class PeminjamanBarangStatusForm(forms.ModelForm):
    class Meta:
        model = PeminjamanBarang
        fields = ['status'] 

    STATUS_CHOICES = [
        ('Diterima', 'Diterima'),
        ('Ditolak', 'Ditolak'),
    ]
    
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))