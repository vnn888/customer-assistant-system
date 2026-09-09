"""
Generates a clean, safe, customer-service-themed knowledge base, replacing
the raw provided dataset (which turned out to contain unsafe content and
didn't match the assignment's described customer-service theme anyway).
Covers exactly what the brief asks for: FAQ, policy, troubleshooting,
contact information -- across 8 categories.
"""
import json

entries = []


def add(category, qa_pairs):
    for q, a in qa_pairs:
        entries.append({"category": category, "prompt": q, "response": a})


add("akun_login", [
    ("Bagaimana cara membuat akun baru?", "Klik tombol 'Daftar' di halaman utama, isi email dan nomor HP, lalu verifikasi lewat kode OTP yang dikirim ke email atau SMS kamu."),
    ("Saya lupa password, bagaimana cara reset?", "Klik 'Lupa Password' di halaman login, masukkan email terdaftar, lalu ikuti link reset password yang dikirim ke email kamu dalam 5 menit."),
    ("Kenapa akun saya tiba-tiba logout sendiri?", "Ini biasanya terjadi kalau sesi login kadaluarsa (30 hari) atau kamu login di perangkat baru yang otomatis mengeluarkan sesi lama karena alasan keamanan."),
    ("Bagaimana cara mengganti email yang terdaftar?", "Masuk ke menu Pengaturan Akun > Ubah Email, masukkan email baru, lalu konfirmasi lewat link verifikasi yang dikirim ke email lama dan baru."),
    ("Apakah saya bisa punya lebih dari satu akun?", "Setiap pengguna hanya diperbolehkan memiliki satu akun aktif per nomor identitas untuk mencegah penyalahgunaan promo dan menjaga keamanan transaksi."),
    ("Bagaimana cara menghapus akun saya secara permanen?", "Ajukan penghapusan akun lewat menu Pengaturan > Hapus Akun. Proses ini butuh 14 hari kerja dan tidak bisa dibatalkan setelah selesai."),
    ("Kenapa verifikasi OTP saya tidak masuk-masuk?", "Cek folder spam untuk email, atau pastikan nomor HP aktif dan sinyal stabil untuk SMS. Kode OTP juga bisa diminta ulang setelah 60 detik."),
    ("Bagaimana cara mengaktifkan autentikasi dua faktor (2FA)?", "Masuk ke Pengaturan Akun > Keamanan > Aktifkan 2FA, lalu scan QR code menggunakan aplikasi authenticator seperti Google Authenticator."),
    ("Apakah data pribadi saya aman?", "Data kamu dienkripsi dan disimpan sesuai standar keamanan industri. Kami tidak pernah membagikan data pribadi ke pihak ketiga tanpa persetujuan kamu."),
    ("Bagaimana cara mengubah nomor HP yang terdaftar?", "Masuk ke Pengaturan Akun > Ubah Nomor HP, masukkan nomor baru, lalu verifikasi dengan kode OTP yang dikirim ke nomor tersebut."),
    ("Akun saya diblokir, apa yang harus saya lakukan?", "Hubungi tim support lewat live chat atau email dengan menyertakan ID akun kamu, tim kami akan meninjau dan merespons dalam 1x24 jam kerja."),
    ("Bagaimana cara mengubah nama profil?", "Masuk ke menu Profil > Edit Profil, ubah nama tampilan, lalu simpan perubahan."),
    ("Apakah saya perlu memverifikasi identitas (KYC)?", "Verifikasi identitas dibutuhkan untuk fitur tertentu seperti penarikan dana besar, cukup upload foto KTP dan foto selfie sesuai instruksi di aplikasi."),
    ("Kenapa aplikasi minta saya login ulang terus?", "Coba update aplikasi ke versi terbaru dan pastikan tanggal-waktu perangkat kamu sudah otomatis/akurat, karena ini bisa mengganggu proses autentikasi."),
    ("Bagaimana cara menghubungkan akun dengan Google/Facebook?", "Masuk ke Pengaturan Akun > Hubungkan Akun, pilih platform yang diinginkan, lalu ikuti proses login dan izinkan aksesnya."),
])

