// Fungsi javascript untuk menampilkan modal QR-Code dari Dashboard
$('#showQRCodeModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); 

    // Extract atribut data
    var nama_user = button.data('nama_user');
    var qr_code_user = button.data('qr_code_user');

    var modal = $(this);

    // Menampilkan profile picture di modal
    if (qr_code_user) {
        modal.find('.qr-code-preview').html('<img src="' + qr_code_user + '" width="350" height="350">');
    } else {
        modal.find('.qr-code-preview').html('<img src="{% static \'images/logo.png\' %}" alt="No QR Code Available" width="300" height="300">');
    }

    // Menampilkan pemilik qr code di modal
    $('.user-nama').html(nama_user);
});

// Fungsi javascript untuk menampilkan modal foto profil dari Dashboard
$('#showProfilePictureModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); 

    // Extract atribut data
    var nama_user = button.data('nama_user');
    var profile_picture = button.data('profile_picture');

    var modal = $(this);

    // Menampilkan profile picture di modal
    if (profile_picture) {
        modal.find('.profile-picture-preview').html('<img src="' + profile_picture + '" width="300">');
    } else {
        modal.find('.profile-picture-preview').html('<img src="{% static \'images/logo.png\' %}" alt="No QR Code Available" width="300" height="300">');
    }

    // Menampilkan pemilik qr code di modal
    $('.user-nama').html(nama_user);
});

// Fungsi javascript untuk menampilkan modal delete data user dari Dashboard
$(document).ready(function(){
    // Pass ID User ke delete modal
    $('.delete').click(function(){
        var id_user = $(this).data('id_user');
        $('#delete_id_user').val(id_user);
    });
});

// Fungsi javascript untuk menampilkan modal edit data user dari Dashboard
$('#editUserModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); 

    // Extract atribut data 
    var id_user = button.data('id_user');
    var nama_user = button.data('nama_user');
    var jabatan = button.data('jabatan');
    var status = button.data('status');
    var profile_picture = button.data('profile_picture');
    var username = button.data('username');
    var password = button.data('password');

    var modal = $(this);

    // Set values di modal
    modal.find('input[name="id_user"]').val(id_user);
    modal.find('input[name="nama_user"]').val(nama_user);
    modal.find('input[name="jabatan"]').val(jabatan);
    modal.find('input[name="status"]').val(status);
    modal.find('input[name="username"]').val(username);

    // Menampilkan foto profil jika ada
    if (profile_picture) {
        modal.find('.edit-profile-picture-preview').html('<img src="' + profile_picture + '" width="70" height="70">');
    } else {
        modal.find('.edit-profile-picture-preview').html('No profile picture');
    }

    $('.modal-title').html('Edit Data <b>' + nama_user + '</b>');
});