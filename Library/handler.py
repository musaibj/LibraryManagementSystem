import json, http
from inventory import Inventory
from http.server import HTTPServer, BaseHTTPRequestHandler

obj = Inventory("localhost", "root", "MySQL@123", "Library")

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
    customer_name = data.get('customerName')
    registration_date = data.get('registrationDate')
    expiry_date = data.get('expiryDate')
    obj.insertCustomer(customer_name, registration_date, expiry_date)
  
  def remove_customer(self):
    data = self.headerInfo()
    customer_id = data.get('CustomerID')
    obj.removeCustomer(customer_id)

  def add_book(self):
    data = self.headerInfo()
    bookName = data.get('BookName')
    authorName = data.get('AuthorName')
    genre = data.get('Genre')
    bookStatus = data.get('BookStatus')
    obj.insertBook(bookName, authorName, genre, bookStatus)

  def remove_book(self):
    data = self.headerInfo()
    bookName = data.get('BookName')
    obj.removeBook(bookName)

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

  def do_GET(self):
    if self.path == '/get_customers':
      customers = obj.viewCustomers()
      message = {'status': 'success', 'customers': customers}
      self.response(200, message)

    if self.path == '/get_books':
      books = obj.getBooks()
      message = {'status': 'success', 'customers': books}
      self.response(200, message)

handler = MyHandler
server = HTTPServer(("localhost", 8000), handler)
print("Server started on port 8000")
server.serve_forever()