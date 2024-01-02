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
        BookStatus VARCHAR(255)
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
    sql = "INSERT INTO Books (BookName, AuthorName, Genre, BookStatus) VALUES (%s, %s, %s, %s)"
    values = (bookName, authorName, genre, bookStatus)
    cursor = self.mydb.cursor()
    cursor.execute(sql, values)
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
"""
  def insertLogbook(self, issueDate, returnDate, issuedTo, customerID, bookID):
    sql = "INSERT INTO Logbook (BookIssueDate, BookReturnDate, IssuedTo, CustomerID, BookID) VALUES (%s, %s, %s, %s, %s)"
    values = (issueDate, returnDate, issuedTo, customerID, bookID)
    cursor = self.mydb.cursor()
    cursor.execute(sql, values)
    self.mydb.commit()

  def getLogs(self):
    sql = "SELECT * FROM Logbook"
    cursor = self.mydb.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result
"""
