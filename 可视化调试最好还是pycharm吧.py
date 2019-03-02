
# coding: utf-8
import random
guess = ''
toss={0:'heads',1:'tails'}
while guess not in ('heads', 'tails'):
    guess = input('Guess the coin toss! Enter heads or tails:\n')
tossvalue = toss[random.randint(0, 1)] # 0 is tails, 1 is heads
if tossvalue == guess:
    print('You got it!') 
else:
    print('Nope! Guess again!') 
    guess = input()
    if tossvalue == guess:
        print('You got it!') 
    else: 
        print('Nope. You are really bad at this game.')

