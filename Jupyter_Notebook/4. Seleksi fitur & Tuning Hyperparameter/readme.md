## Seleksi Fitur
![Seleksi fitur](https://github.com/fando-tek/Hybrid-learning-IDS/assets/81504312/23ec8fe5-3917-44fb-8eec-b01a9ecda91c)
\
Seleksi fitur dilakukan dengan menggunakan alur seperti gambar diatas, terdapat 32 kombinasi fitur terpilih yang berbeda yang dihasilkan dari empat dataset dengan rasio 1:1, 2:1, 3:1 dan 5:1, dimana masing-masing dataset memiliki 8 kombinasi fitur terpilih.\
\
Seleksi fitur menggunakan metode Chi-square dan Random Forest. Jumlah persentase skor sebesar 95% dan 99% digunakan sebagai ambang batas. Skor diurutkan dari yang terbesar, kemudian dijumlahkan. Fitur – fitur yang membentuk besaran persentase skor ≤ 95% atau ≤ 99% dipilih untuk digunakan dalam pembangunan model. Sedangkan  fitur – fitur dengan sisa persentase skor 5 % atau 1%, fitur – fitur ini dihapus.
Total terdapat 8 kombinasi fitur terpilih berdasarkan kombinasi pengaturan berikut ini:
```
1.	Metode Chi-square, vektor target biner, ambang batas skor 95%
2.	Metode Chi-square, vektor target biner, ambang batas skor 99%
3.	Metode Chi-square, vektor target multikelas, ambang batas skor 95%
4.	Metode Chi-square, vektor target multikelas, ambang batas skor 99%
5.	Metode Random Forest, vektor target biner, ambang batas skor 95%
6.	Metode Random Forest, vektor target biner, ambang batas skor 99%
7.	Metode Random Forest, vektor target multikelas, ambang batas skor 95%
8.	Metode Random Forest, vektor target multikelas, ambang batas skor 99%
```
## Tuning Hyperparameter
Tuning hyperparameter bertujuan untuk mendapatkan nilai hyperparameter yang memberikan model optimal menggunakan teknik random grid search. Random grid search memilih secara acak kombinasi nilai hyperparameter yang telah ditentukan. Setiap kombinasi nilai hyperparameter dilakukan validasi silang 5 lipatan (5-fold cross validation).\
![Tuning Hyper](https://github.com/fando-tek/Hybrid-learning-IDS/assets/81504312/d4588aeb-63ea-4019-ba02-e70a8d8965f8)
\
Hasil evaluasi dari setiap kombinasi nilai hyperparameter diperoleh dengan menghitung nilai rata – rata  f1-score dari cross validation. Tuning hyperparameter dilakukan pada 3 lapisan menggunakan 8 kombinasi fitur terpilih yang didapat dari tahap seleksi fitur. Dengan demikian, terdapat 24 kali tuning pada setiap dataset dari 4 dataset yang berbeda (dataset rasio 1:1, 2:1, 3:1, dan 5:1), sehingga total dilakukan 96 kali tuning pada keempat dataset, menghasilkan 96 kombinasi nilai hyperparameter.\
\
Tuning hyperparameter dilakukan hanya pada beberapa hyperparameter untuk menghindari biaya komputasi yang mahal. 
#### Pada lapisan pertama LSTM, hyperparameter yang digunakan dalam tuning meliputi :
```
- hidden layer/unit  = 16, 32, 48, 64
- learning rate      = 0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1
- dropout            = 0.1, 0.2, 0.3, 0.4, 0.5
- epoch              = 10, 20, 30, 40
- batch size         = 256, 512, 1024, 2048
```
dan hyperparameter yang ditetapkan tanpa dilakukan tuning adalah sebagai berikut:
```
- activation	     = sigmoid
- Optimizers	     = Adam
- Loss		     = binary_crossentropy
```
Sedangkan hyperparameter lainnya ditetapkan ke nilai default dari TensorFlow.
#### Pada lapisan kedua dan lapisan ketiga dengan Random Forest, hyperparameter yang digunakan meliputi :
Sebelum dilakukan tuning pada lapisan kedua dan ketiga, terlebih dahulu mencari jumlah decision trees/estimators yang sesuai, jumlah decision trees dipilih berdasarkan nilai f1-score tertinggi.
```
- estimators        = 10, 15, 20, 25, 30, 35, 40, 45, 50
- max features      = 5, 9, 12, 15, 18
- max depth         = None, 5, 10, 15, 20, 25, 30, 35
- min samples split = 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
- min samples leaf  = 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
```
Sedangkan hyperparameter lainnya ditetapkan ke nilai default dari scikit-learn.\
\
Selama tahap tuning, total pembangunan model yang dilakukan sebanyak 7200 model dan total waktu yang dibutuhkan selama tahap tuning sebesar 3527341 detik (979 jam, 49 menit, 1 detik).\
\
 ![Tuning Hyperparameter](https://github.com/fando-tek/Hybrid-learning-IDS/assets/81504312/093decc0-fbb5-4f0f-aff1-f75fabf13a0f)
