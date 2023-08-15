## IDS dengan 3 lapisan pembelajaran hibrid
Untuk menguji kinerja model hibrid maka digunakan IDS yang dimodifikasi dari CICflowmeter berbasis python. IDS ini hanya digunakan untuk tujuan simulasi dan tidak digunakan secara langsung untuk menangani serangan yang sebenarnya.\
\
\
IDS melakukan analisis dan klasifikasi pada aliran lalu lintas yang ditangkap. Aliran lalu lintas merupakan kumpulan dari beberapa paket yang saling terkait, memiliki kuintupel yang sama, yaitu IP sumber, IP tujuan, port sumber, port tujuan, dan protokol.
Jika analisis dan klasifikasi dilakukan secara offline, IDS akan dihentikan setelah selesai menganalisis dan mengklasifikasikan semua aliran lalu lintas pada file PCAP. Sedangkan jika dilakukan secara real time, IDS akan terus melakukan analisis dan klasifikasi tanpa batasan waktu. \
\
Untuk menguji kinerja IDS secara offline, digunakan data lalu lintas serangan hasil simulasi yang ditangkap melalui Wireshark, kemudian dianalisis dan diklasifikasikan. Sedangkan untuk menguji kinerja IDS secara real time, dilakukan simulasi serangan jaringan yang ditargetkan langsung pada perangkat yang menjalankan IDS tanpa perlu menggunakan wireshark. \
\
Gambar berikut merupakan tampilan hasil klasifikasi dengan IDS.\
![image](https://github.com/fando-tek/Hybrid-learning-IDS/assets/81504312/267f5eb1-3829-4f0a-926d-5a297d2477c1)
