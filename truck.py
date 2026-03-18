from datetime import timedelta

#Create truck class and helper function to add packages to the truck, also import timedelta to easily keep track of time.
class Truck:
    def __init__(self, truck_id, departure_time):
        self.truck_id = truck_id
        self.departure_time = departure_time
        self.packages = []
        self.mileage = 0.0
        self.current_location = "HUB"
        self.current_time = departure_time
        self.return_time = None

    def add_package(self, package):
        self.packages.append(package)
        package.truck_id = self.truck_id
        package.departure_time = self.departure_time

    def __str__(self):
        return f"Truck {self.truck_id} | Packages: {len(self.packages)} | Mileage: {self.mileage} | Current Location: {self.current_location}"