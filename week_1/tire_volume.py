''' I added an input to ask if the user wants to purchase the tire with the entered dimensions (lines 17-28) 
and while loop to repeat the input until a valid respose is entered.If the yes, the user is asked for a phone number.
Then the number is added to the volumes.txt file (lines 31-32) and the loop breaks. If no, a goodbye message is printed. and the loop breaks. '''

from datetime import datetime
import math

print()

width = int(input('Enter the width of the tire in mm (ex 205): '))
ratio = int(input('Enter the aspect ratio of the tire (ex 60): '))
diameter = int(input('Enter the diameter of the wheel in inches (ex 15): '))

volume = math.pi * (width ** 2) * ratio * (width * ratio + 2540 * diameter) / 10_000_000_000

print(f'The approximate volume is {volume:.2f} liters')

while True:
    purchase_tire = input('\nDo you want to buy tires with the specified dimensions? (yes/no): ')

    if purchase_tire.lower() == 'yes'.lower():
        phone_number = input('Enter phone number: ')
        print('Thank you for patronising us. Goodbye.')
        break
    elif purchase_tire.lower() == 'no'.lower():
        print('Thank you for checking in with us. Goodbye.')
        break
    else:
        print('Input a valid response (yes/no)')

with open('volumes.txt', 'at') as file:
    if purchase_tire.lower() == 'yes'.lower():
        file.write(f'{datetime.now().date()}, {width}, {ratio}, {diameter}, {volume:.2f}, {phone_number}\n')
    else:
        file.write(f'{datetime.now().date()}, {width}, {ratio}, {diameter}, {volume:.2f}\n')

print()