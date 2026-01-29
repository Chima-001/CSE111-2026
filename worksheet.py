#-------------------------------------Fuel Efficiency--------------------------------------------
'''def main():
    start = float(input('Enter first odometer reading (miles): '))
    end = float(input('Enter second odometer reading (miles): '))
    gallons = float(input('Enter amount of fuel used (gallons): '))

    mpg = miles_per_gallon(start, end, gallons)
    lp100k = lp100k_from_mpg(mpg)

    print(f'{mpg:.1f} miles per gallon')
    print(f'{lp100k:.2f} liters per 100 kilometers')

def miles_per_gallon(start_miles, end_miles, amount_gallons):
    mpg = abs(end_miles - start_miles) / amount_gallons
    return mpg

def lp100k_from_mpg(mpg):
    lp100k = 235.215 / mpg
    return lp100k

main()'''

#-------------------------------------Cone Volume--------------------------------------------

'''import math

def main():
    ex_radius = 2.8
    ex_height = 3.2
    ex_vol = cone_volume(ex_radius, ex_height)

    print('This program computes the volume of a right circular cone. For example, if the radius of a')
    print(f'cone is {ex_radius} and the height is {ex_height}, then the volume is {ex_vol:.1f}')
    print()

    radius = float(input('Please enter the radius of the cone: '))
    height = float(input('Please enter the height of the cone: '))

    vol = cone_volume(radius, height)

    print(f'Radius: {radius}')
    print(f'Height: {height}')
    print(f'Volume: {vol:.1f}')

def cone_volume(radius, height):
    volume = math.pi * radius**2 * height / 3
    return volume

main()'''


#------------------------------------- Testing Functions--------------------------------------------
