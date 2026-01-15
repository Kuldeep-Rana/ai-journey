# write a function to add two numbers
# write a function to find factorial

def sum(a , b):
    print (f"sum is {a+b}")    


def factorial(num):
    result = 1
    while num > 0:
        result = result * num
        num -= 1
    return result

if __name__ == "__main__":
    sum(10,20)
    print(f"factorial is {factorial(5)}")