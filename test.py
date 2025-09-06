import random
ids = [1,2,3,5,6,7,8,9]

while True:
    id = random.randint(0,10)
    valid = False
    while valid == False:
        valid = True
        for num in ids:
            if num == id:
                valid = False
                id = random.randint(0,10)
    if id in ids:
        print("failed")
    else:
        print(id)