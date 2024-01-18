from http.server import BaseHTTPRequestHandler, HTTPServer,os
import json
import urllib.parse

file_path = "data.txt"
token_str = open('token.txt', 'r').read()
port = "5678"
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url_path = urllib.parse.urlparse(self.path)
        if url_path.path == '/get_ip_data':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
        
            data ="no ip"
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    data = file.read()
            self.wfile.write(bytes(data, "utf8"))
        elif url_path.path == '/nas':
            data ="{'ip':''}"
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    data = file.read()
            ip_map = json.loads(data)
            ip_str = ip_map['ip']
            self.send_response(302)
            self.send_header('Location', 'http://[{}]:{}'.format(ip_str,port))
            self.end_headers()

        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes("empty", "utf8"))
        return
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        url_path = urllib.parse.urlparse(self.path)
        query_components = urllib.parse.parse_qs(url_path.query)
        token_check_pass = False
        if 'token' in query_components and query_components['token'][0] == token_str:
            print("input token is not correct")
            token_check_pass = True
        if token_check_pass and url_path.path == '/receive_ip_data':
            with open(file_path, 'w') as f:
                    f.write(json.dumps(data))

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Success')
        else:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b'Forbidden')

def run(server_class=HTTPServer, handler_class=RequestHandler, port=4999):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
