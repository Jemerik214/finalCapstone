
#========The beginning of the class==========
# define shoe class
class Shoe:
    # constructor method
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity


    def get_cost(self):
        return int(self.cost)

    def get_quantity(self):
        return int(self.quantity)

    def get_code(self):
        return self.code

    # define string method
    def __str__(self):
        return f"""
        -----------------------------------
        Country of origin: \t {self.country}
        Product code: \t\t {self.code}
        Product name: \t\t {self.product}
        Cost: \t\t\t\t {self.cost}
        Quantity: \t\t\t {self.quantity}
        -----------------------------------
        """


#=============Shoe list===========
# The list will be used to store a list of objects of shoes.

shoe_list = []
#==========Functions outside the class==============

# function to create shoe instances from the lines of the given txt file and add them to the shoe_list
# skip the first line of the file - that is the heading
def read_shoes_data():
    try:
        with open("inventory.txt", "r") as read_data:
            data = read_data.readlines()[1:]
            for line in data:
                split_data = line.strip().split(",")
                shoe_list.append(Shoe(split_data[0], split_data[1], split_data[2], split_data[3], split_data[4]))

    except FileNotFoundError:
        print("Error: stock info could not be loaded, because file: 'inventory.txt' is not found.")
        return

read_shoes_data()

# function to allow the user to create new shoe instance.
def capture_shoes():
    # get new product details
    country = input("Which country are the shoes from?").strip()
    code = input("Enter the code of the product:").strip()
    product = input("What is the product name?").strip()

    try:
        cost = int(input("Enter the cost: "))

    except ValueError:
        print("That does not seem like a number, try again.")
        return

    try:
        quantity = int(input("Enter quantity: "))

    # prevent error
    except ValueError:
        print("That does not seem like a number, try again.")
        return

    # create new object and add it to the list
    shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(shoe)

    # add new object to the txt file
    with open("inventory.txt", "a") as file:
        file.write(f"\n{country},{code},{product},{cost},{quantity}")


# print all products
def view_all():
    print(*shoe_list)

# identify the shoes with the lowest quantity and offer to add to the stock
def re_stock():

    # Set the first shoe object as lowest to begin
    lowest_quantity = shoe_list[0].get_quantity()
    index_of_lowest_quantity = 0

    # find the lowest quantity
    for i in range(len(shoe_list)):
        if lowest_quantity > shoe_list[i].get_quantity():
            lowest_quantity = shoe_list[i].get_quantity()
            index_of_lowest_quantity = i

    re_stock_qty = None

    while re_stock_qty is None:

        try:
            # ask user if they would like to re-stock
            re_stock_qty = int(input(
                f"""\nThere are only {lowest_quantity} in stock of {shoe_list[index_of_lowest_quantity]}
            To re-stock, please enter the quantity to be added to the stock (or enter -1 to return to the menu): """))

            # option to return to main menu
            if re_stock_qty == -1:
                return

            if re_stock_qty < -1:
                print("\nInvalid value, try again.")
                re_stock_qty = None

            else:
                # update stock
                new_stock = shoe_list[index_of_lowest_quantity].get_quantity() + re_stock_qty
                shoe_list[index_of_lowest_quantity].quantity = str(new_stock)

                # update inventory txt file
                with open("inventory.txt", "w") as file:
                    file.write("Country,Code,Product,Cost,Quantity")
                    for shoes in shoe_list:
                        file.write(f"\n{shoes.country},{shoes.code},{shoes.product},{shoes.cost},{shoes.quantity}")

        # handle error
        except ValueError:
            print("\nThat does not seem like a number, try again.")

# find product from code provided by the user
def search_shoes():
    # get code input
    code = input("Enter the code of the shoes: ").strip()

    # find and print matching shoes in shoe_list
    for index, shoes in enumerate(shoe_list):
        if shoes.get_code == code:
            print(shoes)


    '''
    This function calculates the total value for each item.
    And it pints this information on the console for all the shoes.
    '''
def value_per_item():
    try:
        # find cost and quantity for each shoes, then calculate total value
        with open("inventory.txt", "r") as read_data:
            data = read_data.readlines()[1:]
            for index, line in enumerate(data):
                split_data = line.strip().split(",")
                value = shoe_list[index].get_cost()*shoe_list[index].get_quantity()

                # print results
                print(f"""
                Code: \t\t{shoe_list[index].code}
                Product: \t{shoe_list[index].product}
                Value: \t\t{value}
                """)

    # error handling
    except FileNotFoundError:
        print("Error! File: 'inventory.txt' is not found.")
        return

# find shoes with highest quantity and print them as being on sale
def highest_qty():
    # Set the first shoe object as highest to begin
    highest_quantity = shoe_list[0].get_quantity()
    index_of_highest_quantity = 0

    # find highest quantity
    for i in range(1, len(shoe_list)):
        if highest_quantity <= shoe_list[i].get_quantity():
            highest_quantity = shoe_list[i].get_quantity()
            index_of_highest_quantity = i

    # print shoes and sale message
    print(f"{shoe_list[index_of_highest_quantity]} \n\t\t\t\t\t is on sale!")



#==========Main Menu=============

while True:

    user_selection = input("""
Please select:
    a  - to add shoes
    rs - to re-stock
    ss - to search shoes
    va - to view all shoes
    dv - to display value of total stock
    sa - to get shoes on sale
    e  - exit
    : """).lower().strip()

    # add shoes
    if user_selection == 'a':
        capture_shoes()

    # re-stock
    elif user_selection == 'rs':
        re_stock()

    # search shoes
    elif user_selection == 'ss':
        search_shoes()

    # view all shoes
    elif user_selection == 'va':
        view_all()

    # display stock value for all items
    elif user_selection == 'dv':
        value_per_item()

    # the shoes with the highest quantity are on sale
    elif user_selection == 'sa':
        highest_qty()

    # exit
    elif user_selection == 'e':
        print("Goodbye!")
        exit()

    # incorrect selection
    else:
        print("\nIncorrect selection, try again.")