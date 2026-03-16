# Package class to 
class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, notes):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = "At hub"
        self.departure_time = None
        self.delivery_time = None
        self.truck_id = None

    def __str__(self):
        if self.status == "Delivered":
            return f"Package {self.package_id} | {self.address} {self.city}, {self.state} {self.zip_code} | Weight: {self.weight} | Deadline: {self.deadline} | Status: {self.status} | Delivered At: {self.delivery_time}"
        else:
            return f"Package {self.package_id} | {self.address} {self.city}, {self.state} {self.zip_code} | Weight: {self.weight} | Deadline: {self.deadline} | Status: {self.status}"