from rest_framework import serializers
from .models import Aduan

class AduanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aduan
        fields = "__all__"