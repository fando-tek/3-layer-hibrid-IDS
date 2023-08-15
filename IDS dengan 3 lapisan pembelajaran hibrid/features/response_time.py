import numpy
from scipy import stats as stat
from .context.packet_direction import PacketDirection


class ResponseTime:
    def __init__(self, feature):
        self.feature = feature

    def get_dif(self) -> list:
        time_diff = []
        temp_packet = None
        temp_direction = None
        for packet, direction in self.feature.packets:
            if (
                temp_direction == PacketDirection.FORWARD
                and direction == PacketDirection.REVERSE
            ):
                diff = packet.time - temp_packet.time
                time_diff.append(float(diff))
            temp_packet = packet
            temp_direction = direction
        return time_diff

    def get_var(self) -> float:
        """ Menghitung variasi perbedaan waktu. """
        
        var = -1
        if len(self.get_dif()) != 0:
            var = numpy.var(self.get_dif())

        return var

    def get_mean(self) -> float:
        """ Menghitung daftar rata-rata perbedaan waktu. """
        
        mean = -1
        if len(self.get_dif()) != 0:
            mean = numpy.mean(self.get_dif())

        return mean

    def get_median(self) -> float:
        """ Menghitung daftar median perbedaan waktu. """
        
        return numpy.median(self.get_dif())

    def get_mode(self) -> float:
        """ Menghitung modus dari daftar perbedaan waktu. """
        
        mode = -1
        if len(self.get_dif()) != 0:
            mode = float(stat.mode(self.get_dif())[0])

        return mode

    def get_skew(self) -> float:
        """ Skew dari daftar perbedaan waktu. """
        
        mean = self.get_mean()
        median = self.get_median()
        dif = 3 * (mean - median)
        std = self.get_std()
        skew = -10
        if std != 0:
            skew = dif / std

        return skew

    def get_skew2(self) -> float:

        mean = self.get_mean()
        mode = self.get_mode()
        dif = float(mean) - mode
        std = self.get_std()
        skew2 = -10
        if std != 0:
            skew2 = dif / float(std)

        return skew2

    def get_std(self) -> float:
        """ Menghitung standar deviasi dari daftar perbedaan waktu """
        
        std = -1
        if len(self.get_dif()) != 0:
            std = numpy.sqrt(self.get_var())

        return std

    def get_cov(self) -> float:
        """ Menghitung koefisien varian dari daftar perbedaan waktu.
        Nilai -1 jika pembagian dengan 0. """
        
        cov = -1
        if self.get_mean() != 0:
            cov = self.get_std() / self.get_mean()

        return cov
