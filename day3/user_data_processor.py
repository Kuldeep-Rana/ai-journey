#User Data Processor – v1


def load_users(file_path):
    with open(file_path) as file_obj:
        users = file_obj.read().splitlines()
        return users

def get_unique_roles(users):
    roles = set()
    for user in users:
        fields = user.split(",")
        roles.add(fields[-1])
    return roles    

def filter_users_by_role(users, role):
    filtered_uers = []
    for user in users:
        fields = user.split(",")
        if fields[-1] == role:
            filtered_uers.append(user)
    return filtered_uers

def average_age(users):
    total_age = 0
    for user in users:
         total_age += int(user.split(",")[2])
    return total_age / len(users)    

def count_per_role(users, roles):
    role_summaries = []
    for role in roles:
        user_by_role = filter_users_by_role(users, role)
        d = {}
        d["role"] = role
        d["count"] = len(user_by_role)
        role_summaries.append(d)
    return role_summaries   
#total users
#unique roles
#average age
#Count per role
def generate_summary(users):
    print(f"total users {len(users)}")
    print(f"unique roles {get_unique_roles(users)}")
    print(f"average age {average_age(users)}")
    print(f"count per role {count_per_role(users,get_unique_roles(users))}")


if __name__ == "__main__":
    users = load_users("day3//users.txt")
    generate_summary(users)
    print(filter_users_by_role(users, "Dev"))


