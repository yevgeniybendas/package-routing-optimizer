from datetime import timedelta

class Truck:
    def __init__(self, truck_id, departure_time):
        self.truck_id = truck_id
        self.departure_time = departure_time
        self.packages = []
        self.mileage = 0.0
        self.current_location = "HUB"
        self.current_time = departure_time

    def add_package(self, package):
        self.packages.append(package)
        package.truck_id = self.truck_id

    def __str__(self):
        return f"Truck {self.truck_id} | Packages: {len(self.packages)} | Mileage: {self.mileage} | Current Location: {self.current_location}"