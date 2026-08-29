# User Data Processor – v3

roles = set()

def load_users(path):
    users = [] 
    
    with open(path) as file_obj:
     for line in file_obj.read().splitlines():
            try: 
                name, email, age, role = fields = line.split(",") 
                users.append({ "name": name.strip(), "email": email.strip(), "age": int(age), "role": role.strip() }) 
            except ValueError:
                print(f"Invalid age in row {line}")
            except Exception as e:
                print(f"Error in row {line}: {e}")

    return users     

def unique_roles(users):
    return {user['role'] for user in users}


def group_users_by_role(users):
    role_map = {}
    for user in users:
        role = user["role"]
        role_map.setdefault(role, []).append(user)
    return role_map  
                     

def calculate_statistics(grouped_users):
    role_stats = {}
    all_ages = []

    for role, users in grouped_users.items():
        ages = [u["age"] for u in users]
        all_ages.extend(ages)

        role_stats[role] = {
            "count": len(ages),
            "min_age": min(ages),
            "max_age": max(ages),
            "avg_age": round(sum(ages) / len(ages), 2)
        }

    overall_stats = {
        "total_users": len(all_ages),
        "min_age": min(all_ages),
        "max_age": max(all_ages),
        "avg_age": round(sum(all_ages) / len(all_ages), 2)
    }

    return {
        "per_role": role_stats,
        "overall": overall_stats
    }
 

def write_summary_csv(stats, path):
    with open(path, "w") as f:
        f.write("role,count,min_age,max_age,avg_age\n")
        for role, data in stats["per_role"].items():
            f.write(f"{role},{data['count']},{data['min_age']},{data['max_age']},{data['avg_age']}\n")
                        

if __name__ == "__main__":
    users = load_users("day5//users.txt")
    unique_roles(users)
    users_by_group = group_users_by_role(users)
    stats = calculate_statistics(users_by_group)
    write_summary_csv(stats, "day5\\summary.csv")
    
 