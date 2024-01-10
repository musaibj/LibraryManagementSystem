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
    self.cursor.execute("CREATE DATABASE IF NOT EXISTS library")

    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS customers (
        CustomerID INT AUTO_INCREMENT PRIMARY KEY,
        CustomerName VARCHAR(255),
        BooksIssued INT,
        MembershipID INT,
        MembershipFrom DATE,
        MembershipTill DATE,
        CurrentFine DECIMAL(10, 2)
      )
    """)

    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS membership (
        MembershipID INT AUTO_INCREMENT PRIMARY KEY,
        MembershipFrom DATE,
        MembershipTill DATE,
        CustomerID INT, 
        FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID)
      )
    """)

    # Alter the customers table to add the foreign key reference
    self.cursor.execute("""
      ALTER TABLE customers
      ADD FOREIGN KEY (MembershipID) REFERENCES membership(MembershipID)
    """)

    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS books (
        BookID INT PRIMARY KEY,
        BookName VARCHAR(255),
        Author VARCHAR(255),
        Genre VARCHAR(255),
        Quantity INT,
        IssuedTo INT,
        IssuedTill DATE,
        FOREIGN KEY (IssuedTo) REFERENCES customers(CustomerID)
      )
    """)

    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS log (
        TransactionID INT AUTO_INCREMENT PRIMARY KEY,
        IssuedTo INT,
        IssuedFrom INT,
        IssuedTill DATE,
        BookName VARCHAR(255),
        BookID INT,
        FOREIGN KEY (IssuedTo) REFERENCES customers(CustomerID),
        FOREIGN KEY (IssuedFrom) REFERENCES customers(CustomerID),
        FOREIGN KEY (BookID) REFERENCES books(BookID)
      )
    """)


    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS bookstatus (
        IssuedTo INT,
        IssuedFrom INT,
        IssuedTill DATE,
        BookID INT,
        BookName VARCHAR(255),
        PRIMARY KEY (IssuedTo, bookID),
        FOREIGN KEY (IssuedTo) REFERENCES customers(CustomerID),
        FOREIGN KEY (BookID) REFERENCES books(BookID)
      )
    """)

    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS finemanagement (
        IssuedTo INT,
        IssuedFrom INT,
        IssuedTill DATE,
        CurrentFine DECIMAL(10, 2),
        PRIMARY KEY (IssuedTo),
        FOREIGN KEY (IssuedTo) REFERENCES customers(CustomerID)
      )
    """)

  def insertCustomer(self, customerName, membershipMonths, booksIssued):
    
    
    membershipFrom = datetime.date.today()
    membershipTill = membershipFrom + relativedelta(months=membershipMonths)

    sql_insert_customer = "INSERT INTO customers (CustomerName, BooksIssued) VALUES (%s, %s)"
    values_customer = (customerName, booksIssued)
    self.cursor.execute(sql_insert_customer, values_customer)
  
    sql_insert_membership = """
        INSERT INTO membership (MembershipFrom, MembershipTill, CustomerID)
        VALUES (%s, %s, LAST_INSERT_ID())
    """
    values_membership = (membershipFrom, membershipTill)
    self.cursor.execute(sql_insert_membership, values_membership)

    self.mydb.commit()

  def viewCustomers(self):
    sql = """
        SELECT customers.CustomerID as CustomerID,
               customers.CustomerName as CustomerName,
               customers.BooksIssued as BooksIssued,
               membership.MembershipFrom as MembershipFrom,
               membership.MembershipTill as MembershipTill
        FROM customers
        INNER JOIN membership ON customers.CustomerID = membership.CustomerID
    """
    self.cursor.execute(sql)
    result = self.cursor.fetchall()

    labels = ["CustomerID", "CustomerName", "BooksIssued", "MembershipFrom", "MembershipTill"]
    customers_data = []
    for x in result:
      customer_dict = {}
      for i in range(len(labels)):
          customer_dict[labels[i]] = x[i]
      customers_data.append(customer_dict)

    return customers_data

  
"""
  def removeCustomer(self, customerID):
    sql = "DELETE FROM customer WHERE CustomerID = %s"
    values = (customerID,)
    cursor = self.mydb.cursor()
    cursor.execute(sql, values)
    self.mydb.commit()

  def insertBook(self, bookName, authorName, genre, bookStatus):
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
    else:
      sql_insert = "INSERT INTO books (BookName, AuthorName, Genre, BookStatus, Quantity) VALUES (%s, %s, %s, %s, %s)"
      values_insert = (bookName, authorName, genre, bookStatus, 1)
      self.cursor.execute(sql_insert, values_insert)

    self.mydb.commit()

  def getBooks(self):
    sql = "SELECT * FROM books"
    cursor = self.mydb.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

  def removeBook(self, bookName):
    sql = "DELETE FROM books WHERE BookName = %s"
    values = (bookName,)
    cursor = self.mydb.cursor()
    cursor.execute(sql, values)
    self.mydb.commit()

  def recordTransaction(self, bookIssueDate, bookReturnDate, issuedTo, customerID, bookID):
    sql = "INSERT INTO logbook (BookIssueDate, BookReturnDate, IssuedTo, CustomerID, BookID) VALUES (%s, %s, %s, %s, %s)"
    values = (bookIssueDate, bookReturnDate, issuedTo, customerID, bookID)
    self.cursor.execute(sql, values)
    self.mydb.commit()

  def getLogbook(self):
    sql = "SELECT * FROM logbook"
    self.cursor.execute(sql)
    result = self.cursor.fetchall()
    return result
"""