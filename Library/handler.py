import json, http
from inventory import Inventory
from http.server import HTTPServer, BaseHTTPRequestHandler

obj = Inventory('localhost', 'root', 'MySQL@123', 'library')

class MyHandler(BaseHTTPRequestHandler):
  def response(self, responseCode, message):
    self.send_response(responseCode)
    self.send_header('Content-type', 'application/json')
    self.end_headers()
    self.wfile.write(json.dumps(message, default=str).encode('utf-8'))

  def headerInfo(self):
    contentLength = int(self.headers['Content-Length'])
    getData = self.rfile.read(contentLength)
    data = json.loads(getData.decode('utf-8'))
    return data

  def register_customer(self):
    data = self.headerInfo()
    customerName = data.get('customerName')
    membershipMonths = data.get('membershipMonths')
    obj.registerCustomer(customerName, membershipMonths)
  
  def remove_customer(self):
    data = self.headerInfo()
    customer_id = data.get('CustomerID')
    obj.removeCustomer(customer_id)

  def add_book(self):
    data = self.headerInfo()
    bookName = data.get('BookName')
    authorName = data.get('Author')
    genre = data.get('Genre')
    obj.insertBook(bookName, authorName, genre)

  def remove_book(self):
    data = self.headerInfo()
    bookName = data.get('BookName')
    obj.removeBook(bookName)

  def record_transaction(self):
    data = self.headerInfo()
    customerID = data.get('customerID')
    bookID = data.get('bookID')
    issuedOn = data.get('issuedOn')
    issuedTill = data.get('issuedTill')
    obj.recordTransaction(customerID, bookID, issuedOn, issuedTill)

  def get_book_status(self):
    data = self.headerInfo()
    bookID = data.get('bookID')
    return obj.getBookStatus(bookID)

  def do_POST(self):
    if self.path == '/register_customer':
      self.register_customer()
      message = {'status': 'success', 'message': 'Customer registered successfully'}
      self.response(200, message)

    if self.path == '/remove_customer':   
      self.remove_customer()
      message = {'status': 'success', 'message': 'Customer removed successfully'}
      self.response(200, message)
    
    if self.path == '/add_book':
      self.add_book()
      message = {'status': 'success', 'message': 'Book added successfully'}
      self.response(200, message)

    if self.path == '/remove_book':
      self.remove_book()
      message = {'status': 'success', 'message': 'Book removed successfully'}
      self.response(200, message)

    if self.path == '/transaction':
      self.record_transaction()
      message = {'status': 'success', 'message': 'Transaction recorded successfully'}
      self.response(200, message)
    
    if self.path == '/book_status':
      status =  self.get_book_status()
      message = {'status': 'success', 'customers': status}
      self.response(200, message)

  def do_GET(self):
    if self.path == '/get_customers':
      customers = obj.viewCustomers()
      message = {'status': 'success', 'customers': customers}
      self.response(200, message)

    if self.path == '/get_books':
      books = obj.getBooks()
      message = {'status': 'success', 'customers': books}
      self.response(200, message)

    if self.path == '/get_logs':
      logs = obj.getLogbook()
      message = {'status': 'success', 'logs': logs}
      self.response(200, message)

handler = MyHandler
server = HTTPServer(("localhost", 8000), handler)
print("Server started on port 8000")
server.serve_forever()