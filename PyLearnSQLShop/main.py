import sqlite3
import qrcode

def show_menu():
    print('1- Show list')
    print('2- Add new')
    print('3- Edit')
    print('4- Remove')
    print("5- Search")
    print("6- Buy")
    print("7- Creat Qr Code")
    print("8- Exit")

def show_list():
    result = my_coursor.execute('SELECT * FROM products')
    products = result.fetchall()
    for product in products:
        print(product)

def load_database():
    global connection
    global my_coursor
    connection = sqlite3.connect('shop.db')
    my_coursor = connection.cursor()

def add_new():
    name = input("enter name: ")
    price = input("enter price: ")
    count = input("enter count: ")
    my_coursor.execute(f'INSERT INTO products(Name,Price,Count) VALUES("{name}","{price}","{count}")')
    connection.commit()

def edit():
    ProductId = input('enter productId: ')
    print("1- Name      2- Price        3- count")
    user_choice = int(input("your choice: "))
    if user_choice == 1:
        new_name = input('New name: ')
        my_coursor.execute(f'UPDATE products SET Name="{new_name}" WHERE ProductId = {ProductId}')
    elif user_choice == 2:
        new_price = input('New price: ')
        my_coursor.execute(f'UPDATE products SET Price="{new_price}" WHERE ProductId = {ProductId}')
    elif user_choice == 3:
        new_count = input('New count: ')
        my_coursor.execute(f'UPDATE products SET Count="{new_count}" WHERE ProductId = {ProductId}')
    else:
        print('enter number between 1-3')
        return
    connection.commit()
    print('Data changed successfully')

def remove():
    ProductId = input('enter productId: ')
    my_coursor.execute(f'DELETE FROM products WHERE ProductId = "{ProductId}"')
    connection.commit()

def qrcode0():
    ProductId = input('enter productId: ')
    result = my_coursor.execute(f'SELECT * FROM products WHERE ProductId = {ProductId}')
    product = result.fetchone()
    print(product)
    QRcode = qrcode.make(product)
    QRcode.save(str(ProductId) + "QrCode.png")
    print('QrCode saved successfully')

def search():
    ProductId = input('enter productId: ')
    result = my_coursor.execute(f'SELECT * FROM products WHERE ProductId = {ProductId}')
    product = result.fetchone()
    print(product)


def buy_new_product(shopper_products, customer_name,ProductId):
    result = my_coursor.execute(f'SELECT Count FROM products WHERE ProductId = {ProductId}')
    resultfetchone = result.fetchone()
    if resultfetchone == None:
        print('this Id is invalid')
        return
    count = float(resultfetchone[0])
    result = my_coursor.execute(f'SELECT Price FROM products WHERE ProductId = {ProductId}')
    price = float(result.fetchone()[0])
    result = my_coursor.execute(f'SELECT Name FROM products WHERE ProductId = {ProductId}')
    name = result.fetchone()[0]
    user_count = float(input('enter your count: '))
    if user_count <= count:
        new_count = count - user_count
        my_coursor.execute(f'UPDATE products SET Count="{new_count}" WHERE ProductId = {ProductId}')
        my_coursor.execute(f'INSERT INTO buy(ProductId,Customer,Price,Count) VALUES("{ProductId}","{customer_name}","{price}","{user_count}")')
        connection.commit()
        new_product = {'code': ProductId, 'name': name, 'price': price, 'count': user_count}
        shopper_products.append(new_product)
        print(str(user_count) + ' ' + name + ' add to your list')
    else:
        print('Insufficient inventory')

    return shopper_products

def print_purchase_invoice(customer_name,shopper_products):
    total_price = 0
    print('\n------------------------\n')
    print('\n    *   *   *   *   *   *   *     ')
    print('     Purchase Invoice     \n')
    print("code\t\tname\t\tprice\t\tcount")
    for product in shopper_products:
        print(str(product["code"]) + "\t\t" + str(product["name"]) + "\t\t" + str(product["price"]) + "\t\t"+ str(product["count"]))
        total_price += int(product["price"])*int(product['count'])
    print('\nTotal price is: ' , str(total_price))
    print('Thank you ',customer_name,'for your shopping')
    print('\n------------------------\n')


def buy():    
    shopper_products = []
    print('Exit by \'exit\'')
    customer_name = input('enter your name: ')
    while True:
        ProductId = input('enter productId: ')
        if ProductId == 'exit':
            print_purchase_invoice(customer_name, shopper_products)
            break
        else:
            ProductId = int(ProductId)
            buy_new_product(shopper_products, customer_name, ProductId)

print("welcome to Mahammad Store")
print("Loading...")
load_database()
print("Data loaded.")

while True:
    show_menu()
    choice_user = input("enter your choice: ")
    if choice_user.isdigit():
        choice = int(choice_user)
        if 0 < choice < 9:
            if choice == 1:
                show_list()
            elif choice == 2:
                add_new()
            elif choice == 3:
                edit()
            elif choice == 4:
                remove()
            elif choice == 5:
                search()
            elif choice == 6:
                buy()
            elif choice == 7:
                qrcode0()
            elif choice == 8:
                exit(0)
        else:
            print('⚠ you have to enter number between 1-8')
    else:
        print('⚠ you have to enter number between 1-8')
