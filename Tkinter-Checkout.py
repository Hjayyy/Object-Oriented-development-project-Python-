# imports the global variable random to generate a random
# number of items in the basket
import random
# imports the global variable time to get the time when the
# customer checks out
import time
from datetime import datetime
from tkinter import *  # imports everything from tkinter

today_date = datetime.now()


class Lane:

    def __init__(self, lane_num, type, size):
        # Initializes a checkout lane with a specified type (regular or self-checkout) and maximum customer capacity
        self.lane_num = lane_num
        self.type = type
        self.size = size
        # List to store customers currently in the lane
        self.customers = []
        # Status of the lane, initially set to 'Close'
        self.status = 'Close'

    def add_customer(self, customer):
        # Adds a customer to the lane if there is space available
        if len(self.customers) < self.size:
            self.customers.append(customer)

    def remove_customer(self):
        # Removes a customer from the lane if there are customers in the lane
        if len(self.customers) > 0:
            self.customers.pop(0)

    def update_status(self):
        # Updates the status of the lane based on the current number of customers
        if len(self.customers) < self.size:
            self.status = 'Open'
        else:
            self.status = 'Close'

    def display(lane):
        # Displays the status of the lane, whether it's open or closed, and the number of customers using '*'
        if lane.status == 'Close':
            print(lane.lane_num + "(" + lane.type + ")", "-> Closed")
        else:
            consumer = '*' * len(lane.customers)
            print(lane.lane_num + "(" + lane.type + ")", "->", consumer)


# creates a customer class with parameters which will be needed
# further down in the code
# assigns the value 4 and 6 to the times of the checkout type


class Customer:
    def __init__(self, customer_id, basket_items):
        self.customer_id = customer_id
        self.basket_items = basket_items
        self.__cashier_time = 4  # value assigned so it can be multiplied by no. of items to get the total time
        self.__self_checkout_time = 6  # value assigned so it can be multiplied by no. of items to get the total time
        self.lottery_ticket = False  # since nothing has been calculated, no tickets have been awarded so its initial
        # value is False

    def get_number_of_items(self):  # gets the number of items generated randomly in the basket
        return len(self.basket_items)  # outputs how many items are in the basket

    def get_processing_time(self, checkout_type):  # gets the time of how long it takes to fulfill a shop
        processing_time = self.__cashier_time if checkout_type == 'cashier' else self.__self_checkout_time
        return len(self.basket_items) * processing_time

    def award_lottery_ticket(self):  # defines the function of getting a reward provided that the conditions are met
        if len(self.basket_items) >= 10:  # the number needed in the basket to get a lottery ticket
            self.lottery_ticket = True  # if the condition is met, then the ticket is awarded
            print("Congrats, you have won a lottery ticket!")
        else:
            print("Unlucky, you did not win the lottery ticket. Better luck next time")

    # function to display the customers details
    def show_customer_details(self, checkout_type):
        # f string used for interpolation which allows for embedded expressions
        print(f"The number of items in the basket is: {len(self.basket_items)}")
        print(f"Processing time at {checkout_type} till: {self.get_processing_time(checkout_type)} Seconds")


