from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.storage import default_storage
from django.contrib import messages
from rest_framework import viewsets
from .models import Aduan, Barang, User
from .utils import generate_prioritas_catatan
from .serializers import AduanSerializer
from .forms import AduanStatusForm, UserForm

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

# View untuk dashboard aduan dan menambahkan data aduan di admin
@login_required(login_url='login')
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

# View untuk mengubah status aduan di dashboard aduan
@login_required(login_url='login')
def update_status_aduan(request, aduan_id):
    # Fetch semua data aduan
    aduan = get_object_or_404(Aduan, id=aduan_id)

    if request.method == "POST":
        form = AduanStatusForm(request.POST, instance=aduan)

        # Melakukan validasi form dan menyimpan data
        if form.is_valid():
            # Simpan ke database
            form.save()
            
            # Redirect ke dashboard view yang sama
            return redirect("dashboard_aduan")
    else:
        form = AduanStatusForm(instance=aduan)
    
    return render(request, "dashboard_aduan.html", {"form": form})

# View untuk dashboard stok barang dan menambahkan data barang di admin
@login_required(login_url='login')
def dashboard_barang(request):
    barang_list = Barang.objects.all()

    if request.method == "POST":
        kode_barang = request.POST["kode_barang"]
        nama_barang = request.POST["nama_barang"]
        kondisi_barang = request.POST["kondisi_barang"]
        status = "Tersedia"
        jumlah = request.POST["jumlah"]
        
        # Simpan ke database
        barang = Barang(
            kode_barang=kode_barang,
            nama_barang=nama_barang,
            kondisi_barang=kondisi_barang,
            status=status,
            jumlah=jumlah,
        )
        barang.save()
        
        # Redirect ke dashboard view yang sama
        return redirect("dashboard_barang")  
    
    # Pass Barang list dan form context ke template
    context = {
        "barang_list": barang_list,
    }

    return render(request, "dashboard_barang.html", context)

# View untuk menghapus barang di dashboard barang
@login_required(login_url='login')
def delete_barang(request):
    if request.method == "POST":
        kode_barang = request.POST["kode_barang"]
        
        # Hapus barang dari database jika request valid
        if kode_barang: 
            barang = get_object_or_404(Barang, kode_barang=kode_barang)
            barang.delete()
        else:
            messages.error(request, 'Invalid ID.')

    # Redirect ke dashboard view yang sama
    return redirect("dashboard_barang")

# View untuk melakukan edit barang di dashboard barang
@login_required(login_url='login')
def edit_barang(request):
    if request.method == "POST":
        kode_barang = request.POST["kode_barang"]
        nama_barang = request.POST["nama_barang"]
        kondisi_barang = request.POST["kondisi_barang"]
        status = request.POST["status"]
        jumlah = request.POST["jumlah"]   
        
        # Edit barang dari database jika request valid
        if kode_barang: 
            barang = get_object_or_404(Barang, kode_barang=kode_barang)
            barang.nama_barang = nama_barang
            barang.kondisi_barang = kondisi_barang
            barang.status = status
            barang.jumlah = jumlah
            barang.save()
        else:
            messages.error(request, 'Invalid ID.')

    # Redirect ke dashboard view yang sama
    return redirect("dashboard_barang")

# View untuk dashboard stok absensi user dan menambahkan data user di admin
@login_required(login_url='login')
def dashboard_user(request):
    user_list = User.objects.all()

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)

        # Melakukan validasi form dan menyimpan data
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            
            # Redirect ke dashboard view yang sama
            return redirect("dashboard_user")
        else:
            messages.error(request, 'Invalid form.')
    else:
        form = UserForm()
    
    # Pass User list dan form context ke template
    context = {
        "form": form,
        "user_list": user_list,
    }

    return render(request, "dashboard_user.html", context)

# View untuk menghapus user di dashboard user
@login_required(login_url='login')
def delete_user(request):
    if request.method == "POST":
        id_user = request.POST["id_user"]
        
        # Hapus user dari database jika request valid
        if id_user: 
            user = get_object_or_404(User, id_user=id_user)
            # Menghapus QR Code user jika ada
            if user.qr_code_user:
                qr_user_path = user.qr_code_user.name  
                if default_storage.exists(qr_user_path):  
                    default_storage.delete(qr_user_path)  

            # Menghapus foto profil user jika ada
            if user.profile_picture:
                profile_picture_path = user.profile_picture.name
                if default_storage.exists(profile_picture_path):
                    default_storage.delete(profile_picture_path)
                    
            user.delete()
        else:
            messages.error(request, 'Invalid ID.')

    # Redirect ke dashboard view yang sama
    return redirect("dashboard_user")

# View untuk melakukan edit user di dashboard user
@login_required(login_url='login')
def edit_user(request):
    if request.method == "POST":
        id_user = request.POST["id_user"]
        nama_user = request.POST["nama_user"]
        jabatan = request.POST["jabatan"]
        status = request.POST["status"]
        profile_picture = request.FILES.get('profile_picture')
        username = request.POST["username"]
        password = request.POST["password"]   
        confirm_password = request.POST["confirm_password"]   
        
        # Edit user dari database jika request valid
        if id_user: 
            user = get_object_or_404(User, id_user=id_user)
            user.nama_user = nama_user
            user.jabatan = jabatan
            user.status = status
            user.username = username

            # Melakukan checking data apakah ada update di foto profil
            if profile_picture:
                # Menghapus foto profil lama jika ada
                if user.profile_picture:
                    if default_storage.exists(user.profile_picture.name):
                        default_storage.delete(user.profile_picture.name)
                
                # Menimpa data foto profil baru ke database user
                user.profile_picture = profile_picture
            else:
                print("No new profile picture uploaded.")
            
            # Melakukan checking jika password sudah ada dan password tersebut berbeda dengan database
            if password:
                if password == confirm_password:
                    if password != user.password:
                        user.password = make_password(password)
                    else:
                        print("Password not changed (same as current).")
                else:
                    messages.error(request, "Passwords do not match.")
            else:
                print("No new password provided.")
            
            # Menyimpan data member terbaru kedalam database
            user.save()
        else:
            messages.error(request, 'Invalid ID User.')

    # Redirect ke dashboard view yang sama
    return redirect("dashboard_user")