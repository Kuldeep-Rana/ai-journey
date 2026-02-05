#User Data Processor – v4 
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

# def unique_roles(users):
#     return {user['role'] for user in users}


# def group_users_by_email(users):
#     role_map = {}
#     for user in users:
#         email = user["email"]
#         role_map.setdefault(email, []).append(user)
#     return role_map  


def find_user_by_email(users, email):
    for user in users:
        u_email = user["email"]
        if u_email == email:
            return user
        else:
            "None"
            
def sort_users(users, by="age", order="asc"):
    reverse = order == "desc"
    return sorted(users, key=lambda u: u.get(by), reverse=reverse)

def get_top_n_oldest_users(users, n):
    return  users[:n]

import json

def generate_summary(users):
    ages = [u["age"] for u in users]
    roles = {}

    for u in users:
        role = u["role"]
        roles[role] = roles.get(role, 0) + 1

    return {
        "total_users": len(users),
        "roles": roles,
        "age_stats": {
            "min": min(ages),
            "max": max(ages),
            "average": round(sum(ages) / len(ages), 2)
        }
    }


def write_summary_json(summary, path):
    with open(path, "w") as f:
        json.dump(summary, f, indent=2)

    

if __name__ == "__main__":
    users = load_users("day5//users.txt")
    oldest_user = sort_users(users, by="age", order="desc")
    n_users = get_top_n_oldest_users(oldest_user,2)
    summary = generate_summary(users)
    write_summary_json(summary, "day6\\summary.json")