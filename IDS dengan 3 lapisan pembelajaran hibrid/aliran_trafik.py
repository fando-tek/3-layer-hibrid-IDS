import csv
import time
from collections import defaultdict
from scapy.sessions import DefaultSession
from scapy.all import wrpcap
from features.context.packet_direction import PacketDirection
from features.context.packet_flow_key import get_packet_flow_key
from flow import Flow
import numpy as np
import model
from datetime import datetime
import pandas as pd

WAKTU_KADALUARSA = 40
BATAS_PAKET = 100

class aliran_jaringan(DefaultSession):
    """ list aliran trafik. """

    def __init__(self, *args, **kwargs):
        self.flows = {}
        self.csv_line = 0
        self.total = {
            'benign': 0,
            'ddos_attack_hoic': 0,
            'ddos_attacks_loic_http': 0,
            'dos_attacks_hulk': 0,
            'bot': 0,
            'ftp_bruteforce': 0,
            'ssh_bruteforce': 0,
            'infilteration': 0,
            'dos_attacks_slowhttptest': 0,
            'dos_attacks_goldeneye': 0,
            'dos_attacks_slowloris': 0,
            'ddos_attack_loic_udp': 0,
            'brute_force__web': 0,
            'brute_force__xss': 0,
            'sql_injection': 0
        }
        
        if self.output_mode == "flow":
            output = open(self.output_file, "w", newline='')
            self.csv_writer = csv.writer(output)
            self.pcap_file = self.output_file[:-4]+'.pcap'

        self.packets_count = 0     
        self.clumped_flows_per_label = defaultdict(list)
        super(aliran_jaringan, self).__init__(*args, **kwargs)
        
        # membuat objek Model
        model_ml = model.Model()

        # mengakses variabel normalisasi dari objek my_model
        self.normalisasi = model_ml.normalisasi
        self.fitur_dihapus_1 = model_ml.fitur_dihapus_1
        self.fitur_dihapus_2 = model_ml.fitur_dihapus_2
        self.fitur_dihapus_3 = model_ml.fitur_dihapus_3
        self.X_kolom = model_ml.X_kolom
        self.model_lapisan_1 = model_ml.model_lapisan_1
        self.model_lapisan_2 = model_ml.model_lapisan_2
        self.model_lapisan_3 = model_ml.model_lapisan_3

    def toPacketList(self):
        self.pembersihan_paket(None)
        return super(aliran_jaringan, self).toPacketList()

    def on_packet_received(self, packet):
        count = 0
        direction = PacketDirection.FORWARD

        if self.output_mode != "flow":
            if "TCP" not in packet:
                return
            elif "UDP" not in packet:
                return
        try:
            packet_flow_key = get_packet_flow_key(packet, direction)
            flow = self.flows.get((packet_flow_key, count))
        except Exception:
            return

        self.packets_count += 1
        wrpcap(self.pcap_file, packet, append=True)

        if flow is None:
            direction = PacketDirection.REVERSE
            packet_flow_key = get_packet_flow_key(packet, direction)
            flow = self.flows.get((packet_flow_key, count))

        if flow is None:
            direction = PacketDirection.FORWARD
            flow = Flow(packet, direction)
            packet_flow_key = get_packet_flow_key(packet, direction)
            self.flows[(packet_flow_key, count)] = flow

        elif (packet.time - flow.latest_timestamp) > WAKTU_KADALUARSA:
            expired = WAKTU_KADALUARSA
            while (packet.time - flow.latest_timestamp) > expired:
                count += 1
                expired += WAKTU_KADALUARSA
                flow = self.flows.get((packet_flow_key, count))

                if flow is None:
                    flow = Flow(packet, direction)
                    self.flows[(packet_flow_key, count)] = flow
                    break
        elif "TCP" in packet and "F" in str(packet.flags):
            flow.add_packet(packet, direction)
            self.pembersihan_paket(packet.time)
            return

        flow.add_packet(packet, direction)

        if self.packets_count % BATAS_PAKET == 0 or (flow.duration > 120 and self.output_mode == "flow"):
            self.pembersihan_paket(packet.time)

    def get_flows(self) -> list:
        return self.flows.values()

    def pembersihan_paket(self, latest_time):
                  
        keys = list(self.flows.keys())
        for k in keys:
            flow = self.flows.get(k)
            if (latest_time is None or latest_time - flow.latest_timestamp > WAKTU_KADALUARSA
                or (flow.duration > 120)):
                data = flow.get_data()
                #timestamp = data.get('timestamp')
                # Konversi ke Unix timestamp
                #timestamp = int(timestamp.timestamp())
                #timestamp = (timestamp - pd.Timestamp("1970-01-01 00:00:00")) / pd.Timedelta('1s')
                #unix_time = {'timestamp': timestamp}
                #data.update(unix_time)

                if self.csv_line == 0:
                    string_fitur = [str(i) for i in data.keys()]
                    self.csv_writer.writerow(string_fitur + ['label_prediksi'])
                string_nilai = [str(i) for i in data.values()]
                hasil_prediksi = self.klasifikasi(data)
                self.csv_writer.writerow((string_nilai) + hasil_prediksi)
                self.csv_line += 1

                kelas = hasil_prediksi[0]
                if hasil_prediksi[0] in self.total:
                    self.total[kelas] += 1
                else:
                    self.total[kelas] = 1
                del self.flows[k]
            else:
                data = []
            
    def total_klasifikasi(self):
        for kelas, jumlah in self.total.items():
            print(f"Total {kelas}: {jumlah}")
    
    def klasifikasi(self, data):       
        nilai_fitur = list(data.values())
        waktu       = data.get('timestamp')
        port_sumber = data.get('src_port')
        port_tujuan = data.get('dst_port')
        ip_sumber   = data.get('src_ip')
        ip_tujuan   = data.get('dst_ip')
        data = dict((k, data[k]) for k in self.X_kolom if k in data)
            
        list_nilai = list(data.values())
        list_fitur = list(data.keys())
        
        list_nilai_fitur = [np.nan if x in [np.inf, -np.inf] else float(x) for x in list_nilai]
        if np.nan in list_nilai_fitur:
            return

        # Normalisasi
        X_test_norm = self.normalisasi.transform([list_nilai_fitur])
        X_test_norm = pd.DataFrame(X_test_norm)
        X_test_norm.columns = list_fitur

        # Huruf besar ke huruf kecil
        fitur_dihapus_1 = [kata.lower() for kata in self.fitur_dihapus_1]
        fitur_dihapus_1 = [kata.translate(str.maketrans(' /', '__')) for kata in fitur_dihapus_1]
        fitur_dihapus_2 = [kata.lower() for kata in self.fitur_dihapus_2]
        fitur_dihapus_2 = [kata.translate(str.maketrans(' /', '__')) for kata in fitur_dihapus_2]
        fitur_dihapus_3 = [kata.lower() for kata in self.fitur_dihapus_3]
        fitur_dihapus_3 = [kata.translate(str.maketrans(' /', '__')) for kata in fitur_dihapus_3]
        
        
        # Hapus fitur
        #df = df.drop(fitur_dihapus_chi, axis=1)
        X_test_layer_1 = X_test_norm.drop(fitur_dihapus_1, axis=1)
        X_test_layer_2 = X_test_norm.drop(fitur_dihapus_2, axis=1)
        X_test_layer_3 = X_test_norm.drop(fitur_dihapus_3, axis=1)
            
        # Prediksi Layer 1 #
        # ================ #
        X_test_1 = X_test_layer_1.to_numpy()
        X_test_1 = np.reshape(X_test_1,(X_test_1.shape[0],1,X_test_1.shape[1]))

        y_pred_1 = self.model_lapisan_1.predict(X_test_1, verbose=0)
        y_pred_1 = ((y_pred_1 > 0.5)+0).ravel()

        # konversi hasil prediksi menjadi 'benign' dan 'attack'        
        y_pred_1 = pd.DataFrame(np.where(y_pred_1 == 0,'benign','attack'),columns=['label_prediksi'])

        # Gabung X dan y prediksi dari lapisan 1
        data_1 = pd.concat([X_test_layer_2, y_pred_1], axis=1)

        # Prediksi Layer 2 #
        # ================ #
        if data_1[data_1['label_prediksi'] == 'attack'].empty :
            X_normal_1 = data_1.iloc[:,:-1]
            y_pred_2 = self.model_lapisan_2.predict(X_normal_1)

            # Gabung X dan y prediksi dari lapisan 1 dan 2
            data_1_2 = pd.concat([X_test_layer_3, pd.DataFrame(y_pred_2, columns=['label_prediksi'])], axis=1)
            
            # Prediksi Layer 3 #
            # ================ #
            if data_1_2[data_1_2['label_prediksi'] == 'benign'].empty :
                X_serangan_2 = data_1_2.iloc[:,:-1]
                hasil = self.model_lapisan_3.predict(X_serangan_2)      
            else :
                hasil = y_pred_2

        # Prediksi Layer 3 #
        # ================ #
        else :
            data_1_2 = pd.concat([X_test_layer_3, y_pred_1], axis=1)
            X_serangan_1 = data_1_2.iloc[:,:-1]
            hasil = self.model_lapisan_3.predict(X_serangan_1)
            
        string_nilai = [str(i) for i in nilai_fitur]
        klf = [str(''.join(hasil))]
        print("")
        print("+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=")
        print(f"Waktu          : {datetime.fromtimestamp(int(waktu))}")
        print(f"Alamat IP      : {ip_sumber} ==> {ip_tujuan}")
        print(f"Nomor Port     : {port_sumber} ==> {port_tujuan}")
        print(f"Prediksi       : {''.join(hasil)}")
        
        return klf
 
def generate_session_class(output_mode, output_file):
    return type("NewFlowSession",(aliran_jaringan,),
                {"output_mode": output_mode,
                 "output_file": output_file,},)
