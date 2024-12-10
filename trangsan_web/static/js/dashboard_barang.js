// Fungsi javascript untuk menampilkan modal delete data barang dari Dashboard
$(document).ready(function(){
    // Pass Kode Barang ke delete modal
    $('.delete').click(function(){
        var kode_barang = $(this).data('kode_barang');
        $('#delete_kode_barang').val(kode_barang);
    });
});

// Fungsi javascript untuk menampilkan modal edit data barang dari Dashboard
$('#editBarangModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); 

    // Extract atribut data 
    var kode_barang = button.data('kode_barang');
    var nama_barang = button.data('nama_barang');
    var kondisi_barang = button.data('kondisi_barang');
    var status = button.data('status');
    var jumlah = button.data('jumlah');

    var modal = $(this);

    // Set values di modal
    modal.find('input[name="kode_barang"]').val(kode_barang);
    modal.find('input[name="nama_barang"]').val(nama_barang);
    modal.find('select[name="kondisi_barang"]').val(kondisi_barang);
    modal.find('select[name="status"]').val(status);
    modal.find('input[name="jumlah"]').val(jumlah);
});   