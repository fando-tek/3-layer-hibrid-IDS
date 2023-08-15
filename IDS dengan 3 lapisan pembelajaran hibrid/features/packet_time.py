from datetime import datetime
import numpy
from scipy import stats as stat


class PacketTime:
    """ Class ini mengekstraksi fitur yang terkait dengan Waktu Paket. """

    count = 0

    def __init__(self, flow):
        self.flow = flow
        PacketTime.count += 1
        self.packet_times = None

    def _get_packet_times(self):
        """ list waktu paket pada aliran. """
        
        if self.packet_times is not None:
            return self.packet_times
        first_packet_time = self.flow.packets[0][0].time
        self.packet_times = [
            float(packet.time - first_packet_time) for packet, _ in self.flow.packets
        ]
        return self.packet_times

    def get_packet_iat(self, packet_direction=None):
        if packet_direction is not None:
            packets = [
                packet
                for packet, direction in self.flow.packets
                if direction == packet_direction
            ]
        else:
            packets = [packet for packet, direction in self.flow.packets]

        packet_iat = []
        for i in range(1, len(packets)):
            packet_iat.append(1e6 * float(packets[i].time - packets[i - 1].time))

        return packet_iat

    def relative_time_list(self):
        relative_time_list = []
        packet_times = self._get_packet_times()
        for index, time in enumerate(packet_times):
            if index == 0:
                relative_time_list.append(0)
            elif index < len(packet_times):
                relative_time_list.append(float(time - packet_times[index - 1]))
            elif index < 50:
                relative_time_list.append(0)
            else:
                break

        return relative_time_list

    def get_time_stamp(self):
        """ Tanggal dan waktu. """
        
        time = self.flow.packets[0][0].time
        #date_time = datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")
        #date_time = datetime.fromtimestamp(int(time))
        date_time = int(time)
        return date_time

    def get_duration(self):
        """ Menghitung durasi aliran. """

        return max(self._get_packet_times()) - min(self._get_packet_times())

    def get_var(self):
        """ Menghitung variasi waktu paket dalam aliran. """
        
        return numpy.var(self._get_packet_times())

    def get_std(self):
        """ Menghitung deviasi standar waktu paket dalam aliran. """
        
        return numpy.sqrt(self.get_var())

    def get_mean(self):
        """ Menghitung rata-rata waktu paket dalam aliran. """
        
        mean = 0
        if self._get_packet_times() != 0:
            mean = numpy.mean(self._get_packet_times())

        return mean

    def get_median(self):
        """ Median waktu paket dalam aliran. """
        
        return numpy.median(self._get_packet_times())

    def get_mode(self):
        """ Modus waktu paket dalam aliran. """
        
        mode = -1
        if len(self._get_packet_times()) != 0:
            mode = stat.mode(self._get_packet_times())
            mode = float(mode[0])

        return mode

    def get_skew(self):
        """ Skew waktu paket dalam aliran jaringan menggunakan median. """
        
        mean = self.get_mean()
        median = self.get_median()
        dif = 3 * (mean - median)
        std = self.get_std()
        skew = -10

        if std != 0:
            skew = dif / std

        return skew

    def get_skew2(self):
        """ Skew waktu paket dalam aliran jaringan menggunakan modus. """
        
        mean = self.get_mean()
        mode = self.get_mode()
        dif = float(mean) - mode
        std = self.get_std()
        skew2 = -10

        if std != 0:
            skew2 = dif / float(std)

        return skew2

    def get_cov(self):
        """ Menghitung koefisien varian waktu paket dalam aliran. """
        
        cov = -1
        if self.get_mean() != 0:
            cov = self.get_std() / self.get_mean()

        return cov
