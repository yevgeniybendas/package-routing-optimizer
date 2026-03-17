class Distance:
    def __init__(self):
        self.addresses = []
        self.distances = []
    #Functions to store addresses in a list and get address index for calculating distances later
    def add_address(self, address):
        self.addresses.append(address)
    
    def get_address_index(self, address):
        return self.addresses.index(address)
    
    def add_distance_row(self, row):
        self.distances.append(row)

    def get_distance(self, address1, address2):
        index1 = self.get_address_index(address1)
        index2 = self.get_address_index(address2)

        distance = self.distances[index1][index2]

        if distance == "":
            distance = self.distances[index2][index1]
        
        return float(distance)