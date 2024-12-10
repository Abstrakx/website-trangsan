// Fungsi javascript untuk menampilkan modal foto Kondisi Awal dari Dashboard
$('#showKondisiAwal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); 

    // Extract atribut data
    var tanggal_pinjam = button.data('tanggal_pinjam');
    var kondisi_awal = button.data('kondisi_awal');

    var modal = $(this);

    // Menampilkan profile picture di modal
    if (kondisi_awal) {
        modal.find('.picture-preview').html('<img src="' + kondisi_awal + '" width="350">');
    } else {
        modal.find('.picture-preview').html('<img src="{% static \'images/logo.png\' %}" alt="No QR Code Available" width="300" height="300">');
    }

    // Menampilkan pemilik qr code di modal
    $('.request-date').html("<b>Peminjaman : </b>" + tanggal_pinjam);
});

// Fungsi javascript untuk menampilkan modal foto Kondisi Akhir dari Dashboard
$('#showKondisiAkhir').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); 

    // Extract atribut data
    var tanggal_kembali = button.data('tanggal_kembali');
    var kondisi_akhir = button.data('kondisi_akhir');

    var modal = $(this);

    // Menampilkan profile picture di modal
    if (kondisi_akhir) {
        modal.find('.picture-preview').html('<img src="' + kondisi_akhir + '" width="350">');
    } else {
        modal.find('.picture-preview').html('<img src="{% static \'images/logo.png\' %}" alt="No QR Code Available" width="300" height="300">');
    }

    // Menampilkan pemilik qr code di modal
    $('.request-date').html("<b>Pengembalian : </b>" + tanggal_kembali);
});

// Fungsi javascript untuk menampilkan modal delete data peminjaman dari Dashboard
$(document).ready(function(){
    // Pass id peminjaman ke delete modal
    $('.delete').click(function(){
        var id = $(this).data('id');
        $('#delete_id').val(id);
    });
});