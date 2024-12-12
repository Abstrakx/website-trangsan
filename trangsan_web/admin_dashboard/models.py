from django.db import models
from django.core.files import File
from django.conf import settings
from model_utils import FieldTracker
from io import BytesIO
import qrcode
import os

# Database model Aduan
class Aduan(models.Model):
    nama_pengadu = models.CharField(max_length=100)
    tanggal_aduan = models.DateField(auto_now_add=True)
    isi_aduan = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('Baru', 'Baru'),
            ('Diproses', 'Diproses'),
            ('Selesai', 'Selesai'),
        ]
    )
    kategori = models.CharField(
        max_length=20,
        choices=[
            ('Administrasi', 'Administrasi'),
            ('Infrastruktur', 'Infrastruktur'),
            ('Kamtibmas', 'Kamtibmas'),
            ('Kebersihan', 'Kebersihan'),
            ('Anggaran', 'Anggaran'),
            ('Lainnya', 'Lainnya'),
        ]
    )
    prioritas = models.CharField(
        max_length=10,
        choices=[
            ('Tinggi', 'Tinggi'),
            ('Sedang', 'Sedang'),
            ('Rendah', 'Rendah'),
        ],
        blank=True,  
        null=True
    )
    catatan = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Aduan dari {self.nama_pengadu} - {self.prioritas}"
    
# Database model Barang 
class Barang(models.Model):
    kode_barang = models.CharField(max_length=20, primary_key=True)
    nama_barang = models.CharField(max_length=100)
    kondisi_barang = models.CharField(
        max_length=50,
        choices=[
            ("Baik", "Baik"),
            ("Dalam Perbaikan", "Dalam Perbaikan"),
            ("Rusak", "Rusak"),
        ]
    )
    status = models.CharField(
        max_length=50,
        choices=[
            ("Tersedia", "Tersedia"),
            ("Stok Kosong", "Stok Kosong"),
        ]
    )
    jumlah = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nama_barang} ({self.kode_barang})"
    
# Database model Absensi dan data karyawan serta warga desa
class User(models.Model):
    id_user = models.CharField(max_length=20, primary_key=True)
    nama_user = models.CharField(max_length=255)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=255)
    jabatan = models.CharField(max_length=255) 
    status = models.CharField(
        max_length=50,
        choices=[
            ('Pemerintah Desa', 'Pemerintah Desa'),
            ('Masyarakat', 'Masyarakat'),
        ]
    )
    qr_code_user = models.ImageField(upload_to='qr_code_user/', blank=True, null=True)
    last_in = models.JSONField(default=list)
    profile_picture = models.ImageField(upload_to='profile_picture/', blank=True, null=True)

    # Field tracker untuk melacak perubahan field tertentu
    tracker = FieldTracker(fields=['id_user', 'nama_user', 'jabatan', 'status'])

    def save(self, *args, **kwargs):
        if self.status == 'Pemerintah Desa':
            nama_depan = self.nama_user.split(" ")[0]

            # Logika untuk Auntentikasi QR Code
            if not self.qr_code_user or self._state.adding or self.tracker.has_changed('id_user') or self.tracker.has_changed('nama_user') or self.tracker.has_changed('jabatan') or self.tracker.has_changed('status'):
                # Hapus file QR mahasiswa lama
                if self.qr_code_user:
                    qr_path = os.path.join(settings.MEDIA_ROOT, self.qr_code_user.name)
                    if os.path.exists(qr_path):
                        os.remove(qr_path)
                    self.qr_code_user.delete(save=False)

                # Generate QR mahasiswa baru
                qrcode_img = qrcode.make(f'{self.id_user}-{nama_depan}-{self.jabatan}')
                qr_io = BytesIO()
                qrcode_img.save(qr_io, 'PNG')
                qr_file = File(qr_io, name=f'{self.id_user}-{nama_depan}-{self.jabatan}.png')
                self.qr_code_user.save(qr_file.name, qr_file, save=False)
    
        # Simpan objek ke database
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nama_user} ({self.id_user})"

# Database model peminjaman barang desa trangsan
class PeminjamanBarang(models.Model):
    class Status(models.TextChoices):
        DIAJUKAN = 'Diajukan', 'Diajukan'
        DITERIMA = 'Diterima', 'Diterima'
        DIKEMBALIKAN = 'Dikembalikan', 'Dikembalikan'
        DITOLAK = 'Ditolak', 'Ditolak'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE)
    tanggal_pinjam = models.DateField(auto_now_add=True)
    tanggal_kembali = models.DateField(null=True, blank=True)
    jumlah_pinjam = models.PositiveIntegerField()
    status = models.CharField(
        max_length=50,
        choices=Status.choices,
        default=Status.DIAJUKAN, 
    )
    kondisi_awal = models.ImageField(upload_to='kondisi_awal/', blank=True, null=True)
    kondisi_akhir = models.ImageField(upload_to='kondisi_akhir/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.nama_user} ({self.barang.nama_barang})"
    
    def is_terlambat(self):
        if self.tanggal_kembali and self.tanggal_kembali > self.tanggal_pinjam:
            return True
        return False
    
    def is_tersedia(self, jumlah_pinjam):
        return self.jumlah >= jumlah_pinjam

    def save(self, *args, **kwargs):
        # Mengurangi jumlah barang di database barang jika statusnya diterima
        if self.status == self.Status.DITERIMA:  
            if self.barang.jumlah < self.jumlah_pinjam:
                raise ValueError("Barang tidak mencukupi!")
            self.barang.jumlah -= self.jumlah_pinjam
            self.barang.save()

        # Mengembalikan jumlah barang jika barang dikembalikan
        if self.status == self.Status.DIKEMBALIKAN:
            self.barang.jumlah += self.jumlah_pinjam
            self.barang.save()

        # Mengganti status barang jika barang kosong
        if self.barang.jumlah == 0:
            self.barang.status = 'Stok Kosong'
            self.barang.save()

        # Mengganti status barang jika barang tersedia
        if self.barang.jumlah >= 0:
            self.barang.status = 'Tersedia'
            self.barang.save()

        super().save(*args, **kwargs)