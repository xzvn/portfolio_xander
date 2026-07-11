# Struktur CSS Portfolio Publik

CSS publik yang sebelumnya berada dalam satu `portfolio.css` besar sudah dipisahkan agar lebih mudah dirawat.

## Urutan file

1. `portfolio-foundation.css` — reset, variabel awal, header dasar, footer, dan komponen generik.
2. `portfolio-home.css` — halaman Home.
3. `portfolio-theme.css` — palet navy–indigo dan override navigasi global.
4. `portfolio-about.css` — halaman Tentang.
5. `portfolio-skills.css` — halaman Skills.
6. `portfolio-experience.css` — halaman Pengalaman.
7. `portfolio-projects.css` — halaman Proyek.
8. `portfolio-contact.css` — halaman Kontak.
9. `portfolio-interactions.css` — typewriter, animasi interaktif, aksesibilitas, kartu statistik, dan override final.

Urutan pemanggilan pada `templates/base.html` jangan diubah karena CSS masih mengikuti urutan cascade dari file lama.

## Aturan pengeditan

- Perubahan tampilan satu halaman diletakkan di file halaman tersebut.
- Interaksi lintas halaman diletakkan di `portfolio-interactions.css`.
- Jangan menempel override baru ke `portfolio.css`; file tersebut hanya menjadi penanda bahwa struktur lama sudah tidak dipakai.
- Sebelum menambah selector baru, cari selector serupa agar aturan tidak diduplikasi.
- Uji desktop, tablet, dan mobile setelah perubahan.

## Hasil pembersihan

- Blok interaksi Projects yang terduplikasi telah dihapus.
- Selector lama yang tidak dipakai oleh template publik atau JavaScript publik telah dihapus secara konservatif.
- File CSS kosong yang tidak digunakan telah dihapus.
- Sintaks semua file CSS telah divalidasi.


## Lapisan alur pengguna

- `portfolio-user-flow.css` dimuat paling akhir.
- File ini membedakan kartu informasi dari tombol, memperjelas navigasi
  mobile, menyusun ulang alur Home, dan memberi CTA langkah berikutnya.
- Jangan menambahkan efek klik pada kartu yang tidak melakukan tindakan.

- `portfolio-mobile-refinement.css` — drawer navigasi mobile dan perapian hero/mobile; dimuat paling akhir.