add("pemesanan_pengiriman", [
    ("Berapa lama waktu pengiriman standar?", "Pengiriman standar memakan waktu 2-4 hari kerja untuk area dalam kota dan 4-7 hari kerja untuk luar kota, tergantung jasa kurir yang dipilih."),
    ("Bagaimana cara melacak pesanan saya?", "Buka menu 'Pesanan Saya', pilih pesanan yang ingin dilacak, nomor resi akan otomatis terhubung ke status pengiriman real-time."),
    ("Apakah saya bisa mengubah alamat pengiriman setelah checkout?", "Alamat bisa diubah selama status pesanan masih 'Menunggu Diproses'. Setelah masuk status 'Dikemas', perubahan alamat tidak bisa dilakukan."),
    ("Bagaimana cara membatalkan pesanan?", "Buka 'Pesanan Saya', pilih pesanan yang ingin dibatalkan, klik 'Batalkan Pesanan'. Ini hanya berlaku sebelum status berubah menjadi 'Dikirim'."),
    ("Apa yang terjadi jika saya tidak ada di rumah saat kurir datang?", "Kurir akan mencoba pengiriman ulang di hari berikutnya, atau paket dititipkan ke agen terdekat sesuai kebijakan masing-masing jasa kurir."),
    ("Apakah tersedia pengiriman same-day?", "Same-day delivery tersedia untuk beberapa kota besar dengan pesanan sebelum jam 14.00, biaya tambahan berlaku sesuai jarak."),
    ("Bagaimana jika paket saya hilang dalam pengiriman?", "Laporkan lewat menu Bantuan dengan menyertakan nomor pesanan, tim kami akan menginvestigasi bersama jasa kurir dan memproses klaim penggantian."),
    ("Apakah saya bisa memilih jasa kurir sendiri?", "Ya, pada halaman checkout tersedia beberapa pilihan kurir beserta estimasi waktu dan biaya masing-masing."),
    ("Kenapa status pesanan saya belum berubah setelah 2 hari?", "Keterlambatan update status bisa terjadi karena volume pengiriman tinggi. Jika lebih dari 3 hari kerja tidak ada perubahan, hubungi support kami."),
    ("Apakah bisa request pengiriman di jam tertentu?", "Untuk saat ini kami belum mendukung penjadwalan jam spesifik, tapi kamu bisa memilih preferensi pagi/siang/sore pada beberapa kurir tertentu."),
    ("Bagaimana cara mengetahui ongkos kirim sebelum checkout?", "Ongkos kirim otomatis terhitung setelah kamu memasukkan alamat pengiriman di halaman keranjang, sebelum melanjutkan ke pembayaran."),
    ("Apakah pesanan bisa digabung untuk hemat ongkir?", "Ya, selama pesanan belum dibayar, kamu bisa menambahkan produk lain ke keranjang yang sama untuk digabung dalam satu pengiriman."),
    ("Apa itu status 'Retur ke Pengirim'?", "Status ini muncul jika paket gagal terkirim beberapa kali dan dikembalikan ke gudang kami. Kami akan menghubungi kamu untuk pengiriman ulang atau refund."),
    ("Bagaimana cara komplain jika barang diterima rusak?", "Ajukan komplain dalam 2x24 jam sejak barang diterima lewat menu Bantuan, sertakan foto/video kondisi barang sebagai bukti."),
    ("Apakah ada pengiriman internasional?", "Saat ini kami hanya melayani pengiriman domestik. Ekspansi ke pengiriman internasional sedang dalam tahap perencanaan."),
])

