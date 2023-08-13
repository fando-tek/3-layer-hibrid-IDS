## Undersampling Dataset CSE-CIC-2018
Setelah beberapa tahapan praproses, dataset yang tersisa memiliki 63 fitur dan 15.898.871 sampel dari dataset awal yang memiliki 83 fitur dan 16.232.943 sampel. Terjadi penghapusan sebanyak 20 fitur dan 334.072 sampel. Dataset ini kemudian disimpan dalam format CSV. Selanjutnya, dataset yang telah disimpan pada tahap sebelumnya dimuat dengan tipe data pada tahap eksplorasi data. Kemudian, dilakukan peneyimbangan kelas menggunakan teknik under sampling dengan metode nearmiss-2. Dilakukan tiga rasio pengambilan sampel yang berbeda, 1:1, 2:1, dan 3:1. Pembangunan model juga dilakukan dengan dataset tanpa under sampling dengan rasio kelas normal terhadap kelas serangan 5:1. Jumlah data pada setiap dataset dapat dilihat pada Tabel dibawah.
|Under sampling|Rasio dataset|Jumlah Kelas normal	| Jumlah Kelas serangan|	
|Nearmiss-2	|1 : 1	|2.744.000	|2.744.400|
|Nearmiss-2	|2 : 1	|5.488.800	|2.744.400|
|Nearmiss-2	|3 : 1	|8.233.200	|2.744.400|
|Tanpa under sampling	|5 : 1	|13.154.471	|2.744.400|
