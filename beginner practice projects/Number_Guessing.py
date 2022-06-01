import random
import sys

"""
Just a random number guess game
with random function and interactive inputs
"""

run_game = True
times = 0

print('-' * 15, 'Welcome', '-' * 15)

name = input("tell me your name pls? (Optional): ")

if len(name) <= 0:
    name = 'anonymous'

while run_game:
    times += 1
    print('guess a number in between 1 to 9:')
    number = input("> ")
    secret_number = random.randint(0, 10)
    if int(number) == secret_number:
        print("you got it!", name, "you took",
              times, ' guesses, to find that number')
        times = 0
        print("want to play one more time? (yes or no)")
        think = input("> ")
        if think.lower() in ['y', 'yes', 'yup!']:
            print('ok')
        else:
            break
    else:
        print("that's a wrong number", name)
        print("want to play one more time? (yes or no)")
        think = input("> ")
        if think.lower() in ['y', 'yes', 'yup!']:
            print('ok')
        else:
            break

sys.exit('Have fun')
