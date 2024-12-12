from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.conf import settings
from django.urls import reverse
from rest_framework import viewsets
from functools import wraps
from pyzbar.pyzbar import decode
from PIL import Image
from .models import Aduan, Barang, User, PeminjamanBarang
from .utils import generate_prioritas_catatan
from .serializers import AduanSerializer, UserSerializer, PeminjamanBarangSerializer, BarangSerializer
from .forms import AduanStatusForm, UserForm, PeminjamanForm, PeminjamanBarangStatusForm
import os

# Menampilkan view aduan ke dalam REST API
class AduanViewSet(viewsets.ModelViewSet):
    queryset = Aduan.objects.all()
    serializer_class = AduanSerializer

# Menampilkan view user ke dalam REST API
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Menampilkan view peminjaman barang ke dalam REST API
class PeminjamanBarangViewSet(viewsets.ModelViewSet):
    queryset = PeminjamanBarang.objects.all()
    serializer_class = PeminjamanBarangSerializer

# Menampilkan view barang ke dalam REST API
class BarangViewSet(viewsets.ModelViewSet):
    queryset = Barang.objects.all()
    serializer_class = BarangSerializer

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

# View untuk dashboard absensi user dan menambahkan data user di admin
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

# View untuk dashboard stok absensi user dan menambahkan data user di admin
@login_required(login_url='login')
def dashboard_peminjaman_barang(request):
    peminjaman_list = PeminjamanBarang.objects.all()

    if request.method == "POST":
        form = PeminjamanForm(request.POST, request.FILES)

        # Melakukan validasi form dan menyimpan data
        if form.is_valid():
            peminjaman = form.save(commit=False)
            peminjaman.save()
            
            # Redirect ke dashboard view yang sama
            return redirect("dashboard_peminjaman_barang")
        else:
            messages.error(request, 'Invalid form.')
    else:
        form = PeminjamanForm()
    
    # Pass User list dan form context ke template
    context = {
        "form": form,
        "peminjaman_list": peminjaman_list,
    }

    return render(request, "dashboard_peminjaman.html", context)

# View untuk menghapus peminjaman di dashboard peminjaman
@login_required(login_url='login')
def delete_peminjaman_barang(request):
    if request.method == "POST":
        id = request.POST["id"]
        
        # Hapus data peminjaman dari database jika request valid
        if id: 
            peminjaman = get_object_or_404(PeminjamanBarang, id=id)
            # Menghapus foto kondisi awal data peminjaman jika ada
            if peminjaman.kondisi_awal:
                kondisi_awal_path = peminjaman.kondisi_awal.name
                if default_storage.exists(kondisi_awal_path):
                    default_storage.delete(kondisi_awal_path)

            # Menghapus foto kondisi akhir data peminjaman jika ada
            if peminjaman.kondisi_akhir:
                kondisi_akhir_path = peminjaman.kondisi_akhir.name
                if default_storage.exists(kondisi_akhir_path):
                    default_storage.delete(kondisi_akhir_path)

            peminjaman.delete()
        else:
            messages.error(request, 'Invalid ID.')

    # Redirect ke dashboard view yang sama
    return redirect("dashboard_peminjaman_barang")

# View untuk mengubah status peminjaman di dashboard peminjaman
@login_required(login_url='login')
def update_status_peminjaman(request, peminjaman_id):
    # Fetch semua data peminjaman
    peminjaman = get_object_or_404(PeminjamanBarang, id=peminjaman_id)

    if request.method == "POST":
        form = PeminjamanBarangStatusForm(request.POST, instance=peminjaman)

        # Melakukan validasi form dan menyimpan data
        if form.is_valid():
            # Simpan ke database
            form.save()
            
            # Redirect ke dashboard view yang sama
            return redirect("dashboard_peminjaman_barang")
    else:
        form = PeminjamanBarangStatusForm(instance=peminjaman)
    
    return render(request, "dashboard_peminjaman.html", {"form": form})

