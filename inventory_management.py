from datetime import datetime
from copy import deepcopy

################################################################################
##      Fundamental operations
################################################################################

##      Dictionary to hold inventory and balances

INVENTORY = {}
PURCHASE_ORDER = {}
RETURN_ORDER = {}
ORDER_LOG = {}
TRANSACTION_NUM = 0
TILL_BALANCE = 500.00
ITEMS_IN_STOCK = 0
STOCK_VALUE = 0.00

##      Methods to request info

def get_item_name():
    return input('Enter item name: ')

def get_qty():
    return int(input('Enter item quantity: '))

def get_price():
    return float(input('Enter item price: '))

##       Update history

def update_order_log(trans_type, total_items, trans_total, details):
    global TRANSACTION_NUM
    TRANSACTION_NUM += 1
    now = datetime.now()
    formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
    ORDER_LOG[TRANSACTION_NUM] = {
        'Date/Time' : formatted_time,
        'Transaction Type' : trans_type,
        'Total items' : total_items,
        'Transaction total $' : trans_total,
        'Transaction details' : details
    }

##       Calculators

def sync_data():
    global ITEMS_IN_STOCK, STOCK_VALUE
    tmp_items_in_stock = 0
    tmp_stock_value = 0.00
    for item in INVENTORY.values():
       tmp_items_in_stock += item['Quantity']
       tmp_stock_value += item['Price'] * item['Quantity']
    ITEMS_IN_STOCK = tmp_items_in_stock
    STOCK_VALUE = tmp_stock_value

##       Printers

def print_dict(dict):
    for key, value in dict.items():
        if isinstance(value, float):
            print(f'{key}: ${value:,.2f}')
        else:
            print(f'{key}: {value}')

def order_printer(dict):
    for key, value in dict.items():
        print(f'    ---< {key} >---Item: {value['Item name']} | Quantity: {value['Quantity']} | Price: {value['Price']}')

##      Create dictionary out of values

def make_dict(name, qty, price):
    return {"Item name": name, "Quantity": qty, "Price": price}

##      Search fuctions

def view_and_select_item(dict):
    for index, (key, value) in enumerate(dict.items(), 1):
        print(f'---< {index} >---Item: {value['Item name']} | Quantity: {value['Quantity']} | Price: {value['Price']}')
    selection = int(input('\nEnter selection: '))
    if 1 <= selection <= len(dict):
        selection_key = list(dict.keys())[selection - 1]
        return deepcopy(dict[selection_key])
    else:
            print('\n...Invalid selection...\n')

def add_to_order(dict):
    selection_copy = view_and_select_item(INVENTORY)
    if selection_copy:
        qty = int(input('Enter quantity: '))
        if qty <= selection_copy['Quantity']:
            selection_copy['Quantity'] = qty                    
            dict[selection_copy['Item name']] = selection_copy    
            print('\n< Success! >\n')
        else:
            print('\n...Invalid quantity...\n')

################################################################################
##      1. Purchase function
################################################################################

def add_to_po():
    print('''
    <  Add item to cart  >
          ''')
    add_to_order(PURCHASE_ORDER)

def remove_from_po():
    print('''
    < Select an item to remove >
          ''')
    
    selection_copy = view_and_select_item(PURCHASE_ORDER)
    
    if not selection_copy:
        return
    
    del PURCHASE_ORDER[selection_copy['Item name']]
    print('\n< Success! >\n')

def update_po_qty():
    print('''
    < Select an item to update >
          ''')
    
    selection_copy = view_and_select_item(PURCHASE_ORDER)
    
    if not selection_copy:
        return

    qty = int(input('< Enter updated quantity: '))
    if qty <= INVENTORY[selection_copy['Item name']]['Quantity']:
        PURCHASE_ORDER[selection_copy['Item name']]['Quantity'] = qty
        print('\n< Success! >\n')
    else:
        print('\n...Invalid quantity...\n')

def view_purchase():
    if PURCHASE_ORDER:
        print('\n< Purchase order:\n')
        order_printer(PURCHASE_ORDER)
    else:
        print('\n...EMPTY purchase order...\n')

