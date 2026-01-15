# task - create a list of users, iterate and filter, store unique role using set

users = [ 
    {"name": "kuldeep", "email": "kuldeep@test.com", "age": 30, "role": "Dev" },
    {"name": "Amit", "email": "Amit@test.com", "age": 32, "role": "Dev" },
    {"name": "Sumit", "email": "Sumit@test.com", "age": 35, "role": "QA" },
    {"name": "Anil", "email": "Anil@test.com", "age": 38, "role": "BA" }
]


def get_unique_roles(users):
    roles = set()
    for user in users:
        role = user.get("role")
        if role:
            roles.add(role)
    return roles


def users_by_role(users, target_role):
    result = []
    for user in users:
        if user.get("role") == target_role:
            result.append(user)
    return result


if __name__ == "__main__":
    unique_roles = get_unique_roles(users)
    print("Unique roles:", unique_roles)
    print("Count:", len(unique_roles))

    devs = users_by_role(users, "Dev")
    print("Dev users:", devs)
    print("Dev count:", len(devs))
