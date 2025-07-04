from astm.constants import ENCODING 
import logging

log = logging.getLogger(__name__)

class BaseRecordsDispatcher(object):
    encoding = ENCODING
    def __init__(self, encoding=None):
        self.encoding = encoding or self.encoding
        self.dispatch = {
            'H': self.on_header,
            'P': self.on_patient,
            'O': self.on_order,
            'R': self.on_result,
            'C': self.on_comment,
            'Q': self.on_query,
            'L': self.on_terminator
        }
        self.wrappers = {}

    def __call__(self, message):
        seq, records, cs = (message, self.encoding)
        for record in records:
            self.dispatch.get(record[0], self.on_unknown)(self.wrap(record))

    def wrap(self, record):
        rtype = record[0]
        if rtype in self.wrappers:
            return self.wrappers[rtype](*record)
        return record

    def _default_handler(self, record):
        log.warning('Record remains unprocessed: %s', record)

    def on_header(self, record):
        """Header record handler."""
        self._default_handler(record)

    def on_comment(self, record):
        """Comment record handler."""
        self._default_handler(record)

    def on_patient(self, record):
        """Patient record handler."""
        self._default_handler(record)

    def on_order(self, record):
        """Order record handler."""
        self._default_handler(record)

    def on_result(self, record):
        """Result record handler."""
        self._default_handler(record)

    def on_query(self, record):
        """Query reocrd handler to get patient info from LIS 
            Analyzer => host
        """
        self._default_handler(record)

    def on_terminator(self, record):
        """Terminator record handler."""
        self._default_handler(record)

    def on_unknown(self, record):
        """Raise Error and log the error"""
        self._default_handler(record)
