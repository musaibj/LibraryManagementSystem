import mysql.connector
import datetime
from dateutil.relativedelta import relativedelta

class Inventory:
  def __init__(self, host, user, passwd, database):
    self.mydb = mysql.connector.connect(
      host = host,
      user = user,
      passwd = passwd,
      database = database
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

  def viewCustomers(self, customerID = None):
    if customerID is not None:
      pass
    else:
      sql = """
          SELECT Customers.CustomerID, Customers.CustomerName, Membership.MembershipIssued, Membership.MembershipExpire
          FROM Customers
          INNER JOIN Membership ON Customers.CustomerID = Membership.CustomerID
          """
      self.cursor.execute(sql)
      result = self.cursor.fetchall()

      labels = ["CustomerID", "CustomerName", "MembershipIssued", "MembershipExpire"]
      customersData = []
      for x in result:
        customerData = {}
        for i in range(len(labels)):
          customerData[labels[i]] = x[i]
        customersData.append(customerData)
      return customersData

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
      sql_insert = "INSERT INTO Books (BookName, Author, Genre, Quantity) VALUES (%s, %s, %s, 1)"
      values_insert = (bookName, authorName, genre)
      self.cursor.execute(sql_insert, values_insert)
      self.mydb.commit()

  def getBooks(self, bookID = None):
    if bookID is not None:
      sql = """
          SELECT BookName, Author, Genre, Quantity FROM Books WHERE BookID = %s
          UNION
          SELECT TransactionID, CustomerID, IssuedOn, IssuedTill FROM Transactions WHERE BookID = %s
        """
      value = (bookID, bookID)
      self.cursor.execute(sql, value)
      result = self.cursor.fetchall()

      labels = ["BookName", "Author", "Genre", "Quantity"]
      labels2 = ["TransactionID", "CustomerID", "IssuedOn", "IssuedTill"]
      booksData = []
      firstBookTuple = result[0]
      bookDict = {}
      for i in range(len(labels)):
        bookDict[labels[i]] = firstBookTuple[i]
      booksData.append(bookDict)
      for bookTuple in result[1:]:
        bookDict = {}
        for i in range(1, len(labels2)):
          bookDict[labels2[i]] = bookTuple[i]
        booksData.append(bookDict)
      return booksData
    else:
      sql = "SELECT * FROM Books"
      self.cursor.execute(sql)
      result = self.cursor.fetchall()

      labels = ["BookID", "BookName", "Author", "Genre", "Quantity"]
      booksData = []
      for bookTuple in result:
        bookDict = {}
        for i in range(len(labels)):
          bookDict[labels[i]] = bookTuple[i]
        booksData.append(bookDict)
      return booksData 
  
  def recordTransaction(self, customerID, bookID, issuedOn, issuedTill):
    availability = "SELECT Quantity FROM Books WHERE BookID = %s"
    valuesAvailability = (bookID,)
    self.cursor.execute(availability, valuesAvailability)
    book_availability = self.cursor.fetchone()

    if not book_availability:
      return {"status": "error", "message": "Book not available"}
    else:
      recordTransaction = "INSERT INTO Transactions (CustomerID, BookID, IssuedOn, IssuedTill) VALUES (%s, %s, %s, %s)"
      valuesRecordTransaction = (customerID, bookID, issuedOn, issuedTill)
      self.cursor.execute(recordTransaction, valuesRecordTransaction)

      updateQuantity = "UPDATE Books SET Quantity = Quantity - 1 WHERE BookID = %s"
      valuesUpdateQuantity = (bookID,)
      self.cursor.execute(updateQuantity, valuesUpdateQuantity)

      self.mydb.commit()
  
  def getLogbook(self):
    sql = "SELECT * FROM Transactions"
    self.cursor.execute(sql)
    result = self.cursor.fetchall()

    labels = ["TransactionID", "CustomerID", "BookID", "IssuedOn", "IssuedTill"]
    booksData = []
    for bookTuple in result:
        bookDict = {}
        for i in range(len(labels)):
            bookDict[labels[i]] = bookTuple[i]
        booksData.append(bookDict)

    return booksData 

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
obj = Inventory('localhost', 'root', 'MySQL@123', 'library')
"""