from astm.server import Server
from core.Dispatcher import MyDispatcher
from core.Handler import RequestHandler
from astm.asynclib import Dispatcher, loop
import errno
import logging
import socket

log = logging.getLogger(__name__)

class Server(Dispatcher):
    """Server class that listens for client connections"""
    
    dispatcher = MyDispatcher

    def __init__(self, host='localhost', port=15200, request=None, encoding=None, timeout=None):
        super(Server, self).__init__()
        
        self.host = host
        self.port = port
        self.encoding = encoding
        self.timeout = timeout
        self.requestHandler = request or RequestHandler
        self.configureConnection()

    def configureConnection(self):
        """Configure Socket Connection for the Server"""
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        if self.host and self.port:
            self.bind((self.host, self.port))
        else:
            raise ConnectionError(f"Disconnected or invalid socket state. Error code: {errno.ENOTCONN}")
        self.listen(5)

    def handle_accept(self):
        """Handle new client connections"""
        pair = self.accept()
        if pair is None:
            return
        sock, addr = pair
        log.info('New client connection from %s:%d', addr[0], addr[1])
        self.requestHandler(sock, self.dispatcher, self.encoding, timeout=self.timeout)

    def handle_read(self):
        return super().handle_read()
    
    def handle_write(self):
        return super().handle_write()

    # def serve_forever(self, timeout=30.0):        
    def serve_forever(self, timeout=1.0):
        """Start the server and handle connections indefinitely"""
        try:
            loop(timeout=timeout)
        except KeyboardInterrupt:
            log.info('Server shutting down...')
        finally:
            self.close()

if __name__ == '__main__':
    server = Server(
            host='localhost',
            port=15200,
            encoding='latin-1'
    )    
    print("Server starting on localhost:15200")
    print("Press Ctrl+C to stop the server")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
