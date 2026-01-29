import csv
from datetime import datetime, timedelta

# I added code to print the reminder of days left till new year sales. I also added 
# code to print 'return by' date, which is due 30 days from current day (lines 56-59).
# I decided to use constant variables and although some of them have the same value, 
# I still chose to give them separate variables for better readability.

KEY_INDEX = 0
INAME_INDEX = 1     # INAME for item name
IPRICE_INDEX = 2    # IPRICE for item price
PN_INDEX = 0        # PN for product number in the request.csv file
QUANTITY_INDEX = 1
STORE_NAME = 'ROBERT STORES'

def main():
    try:
        products_dict = read_dictionary('products.csv', KEY_INDEX)

        #print(products_dict)   <—— I added this line to fulfil the milestone requirements.
                                  # But I'm commenting it out as required in the final submission,
                                  # because I completed the program the same day, and intend to submit
                                  # this same version for the milestone and final submission. 

        total_quantity = 0
        subtotal = 0
        current_date = datetime.now().strftime('%a %b %d  %H:%M:%S %Y')

        print(f'-:::::::- {STORE_NAME} -:::::::-')
        print()

        with open('request.csv', 'rt') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)

            for row in reader:
                prod_num = row[PN_INDEX]
                prod_info = products_dict[prod_num]
                quantity = int(row[QUANTITY_INDEX])
                total_quantity += quantity
                price = float(prod_info[IPRICE_INDEX])

                subtotal += price * quantity
                tax = (subtotal * 6) / 100
                total = subtotal + tax

                print(f'{prod_info[INAME_INDEX]}: {quantity} @ {prod_info[IPRICE_INDEX]}')
        
    except FileNotFoundError as e:
        print(f'Error: missing file\n{e}')
    except PermissionError:
        print('Error: permission denied')
    except KeyError as e:
        print(f'Error: unknown product ID in the request.csv file {e}')

    today = datetime.now()
    return_by = (today + timedelta(days= 30)).replace(hour= 21, minute=0, second=0).strftime('%b %d, %Y  %I:%M %p')
    new_year = datetime(2027, 1, 1)
    days_left = (new_year - today).days


    print(f'Number of items: {total_quantity}')
    print(f'Subtotal: {subtotal:.2f}')
    print(f'Sales Tax: {tax:.2f}')
    print(f'Total: {total:.2f}')
    print(f'Thank you for shopping at {STORE_NAME}.')
    print(current_date)
    print(f'Return by {return_by}')
    print(f'\n🌲 New Year Sales countdown. 🌲\nStarts in Jan 1, "{days_left}" days left! 🎁\n')

def read_dictionary(filename, key_column_index):
    products_dict = {}

    with open(filename, 'rt') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        for row in reader:
            if len(row) != 0:
                key = row[key_column_index]
                products_dict[key] = row

    return products_dict

if __name__ == '__main__':
    main()