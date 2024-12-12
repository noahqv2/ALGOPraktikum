# Die Klasse MaxHeap implementiert einen Max-Heap

# TODO: Diese Klasse implementieren Sie in Praktikum 2

class MaxHeap:
    def __init__(self):
        """ Initialisierung des Max-Heaps.
            Ein Knoten speichert die Anzahl der Bieter für eine Auktion sowie die ID-Nummer der Auktion.
            Die Auktion mit den meisten Bietern soll an der Spitze des Max-Heaps stehen.

        heap: Eine Liste zur Speicherung des Heaps, bestehend aus Tupeln in der Form (bid_count, auction_id).
        auction_map: Eine Hash-Map, welche die Position der Auktionen im Max-Heap speichert.
                     (key = auction_id, value = (bid_count, heap_index))
        """
        self.heap = []
        self.auction_map = {}

        # TODO: wenn Sie die anderen Methoden implementiert haben, können Sie diese Zeile auskommentieren
        #raise NotImplementedError

    # *** PUBLIC methods ***

    def add_auction(self, auction_id, bid_count):
        """ Fügt eine neue Auktion zum Max-Heap hinzu.
            Wenn die Auktion schon im heap ist, wird die Auktion nicht hinzugefügt.

        Args:
            auction_id: Die ID-Nummer der Auktion.
            bid_count: Die Anzahl der Bieter für diese Auktion.
        """
        if auction_id in self.auction_map:
            raise ValueError("Auktion existiert bereits")

        #raise NotImplementedError
        # TODO:

        self.heap.append((bid_count, auction_id))
        #print(auction_id, bid_count)
        self.auction_map[auction_id] = (bid_count, len(self.heap) - 1)
        self._heapify_up(len(self.heap) - 1)

    def update_bidders(self, auction_id, new_bid_count):
        """ Aktualisiert die Anzahl der Bieter für eine Auktion.
            Wenn die Auktion nicht im Heap ist, wird keine Auktion geändert.

        Args:
            auction_id: Die ID-Nummer der Auktion.
            new_bid_count: Die neue Anzahl der Bieter für diese Auktion.
        """
        if auction_id not in self.auction_map:
            raise ValueError("Auktion existiert nicht")
        # TODO:
        old_bid_count=self.auction_map[auction_id][0]
        index=self.auction_map[auction_id][1]
        self.heap[index] = (new_bid_count, auction_id)
        self.auction_map[auction_id] = (new_bid_count, index)
        #print("IF STATEMENT:",new_bid_count, old_bid_count)
        #print("OLD_BID_COUNT:",old_bid_count)
        if new_bid_count > old_bid_count:
            self._heapify_up(index)
        else:
            self._heapify_down(index)
        #raise NotImplementedError

    def remove(self, auction_id):
        """ Entfernt die Auktion aus dem Max-Heap.
            Wenn die Auktion nicht im Heap ist, wird keine Auktion entfernt.

        Args:
            auction_id: Die ID-Nummer der Auktion.
        """
        if auction_id not in self.auction_map:
            raise ValueError("Auktion existiert nicht")

        # TODO:

        index= self.auction_map[auction_id][1]
        self._swap(index, -1) # Tauscht es mit dem letzten Element
        del self.auction_map[auction_id] # del & pop sollten selbstverständlich sein
        self.heap.pop()
        self._heapify_down(index) # Wird nach unten "Heapified" um ihn einzusortieren

    # *** PUBLIC GET methods ***

    def get_auction_with_max_bidders(self):
        """ Gibt die Auktion mit der höchsten Anzahl an Bietern zurück.

        Returns:
            Tuple[int, int]: (bid_count, auction_id)
        """

        if not self.heap:
            return None
        self.print_heap()
        return self.heap[0][0], self.heap[0][1]

    def get_auction_bidders(self, auction_id):
        """ Gibt die Anzahl der Bieter für eine Auktion zurück.
            Wenn die Auktion nicht im Max-Heap ist, wird None zurückgegeben.

        Args:
            auction_id: Die ID-Nummer der Auktion.

        Returns:
            Optional[int]: bid_count
        """
        if auction_id in self.auction_map:
            return self.auction_map[auction_id][0]
        return None

    # *** PRIVATE methods ***

    def _swap(self, i, j):
        """ Hilfsfunktion zum Tauschen von zwei Auktionen im Max-Heap.
            Aktualisiert ebenfalls die Position der Auktionen in der auction_map.

        Args:
            i: Index der ersten Auktion im Max-Heap.
            j: Index der zweiten Auktion im Max-Heap.
        """
        # TODO:

        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

        temp_id = self.heap[i][1]
        self.auction_map[temp_id] = (self.heap[i][0],i)
        temp_id = self.heap[j][1]
        self.auction_map[temp_id] = (self.heap[j][0],j)
        #raise NotImplementedError

    def _heapify_up(self, index):
        """ Führt das Heapify-Up-Verfahren durch, um die Heap-Eigenschaft nach oben hin wiederherzustellen.
        Ein MaxHeap ist ein Binärbaum
        Args:
            index: Der Index des Elements, das nach oben "heapified" werden soll.
        """
        # TODO:
        while index > 0:
            parent= (index - 1) // 2
            if self.heap[index][0] > self.heap[parent][0]:
                self._swap(index, parent)
                index = parent
            else:
                break

        #raise NotImplementedError

    def _heapify_down(self, index):
        """ Führt das Heapify-Down-Verfahren durch, um die Heap-Eigenschaft nach unten hin wiederherzustellen.
        Ein MaxHeap ist ein Binärbaum

        Args:
            index: Der Index des Elements, das nach unten "heapified" werden soll.
        """
        # TODO:
        heap_length=len(self.heap)
        largest = index
        left = 2 * index + 1
        right = 2 * index + 2
        #print("Printing this now:", self.heap[largest])
        #print("Printing this now2:", self.heap[left])
        #print("Printing this now3:", self.heap[right][1])
        if left < heap_length and self.heap[left][0] > self.heap[largest][0]:
                largest = left

        if right < heap_length and self.heap[right][0] > self.heap[largest][0]:
                largest = right
        if largest != index:
            self._swap(index, largest)
            self._heapify_down(largest)

        #raise NotImplementedError

    def print_heap(self,index=0,level=0):
        if index >= len(self.heap):
            return
        print(" " * level * 2, self.heap[index])

        left = 2 * index + 1
        right = 2 * index + 2
        self.print_heap(left,level+1)
        self.print_heap(right,level+1)