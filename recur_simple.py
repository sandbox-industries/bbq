number = 0

def count_up():
    global number
    if number != 10:
        number += 1
        count_up()
    return
    
print(number)
count_up()
print(number)