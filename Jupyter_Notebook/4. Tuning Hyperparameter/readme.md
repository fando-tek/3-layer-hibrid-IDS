## Tuning Hyperparameter
Tuning hyperparameter bertujuan untuk mendapatkan nilai hyperparameter yang memberikan model dengan hasil yang optimal dengan teknik random grid search untuk menghemat waktu dan biaya komputasi. 
Random grid search memilih secara acak kombinasi nilai hyperparameter yang telah ditentukan. Setiap kombinasi nilai hyperparameter dilakukan validasi silang 5 lipatan (5-fold cross validation). Dalam 5 fold cross validation, data dibagi menjadi 5 fold berukuran kira-kira sama, sehingga memiliki 5 subset data untuk mengevaluasi kinerja model, 4 subset data digunakan untuk pelatihan dan 1 subset data digunakan untuk pengujian.
Hasil evaluasi dari setiap kombinasi nilai hyperparameter diperoleh dengan menghitung nilai rata – rata  f1-score dari cross validation. 
Tuning hyperparameter dilakukan pada 3 lapisan menggunakan 8 kombinasi fitur terpilih yang didapat dari tahap seleksi fitur. Dengan demikian, terdapat 24 kali tuning pada setiap dataset dari 4 dataset yang berbeda (dataset rasio 1:1, 2:1, 3:1, dan 5:1), sehingga total dilakukan 96 kali tuning pada keempat dataset, menghasilkan 96 kombinasi nilai hyperparameter.
Setelah mendapatkan 96 kombinasi nilai hyperparameter, f1-score dari kombinasi nilai hyperparameter dibandingkan pada setiap lapisan dari masing-masing dataset dengan rasio 1:1, 2:1, 3:1 dan 5:1. Satu lapisan terdiri dari 8 kombinasi hyperparameter yang dibandingkan untuk memilih satu kombinasi nilai hyperparameter yang memiliki nilai f1-score tertinggi. 
Total terdapat 12 kombinasi nilai hyperparameter yang dipilih untuk membangun model yang kemudian digunakan pada empat model hibrid, dimana satu model hibrid membutuhkan tiga model. Pemilihan kombinasi nilai hyperparameter berdasarkan nilai f1-score tertinggi, disebabkan dataset yang digunakan adalah dataset yang tidak seimbang sehingga metrik pengukuran yang lebih baik adalah f1-score yang merupakan harmonisasi antara nilai precision dan nilai recall.
Tuning hyperparameter dilakukan hanya pada beberapa hyperparameter untuk menghindari biaya komputasi yang mahal. Pada lapisan pertama LSTM, hyperparameter yang digunakan dalam tuning meliputi :
'''
- hidden layer/unit    = 16, 32, 48, 64
-	learning rate	     = 0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1
-	dropout		     = 0.1, 0.2, 0.3, 0.4, 0.5
-	epoch		     = 10, 20, 30, 40
-	batch size	     = 256, 512, 1024, 2048
'''
dan hyperparameter yang ditetapkan tanpa dilakukan tuning adalah sebagai berikut:
- activation	     = sigmoid
- Optimizers	     = Adam
- Loss		     = binary_crossentropy
Sedangkan hyperparameter lainnya ditetapkan ke nilai default dari TensorFlow.
Pada lapisan kedua dan lapisan ketiga dengan Random Forest, hyperparameter yang digunakan meliputi :
- estimators 	     = 10, 15, 20, 25, 30, 35, 40, 45, 50
- max features	     = 5, 9, 12, 15, 18
- max depth	     = None, 5, 10, 15, 20, 25, 30, 35
- min samples split   = 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
- min samples leaf    = 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
Sedangkan hyperparameter lainnya ditetapkan ke nilai default dari scikit-learn.
Sebelum dilakukan tuning pada lapisan kedua dan ketiga, terlebih dahulu mencari jumlah decision trees/estimators yang sesuai, jumlah decision trees dipilih berdasarkan nilai f1-score tertinggi. Proses ini dilakukan secara terpisah dari proses tuning untuk mengurangi waktu pemilihan kombinasi nilai hyperparameter dengan random grid search.
Tahap tuning hyperparameter dilakukan dengan random grid search untuk mendapatkan nilai hyperparameter yang menghasilkan model dengan f1-score tertinggi. Proses tuning hyperparameter dilakukan pada 3 lapisan menggunakan 8 kombinasi fitur di setiap dataset dari 4 dataset yang berbeda (dataset rasio 1:1, 2:1, 3:1, dan 5:1). Sehingga, terdapat 8 kombinasi nilai hyperparameter pada setiap lapisan, dan 24 kombinasi nilai hyperparameter pada setiap dataset, total didapatkan 96 kombinasi nilai hyperparameter berbeda dari keempat dataset. Hasil rinci 96 kombinasi nilai hyperparameter ini dapat dilihat pada Lampiran 5.
Pada setiap proses tuning menggunakan random grid search, dipilih secara acak 15 kombinasi nilai hyperparameter dari rentang nilai yang telah ditentukan. Setiap kombinasi nilai hyperparameter dievaluasi dengan validasi silang 5 lipatan (5-fold cross validation), dan dihitung rata-rata f1-score dari hasil validasi tersebut. Dari 15 kombinasi nilai hyperparameter, diperoleh 15 nilai rata-rata f1-score yang kemudian diurutkan dari nilai tertinggi. Selanjutnya, dipilih satu kombinasi nilai hyperparameter yang menghasilkan f1-score tertinggi, untuk kemudian dibandingkan dengan lainnya. 
Selama tahap tuning, total pembangunan model yang dilakukan sebanyak 7200 model (4 dataset x 8 kombinasi fitur x 3 lapisan x 15 kombinasi hyperparameter x 5 cross validation) seperti yang di tunjukkan pada Gambar 4.4. Selain itu, total waktu yang dibutuhkan selama tahap tuning sebesar 3527341 detik (979 jam, 49 menit, 1 detik).
 ![Tuning Hyperparameter](https://github.com/fando-tek/Hybrid-learning-IDS/assets/81504312/093decc0-fbb5-4f0f-aff1-f75fabf13a0f)

Gambar 4.4 Total pembangunan model saat tahap tuning hyperparameter
Pada sub subbab 4.5.1, 4.5.2, dan 4.5.3, dijelaskan secara rinci contoh penerapan tuning hyperparameter pada ketiga lapisan dengan menggunakan dataset yang diseimbangkan menggunakan metode nearmiss-2 dengan rasio 1:1. Fitur yang digunakan pada dataset ini merupakan fitur yang telah dipilih menggunakan metode seleksi fitur Chi-square dengan vektor target multi kelas dan batas ambang persentase skor ≤ 95%, tetapi tidak melebihi 95%.
Selain kombinasi nilai hyperparameter, pemilihan kombinasi fitur juga memiliki pengaruh terhadap peningkatan kinerja model. Hasil dari tahap tuning dapat dilihat pada lampiran 5, dimana setiap kombinasi fitur dievaluasi untuk mendapatkan satu kombinasi fitur yang memberikan hasil optimal. Terdapat perbedaan dalam nilai f1-score pada setiap kombinasi fitur yang dievaluasi. Pemilihan kombinasi fitur dengan f1-score tertinggi menunjukkan peningkatan kinerja model dibandingkan dengan kombinasi fitur lainnya pada setiap lapisan untuk setiap dataset (rasio 1:1, 2:1, 3:1 dan 5:1). Hal ini menunjukkan bahwa pemilihan fitur yang tepat memiliki dampak pada peningkatan kinerja model.
