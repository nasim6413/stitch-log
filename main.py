import re
from database import *
from config import DB_CONFIG
from rich.prompt import Console, Prompt
from rich.table import Table
   
# Initialising connection
user_input = ''

console = Console()
console.print('STITCH TRACKER', style='indian_red')

try:
    floss = Database(DB_CONFIG)
    console.print('Connection established successfully.', style='bold')
except:
    console.print('[red]ERROR:[/red] Cannot establish connection.')

# Main loop
while True:
    user_input = Prompt.ask('[bold]ENTER ACTION[/bold]')
    
    if user_input == 'list':
        action = floss.flist()
        if action:
            stock_list = Table(title='Current stock')
            
            stock_list.add_column('Brand', justify='center')
            stock_list.add_column('Number', justify='center')
            
            for item in action:
                stock_list.add_row(item[0], item[1])
                
            console.print(stock_list)
            
        else:
            console.print('[red]ERROR:[/red] Stock empty.')

    if user_input == 'count':
        fcount = floss.stock_count()
        print(f'Currently {fcount} floss in stock.')

    # Checks for command
    pattern = r'(\w+)\s*(DMC|Anchor)\s*(\w?\d{1,4}|B5200|ECRU|White)'
    match = re.match(pattern, user_input, re.IGNORECASE)

    if match:      
        comm, brand, fno = re_input(match)
        
        # Commands
        if comm == 'search':
            action = floss.search(brand, fno)
            
            if action:
                console.print(f'Match found! [green]{brand} {fno}[/green] available in database.', highlight=False)
                    
            else:
                console.print(f'[red]ERROR[/red]: [red]{brand} {fno}[/red] is not in the available stock.', highlight=False)
                print('Checking for possible conversions...')
                
                action = floss.convert_stock(brand, fno)
                
                if action:
                    conv_table = Table(title='Available conversions')
                    
                    conv_table.add_column('DMC', justify='center')
                    conv_table.add_column('Anchor', justify='center')
                    conv_table.add_column('Hex', justify='center')

                    for item in action:
                        colour = f'#{item[2]}'
                        conv_table.add_row(item[0], item[1], f'[{colour}]{item[2]}[/{colour}]')

                    console.print(conv_table)
                else:
                    print('No available conversions.')

        if comm == 'add':
            action = floss.add(brand, fno)
            
            if action:
                console.print(f'Entry [green1]{brand} {fno}[/green1] added successfully.', highlight=False)
                
            else:
                console.print(f'Entry [dark_orange]{brand} {fno}[/dark_orange] already in database.', highlight=False)
            
        if comm == 'del':
            action = floss.delete(brand, fno)
            if action:
                console.print(f'Entry [red1]{brand} {fno}[/red1] deleted successfully.', highlight=False)
            else:
                console.print(f'Entry [dark_orange]{brand} {fno}[/dark_orange] not in database.', highlight=False)

        if comm == 'convert':
            action = floss.convert(brand, fno)
            
            if action:                     
                conv_table = Table(title='Possible conversions')
                conv_table.add_column('DMC', justify='center')
                conv_table.add_column('Anchor', justify='center')
                conv_table.add_column('Hex', justify='center')

                for item in action:
                    colour = f'#{item[2]}'
                    conv_table.add_row(item[0], item[1], f'[{colour}]{item[2]}[/{colour}]')

                console.print(conv_table)
                    
            else:
                print('No possible conversions.')
                
    if user_input == 'exit':
        break

# Closing application
try:
    floss.disconnect()
    console.print('Connection closed successfully.', style='bold')

    console.print('Exiting application.', style='bold')
    
except:
    console.print('[red]ERROR:[/red] Connection unable to close.')