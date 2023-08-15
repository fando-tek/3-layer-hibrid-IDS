# =================== #
#  Pemantau Jaringan  #
# =================== #

# Import library
import os
from scapy.all import *
from scapy.layers.inet import TCP
from scapy.sendrecv import sniff
from aliran_trafik import generate_session_class
import time

def main(input_file, nama_file, output_dir):
    m_trafik = time.time()
    sniffer, flow_session = pemantauan_jaringan(input_file, "flow", f"{nama_file}.csv", output_dir)
    s_trafik = time.time()

    # Tampilkan total benign dan attack
    print('')
    flow_session.total_klasifikasi()
    print('')
    print(f"Lama waktu membuat klasifikasi: {round(s_trafik - m_trafik, 2)} detik")

def pemantauan_jaringan(input_file, output_mode, output_file, output_dir):
    # NewFlowSession = generate_session_class(output_mode, output_file)
    NewFlowSession = generate_session_class(output_mode, os.path.join(output_dir, f"{output_file}"))

    if input_file is not None:
        flow_session = NewFlowSession()
        sniff(offline=input_file,
              prn=None,
              session=flow_session,
              store=False)
    else:
        flow_session = NewFlowSession()
        sniff(iface="Ethernet",
              filter="ip and (tcp or udp)",
              prn=None,
              session=flow_session,
              store=False)  # timeout = lama_snif

    return None, flow_session
        
if __name__ == "__main__":
    main()
    f.close()
