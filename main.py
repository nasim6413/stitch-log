from database import *
from config import DB_CONFIG

# Initialising connection
floss = Database(DB_CONFIG)

print('STITCH TRACKER v0')
user_input = ''

# Main loop
while user_input != 'exit':
    user_input = input('ENTER ACTION: ')
    comm = user_input.split(' ')[0]
    
    if comm == 'list':
        act = floss.flist()
        if act:
            print('Current stock:')
            for item in act:
                print(f'{item[0]} | {item[1]}')
        else:
            print('Stock empty.')

    if comm == 'count':
        fcount = floss.stock_count()
        print(f'Currently {fcount} floss in stock.')

    if comm == 'search':
        brand, fno = user_input.split(' ')[1], user_input.split(' ')[2]
        if not floss.input_validation(brand, fno):
            print('Invalid input.')
            
        else:
            act = floss.search(brand, fno)
            
            if act:
                print('Match found:')
                for r in act:
                    print(f'{r[0]} {r[1]} | {r[2]} | {r[3]}')
                    
            else:
                print('No available stock.')
                print('Checking for possible conversions...')
                
                act = floss.convert_stock(brand, fno)
                
                if act:
                    print('Available conversions:')
                    for r in act:
                        print(f'DMC {r[0]} -> Anchor {r[1]} | {r[2]}')
            
                else:
                    print('No available conversions.')

    if comm == 'add':
        brand, fno = user_input.split(' ')[1], user_input.split(' ')[2]
        if not floss.input_validation(brand, fno):
            print('Not a valid input.')
            
        else:
            act = floss.add(brand, fno)
            
            if act:
                print('Entry added successfully.')
                
            else:
                print('Entry already in database.')
        
    if comm == 'del':
        brand, fno = user_input.split(' ')[1], user_input.split(' ')[2]
        if not floss.input_validation(brand, fno):
            print('Invalid input.')
        
        else:
            act = floss.delete(brand, fno)
            if act:
                print('Entry deleted successfully.')
            else:
                print('Entry not in database.')

    if comm == 'convert':
        brand, fno = user_input.split(' ')[1], user_input.split(' ')[2]
        if not floss.input_validation(brand, fno):
            print('Invalid input.')
            
        else:
            act = floss.convert(brand, fno)
            
            if act:
                print('Possible conversion(s):')
                for r in act:
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