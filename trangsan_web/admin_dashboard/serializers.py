from rest_framework import serializers
from .models import Aduan, User, PeminjamanBarang, Barang

# Serizalizers for rest api Aduan database
class AduanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aduan
        fields = "__all__"

# Serizalizers for rest api User database
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

# Serizalizers for rest api Peminjaman Barang database
class PeminjamanBarangSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeminjamanBarang
        fields = "__all__"

# Serizalizers for rest api Barang database
class BarangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barang
        fields = "__all__"