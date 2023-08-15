# Model Pembelajaran Mesin #
# ======================== #

# import library
import pandas as pd
import numpy as np
import time
import joblib
import warnings
from tensorflow import keras
# warnings.filterwarnings('ignore')

class Model:
    def __init__(self):

        # normalisasi
        normalisasi = joblib.load("H:\\3_hibrid_learning\\3_hibrid_learning_kali\\new_benign\\normalisasi\\normalisasi_minmaxScaler_rasio_4_1.joblib")

        # fitur yang dihapus
        fitur_dihapus_1 = pd.read_csv("H:\\3_hibrid_learning\\3_hibrid_learning_kali\\rasio_4_1\\fitur_hapus\\fitur_dihapus_layer_1_rasio_4_1.txt")
        fitur_dihapus_2 = pd.read_csv("H:\\3_hibrid_learning\\3_hibrid_learning_ori\\rasio_4_1\\fitur_hapus\\fitur_dihapus_layer_2_rasio_4_1.txt")
        fitur_dihapus_3 = pd.read_csv("H:\\3_hibrid_learning\\3_hibrid_learning_ori\\rasio_4_1\\fitur_hapus\\fitur_dihapus_layer_3_rasio_4_1.txt")

        # kolom dataset
        X_kolom = pd.read_csv("H:\\3_hibrid_learning\\3_hibrid_learning_ori\\rasio_4_1\\fitur\\fitur_rasio_4_1.txt")

        print('')
        print("".center(34, '='))
        print(" MEMUAT MODEL ".center(34, '+'))
        print("".center(34, '='))
    
        # lapisan 1 - lstm
        print (" Memuat model lstm pada lapisan 1 ")
        model_lapisan_1 = keras.models.load_model("H:\\3_hibrid_learning\\3_hibrid_learning_kali\\new_benign\\model\\model_lstm_layer_1_rasio_4_1.joblib")
        print (" Selesai memuat ")
    
        # lapisan 2 - random forest
        print (" Memuat model random forest pada lapisan 2 ")
        model_lapisan_2 = joblib.load("H:\\3_hibrid_learning\\3_hibrid_learning_kali\\new_benign\\model\\model_rf_layer_2_rasio_4_1.joblib")
        print (" Selesai memuat ")
        
        # lapisan 3 multi - random forest
        print (" Memuat model random forest pada lapisan 3 ")
        model_lapisan_3 = joblib.load("H:\\3_hibrid_learning\\3_hibrid_learning_kali\\new_benign\\model\\model_rf_layer_3_rasio_4_1.joblib")
        print (" Selesai memuat ")
        
        # membuat objek 
        self.normalisasi = normalisasi
        #self.fitur_dihapus_1 = fitur_dihapus_1
        #self.fitur_dihapus_2 = fitur_dihapus_2
        #self.fitur_dihapus_3 = fitur_dihapus_3
        self.fitur_dihapus_1 = fitur_dihapus_1['0'].values.tolist()
        self.fitur_dihapus_2 = fitur_dihapus_2['0'].values.tolist()
        self.fitur_dihapus_3 = fitur_dihapus_3['0'].values.tolist()
        self.X_kolom = X_kolom['0'].values.tolist()
        self.model_lapisan_1 = model_lapisan_1
        self.model_lapisan_2 = model_lapisan_2
        self.model_lapisan_3 = model_lapisan_3

        print('')
        print("".center(34, '='))
        print(" MULAI ANALISIS TRAFIK ".center(34, '+'))
        print("".center(34, '='))
