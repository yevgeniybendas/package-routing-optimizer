#Student ID: 001031254

from package import Package
from hashtable import Hashtable

package_table = Hashtable(50)

p1 =Package(1, "5010 s mullen st", "Tacoma", "WA", "98409", "10:30 AM", 2, "")
p2 = Package(2, "5000 s mullen st", "Tacoma", "WA", "98409", "EOD", 2, "")

package_table.insert(p1.package_id, p1)
package_table.insert(p2.package_id, p2)

found_package = package_table.lookup(2)
print(found_package)

all_packages = package_table.get_all_values()
for package in all_packages:
    print(package)

print(len(package_table.get_all_values()))