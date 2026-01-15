#Dicts in python

# Creating a dictionary
user = {"name": "Alice", "age": 25, "role": "Dev"}

# Accessing values
print(user["name"])          
print(user.get("email", "N/A")) # Returns "N/A" if key doesn't exist (prevents errors)

# Adding/Updating
user["email"] = "alice@example.com" # Adds a new pair
user["age"] = 26                    # Updates existing key

# Removing items
del user["role"]             # Removes 'role'
last_item = user.popitem()   # Removes and returns the last inserted pair

print(last_item)

print("=======================================")

for k in user.keys():
    print(k)
    

for v in user.values():
    print(v)   
    
 
for i in user.items():
    print(i)
    
    
 # Set in python

# Sets store unique and unordered 

nums = [1,2,3,4,5,5,6]
print(nums)

uniques = set(nums)
print(uniques)   


# emtpy set

alphabets = set()
alphabets.add('a')
alphabets.add('a')
alphabets.add('b')
alphabets.add('c')
alphabets.add('b')
print(alphabets)
alphabets.remove('b')
print(alphabets)