def complete_po():
    global TILL_BALANCE
    print('\n< Purchase Receipt >')
    total_cost = 0.00
    for key, value in PURCHASE_ORDER.items():
        item_cost = value['Quantity'] * value['Price']
        total_cost += item_cost
        INVENTORY[key]['Quantity'] -= value['Quantity']
        print(f'{key} | Quantity: {value['Quantity']} | Cost: ${item_cost:.2f}')
    print(f'\n< Total Purchase:  ${total_cost:.2f}>')
    total_items = len(PURCHASE_ORDER)
    receipt = deepcopy(PURCHASE_ORDER)
    update_order_log('Purchase', total_items, total_cost, receipt)
    TILL_BALANCE += total_cost
    PURCHASE_ORDER.clear()
    sync_data()
    print('''
    < Purchase Completed >
    <      Success!      >
          ''')

def cancel_po():
    if PURCHASE_ORDER:
        PURCHASE_ORDER.clear()
        print('\n...Purchase Canceled...\n< Success! >\n')
    else:
        print('\n...NO PURCHASE ORDER FOUND...\n')

def purchase():
    options = {
        '1': add_to_po,
        '2': remove_from_po,
        '3': update_po_qty,
        '4': view_purchase,
        '5': complete_po,
        '6': cancel_po,
        '7': lambda: None
    }
    while True:
        print('''
Please make a selection from the following:
    < 1 > Add item to purchase order
    < 2 > Remove item from purchase order
    < 3 > Update item quantity
    < 4 > View order
    < 5 > Complete purchase
    < 6 > Cancel purchase
    < 7 > Main menu
        ''')

        selection = input()
        if selection in options:
            options[selection]()
            if selection == '7':
                if PURCHASE_ORDER:
                    confirm = input('\n< WARNING: >\n < OPEN PURCHASE ORDER, Cancel it? (y/n): ').strip().lower()
                    if confirm == 'y':
                        cancel_po()
                    else:
                        continue
                print('...Returning to main menu...\n')
                break
        else:
            print('\n...Invalid selection...\n')
        
################################################################################
##      2. Return purchase
################################################################################

def add_to_return():
    print('''
    <  Add item to return  >
          ''')
    add_to_order(RETURN_ORDER)

def remove_from_return():
    print('''
    < Select an item to remove >
          ''')
    
    selection_copy = view_and_select_item(RETURN_ORDER)
    
    if not selection_copy:
        return
    
    del RETURN_ORDER[selection_copy['Item name']]
    print('\n< Success! >\n')

def update_return_qty():
    print('''
    < Select an item to update >
          ''')
    
    selection_copy = view_and_select_item(RETURN_ORDER)
    
    if not selection_copy:
        return
    qty = int(input('< Enter updated quantity: '))
    RETURN_ORDER[selection_copy['Item name']]['Quantity'] = qty
    print('\n< Success! >\n')

def view_return():
    if RETURN_ORDER:
        print('\n< Return order:\n')
        order_printer(RETURN_ORDER)
    else:
        print('\n...EMPTY return order...\n')

def complete_return():
    global TILL_BALANCE
    print('\n< Return Receipt >')
    total_refund = 0.00
    for key, value in RETURN_ORDER.items():
        item_cost = value['Quantity'] * value['Price']
        total_refund += item_cost
        INVENTORY[key]['Quantity'] += value['Quantity']
        print(f'{key} | Quantity: {value['Quantity']} | Cost: -${item_cost:.2f}')
    print(f'\n< Total Return:  -${total_refund:.2f}>')
    total_items = len(RETURN_ORDER)
    receipt = deepcopy(RETURN_ORDER)
    update_order_log('Return', total_items, total_refund, receipt)
    TILL_BALANCE -= total_refund
    RETURN_ORDER.clear()
    sync_data()
    print('''
    < Return Completed >
    <     Success!     >
          ''')

def cancel_return():
    if RETURN_ORDER:
        RETURN_ORDER.clear()
        print('\n...Return Canceled...\n< Success! >\n')
    else:
        print('\n...NO RETURN ORDER FOUND...\n')

