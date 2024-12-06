from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets
from .models import Aduan
from .utils import generate_prioritas_catatan
from .serializers import AduanSerializer

# Menampilkan view aduan ke dalam REST API
class AduanViewSet(viewsets.ModelViewSet):
    queryset = Aduan.objects.all()
    serializer_class = AduanSerializer

# Class untuk login view admin 
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return super().form_invalid(form)

# View untuk dashboard aduan
@login_required()
def dashboard_aduan(request):
    # Fetch semua data aduan
    aduan_list = Aduan.objects.all()

    if request.method == "POST":
        nama_pengadu = request.POST["nama_pengadu"]
        isi_aduan = request.POST["isi_aduan"]
        kategori = request.POST["kategori"]
        status = "Baru"
        
        # Dapatkan prioritas dan catatan dari GPT
        prioritas, catatan = generate_prioritas_catatan(isi_aduan)
        
        # Simpan ke database
        aduan = Aduan(
            nama_pengadu=nama_pengadu,
            isi_aduan=isi_aduan,
            kategori=kategori,
            status=status,
            prioritas=prioritas,
            catatan=catatan,
        )
        aduan.save()
        
        # Redirect ke dashboard view yang sama
        return redirect("dashboard_aduan")  
    
    # Pass Aduan list dan form context ke template
    context = {
        "aduan_list": aduan_list,
    }

    return render(request, "dashboard_aduan.html", context)