import mysql.connector
import datetime
from dateutil.relativedelta import relativedelta

class Inventory:
  def __init__(self, host, user, passwd, database):
    self.mydb = mysql.connector.connect(
      host = host,
      user = user,
      passwd = passwd,
      database = database.lower()
    )
    self.cursor = self.mydb.cursor()
    self.createdb()

  def createdb(self):
    self.cursor.execute("CREATE DATABASE IF NOT EXISTS Library")

    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS Customers (
        CustomerID INT AUTO_INCREMENT PRIMARY KEY,
        CustomerName VARCHAR(255)
        )
    """)

    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS Membership (
        MembershipID INT AUTO_INCREMENT PRIMARY KEY,
        CustomerID INT,
        MembershipIssued DATE,
        MembershipExpire DATE,
        CONSTRAINT fk_customer_membership FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID)
      )
    """)

    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS Books (
        BookID INT AUTO_INCREMENT PRIMARY KEY,
        BookName VARCHAR(255),
        Author VARCHAR(255),
        Genre VARCHAR(255),
        Quantity INT
      )
    """)

    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS Transactions (
        TransactionID INT AUTO_INCREMENT PRIMARY KEY,
        CustomerID INT,
        BookID INT,
        IssuedON DATE,
        IssuedTill DATE,
        CONSTRAINT fk_customer_transaction FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID),
        CONSTRAINT fk_book_transaction FOREIGN KEY (BookID) REFERENCES Books (BookID)
      )
    """)

    self.mydb.commit()


  def registerCustomer(self, customerName, membershipMonths):
    membershipFrom = datetime.date.today()
    membershipTill = membershipFrom + relativedelta(months=membershipMonths)

    sql_insert_customer = "INSERT INTO Customers (CustomerName) VALUES (%s)"
    values_customer = (customerName,)
    self.cursor.execute(sql_insert_customer, values_customer)
  
    sql_insert_membership = """
        INSERT INTO Membership (MembershipIssued, MembershipExpire, CustomerID)
        VALUES (%s, %s, LAST_INSERT_ID())
    """
    values_membership = (membershipFrom, membershipTill)
    self.cursor.execute(sql_insert_membership, values_membership)

    self.mydb.commit()

  def viewCustomers(self):
    sql = """
        SELECT Customers.CustomerID, Customers.CustomerName, Membership.MembershipIssued, Membership.MembershipExpire
        FROM customers
        INNER JOIN Membership ON Customers.CustomerID = Membership.CustomerID
    """
    self.cursor.execute(sql)
    result = self.cursor.fetchall()

    labels = ["CustomerID", "CustomerName", "MembershipIssued", "MembershipExpire"]
    customers_data = []
    for x in result:
      customer_dict = {}
      for i in range(len(labels)):
          customer_dict[labels[i]] = x[i]
      customers_data.append(customer_dict)

    return customers_data

  def insertBook(self, bookName, authorName, genre):
    sql_check = "SELECT * FROM books WHERE BookName = %s"
    values_check = (bookName,)
    self.cursor.execute(sql_check, values_check)
    existing_book = self.cursor.fetchone()

    if existing_book:
      quantity_index = self.cursor.column_names.index('Quantity')
      current_quantity = existing_book[quantity_index]

      new_quantity = current_quantity + 1

      sql_update = "UPDATE books SET Quantity = %s WHERE BookName = %s"
      values_update = (new_quantity, bookName)
      self.cursor.execute(sql_update, values_update)
      self.mydb.commit()
    else:
      sql_insert = "INSERT INTO books (BookName, Author, Genre, Quantity) VALUES (%s, %s, %s, 1)"
      values_insert = (bookName, authorName, genre)
      self.cursor.execute(sql_insert, values_insert)
      self.mydb.commit()

  
  def getBooks(self):
    sql = "SELECT * FROM books"
    self.cursor.execute(sql)
    result = self.cursor.fetchall()

    labels = ["BookID", "BookName", "Author", "Genre", "Quantity"]
    books_data = []
    for book_tuple in result:
        book_dict = {}
        for i in range(len(labels)):
            book_dict[labels[i]] = book_tuple[i]
        books_data.append(book_dict)

    return books_data 
  
  def recordTransaction(self, issuedTo, issuedFrom, issuedTill, bookName, bookID):
    availability = "SELECT Quantity FROM books WHERE BookID = %s"
    values_availability = (bookID,)
    self.cursor.execute(availability, values_availability)
    book_availability = self.cursor.fetchone()

    if not book_availability:
      return {"status": "error", "message": "Book not available"}

    recordTransaction = """
        INSERT INTO log (IssuedTo, IssuedFrom, IssuedTill, BookName, BookID)
        VALUES (%s, %s, %s, %s, %s)
    """
    valuesRecordTransaction = (issuedTo, issuedFrom, issuedTill, bookName, bookID)
    self.cursor.execute(recordTransaction, valuesRecordTransaction)

    updateQuantity = "UPDATE books SET Quantity = Quantity - 1 WHERE BookID = %s"
    valuesUpdateQuantity = (bookID,)
    self.cursor.execute(updateQuantity, valuesUpdateQuantity)

    self.mydb.commit()
  
  def getLogbook(self):
    sql = "SELECT * FROM log"
    self.cursor.execute(sql)
    result = self.cursor.fetchall()
    return result
"""
  def removeCustomer(self, customerID):
    sql = "DELETE FROM customer WHERE CustomerID = %s"
    values = (customerID,)
    cursor = self.mydb.cursor()
    cursor.execute(sql, values)
    self.mydb.commit()

  def removeBook(self, bookName):
    sql = "DELETE FROM books WHERE BookName = %s"
    values = (bookName,)
    cursor = self.mydb.cursor()
    cursor.execute(sql, values)
    self.mydb.commit()
"""