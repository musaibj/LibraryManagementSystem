import mysql.connector

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
      CREATE TABLE IF NOT EXISTS Customer (
        CustomerID INT AUTO_INCREMENT PRIMARY KEY,
        CustomerName VARCHAR(255),
        RegistrationDate DATE,
        RegistrationExpiryDate DATE
      )
    """)

    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS Books (
        BookID INT AUTO_INCREMENT PRIMARY KEY,
        BookName VARCHAR(255),
        AuthorName VARCHAR(255),
        Genre VARCHAR(255),
        BookStatus VARCHAR(255),
        Quantity INT
      )
    """)

    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS Logbook (
        LogID INT AUTO_INCREMENT PRIMARY KEY,
        BookIssueDate DATE,
        BookReturnDate DATE,
        IssuedTo VARCHAR(255),
        CustomerID INT,
        BookID INT,
        FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
        FOREIGN KEY (BookID) REFERENCES Books(BookID)
      )
    """)
  def insertCustomer(self, customerName, registrationDate, expiryDate):
    sql = "INSERT INTO Customer (CustomerName, RegistrationDate, RegistrationExpiryDate) VALUES (%s, %s, %s)"
    values = (customerName, registrationDate, expiryDate)
    self.cursor.execute(sql, values)
    self.mydb.commit()

  def viewCustomers(self):
    sql = "SELECT * FROM Customer"
    self.cursor.execute(sql)
    result = self.cursor.fetchall()
    return result

  def removeCustomer(self, customerID):
    sql = "DELETE FROM Customer WHERE CustomerID = %s"
    values = (customerID,)
    cursor = self.mydb.cursor()
    cursor.execute(sql, values)
    self.mydb.commit()

  def insertBook(self, bookName, authorName, genre, bookStatus):
    # Check if the book already exists
    sql_check = "SELECT * FROM Books WHERE BookName = %s"
    values_check = (bookName,)
    self.cursor.execute(sql_check, values_check)
    existing_book = self.cursor.fetchone()

    if existing_book:
      # If the book exists, increment the quantity
      quantity_index = self.cursor.column_names.index('Quantity')
      current_quantity = existing_book[quantity_index]

      new_quantity = current_quantity + 1

      sql_update = "UPDATE Books SET Quantity = %s WHERE BookName = %s"
      values_update = (new_quantity, bookName)
      self.cursor.execute(sql_update, values_update)
    else:
      # If the book doesn't exist, insert a new record with quantity 1
      sql_insert = "INSERT INTO Books (BookName, AuthorName, Genre, BookStatus, Quantity) VALUES (%s, %s, %s, %s, %s)"
      values_insert = (bookName, authorName, genre, bookStatus, 1)
      self.cursor.execute(sql_insert, values_insert)

    self.mydb.commit()

  def getBooks(self):
    sql = "SELECT * FROM Books"
    cursor = self.mydb.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

  def removeBook(self, bookName):
    sql = "DELETE FROM Books WHERE BookName = %s"
    values = (bookName,)
    cursor = self.mydb.cursor()
    cursor.execute(sql, values)
    self.mydb.commit()

  def recordTransaction(self, bookIssueDate, bookReturnDate, issuedTo, customerID, bookID):
    sql = "INSERT INTO Logbook (BookIssueDate, BookReturnDate, IssuedTo, CustomerID, BookID) VALUES (%s, %s, %s, %s, %s)"
    values = (bookIssueDate, bookReturnDate, issuedTo, customerID, bookID)
    self.cursor.execute(sql, values)
    self.mydb.commit()

  def getLogbook(self):
    sql = "SELECT * FROM Logbook"
    self.cursor.execute(sql)
    result = self.cursor.fetchall()
    return result