class CheckoutSystem:
    def __init__(self):
        # starts with one cashier and one self-service checkout / lane
        self.lanes = [Lane('L1', 'cashier', 5), Lane('L2', 'cashier', 5),
                      Lane('L3', 'cashier', 5), Lane('L4', 'cashier', 5),
                      Lane('L5', 'cashier', 5), Lane('L6', 'self-checkout', 15)]
        self.lanes[0].update_status()
        self.lanes[5].update_status()

    def open_status(self):
        # Opens Lane 2 if it is currently closed and Lane 1 is full
        if len(self.lanes[0].customers) == self.lanes[0].size:
            if self.lanes[1].status == 'Close':
                self.lanes[1].update_status()
                print("Lane 2 is now open")
            # Opens Lane 3 if it is currently closed and Lane 2 is full
            elif len(self.lanes[1].customers) == self.lanes[1].size and self.lanes[2].status == 'Close':
                self.lanes[2].update_status()
                print("Lane 3 is now open")
            # Opens Lane 4 if it is currently closed and Lane 3 is full
            elif len(self.lanes[2].customers) == self.lanes[2].size and self.lanes[3].status == 'Close':
                self.lanes[3].update_status()
                print("Lane 4 is now open")
            # Opens Lane 5 if it is currently closed and Lane 4 is full
            elif len(self.lanes[3].customers) == self.lanes[3].size and self.lanes[4].status == 'Close':
                self.lanes[4].update_status()
                print("Lane 5 is now open")

    def checkout_simulation(self):
        start_time = time.time()  # calls the global variable into this function
        print(f"The simulation started at: {time.ctime(start_time)}")  # displays the time that the simulation starts

        while not self.end_checkout_simulation(start_time):  # initializes a loop so long as the conditions are met
            self.simulate_checkout()  # calls the checkout method which simulates and assigns customers to lanes
            time.sleep(30)  # simulation should last 30 seconds before stopping and restarting

        print("The simulation has ended.")

    def end_checkout_simulation(self, start_time):
        return time.time() - start_time >= 90  # should run for an hour. 60x60 seconds

    def simulate_checkout(self):
        # Simulate the checkout process
        self.create_and_assign_customers()
        self.open_status()

        for lane in self.lanes:  # iterates through each lane in the system
            for customer in lane.customers:  # iterates through each customer in the lanes
                customer.show_customer_details(lane.type)  # displays each customer's details and
                # displayed using the show customer details method

                if not customer.lottery_ticket:  # checks if the customer meets the condition to get a ticket
                    customer.award_lottery_ticket()

        self.report_simulation_state()  # displays the state at fixed intervals of 30 seconds

    def create_and_assign_customers(self):  # this code creates random customers and puts them in lanes
        number_of_customers = random.randint(1, 10)
        for _ in range(number_of_customers):
            customer = Customer(random.randint(1, 999),
                                [random.randint(1, 100) for _ in range(random.randint(1, 30))])
            # Inside the loop, it creates a Customer object with a random customer ID between 1 and 999
            # (inclusive) and a random list of basket items. The number
            # of items in the basket is also randomly determined between 1 and 30.
            self.put_customer_in_lane(customer)  # calls the put_customer_in method and passes the new customer object

    def report_simulation_state(self):
        # Display the state of the simulation at fixed intervals
        print("### Lane status at the current simulation interval ###")
        for lane in self.lanes:
            lane.display()

    def put_customer_in_lane(self, customer):  # Finds an open lane with sufficient capacity
        # creates a list and has the size determined by lane.size
        open_lanes = [lane for lane in self.lanes if lane.status == 'Open' and len(lane.customers) < lane.size]
        # on the condition that there are lanes available
        if open_lanes:
            chosen_lane = random.choice(open_lanes)  # randomly allocates one lane from the list of open lanes.
            # it simulates random assignment of a customer to an available lane
            chosen_lane.add_customer(customer)
        else:
            print("There are no open lanes.")

    def remove_customers_from_lane(self):
        # Get a list of open lanes with customers
        open_lanes = [lane for lane in self.lanes if lane.status == 'Open' and len(lane.customers) > 0]
        # Iterate through open lanes and remove a random number of customers
        for lane in open_lanes:
            # Determine the number of customers to remove, limited to 5 or the current number of customers
            remove_num = random.randint(1, min(5, len(lane.customers)))
            # Remove customers from the lane
            for _ in range(remove_num):
                lane.remove_customer()
                print("A customer has left a lane")


class Simulation:
    def __init__(self, checkout_system, root):
        self.checkout_system = checkout_system
        self.root = root
        self.run_simulation = False  # simulation has not started to run yet, so it is false

    def start_simulation(self):
        if not self.run_simulation:
            self.run_simulation = True  # simulation starts running now
            self.root.after(0, self.simulate)  # refers to the tkinter window

    def simulate(self):
        # checks if simulation is running
        if self.run_simulation:
            # if simulation is running, then the checkout_system method is called
            self.checkout_system.checkout_simulation()
            # creates a loop after running simulation for every 30 seconds
            self.root.after(30000, self.simulate)

    def end_simulation(self):  # end_simulation method is called to end it
        self.run_simulation = False  # run_simulation attributes are false so simulation has ended

    def show_customer_details(self):  # this method is responsible for showing customers details
        # Iterating through each lane and each customer in the lane
        for lane in self.checkout_system.lanes:
            for customer in lane.customers:
                customer.show_customer_details(lane.type)
        # calls the report_simulation method
        self.checkout_system.create_and_assign_customers()

    def checkout_simulation_gui(self):
        # creating a label widget
        customer_checkout = Label(self.root, text="Customer Checkout")
        # putting the label onto the screen
        customer_checkout.pack()

        # creates four buttons, one to start, one to end, one to display details and one to exit the program
        start_simulation_button = Button(self.root, text="Start Simulation", command=self.start_simulation)
        start_simulation_button.pack()  # displays the code on the screen

        show_customer_details = Button(self.root, text="Display Customer Details", command=self.show_customer_details)
        show_customer_details.pack()

        end_simulation = Button(self.root, text="End Simulation", command=self.end_simulation)
        end_simulation.pack()

        exit_button = Button(self.root, text="Exit", command=self.exit, fg="white", bg="red")
        exit_button.pack()
        # loops the constant loop
        self.root.mainloop()

    def exit(self):
        self.run_simulation = False
        self.root.destroy()  # this is for the exit button so that when it is
        # pressed, the program is completely closed and exited


if __name__ == "__main__":
    checkout_system = CheckoutSystem()
    root = Tk()

    simulation = Simulation(checkout_system, root)  # creates an instance of the simulation
    simulation.checkout_simulation_gui()
