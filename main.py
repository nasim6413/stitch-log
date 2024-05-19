import re
from database import *
from config import DB_CONFIG
   
# Initialising connection
print('STITCH TRACKER')

floss = Database(DB_CONFIG)
user_input = ''

# Main loop
while user_input != 'exit':
    user_input = input('ENTER ACTION: ')
    
    if user_input == 'list':
        action = floss.flist()
        if action:
            print('Current stock:')
            for item in action:
                print(f'{item[0]} | {item[1]}')
        else:
            print('Stock empty.')

    if user_input == 'count':
        fcount = floss.stock_count()
        print(f'Currently {fcount} floss in stock.')

    # Checks for command
    pattern = r'(\w+)\s*(DMC|Anchor)\s*(\d{1,4}|B5200|ECRU|BLANC|White)'
    match = re.match(pattern, user_input, re.IGNORECASE)

    if match:      
        comm, brand, fno = re_input(match)
        
        # Commands
        if comm == 'search':
            if not floss.input_validation(brand, fno):
                print('Invalid input.')
                
            else:
                action = floss.search(brand, fno)
                
                if action:
                    print('Match found:')
                    for r in action:
                        print(f'{r[0]} {r[1]} | {r[2]} | {r[3]}')
                        
                else:
                    print('No available stock.')
                    print('Checking for possible conversions...')
                    
                    action = floss.convert_stock(brand, fno)
                    
                    if action:
                        print('Available conversions:')
                        for r in action:
                            print(f'DMC {r[0]} -> Anchor {r[1]} | {r[2]}')
                
                    else:
                        print('No available conversions.')

        if comm == 'add':
            if not floss.input_validation(brand, fno):
                print('Not a valid input.')
                
            else:
                action = floss.add(brand, fno)
                
                if action:
                    print('Entry added successfully.')
                    
                else:
                    print('Entry already in database.')
            
        if comm == 'del':
            if not floss.input_validation(brand, fno):
                print('Invalid input.')
            
            else:
                action = floss.delete(brand, fno)
                if action:
                    print('Entry deleted successfully.')
                else:
                    print('Entry not in database.')

        if comm == 'convert':
            if not floss.input_validation(brand, fno):
                print('Invalid input.')
                
            else:
                action = floss.convert(brand, fno)
                
                if action:
                    print('Possible conversion(s):')
                    for r in action:
                        print(f'DMC {r[0]} -> Anchor {r[1]} | {r[2]}')
                        
                else:
                    print('No possible conversions.')

# Closing application
try:
    floss.disconnect()
    print('Connection closed successfully.')
    
    print('Exiting application.')
    
except:
    print('Connection unable to close.')