from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import subprocess

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        alert = json.loads(post_data.decode('utf-8'))
        print("Received alert:")
        print(json.dumps(alert, indent=2))

def kill_process_on_port(port):
    # Find process ID (PID) using netstat
    netstat_output = subprocess.check_output(['netstat', '-tuln'])
    for line in netstat_output.splitlines():
        parts = line.split()
        if len(parts) >= 4 and parts[3] == f'127.0.0.1:{port}':
            pid = parts[6].decode('utf-8').split('/')[0]
            # Kill the process
            subprocess.call(['kill', pid])
            print(f"Killed process with PID {pid}")
            return

def run(server_class=HTTPServer, handler_class=RequestHandler, port=5001):
    kill_process_on_port(port)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting HTTP server on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()