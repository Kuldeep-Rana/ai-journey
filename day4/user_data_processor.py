#Task Name: User Data Processor – v2
def load_users(path): 
    users = [] 
    with open(path) as file_obj: 
        for line in file_obj.read().splitlines():
            fields = line.split(",") 
            try: 
                if len(fields) == 4: 
                    name, email, age, role = fields 
                    users.append({ "name": name, "email": email, "age": age, "role": role }) 
            except: print(f"Error in row {line}") 
        return users 

def get_unique_roles(users): 
    roles = set() 
    for user in users: 
        roles.add(user['role']) 
    return roles 

def filter_users_by_role(users, role): 
    filtered_uers = [] 
    for user in users: 
        user_role = user['role'] 
        if user_role == role: 
            filtered_uers.append(user)
    return filtered_uers 
    
def average_age(users):
    total_age = 0 
    for user in users: 
        total_age += int(user["age"])
    return total_age / len(users)

def average_age_by_role(users): 
    roles = get_unique_roles(users)
    avg_age_by_role = [] 
    for role in roles:
        user_by_role = filter_users_by_role(users, role) 
        data = {} 
        data["role"] = role 
        data["avg age"] = average_age(user_by_role) 
        avg_age_by_role.append(data) 
    return avg_age_by_role 

def count_per_role(users):
    roles = get_unique_roles(users)
    users_counts = [] 
    for role in roles: 
        user_by_role = len(filter_users_by_role(users, role)) 
        data = {} 
        data["role"] = role 
        data["count"] = user_by_role 
        users_counts.append(data) 
        
        sorted_data = sorted(users_counts, key=lambda x: x['count']) 
    return sorted_data 

def generate_summary(users):
    total_user = len(users) 
    unique_roles = get_unique_roles(users)
    average_age_by_r = average_age_by_role(users)
    
    with open("day4//summary.txt", "w") as file_obj:
        file_obj.write(f"total users - {total_user} \n") 
        file_obj.write(f"unique roles - {unique_roles}\n") 
        file_obj.write(f"average age by role - {average_age_by_r}\n")
        file_obj.write(f"count per role {count_per_role(users)}\n")
        file_obj.write(f"average age per role {average_age_by_r}")
        
        
if __name__ == "__main__":
    users = load_users("day4//users.txt")
    print(users)
    generate_summary(users)