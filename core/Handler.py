import logging
from astm.protocol import ASTMProtocol 
from astm.constants import CRLF, EOT, ACK, NAK
from astm.exceptions import NotAccepted, InvalidState
from Analyzers.Bs240.Protocol.Astm.Parser.Astmparser import enhanced_decode

log = logging.getLogger(__name__)

class RequestHandler(ASTMProtocol):

    def __init__(self, sock, dispatcher, encoding, timeout=None):
        super(RequestHandler, self).__init__(sock, timeout=timeout)
        self._chunks = []
        host, port = sock.getpeername() if sock is not None else (None, None)
        self.client_info = {'host': host, 'port': port}
        self.dispatcher = dispatcher
        self._is_transfer_state = False
        self.terminator = 1
        self.encoding = encoding

    def on_enq(self):
        if not self._is_transfer_state:
            log.debug("Received the enq on server")
            self._is_transfer_state = True
            self.terminator = [CRLF, EOT]
            return ACK
        else:
            log.error('ENQ is not expected')
            return NAK
    
    def on_ack(self):
        raise NotAccepted('Server should not be ACKed.')

    def on_nak(self):
        raise NotAccepted('Server should not be NAKed.')

    def on_eot(self):
        if self._is_transfer_state:
            self._is_transfer_state = False
            self.terminator = 1
            return ACK
        else:
            raise InvalidState('Server is not ready to accept EOT message.')
            
    def on_message(self):
        if not self._is_transfer_state:
            self.discard_input_buffers()
            return NAK
        else:
            try:
                if isinstance(self._last_recv_data, str):
                    print('The last received is string converting it to bytes...')
                    self._last_recv_data = self._last_recv_data.strip().encode()
                
                parsed = enhanced_decode(self._last_recv_data)
                if not parsed:
                    return NAK
                
                return ACK
            except Exception as e:
                print('Error occurred on message handling.', e.with_traceback())
                return NAK
            
    def parse(self, message:bytes):
        """Splits a full ASTM message block into individual records."""
        return [record for record in message.decode().strip().split('\r') if record]

    def discard_input_buffers(self):
        self._chunks = []
        return super(RequestHandler, self).discard_input_buffers()

    def on_timeout(self):
        """Closes connection on timeout."""
        super(RequestHandler, self).on_timeout()
        self.close()