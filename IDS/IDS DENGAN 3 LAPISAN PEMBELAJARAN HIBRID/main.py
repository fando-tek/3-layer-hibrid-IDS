# Main class #
# ========== #

import os
import pemantau_jaringan

def main():
    print("|=================================================================|")
    print("| DETEKSI INTRUSI BERBASIS PEMBELAJARAN MESIN HIBRID TIGA LAPISAN |")
    print("|=================================================================|\n") 
    print("Tekan 'enter' untuk merekam dan menganalisis paket")
    mode = input("Ketik 'p' untuk menganalisis file pcap : ")
    print("")

    output_dir = "H:\\3_hibrid_learning\\hasil_prediksi\\pcap\\"
    
    if mode == 'p':
        print("".center(34, '#'))
        print(" ANALISIS FILE PCAP ".center(34, '#'))
        print("".center(34, '#'))   
        list_pcap = os.listdir('G:\\Universitas Indonesia\\Rancangan Paper\\Dataset CSE-CIC-IDS2018-AWS\\pcap_test\\Pcap')
        #list_pcap = os.listdir('H:\\3_hibrid_learning\\Fajar Ndolu_3 Capture Trafik_python')
        print("")
        print('List PCAP \n---------\n',list_pcap)
        print("")
        file_pcap = input('ketik nama file pcap yang akan di analisis : ' )
        simpan_csv = input('ketik nama file csv yang akan di simpan : ' )
        f = "G:\\Universitas Indonesia\\Rancangan Paper\\Dataset CSE-CIC-IDS2018-AWS\\pcap_test\\Pcap\\"+file_pcap+".pcap"
        pemantau_jaringan.main(f,simpan_csv, output_dir)
    else:
        simpan_csv = input('ketik nama file csv yang akan di simpan : ' )
        print("")
        print("".center(34, '#'))
        print(" ANALISIS TRAFIK JARINGAN ".center(34, '#'))
        print("".center(34, '#'))
        pemantau_jaringan.main(None,simpan_csv, output_dir)

if __name__ == '__main__':
    main()

