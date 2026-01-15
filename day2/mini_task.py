# task - create a list of users, iterate and filter, store unique role using set

users = [ 
    {"name": "kuldeep", "email": "kuldeep@test.com", "age": 30, "role": "Dev" },
    {"name": "Amit", "email": "Amit@test.com", "age": 32, "role": "Dev" },
    {"name": "Sumit", "email": "Sumit@test.com", "age": 35, "role": "QA" },
    {"name": "Anil", "email": "Anil@test.com", "age": 38, "role": "BA" }
]


# Using set to collect unique roles
def countUniqueRole():
    roles = set()
    for user in users:
           roles.add(user["role"])
    return roles.__len__();       

def userByGivenRole(role):
    usersByRoles = []
    for user in users:
           if user["role"] == role:
               usersByRoles.append(user)
    return usersByRoles.__len__()
            

if __name__ == "__main__":
    print(f"count of unique roles are {countUniqueRole()} \n")
    print(f"User by role Dev are {userByGivenRole("Dev")} \n")            
    print(f"User by role QA are {userByGivenRole("QA")} \n")            