add("pembayaran_tagihan", [
    ("Metode pembayaran apa saja yang tersedia?", "Kami mendukung transfer bank, kartu kredit/debit, e-wallet (OVO, GoPay, DANA, ShopeePay), dan cicilan tanpa kartu kredit untuk produk tertentu."),
    ("Apakah harga yang tertera sudah termasuk pajak?", "Ya, semua harga yang ditampilkan sudah termasuk PPN sesuai ketentuan yang berlaku, kecuali dinyatakan lain pada halaman produk."),
    ("Bagaimana cara menggunakan kode voucher?", "Masukkan kode voucher pada kolom 'Kode Promo' di halaman checkout sebelum melakukan pembayaran, diskon akan otomatis terpotong."),
    ("Kenapa pembayaran saya gagal padahal saldo cukup?", "Ini bisa terjadi karena gangguan jaringan sementara pada bank/e-wallet, atau limit transaksi harian sudah tercapai. Coba ulangi beberapa saat lagi."),
    ("Berapa lama proses verifikasi pembayaran transfer bank?", "Verifikasi otomatis biasanya selesai dalam 10-30 menit. Jika lebih dari 1 jam, unggah bukti transfer manual lewat menu Pesanan Saya."),
    ("Apakah tersedia cicilan tanpa kartu kredit?", "Tersedia lewat mitra paylater kami untuk produk dengan minimum harga tertentu, dengan pilihan tenor 3, 6, atau 12 bulan."),
    ("Bagaimana cara mendapatkan invoice/kwitansi?", "Invoice otomatis dikirim ke email setelah pembayaran berhasil, dan juga bisa diunduh dari menu Pesanan Saya > Detail Pesanan."),
    ("Apakah saya dikenakan biaya admin untuk transfer bank?", "Biaya admin bervariasi tergantung metode dan bank yang dipilih, besarannya akan ditampilkan secara transparan sebelum kamu konfirmasi pembayaran."),
    ("Bagaimana jika saya sudah bayar tapi status masih 'Menunggu Pembayaran'?", "Tunggu maksimal 1 jam untuk sinkronisasi otomatis. Jika status belum berubah, kirimkan bukti pembayaran ke tim support untuk verifikasi manual."),
    ("Apakah bisa membayar sebagian (DP)?", "Saat ini kami hanya mendukung pembayaran penuh di muka atau cicilan penuh lewat paylater, belum ada opsi DP sebagian."),
    ("Bagaimana cara mengubah metode pembayaran setelah checkout?", "Metode pembayaran tidak bisa diubah setelah pesanan dibuat. Kamu perlu membatalkan pesanan lalu membuat pesanan baru dengan metode yang diinginkan."),
    ("Apakah kartu kredit saya aman digunakan di sini?", "Ya, semua transaksi kartu kredit diproses lewat payment gateway bersertifikat PCI-DSS, kami tidak menyimpan data kartu kamu di server kami."),
])

add("pengembalian_refund", [
    ("Bagaimana cara mengajukan pengembalian barang?", "Ajukan lewat menu 'Pengembalian Barang' maksimal 7 hari setelah barang diterima, sertakan alasan dan foto kondisi barang."),
    ("Berapa lama proses refund setelah disetujui?", "Dana dikembalikan dalam 3-14 hari kerja tergantung metode pembayaran awal, e-wallet biasanya lebih cepat dibanding transfer bank."),
    ("Produk apa saja yang tidak bisa diretur?", "Barang custom/pesanan khusus, produk digital yang sudah diaktivasi, dan produk kebersihan pribadi yang segelnya sudah dibuka tidak bisa diretur."),
    ("Apakah biaya pengiriman retur ditanggung penjual?", "Jika retur disebabkan kesalahan penjual (barang rusak/salah kirim), biaya retur ditanggung penuh oleh kami. Selain itu, biaya ditanggung pembeli."),
    ("Bagaimana jika barang yang diterima tidak sesuai deskripsi?", "Ajukan komplain dalam 2x24 jam sejak diterima lewat menu Bantuan, sertakan foto/video sebagai bukti, tim kami akan memfasilitasi retur atau penukaran."),
    ("Apakah saya bisa tukar barang dengan ukuran/warna lain?", "Ya, penukaran ukuran/warna bisa diajukan dalam 7 hari lewat menu Pengembalian Barang, dengan syarat stok pengganti tersedia."),
    ("Kemana refund saya dikirim jika bayar pakai transfer bank?", "Refund untuk pembayaran transfer bank akan dikirim ke rekening bank yang kamu daftarkan saat pengajuan retur disetujui."),
    ("Apakah ongkos kirim ikut direfund?", "Ongkos kirim awal akan direfund penuh jika retur disebabkan kesalahan kami. Untuk alasan lain, hanya harga barang yang direfund."),
    ("Bagaimana status pengajuan retur bisa saya pantau?", "Status retur bisa dicek real-time di menu 'Pengembalian Barang', mulai dari 'Diajukan', 'Disetujui', hingga 'Dana Dikembalikan'."),
    ("Apa yang terjadi jika pengajuan retur saya ditolak?", "Kamu akan menerima notifikasi beserta alasan penolakan, dan bisa mengajukan banding dengan bukti tambahan lewat live chat support."),
    ("Apakah retur bisa diajukan untuk produk diskon?", "Bisa, selama masih dalam periode 7 hari dan produk memenuhi syarat retur lainnya, status diskon tidak mempengaruhi hak retur."),
])

