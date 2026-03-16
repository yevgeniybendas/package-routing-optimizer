#Create the hashtable to store the package data
class Hashtable:
    def __init__(self, size):
        #Store the table size
        self.size = size

        #Create the table
        self.table = []

        #Ceate buckets for collision handling
        for i in range(size):
            self.table.append([])

    #Create hash function to determine bucket assignment
    def hash_function(self, key):
        return key % self.size
    
    #Determine the bucket index and then grab the actual bucket to insert a package
    def insert(self, key, value):
        bucket_index = self.hash_function(key)
        bucket = self.table[bucket_index]
        #Check for an existing key in the bucket and update the value if it exists
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        #If key was not found, add th package    
        bucket.append([key, value])

    #Find the bucket using the key to lookup package data
    def lookup(self, key):
        bucket_index = self.hash_function(key)
        bucket = self.table[bucket_index]

        #Check if package exists and return values, otherwise return None
        for pair in bucket:
            if pair[0] == key:
                return pair[1]
            
        return None
    
    #Return all packages to later return all values in the packages for reporting
    def get_all_values(self):
        values = []

        #iterate through every pair in every bucket and add the package object to the values list
        for bucket in self.table:
            for pair in bucket:
                values.append(pair[1])
        
        return values