def return_purchase():
    options = {
        '1': add_to_return,
        '2': remove_from_return,
        '3': update_return_qty,
        '4': view_return,
        '5': complete_return,
        '6': cancel_return,
        '7': lambda: None
    }
    while True:
        print('''
Please make a selection from the following:
    < 1 > Add item to return
    < 2 > Remove item from return
    < 3 > Update item return quantity
    < 4 > View order
    < 5 > Complete return
    < 6 > Cancel return
    < 7 > Main menu
        ''')
        selection = input()
        if selection in options:
            options[selection]()
            if selection == '7':
                if RETURN_ORDER:
                    confirm = input('\n< WARNING: >\n < OPEN RETURN ORDER, Cancel it? (y/n): ').strip().lower()
                    if confirm == 'y':
                        cancel_return()
                    else:
                        continue
                print('...Returning to main menu...\n')
                break
        else:
            print('\n...Invalid selection...\n')

################################################################################
##      3. Add item to stock
################################################################################

def add_stock():
    print('\n< Add new item to stock >')

    name = get_item_name()

    if name not in INVENTORY:
        qty = get_qty()
        price = get_price()
        dict = make_dict(name, qty, price)
        INVENTORY[name] = dict
        sync_data()
        print_dict(INVENTORY[name])
        print('\n< Item successfully added to inventory! >\n')

    else:
        print('\n...Item already exists...\n')

        print('Existing stock:')
        print_dict(INVENTORY[name])
        
        print('\nWould you like to update the existing item?\n')
        
        choice = input('1 = yes\nAny key = no: ')

        if choice == '1':
            update_stock_item(INVENTORY[name])
            sync_data()
            print('\n< Success! >\n')
        else:
            print('...Returning to main menu...\n')

################################################################################
##      4. Update item in stock
################################################################################

def modify_stock(old_key, updated_stock):
    if old_key in INVENTORY:
        del INVENTORY[old_key]
    new_key = updated_stock['Item name']
    INVENTORY[new_key] = updated_stock
    
def update_stock_item(item):
    print('\n< Current item details: >\n')
    print_dict(item)

    tmp_item = item.copy()

    options = {
        '1': lambda: tmp_item.update({'Item name': get_item_name()}),
        '2': lambda: tmp_item.update({'Quantity': get_qty()}),
        '3': lambda: tmp_item.update({'Price': get_price()}),
        '4': lambda: print('...Success!...\n'),
        '5': lambda: print('...Returning to main menu...\n')
    }

    while True:
        print('''
    < 1 > Edit Item name
    < 2 > Edit Quantity
    < 3 > Edit Price
    < 4 > Commit Editing
    < 5 > Cancel Editing
        ''')

        selection = input().strip()
        if selection in options:
            options[selection]()
            if selection == '4':
                old_key = item['Item name']
                modify_stock(old_key, tmp_item)
                break
            elif selection == '5':
                break
        else:
            print('\n...Invalid selection...\n')

def update_stock():
    print('''
    <   Select an item   >
    <   Update an item   >
          ''')

    selection_copy = view_and_select_item(INVENTORY)
    
    if not selection_copy:
        return
    
    update_stock_item(selection_copy)
    sync_data()

################################################################################
##      5. Delete item from stock
################################################################################

def delete_stock():
    print('''
    <   Select an item   >
    <   Delete an item   >
          ''')
    
    selection_copy = view_and_select_item(INVENTORY)
    
    if not selection_copy:
        return
    
    del INVENTORY[selection_copy['Item name']]
    print('\n< Success! >\n')
    sync_data()


################################################################################
##      6. View inventory
################################################################################

def items_in_stock():
    print('\n< Items in stock:\n')
    for item in INVENTORY.values():
        print(f'    <  {item['Item name']}')

def items_and_details():
    print('\n< Items in stock and totals:\n')
    for item in INVENTORY.values():
        print(f'    Item: {item['Item name']} | Price: ${item['Price']:.2f} | Quantity in stock: {item['Quantity']} | Total value in stock: ${(item['Price'] * item['Quantity']):.2f}')