add("troubleshooting_teknis", [
    ("Aplikasi sering force close, apa solusinya?", "Coba update aplikasi ke versi terbaru, bersihkan cache di Pengaturan HP > Aplikasi, atau install ulang jika masalah masih berlanjut."),
    ("Kenapa halaman produk tidak bisa dimuat?", "Ini biasanya karena koneksi internet tidak stabil. Coba refresh halaman atau ganti jaringan (WiFi ke data seluler atau sebaliknya)."),
    ("Bagaimana cara membersihkan cache aplikasi?", "Buka Pengaturan HP > Aplikasi > pilih aplikasi kami > Penyimpanan > Hapus Cache. Ini tidak akan menghapus data akun kamu."),
    ("Kenapa notifikasi tidak muncul di HP saya?", "Pastikan izin notifikasi aktif di Pengaturan HP > Aplikasi > Notifikasi, dan aplikasi tidak masuk mode hemat baterai yang membatasi background process."),
    ("Aplikasi lemot padahal sinyal bagus, kenapa?", "Kemungkinan cache aplikasi menumpuk atau versi aplikasi sudah usang. Update ke versi terbaru dan restart aplikasi bisa membantu."),
    ("Bagaimana cara upload foto tapi selalu gagal?", "Pastikan ukuran foto di bawah 5MB dan format JPG/PNG. Jika masih gagal, coba kompres foto atau gunakan koneksi WiFi yang lebih stabil."),
    ("Website tidak responsive di HP saya, kenapa?", "Coba akses lewat browser lain (Chrome/Safari terbaru) atau bersihkan cache browser. Kami juga menyediakan aplikasi mobile untuk pengalaman lebih optimal."),
    ("Kenapa saya tidak bisa checkout, tombolnya tidak bisa diklik?", "Pastikan semua field wajib (alamat, metode pembayaran) sudah terisi. Jika tombol tetap tidak aktif, coba refresh halaman atau ganti browser/aplikasi."),
    ("Bagaimana cara update aplikasi ke versi terbaru?", "Buka Google Play Store atau App Store, cari nama aplikasi kami, lalu klik tombol Update jika tersedia pembaruan."),
    ("Kenapa fitur pencarian tidak menampilkan hasil yang relevan?", "Coba gunakan kata kunci yang lebih spesifik atau periksa filter kategori/harga yang mungkin membatasi hasil pencarian secara tidak sengaja."),
    ("Aplikasi minta izin akses lokasi terus, apakah wajib?", "Akses lokasi membantu menampilkan estimasi ongkir dan waktu pengiriman yang akurat, tapi kamu tetap bisa memasukkan alamat secara manual tanpa akses lokasi."),
    ("Bagaimana jika lupa alamat email untuk login?", "Coba login menggunakan nomor HP terdaftar sebagai alternatif, atau hubungi support dengan menyertakan bukti kepemilikan akun untuk pemulihan."),
])

add("informasi_produk", [
    ("Bagaimana cara mengetahui stok produk tersedia atau tidak?", "Ketersediaan stok ditampilkan langsung di halaman produk; jika stok habis, tombol 'Tambah ke Keranjang' akan berubah menjadi 'Stok Habis'."),
    ("Apakah ada garansi untuk produk elektronik?", "Sebagian besar produk elektronik memiliki garansi resmi 1-2 tahun dari distributor, informasi detail tersedia di deskripsi masing-masing produk."),
    ("Bagaimana cara membaca ukuran produk yang tepat?", "Setiap halaman produk fashion menyediakan tabel ukuran (size chart) yang bisa diakses lewat tautan 'Panduan Ukuran' di bawah pilihan varian."),
    ("Apakah foto produk sama persis dengan barang asli?", "Kami berusaha menampilkan foto seakurat mungkin, namun warna bisa sedikit berbeda tergantung pengaturan layar perangkat kamu."),
    ("Bagaimana cara memberikan ulasan produk?", "Setelah status pesanan 'Selesai', buka menu Pesanan Saya, pilih produk, lalu klik 'Beri Ulasan' untuk menulis rating dan komentar."),
    ("Apakah produk yang dijual asli/original?", "Semua produk yang dijual melalui official store kami dijamin 100% asli, dengan sistem verifikasi ketat terhadap seluruh penjual mitra."),
    ("Bagaimana cara mengetahui produk pengganti jika stok habis?", "Sistem kami menampilkan rekomendasi produk serupa otomatis di bagian bawah halaman produk yang stoknya habis."),
    ("Apakah tersedia layanan konsultasi sebelum membeli?", "Ya, kamu bisa chat langsung dengan penjual lewat fitur 'Tanya Penjual' di halaman produk untuk pertanyaan spesifik sebelum membeli."),
])

