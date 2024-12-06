from django.db import models

# Database model Aduan
class Aduan(models.Model):
    nama_pengadu = models.CharField(max_length=100)
    tanggal_aduan = models.DateField(auto_now_add=True)
    isi_aduan = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('baru', 'Baru'),
            ('diproses', 'Diproses'),
            ('selesai', 'Selesai'),
        ]
    )
    kategori = models.CharField(
        max_length=20,
        choices=[
            ('administrasi', 'Administrasi'),
            ('infrastruktur', 'Infrastruktur'),
            ('kamtibmas', 'Kamtibmas'),
            ('kebersihan', 'Kebersihan'),
            ('anggaran', 'Anggaran'),
            ('lainnya', 'Lainnya'),
        ]
    )
    prioritas = models.CharField(
        max_length=10,
        choices=[
            ('tinggi', 'Tinggi'),
            ('sedang', 'Sedang'),
            ('rendah', 'Rendah')
        ],
        blank=True,  
        null=True
    )
    catatan = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Aduan dari {self.nama_pengadu} - {self.prioritas}"