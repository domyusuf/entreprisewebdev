import base64
import http.server
import json
import socketserver
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from dsa.main import dictionary_lookup, linear_search, transactions, transactions_dict


# --- Authentication ---
USERNAME = "admin"
PASSWORD = "password"


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def _handle_get_requests(self):
        if self.path == "/transactions":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(transactions).encode())
        elif self.path.startswith("/transactions/"):
            try:
                transaction_id = int(self.path.split("/")[-1])
                _, transaction = dictionary_lookup(transaction_id)
                if transaction:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(transaction).encode())
                else:
                    self.send_error(404, "Transaction not found")
            except ValueError:
                self.send_error(400, "Invalid transaction ID")
        elif self.path == "/search-comparison":
            linear_times = []
            dict_times = []
            for i in range(min(20, len(transactions))):
                linear_time, _ = linear_search(i)
                dict_time, _ = dictionary_lookup(i)
                linear_times.append(linear_time)
                dict_times.append(dict_time)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps(
                    {
                        "linear_search_avg_time": sum(linear_times) / len(linear_times),
                        "dictionary_lookup_avg_time": sum(dict_times) / len(dict_times),
                    }
                ).encode()
            )
        else:
            self.send_error(404, "Not Found")

    def _handle_post_requests(self):
        if self.path == "/transactions":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_transaction = json.loads(post_data)
            new_transaction["id"] = len(transactions)
            transactions.append(new_transaction)
            transactions_dict[new_transaction["id"]] = new_transaction
            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(new_transaction).encode())
        else:
            self.send_error(404, "Not Found")

    def _handle_put_requests(self):
        if self.path.startswith("/transactions/"):
            try:
                transaction_id = int(self.path.split("/")[-1])
                if transaction_id in transactions_dict:
                    content_length = int(self.headers["Content-Length"])
                    post_data = self.rfile.read(content_length)
                    updated_data = json.loads(post_data)

                    transactions_dict[transaction_id].update(updated_data)
                    # also update the list
                    for i, t in enumerate(transactions):
                        if t["id"] == transaction_id:
                            transactions[i].update(updated_data)
                            break

                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(
                        json.dumps(transactions_dict[transaction_id]).encode()
                    )
                else:
                    self.send_error(404, "Transaction not found")
            except ValueError:
                self.send_error(400, "Invalid transaction ID")
        else:
            self.send_error(404, "Not Found")

    def _handle_delete_requests(self):
        if self.path.startswith("/transactions/"):
            try:
                transaction_id = int(self.path.split("/")[-1])
                if transaction_id in transactions_dict:
                    del transactions_dict[transaction_id]
                    transactions[:] = [
                        t for t in transactions if t["id"] != transaction_id
                    ]
                    self.send_response(204)
                    self.end_headers()
                else:
                    self.send_error(404, "Transaction not found")
            except ValueError:
                self.send_error(400, "Invalid transaction ID")
        else:
            self.send_error(404, "Not Found")

    def do_request_with_auth(self, method):
        auth_header = self.headers.get("Authorization")
        if auth_header is None:
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="User Visible Realm"')
            self.end_headers()
            self.wfile.write(b"Authentication required")
            return

        auth_type, auth_string = auth_header.split(" ")
        if auth_type.lower() != "basic":
            self.send_error(401, "Unsupported authentication scheme")
            return

        decoded_credentials = base64.b64decode(auth_string).decode("utf-8")
        username, password = decoded_credentials.split(":")

        if username == USERNAME and password == PASSWORD:
            method()
        else:
            self.send_error(401, "Invalid credentials")

    def do_GET(self):
        self.do_request_with_auth(self._handle_get_requests)

    def do_POST(self):
        self.do_request_with_auth(self._handle_post_requests)

    def do_PUT(self):
        self.do_request_with_auth(self._handle_put_requests)

    def do_DELETE(self):
        self.do_request_with_auth(self._handle_delete_requests)


Handler = MyHttpRequestHandler

with socketserver.TCPServer(("", 8000), Handler) as httpd:
    print("serving at port", 8000)
    httpd.serve_forever()