add("kontak_eskalasi", [
    ("Bagaimana cara menghubungi customer service?", "Kamu bisa menghubungi kami lewat live chat di aplikasi (24 jam), email di support@contohtoko.com, atau telepon di 0800-1234-5678 (Senin-Sabtu, 08.00-20.00 WIB)."),
    ("Berapa lama waktu respons tim support?", "Live chat direspons rata-rata dalam 5 menit, sedangkan email dibalas maksimal dalam 1x24 jam kerja."),
    ("Bagaimana jika masalah saya belum terselesaikan oleh CS?", "Kamu bisa meminta eskalasi ke supervisor lewat live chat dengan menyebutkan nomor tiket sebelumnya, atau kirim email ke escalation@contohtoko.com."),
    ("Apakah ada nomor WhatsApp untuk customer service?", "Ya, kamu bisa chat via WhatsApp di 0812-3456-7890 untuk respons yang lebih cepat di jam operasional."),
    ("Bagaimana cara memberikan masukan atau saran?", "Kami sangat terbuka untuk masukan, bisa dikirim lewat form 'Kritik & Saran' di menu Bantuan atau email ke feedback@contohtoko.com."),
    ("Apakah customer service tersedia di hari libur nasional?", "Live chat tetap tersedia 24/7 termasuk hari libur, namun layanan telepon mengikuti jam operasional Senin-Sabtu."),
    ("Bagaimana cara melaporkan penjual yang mencurigakan?", "Gunakan tombol 'Laporkan' di halaman toko/produk terkait, atau hubungi support dengan detail bukti agar bisa segera ditindaklanjuti."),
])

add("kebijakan_umum", [
    ("Apa kebijakan privasi terkait data pengguna?", "Kami hanya mengumpulkan data yang diperlukan untuk transaksi dan tidak membagikannya ke pihak ketiga tanpa izin, sesuai kebijakan privasi lengkap di halaman Kebijakan Privasi."),
    ("Apakah ada batas usia minimum untuk membuat akun?", "Pengguna harus berusia minimal 17 tahun atau menggunakan akun yang diawasi orang tua/wali untuk transaksi yang melibatkan pembayaran."),
    ("Bagaimana kebijakan penggunaan kode promo?", "Setiap kode promo memiliki syarat dan ketentuan spesifik (minimum belanja, periode berlaku, kuota) yang tertera saat kamu mengklaim kode tersebut."),
    ("Apakah akun bisa dibekukan karena pelanggaran kebijakan?", "Ya, akun yang terbukti melanggar Syarat & Ketentuan (seperti transaksi fiktif atau penyalahgunaan promo) dapat dibekukan sementara atau permanen setelah investigasi."),
    ("Di mana saya bisa membaca Syarat dan Ketentuan lengkap?", "Syarat dan Ketentuan lengkap tersedia di footer halaman utama website, atau di menu Pengaturan > Legal & Kebijakan pada aplikasi."),
])

with open("data/knowledge_base.json", "w", encoding="utf-8") as f:
    json.dump(
        [{"id": i + 1, **e} for i, e in enumerate(entries)],
        f, ensure_ascii=False, indent=2,
    )

print(f"Generated {len(entries)} clean FAQ entries across {len(set(e['category'] for e in entries))} categories")
from collections import Counter
print(Counter(e['category'] for e in entries))