def stock_totals():
    print('\n< Stock totals:\n')
    print(f'    Total unique items in stock: {len(INVENTORY)}')
    print(f'    Total units in stock: {ITEMS_IN_STOCK}')
    print(f'    Total stock value: ${STOCK_VALUE:.2f}')

def view_inventory():
    print('''
    < Inventory >
    ''')
    options = {

        '1': items_in_stock,
        '2': items_and_details,
        '3': stock_totals,
        '4': lambda: print('...Returning to main menu...\n')
    }
    while True:
        print('''              
Please make a viewing selection:
    < 1 > Items in stock
    < 2 > Item prices and values
    < 3 > Stock total and total stock value
    < 4 > Return to main menu
        ''')
        selection = input()
        if selection in options:
            options[selection]()
            if selection == '4':
                break
        else:
            print('\n...Invalid selection...\n')

################################################################################
##      7. View order history and till
################################################################################

def view_purchase_history():
    purchase_orders = 0
    items_sold = 0
    transaction_totals = 0.00
    print('\n< Purchase orders:\n')
    for key, value in ORDER_LOG.items():
        if value['Transaction Type'] == 'Purchase':
            print(f'Transaction #: {key} | Date/Time: {value['Date/Time']} | Total items sold: {value['Total items']} | Transaction total: ${value['Transaction total $']:.2f}')
            order_printer(value['Transaction details'])
            purchase_orders += 1
            items_sold += value['Total items']
            transaction_totals += value['Transaction total $']
    print(f'\n< Totals >    Purchase orders: {purchase_orders} | Items sold: {items_sold} | Transactions total: ${transaction_totals:.2f}')

def view_return_history():
    return_orders = 0
    items_returned = 0
    transaction_totals = 0.00
    print('\n< Return orders:\n')
    for key, value in ORDER_LOG.items():
        if value['Transaction Type'] == 'Return':
            print(f'Transaction #: {key} | Date/Time: {value['Date/Time']} | Total items returned: {value['Total items']} | Transaction total: ${value['Transaction total $']:.2f}')
            order_printer(value['Transaction details'])
            return_orders += 1
            items_returned += value['Total items']
            transaction_totals += value['Transaction total $']
    print(f'\n< Totals >    Purchase orders: {return_orders} | Items sold: {items_returned} | Transactions total: ${transaction_totals:.2f}')

def order_history_and_till():
    options = {

        '1': lambda: print(f'\n< Till balance:  ${TILL_BALANCE:.2f}'),
        '2': view_purchase_history,
        '3': view_return_history,
        '4': lambda: print('...Returning to main menu...\n')
    }
    while True:
        print('''
    < Order history and Till >
              
Please make a viewing selection:
    < 1 > View till balance
    < 2 > View purchase order history
    < 3 > View Return order history
    < 4 > Return to main menu
        ''')
        selection = input()
        if selection in options:
            options[selection]()
            if selection == '4':
                break
        else:
            print('\n...Invalid selection...\n')


################################################################################
##      Front end
################################################################################

def front_end():
    options = {

        '1': purchase,
        '2': return_purchase,
        '3': add_stock,
        '4': update_stock,
        '5': delete_stock,
        '6': view_inventory,
        '7': order_history_and_till,
        '8': lambda: print('< Thank you for using the inventory management system >')
    }
    while True:
        print('''
Please make a selection from the following:
    < 1 > Make a purchase
    < 2 > Return a purchase
    < 3 > Add new item to stock
    < 4 > Update stock item
    < 5 > Delete stock item
    < 6 > View inventory details
    < 7 > View till and order history
    < 8 > Exit inventory management system
        ''')
        selection = input()
        if selection in options:
            options[selection]()
            if selection == '8':
                break
        else:
            print('\n...Invalid selection...\n')

################################################################################
##      Initialize front end
################################################################################
    
print('''
##############################################
##                                          ##
##                < Welcome >               ##
##                                          ##
##                  (>'-')>                 ##
##                                          ##
##     Inventory management application     ##
##       Premium inventory management       ##
##            at your fingertips            ##
##                                          ##
##############################################''')

front_end()
