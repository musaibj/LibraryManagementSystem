import json, http
from inventory import Inventory
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

obj = Inventory('localhost', 'root', 'MySQL@123', 'library')

class MyHandler(BaseHTTPRequestHandler):
  def response(self, responseCode, message):
    self.send_response(responseCode)
    self.send_header('Content-type', 'application/json')
    self.end_headers()
    self.wfile.write(json.dumps(message, default=str).encode('utf-8'))

  def headerInfo(self):
    print(f"Content-Length Header: {self.headers.get('Content-Length')}")
    contentLength = int(self.headers.get('Content-Length'))
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

  def get_books(self, bookID = 0):
    data = self.headerInfo()
    bookID_from_data = data.get('bookID')
    if bookID_from_data != 0:
      bookID = bookID_from_data
    if bookID != 0:
      return obj.getBooks(bookID_from_data)
    else:
      return obj.getBooks()
    
  def get_customers(self):
    query_params = parse_qs(urlparse(self.path).query)
    customerID_from_params = query_params.get('customerID', None)
    
    if customerID_from_params:
      customerID = int(customerID_from_params[0])
      return obj.viewCustomers(customerID)
    else:
      customerID = 0
      return obj.viewCustomers()


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

  def do_GET(self):
    if self.path.startswith('/get_customers/'):
      customers = self.get_customers()
      message = {'status': 'success', 'customers': customers}
      self.response(200, message)

    if self.path == '/get_books':
      books = self.get_books()
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