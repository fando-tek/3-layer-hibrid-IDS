from scapy.layers.inet import IP, TCP
from .context.packet_direction import PacketDirection
from .packet_time import PacketTime


class FlowBytes:
    """class ini mengekstrak fitur dari trafik yang terkait dengan jumlah byte dalam aliran"""

    def __init__(self, feature):
        self.feature = feature

    def direction_list(self) -> list:
        """ Daftar arah paket dari 50 paket pertama dalam aliran """
        
        feat = self.feature
        direction_list = [
            (i, direction.name)[1]
            for (i, (packet, direction)) in enumerate(feat.packets)
            if i < 50
        ]
        return direction_list

    def get_bytes(self) -> int:
        """ Menghitung jumlah byte yang ditransfer """
        feat = self.feature
        p = (len(packet) for packet, _ in feat.packets)

        return sum(len(packet) for packet, _ in feat.packets)

    def get_rate(self) -> float:
        """ Menghitung laju byte yang ditransfer dalam aliran """

        duration = PacketTime(self.feature).get_duration()

        if duration == 0:
            rate = 0
        else:
            rate = self.get_bytes() / duration

        return rate

    def get_bytes_sent(self) -> int:
        """Calculates the amount bytes sent from the machine being used to run DoHlyzer.

        Returns:
            int: The amount of bytes.

        """
        feat = self.feature

        return sum(
            len(packet)
            for packet, direction in feat.packets
            if direction == PacketDirection.FORWARD
        )

    def get_sent_rate(self) -> float:
        """ Menghitung laju byte yang dikirim dalam aliran. """
        
        sent = self.get_bytes_sent()
        duration = PacketTime(self.feature).get_duration()

        if duration == 0:
            rate = -1
        else:
            rate = sent / duration

        return rate

    def get_bytes_received(self) -> int:
        """ Menghitung jumlah byte yang diterima. """
        
        packets = self.feature.packets

        return sum(
            len(packet)
            for packet, direction in packets
            if direction == PacketDirection.REVERSE
        )

    def get_received_rate(self) -> float:
        """ Menghitung laju byte yang diterima dalam aliran. """
        
        received = self.get_bytes_received()
        duration = PacketTime(self.feature).get_duration()

        if duration == 0:
            rate = -1
        else:
            rate = received / duration

        return rate

    def get_forward_header_bytes(self) -> int:
        """ Menghitung jumlah byte header di header yang dikirim ke arah yang sama dengan aliran. """

        packets = self.feature.packets

        return sum(
            self._header_size(packet)
            for packet, direction in packets
            if direction == PacketDirection.FORWARD
        )

    def get_forward_rate(self) -> int:
        """ Menghitung byte dalam arah forward pada aliran saat ini. """
        forward = self.get_forward_header_bytes()
        duration = PacketTime(self.feature).get_duration()

        if duration > 0:
            rate = forward / duration
        else:
            rate = -1

        return rate

    def _header_size(self, packet):
        return packet[IP].ihl * 4 if TCP in packet else 8

    def get_reverse_header_bytes(self) -> int:
        """ Menghitung jumlah byte header di header yang dikirim berlawanan arah dengan aliran. """

        packets = self.feature.packets

        if not packets:
            return 0

        return sum(
            self._header_size(packet)
            for packet, direction in packets
            if direction == PacketDirection.REVERSE
        )

    def get_min_forward_header_bytes(self) -> int:
        packets = self.feature.packets
        if not packets:
            return 0
 
        forward_packets = [(packet, direction) for packet, direction in packets if direction == PacketDirection.FORWARD]
        if not forward_packets:
            return 0

        return min(self._header_size(packet)
        for packet, direction in forward_packets)

    def get_reverse_rate(self) -> int:
        """ Menghitung byte dalam arah reverse pada aliran saat ini. """
        reverse = self.get_reverse_header_bytes()
        duration = PacketTime(self.feature).get_duration()

        if duration == 0:
            rate = -1
        else:
            rate = reverse / duration

        return rate

    def get_header_in_out_ratio(self) -> float:
        """ Menghitung rasio antara trafik forward dibanding trafik reverse.
            Jika byte header reverse adalah 0, maka nilainya -1 untuk menghindari kemungkinan pembagian dengan 0. """
        
        reverse_header_bytes = self.get_reverse_header_bytes()
        forward_header_bytes = self.get_forward_header_bytes()

        ratio = -1
        if reverse_header_bytes != 0:
            ratio = forward_header_bytes / reverse_header_bytes

        return ratio

    def get_initial_ttl(self) -> int:
        """ Memperoleh nilai time-to-live awal. """
        
        feat = self.feature
        return [packet["IP"].ttl for packet, _ in feat.packets][0]

    def get_bytes_per_bulk(self, packet_direction):
        if packet_direction == PacketDirection.FORWARD:
            if self.feature.forward_bulk_count != 0:
                return self.feature.forward_bulk_size / self.feature.forward_bulk_count
        else:
            if self.feature.backward_bulk_count != 0:
                return (
                    self.feature.backward_bulk_size / self.feature.backward_bulk_count
                )
        return 0

    def get_packets_per_bulk(self, packet_direction):
        if packet_direction == PacketDirection.FORWARD:
            if self.feature.forward_bulk_count != 0:
                return (
                    self.feature.forward_bulk_packet_count
                    / self.feature.forward_bulk_count
                )
        else:
            if self.feature.backward_bulk_count != 0:
                return (
                    self.feature.backward_bulk_packet_count
                    / self.feature.backward_bulk_count
                )
        return 0

    def get_bulk_rate(self, packet_direction):
        if packet_direction == PacketDirection.FORWARD:
            if self.feature.forward_bulk_count != 0 and self.feature.forward_bulk_duration != 0:
                return (
                    self.feature.forward_bulk_size / self.feature.forward_bulk_duration
                )
        else:
            if self.feature.backward_bulk_count != 0 and self.feature.backward_bulk_duration != 0:
                return (
                    self.feature.backward_bulk_size
                    / self.feature.backward_bulk_duration
                )
        return 0
