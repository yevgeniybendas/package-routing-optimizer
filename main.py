#Student ID: 001031254

import csv
from datetime import timedelta

from package import Package
from hashtable import Hashtable
from distance import Distance
from truck import Truck

package_table = Hashtable(50)

# Read the package file, iterate through each data value in each row and assign it.
with open("data/WGUPS Package File.csv", mode="r") as file:
    csv_reader = csv.reader(file)
    
    for row in csv_reader:
        #check if the first data value is a digit(package id) to bypass all potential headings and titles.
        if not row[0].isdigit():
            continue

        package_id = int(row[0])
        address = row[1].strip()
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
        address = row[1].split("\n")[0].strip()
        distance_row = row[2:]

        distance_table.add_address(address)
        distance_table.add_distance_row(distance_row)

truck1 = Truck(1, timedelta(hours=8))
truck2 = Truck(2, timedelta(hours=8))
truck3 = Truck(3, timedelta(hours=8))

truck1_ids = [1, 2, 4, 7, 13, 14, 15, 16, 19, 20, 21, 29, 33, 34, 39, 40]
truck2_ids = [3, 5, 8, 10, 18, 30, 36, 37, 38]
truck3_ids = [6, 9, 11, 12, 17, 22, 23, 24, 25, 26, 27, 28, 31, 32, 35]

for package_id in truck1_ids:
    package = package_table.lookup(package_id)
    truck1.add_package(package)

for package_id in truck2_ids:
    package = package_table.lookup(package_id)
    truck2.add_package(package)

for package_id in truck3_ids:
    package = package_table.lookup(package_id)
    truck3.add_package(package)

print(truck1)
print(truck2)
print(truck3)

for package in truck1.packages:
    print(package.package_id, package.truck_id)