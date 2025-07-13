import logging
import http.server
import socketserver
import getpass

class MyHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        logging.info("%s - - [%s] %s\n" % (
            self.client_address[0],
            self.log_date_time_string(),
            format%args
        ))

logging.basicConfig(
    filename="/log/http-server.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logging.getlogger().addHandler(logging.StreamHandler())
logging.info('inicializando...')
PORT = 8080

httpd = socketserver.TCPServer(("", PORT), MyHTTPHandler)
logging.info(f'Escutando a porta: {PORT}')
logging.info(f'Usuário: {getpass.getuser()}')
httpd.serve_forever()
