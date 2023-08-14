## Pembuatan model hibrid 
![Model lapisan 1,2 dan 3](https://github.com/fando-tek/Hybrid-learning-IDS/assets/81504312/c1258df1-9677-4547-9ab6-05784a12da89)\
\
Setelah mendapatkan 96 kombinasi nilai hyperparameter, f1-score dari kombinasi nilai hyperparameter dibandingkan pada setiap lapisan dari masing-masing dataset dengan rasio 1:1, 2:1, 3:1 dan 5:1. Satu lapisan terdiri dari 8 kombinasi hyperparameter yang dibandingkan untuk memilih satu kombinasi nilai hyperparameter yang memiliki nilai f1-score tertinggi seperti pada Gambar diatas.\
\
![model hibrid](https://github.com/fando-tek/Hybrid-learning-IDS/assets/81504312/587da801-672b-4a9e-9038-cf2d80f215be)\
\
Pada tahap ini, dilakukan pembangunan model pada setiap lapisan dari masing-masing dataset (rasio 1:1, 2:1, 3:1 dan 5:1) dengan menggunakan nilai hyperparameter terbaik yang telah didapat dari tahap tuning.\
```
- Pada lapisan satu, digunakan algoritma LSTM untuk klasifikasi dua kelas (biner) dengan label "1" menyatakan kelas serangan dan "0" menyatakan kelas normal.
- Pada lapisan dua, digunakan algoritma RF untuk klasifikasi dua kelas (biner) dengan label attack menyatakan kelas serangan dan label benign menyatakan kelas normal.
- Pada lapisan tiga, digunakan algoritma RF tetapi diklasifikasikan secara multi kelas dengan label benign, ddos attack hoic, ddos attacks loic http, dos attacks hulk, bot, ftp bruteforce, ssh bruteforce, infilteration, dos attacks slowhttptest, dos attacks goldeneye, dos attacks slowloris, ddos attack loic udp, brute force web, brute force xss, dan sql injection.
```

Total di ketiga lapisan sebanyak 12 model dibangun dan terdapat empat model hibrid yang masing-masing merupakan gabungan tiga model. Keempat model hibrid ini di evaluasi kinerjanya dan hasilnya dibandingkan.
