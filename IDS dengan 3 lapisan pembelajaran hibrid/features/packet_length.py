import numpy
from scipy import stats as stat


class PacketLength:
    """ class ini mengekstrak fitur yang terkait dengan Panjang Paket """

    mean_count = 0
    grand_total = 0

    def __init__(self, feature):
        self.feature = feature

    def get_packet_length(self, packet_direction=None) -> list:
        """ Membuat list panjang paket. """
        
        if packet_direction is not None:
            return [
                len(packet)
                for packet, direction in self.feature.packets
                if direction == packet_direction
            ]
        return [len(packet) for packet, _ in self.feature.packets]

    def get_header_length(self, packet_direction=None) -> list:
        """ Membuat list panjang header paket. """
        
        if packet_direction is not None:
            return (
                packet["IP"].ihl * 4
                for packet, direction in self.feature.packets
                if direction == packet_direction
            )
        return (packet["IP"].ihl * 4 for packet, _ in self.feature.packets)

    def get_total_header(self, packet_direction=None) -> int:
        """ Menghitung panjang header. """
        
        return sum(self.get_header_length(packet_direction))

    def get_min_header(self, packet_direction=None) -> int:
        """ Min panjang header. """
        
        return min(self.get_header_length(packet_direction))

    def get_max(self, packet_direction=None) -> int:
        """ Maks panjang header. """

        try:
            return max(self.get_packet_length(packet_direction))
        except ValueError:
            return 0

    def get_min(self, packet_direction=None) -> int:
        """ Panjang paket minimum dalam arah forward. """

        try:
            return min(self.get_packet_length(packet_direction))
        except ValueError:
            return 0

    def get_total(self, packet_direction=None) -> int:
        """Total panjang paket. """

        return sum(self.get_packet_length(packet_direction))

    def get_avg(self, packet_direction=None) -> int:
        """Rata - rata panjang paket. """
        
        count = len(self.get_packet_length(packet_direction))

        if count > 0:
            return self.get_total(packet_direction) / count
        return 0

    def first_fifty(self) -> list:
        """ Besar 50 ukuran paket pertama. """
        
        return self.get_packet_length()[:50]

    def get_var(self, packet_direction=None) -> float:
        """ Variasi panjang paket dalam jaringan. """

        var = 0
        if len(self.get_packet_length(packet_direction)) > 0:
            var = numpy.var(self.get_packet_length(packet_direction))
        return var

    def get_std(self, packet_direction=None) -> float:
        """ standar deviasi panjang paket dalam aliran. """
        
        return numpy.sqrt(self.get_var(packet_direction))

    def get_mean(self, packet_direction=None) -> float:
        """ Rata-rata panjang paket dalam aliran. """
        
        mean = 0
        if len(self.get_packet_length(packet_direction)) > 0:
            mean = numpy.mean(self.get_packet_length(packet_direction))

        return mean

    def get_median(self) -> float:
        """ Median panjang paket dalam aliran. """
        
        return numpy.median(self.get_packet_length())

    def get_mode(self) -> float:
        """ Modus panjang paket dalam aliran. """
        
        mode = -1
        if len(self.get_packet_length()) != 0:
            mode = int(stat.mode(self.get_packet_length())[0])

        return mode

    def get_skew(self) -> float:
        """ Skew panjang paket dalam aliran menggunakan median. """
        
        mean = self.get_mean()
        median = self.get_median()
        dif = 3 * (mean - median)
        std = self.get_std()
        skew = -10

        if std != 0:
            skew = dif / std

        return skew

    def get_skew2(self) -> float:
        """ Skew panjang paket dalam aliran menggunakan modus. """
        
        mean = self.get_mean()
        mode = self.get_mode()
        dif = mean - mode
        std = self.get_std()
        skew2 = -10

        if std != 0:
            skew2 = dif / std

        return skew2

    def get_cov(self) -> float:
        """ Koefisien varian panjang paket dalam aliran. """
        
        cov = -1
        if self.get_mean() != 0:
            cov = self.get_std() / self.get_mean()

        return cov
