# Proyek Tengah Semester

## Membuat Situs Web menggunakan Framework Django (Berkelompok)

> [!NOTE] 
> Tujuan kami adalah merancang dan mengimplementasikan halaman web dengan menggunakan framework Django. Kami akan memastikan situs web yang dibuat sudah memiliki  model, tampilan (views), dan template yang diperlukan untuk meningkatkan pengalaman pengguna. Selain itu, kami juga akan memanfaatkan framework CSS untuk memastikan tampilan situs web yang dibuat terlihat menarik. Terakhir, kami akan membuat dan mengimplementasikan unit test untuk memastikan fungsionalitas situs web kami.

### :technologist: Anggota Kelompok:

1. Ghania Larasati Nurjayadi Putri - 2206083003

2. I Putu Gede Kimi Agastya - 2206823695

3. Kristoforus Adi Himawan - 2206812174

4. Muh. Kemal Lathif Galih Putra - 2206081225

5. Shanti Yoga Rahayu - 2206082360

6. Syauqi Armanaya Syaki - 2206829010


### :fairy: Cerita aplikasi yang diajukan serta manfaat.

LiteraKarya adalah platform baca buku online yang memadukan kemudahan akses ke berbagai buku digital dengan elemen-elemen gamifikasi untuk meningkatkan semangat membaca. Dalam upaya memperluas wawasan literasi, LiteraKarya menawarkan berbagai informasi tentang buku, termasuk karya-karya dari penulis Indonesia dan luar negeri. Tak hanya koleksi buku, kami juga menghadirkan fitur-fitur menarik yang membuat pengalaman membaca lebih mengasyikkan. Sejalan dengan tema Kongres Bahasa Indonesia XII, kami berkomitmen untuk meningkatkan kesadaran akan pentingnya literasi dalam kemajuan bangsa dan merayakan kekayaan bahasa serta sastra Indonesia. LiteraKarya, solusi cerdas untuk memberdayakan pengguna dalam menjelajahi dunia literasi dengan semangat tinggi.

### :notebook_with_decorative_cover: Daftar modul yang akan diimplementasikan.

| **Modul** | **Pengembang** | **Deskripsi** |
| ------------ | ------------ | ------------ |
| Authentication | All members | Modul ini menyediakan mekanisme otentikasi dan otorisasi yang diperlukan untuk mengatur akses pengguna ke platform. |
| Persona | Syauqi Armanaya Syaki | Modul ini berfungsi untuk mengelola dan mengidentifikasi pengguna, serta memastikan pengalaman yang didapatkan sudah disesuaikan dan relevan. |
| Homepage | All members | Modul ini menampilkan halaman utama setelah user berhasil login ke dalam website. Di halaman utama ini, terdapat katalog buku dan informasi dari beberapa pilihan buku yang genre nya sesuai dengan pilihan pengguna. Di halaman utama ini  terdapat search bar untuk mencari nama buku yang diinginkan serta tombol untuk mengakses modul-modul lain. |
| Add Book | Kristoforus Adi Himawan | Modul ini memungkinkan pengguna untuk berkontribusi lebih terhadap dunia literasi dengan menambah buku. Untuk menambahkan buku, pengguna akan mengisi form berisi informasi rinci dari buku yang ditambahkan, misalnya judul serta genre. Selain itu, di modul ini, pengguna juga dapat melihat history buku-buku yang sudah pernah ditambahkan sebelumnya. |
| Book Page | Muh. Kemal Lathif Galih Putra | Modul ini dapat menampilkan list dari buku-buku yang sesuai dari dataset dan juga menyediakan informasi rinci setiap buku, termasuk sinopsis, penulis, rating, dan ulasan untuk setiap buku yang dapat diakses oleh pengguna yang sudah login. Selain itu, pengguna yang sudah login dapat memberikan ulasan untuk buku-buku yang dipilih.  |
| Entertainment Space | Ghania Larasati Nurjayadi Putri | Modul ini memberikan pengalaman hiburan yang unik, termasuk konten-konten menarik yang tidak hanya menghibur tetapi juga mendidik.  |
| Notes | Shanti Yoga Rahayu | Modul ini menampilkan keterangan bagi pembaca.  Modul ini memungkinkan pembaca untuk membuat catatan pribadi sehubungan dengan isi buku.  Catatan berfungsi sebagai alat untuk membantu pembaca untuk mengingat informasi penting. Catatan-catatan ini bisa berupa pemikiran, pemahaman, atau pertanyaan yang muncul selama membaca.  |
| Forum Page | I Putu Gede Kimi Agastya | Modul ini memungkinkan user untuk saling berdiskusi dengan user lainnya. User dapat membuat forum yang membahas tentang suatu judul buku atau mengenai topik lainnya yang berkaitan dengan literasi. |

### :card_index_dividers: Sumber dataset katalog buku.
Kami menggunakan dataset katalog yang bersumber di link berikut
<br>
https://drive.google.com/file/d/1vgnF971dMBPa6_cyupPa8VdrCmhSxv7O/view?usp=drive_link  
<br>
Dataset diatas didapatkan melalui scraping website https://www.goodreads.com/ yang merupakan website untuk melihat jenis-jenis buku. Isi dari dataset merupakan data dari 113 buku yang masing-masing memiliki informasi nama_buku, gambar_buku, author, description, genre_1, jumlah_halaman, waktu_publikasi, dsb.


### :man_judge: Role atau peran pengguna beserta deskripsi.
User adalah satu-satunya role pengguna dalam katalog LiteraKarya. Setelah berhasil membuat akun, user dapat memanfaatkan fitur-fitur pendukung seperti notes dan forum page untuk membantu meningkatkan semangat membaca. Selain itu, user juga dapat memilih elemen-elemen seperti nama dan informasi kontak untuk ditampilkan.