# View untuk mengubah status peminjaman ke Dikembalikan di dashboard peminjaman
@login_required(login_url='login')
def update_status_dikembalikan(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        kondisi_akhir = request.FILES.get('kondisi_akhir')  

        # Fetch semua data pemijaman
        peminjaman = get_object_or_404(PeminjamanBarang, id=id)
        if peminjaman:
            # Menambahkan foto kondisi akhir ke data peminjaman
            peminjaman.kondisi_akhir = kondisi_akhir

            # Mengganti status peminjaman barang ke dikembalikan
            peminjaman.status = PeminjamanBarang.Status.DIKEMBALIKAN
            peminjaman.tanggal_kembali = timezone.now()

            # Simpan ke database
            peminjaman.save()
        else:
            return redirect('dashboard_peminjaman_barang')

    # Redirect ke dashboard view yang sama
    return redirect('dashboard_peminjaman_barang')

# View untuk menampilkan detail user di dashboard per user
@login_required(login_url='login')
def user_detail(request, id_user):
    user = get_object_or_404(User, id_user=id_user)  
    return render(request, 'dashboard_user_absensi.html', {'user': user})

# View untuk melakukan deteksi QR Code dari request POST
@csrf_exempt
def detect_qr_code(request):
    if request.method == 'POST':
        try:
            # Parse data JSON dari request
            received_qr_code = request.POST.get('qr_code', '')
            timestamp = request.POST.get('timestamp', '')
            screenshot = request.FILES.get('screenshot', None)

            # Mengekstrak QR Code dari qr_code_user
            try:
                received_id_user = received_qr_code.split('-')[0]
            except IndexError:
                return JsonResponse({'error': 'Invalid QR code format'}, status=400)

            print(f"Received ID User: {received_id_user}")

            # Menemukan user berdasarkan id usernya
            try:
                user = User.objects.filter(qr_code_user__icontains=received_id_user).exclude(qr_code_user__isnull=True).first()

                if not user:
                    return JsonResponse({'error': 'User not found with provided ID User'}, status=404)

                # Mendapatkan QR Code path dari static files
                qr_image_path = os.path.join(settings.MEDIA_ROOT, 'qr_code_user', str(user.qr_code_user).split('/')[-1])

                # Membaca dan decode QR Code dari gambar yang disimpan menggunakan pyzbar
                if os.path.exists(qr_image_path):
                    stored_image = Image.open(qr_image_path)
                    qr_data_list = decode(stored_image)

                    if not qr_data_list:
                        return JsonResponse({
                            'error': 'Could not detect QR code in stored image',
                            'path': qr_image_path
                        }, status=500)

                    # Melakukan decode QR Code data
                    stored_qr_data = qr_data_list[0].data.decode('utf-8')

                    print(f"Stored QR Data: {stored_qr_data}")
                    print(f"Received QR Data: {received_qr_code}")

                    # Melakukan komparasi QR Code dari recived QR Code dan stored QR Code
                    if stored_qr_data != received_qr_code:
                        return JsonResponse({
                            'error': 'QR code mismatch',
                            'stored': stored_qr_data,
                            'received': received_qr_code
                        }, status=400)
                else:
                    return JsonResponse({
                        'error': 'Stored QR image not found',
                        'path': qr_image_path
                    }, status=404)

            except Exception as e:
                return JsonResponse({
                    'error': f'Error validating QR code: {str(e)}',
                    'qr_code': str(user.qr_code_aerobo) if user else 'No user found'
                }, status=400)

            # Save the screenshot if provided
            last_in_entry = {
                "datetime": timestamp,
                "screenshot": None,
                "status_absensi": "Absen Diajukan",
            }
            if screenshot:
                # Menggunakan FileSystemStorage untuk penanganan `upload_to` yang propper
                fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'screenshots'))
                screenshot_filename = f'{received_qr_code}.png'
                filename = fs.save(screenshot_filename, screenshot)
                screenshot_url = fs.url(filename)
                last_in_entry["screenshot"] = f'media/screenshots/{os.path.basename(screenshot_url)}'

            # Update JSONField for last_in entry
            if not user.last_in:
                user.last_in = []
            user.last_in.append(last_in_entry)
            user.save()

            return JsonResponse({
                'message': 'QR code validated and data saved successfully',
                'user': {
                    'id_user': received_id_user,
                    'name': user.nama_user if hasattr(user, 'nama_user') else None
                },
                'screenshot_url': last_in_entry["screenshot"]
            })

        except Exception as e:
            return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

# View untuk mengupdate status absensi user
@login_required(login_url='login')
def update_status_absensi(request, id_user, index):
    user = get_object_or_404(User, id_user=id_user)  

    # Validate the index
    if user.last_in and 0 <= index < len(user.last_in):
        if request.method == "POST":
            # Get the new status from the form
            new_status = request.POST.get("status_absensi", "").strip()
            if new_status:  # Ensure the new status is not empty
                # Copy and update the JSONField data
                last_in_data = user.last_in
                last_in_data[index]["status_absensi"] = new_status
                
                # Save the updated JSONField
                user.last_in = last_in_data
                user.save(update_fields=["last_in"])  # Save only the JSON field
                
                # Redirect to the user detail page after saving
                return redirect(reverse('user_detail', args=[user.id_user]))
        
        # Render the form with the current status
        context = {
            "user": user,
            "entry_index": index,
            "current_status": user.last_in[index]["status_absensi"],
        }
        return render(request, "dashboard_user_absensi.html", context)
    
    # If the index is invalid, redirect to user detail
    return redirect(reverse('user_detail', args=[user.id_user]))