#coding:utf-8
import sqlite3
import time

#data base manager creation
class DataBase:
    """database class manager"""
    def __init__(self, name):
        """ database constructor """
        try:
            #connection with the database
            self.connection = sqlite3.connect(f'database/{name}.db')
            #database cursor
            self.cursor = self.connection.cursor()
        except Exception as error:
            print('DATABASE ERROR:', error)

    def close(self):
        """ database closer """
        #close of the database
        self.connection.close()

    def get_customer_by_number(self, number):
        """ customer getter by his phone number """
        try:
            self.cursor.execute('SELECT * FROM customer WHERE number=?', (number,))
            #get of the customer
            customer = self.cursor.fetchone()
            #return of the customer
            return customer
        except Exception as error:
            print('DATABASE ERROR:', error)
            self.connection.rollback()




    def get_all_customers(self):
        """ all customers getter """
        try:
            #get of the customers
            self.cursor.execute('SELECT * FROM customer')
            customers = self.cursor.fetchall()
            #return of the customers
            return customers
        except Exception as error:
            print('DATABASE ERROR:', error)
            self.connection.rollback()


    def customer_exists(self, number):
        """ existence checking of a customer """
        try:
            #check existence of the customer
            self.cursor.execute('SELECT * FROM customer WHERE number=?', (number,))
            #get the customer
            customer = self.cursor.fetchone()
            return customer
        except Exception as error:
            print('DATABASE ERROR:', error)




    def set_customer(self, name, number):
        """ customer setter """

        #try execution
        try:
            #check existence of the customer
            self.cursor.execute('SELECT * FROM customer WHERE number=?', (number,))
            #get the customer
            customer = self.cursor.fetchone()
            if customer:
                print('Customer exists alrady')
            else:
                self.cursor.execute("""
                    INSERT INTO customer(name, number)
                    VALUES(?, ?)""", (name, number))
                self.connection.commit()
        except Exception as error:
            print('DATBASE ERROR:', error)
            self.connection.rollback()


    def set_customers(self, customers_list):
        """ customer setter """
        #try execution
        try:
            self.cursor.executemany("""
                INSERT INTO customer(name, number)
                VALUES(?, ?)""",customers_list)
            self.connection.commit()
        except Exception as error:
            print('DATBASE ERROR:', error)
            self.connection.rollback()

    def set_data(self, name, motif, number):
        """ customer setter with his information """
        #get of the current time
        moment = time.time()
        #set of the customer
        self.set_customer(name, number)
        #get of the customer
        customer = self.get_customer_by_number(number)
        #customer id getting
        customer_id = customer[0]
        #get of the current timestamp
        current_moment = time.time()
        #set of the customer visit
        self.set_visit(customer_id, current_moment, motif)


    #visit setter
    def set_visit(self, customer, moment, motif):
        """ visit setter """
        #try execution
        try:
            self.cursor.execute("""
                    INSERT INTO visit(customer, moment, motif)
                    VALUES(?, ?, ?)""", (customer, moment, motif))
            self.connection.commit()
        except Exception as error:
            print('DATBASE ERROR:', error)
            self.connection.rollback()

    #customer visits
    def get_visits(self, number):
        """ customer visits getter """
        #get of the customer
        customer = self.get_customer_by_number(number)
        #check of the existence of the customer
        if customer:
            #get of the if of the customer
            customer_id = customer[0]
            try:
                #get of the visit with the customer id
                self.cursor.execute("""
                    SELECT * FROM visit WHERE customer=? """, (customer_id,))
                visits = self.cursor.fetchall()
                #return the vistis if visits find
                if visits:
                    return visits
                #return an empty list of visit not found
                return []
            except Exception as error:
                print('DATABASE ERROR:', error)


if __name__ == '__main__':
    database = DataBase('base')
    #database.set_data('GL', 'Renseignement', 98764598)
    #database.set_data('kea', 'Renseignement', 99797640)
    #database.set_data('jso', 'Renseignement', 98768593)
    for visit in database.get_visits(98768593):
        print(visit)
