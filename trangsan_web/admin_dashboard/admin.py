from django.contrib import admin
from .models import Aduan, Barang, User, PeminjamanBarang

admin.site.register(Aduan)
admin.site.register(Barang)
admin.site.register(User)
admin.site.register(PeminjamanBarang)