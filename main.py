#Student ID: 001031254

import csv
from datetime import timedelta

from package import Package
from hashtable import Hashtable
from distance import Distance
from truck import Truck

def main_menu(trucks, package_table):
    while True:
        print("\nWGUPS Delivery System")
        print("1. View all packages at a specific time")
        print("2. View single package status at a specific time")
        print("3. View total mileage")
        print("4. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            time_input = input("Enter time (HH:MM, 24hr format): ")
            hours, minutes = map(int, time_input.split(":"))
            query_time = timedelta(hours=hours, minutes=minutes)

            print_all_statuses_at_time(query_time, trucks)

        elif choice == "2":
            package_id = int(input("Enter package ID: "))
            time_input = input("Enter time (HH:MM): ")
            hours, minutes = map(int, time_input.split(":"))
            query_time = timedelta(hours=hours, minutes=minutes)

            package = package_table.lookup(package_id)
            status = delivery_status(package, query_time, trucks)

            print(f"Package {package_id} status at {query_time}: {status}")

        elif choice == "3":
            total = sum(truck.mileage for truck in trucks.values())
            print(f"Total mileage: {round(total, 2)}")

        elif choice == "4":
            break

#Fix display for package 9.
def get_display_address(package, query_time):
    if package.package_id == 9 and query_time < timedelta(hours=10, minutes=20):
        return normalize_address("300 State St")
    return package.address

#Define status reports for specific times to be calculated dynamically based on queried time.
def delivery_status(package, query_time, trucks):
    truck = trucks[package.truck_id]

    if query_time < truck.departure_time:
        return "At the hub"
    elif query_time >= package.delivery_time:
        return f"Delivered at {package.delivery_time}"
    else:
        return "En route"
#Print statuses for all packages based on a query time.    
def print_all_statuses_at_time(query_time, trucks):
    print(f"\nPackage statuses at {query_time}:\n")

    for truck_id in sorted(trucks.keys()):
        truck = trucks[truck_id]
        print(f"Truck {truck_id}:")

        for package in sorted(truck.packages, key=lambda p: p.package_id):
            status = delivery_status(package, query_time, trucks)
            print(
                f"Package {package.package_id} | "
                f"Address: {get_display_address(package, query_time)} | "
                f"Deadline: {package.deadline} | "
                f"Status: {status}"
            )

        print()

#Helper function to remove unit numbers and standardize direction naming convention from address to avoid errors
def normalize_address(address):
    address = address.split("#")[0].strip()
    address = address.replace(" South ", " S ")
    address = address.replace(" North ", " N ")
    address = address.replace(" East ", " E ")
    address = address.replace(" West ", " W ")
    return address

#Package router helper to build list of available packages and find the one thats the nearest to the trucks current location.
def get_undelivered_addresses(truck):
    addresses = []

    for package in truck.packages:
        if package.status == "Delivered":
            continue
        
        if package.package_id == 9 and truck.current_time < timedelta(hours=10, minutes=20):
            continue
            
        elif package.package_id == 9 and truck.current_time >= timedelta(hours=10, minutes=20):
            package.address = normalize_address("410 S State St")
            package.city = "Salt Lake City"
            package.zip_code = "84111"
            addresses.append(package.address)

        if package.address not in addresses:
            addresses.append(package.address)

    return addresses

#Package router helper for truck 3 to prioritze deadline packages vs nearest neighbor to meet deadlines
def priority_addresses(truck):

    if truck.truck_id != 3:
        return get_undelivered_addresses(truck)
    
    else:
        undelivered = []
        for package in truck.packages:
            if package.status != "Delivered":
                undelivered.append(package)
        
        priority = []
        for package in undelivered:
            if package.deadline != "EOD" and package.address not in priority:
                priority.append(package.address)
        
        if not priority:
            return get_undelivered_addresses(truck)
        else:
            return priority

#Package router helper to find next nearest address for available packages.
def find_nearest_address(truck, distance_table, addresses):
    
    nearest_address = None
    shortest_distance = float("inf")

    #Find all distances to available packages from current location
    for address in addresses:
        distance = distance_table.get_distance(truck.current_location, address)

        if distance < shortest_distance:
            shortest_distance = distance
            nearest_address = address
        
    return nearest_address, shortest_distance  

#Package routing delivery algorithm 
def deliver_truck(truck, distance_table):
    while True:
        undelivered = priority_addresses(truck)

        if not undelivered:
            distance = distance_table.get_distance(truck.current_location, "HUB")
            truck.mileage += distance
            travel_time = distance  / 18
            truck.current_time += timedelta(hours=travel_time)
            truck.return_time = truck.current_time
            break
        
        #Find the next address and distance using our helper and trucks current location
        next_address, distance = find_nearest_address(truck, distance_table, undelivered)

        #Update truck mileage
        truck.mileage += distance

        #Update truck time
        travel_time = distance / 18
        truck.current_time += timedelta(hours=travel_time)

        #Deliver package and update package details
        for package in truck.packages:
            if package.address == next_address and package.status != "Delivered":
                package.status = "Delivered"
                package.delivery_time = truck.current_time
        
        #Update trucks location
        truck.current_location = next_address

package_table = Hashtable(50)

# Read the package file, iterate through each data value in each row and assign it.
with open("data/WGUPS Package File.csv", mode="r") as file:
    csv_reader = csv.reader(file)
    
    for row in csv_reader:
        #check if the first data value is a digit(package id) to bypass all potential headings and titles.
        if not row[0].isdigit():
            continue

        package_id = int(row[0])
        address = normalize_address(row[1].strip())
        city = row[2].strip()
        state = row[3].strip()
        zip_code = row[4].strip()
        deadline = row[5].strip()
        weight = int(row[6])
        notes = row[7].strip()
        
        #Create package object and insert it into the hash table using the key.
        package = Package(package_id, address, city, state, zip_code, deadline, weight, notes)
        package_table.insert(package.package_id, package)

#Create an object of the distance class, and iterate through the distance file
distance_table = Distance()

with open("data/WGUPS Distance Table.csv", mode="r") as file:
    csv_reader = csv.reader(file)

    #Skip the first 8 rows for headers and titles
    for _ in range(8):
        next(csv_reader)

    #for each row, extract each address and distance value and add it to the distance matrix
    for row in csv_reader:
        address = normalize_address(row[1].split("\n")[0].strip())
        distance_row = row[2:]

        distance_table.add_address(address)
        distance_table.add_distance_row(distance_row)
#Create truck 1 & 2 objects with departure times
truck1 = Truck(1, timedelta(hours=8))
truck2 = Truck(2, timedelta(hours=8))

#Assign packages
truck1_ids = [1, 2, 4, 7, 13, 14, 15, 16, 19, 20, 21, 29, 33, 34, 39, 40]
truck2_ids = [3, 5, 8, 10, 18, 30, 36, 37, 38]
truck3_ids = [6, 9, 11, 12, 17, 22, 23, 24, 25, 26, 27, 28, 31, 32, 35]

#Add packages to each truck
for package_id in truck1_ids:
    package = package_table.lookup(package_id)
    truck1.add_package(package)

for package_id in truck2_ids:
    package = package_table.lookup(package_id)
    truck2.add_package(package)

#Simulate delivery for Trucks 1 & 2
deliver_truck(truck1, distance_table)
deliver_truck(truck2, distance_table)

#Calculate the time a driver is available and its at least 9:05 am for truck 3 departure time with delayed packages
if truck1.return_time < truck2.return_time:
    if truck1.return_time < timedelta(hours=9, minutes=5):
        truck3_departure_time = timedelta(hours=9, minutes=5)
    else:
        truck3_departure_time = truck1.return_time
else:
    if truck2.return_time < timedelta(hours=9, minutes=5):
        truck3_departure_time = timedelta(hours=9, minutes=5)
    else:
        truck3_departure_time = truck2.return_time

#Create truck 3 object, add the packages, simulate delivery
truck3 = Truck(3, truck3_departure_time)

for package_id in truck3_ids:
    package = package_table.lookup(package_id)
    truck3.add_package(package)

deliver_truck(truck3, distance_table)

trucks = {
    1: truck1,
    2: truck2,
    3: truck3
}

main_menu(trucks, package_table)