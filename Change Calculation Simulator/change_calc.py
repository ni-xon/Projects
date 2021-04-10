import random
import math

while True:
    price = round(random.uniform(0.05, 100.00),2)

    paid = random.randrange(math.ceil(price), 100, 5)

    change = str(round(paid - price, 2))

    print(f"Price: {price}\nPaid: {paid}")

    correct = False

    while not correct:
        answer = input("What is the correct change? (q to quit)")

        if answer == 'q':
            quit()

        if answer == change:
            print("Correct\n")
            correct = True

        else:
            print("Incorrect")

## Project addons:
# Mimic Real life change, so 1 cent 2 cent differences should be ignored, only entering what you should give to customer.
