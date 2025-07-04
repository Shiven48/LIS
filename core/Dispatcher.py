from astm.server import BaseRecordsDispatcher
from Analyzers.Bs240.Protocol.Astm.Records.HeaderRecord import ExtraHeaderFields
from Analyzers.Bs240.Protocol.Astm.Records.PatientRecord import ExtendedPatientRecord
from Analyzers.Bs240.Protocol.Astm.Records.OrderRecord import ExtendedOrderRecord
from Analyzers.Bs240.Protocol.Astm.Records.ResultRecord import ExtendedResultRecord
from Analyzers.Bs240.Protocol.Astm.Records.CommentRecord import ExtendedCommentRecord
from astm.records import TerminatorRecord

class MyDispatcher(BaseRecordsDispatcher):

    def __init__(self, encoding=None):
        super(MyDispatcher, self).__init__(encoding)

        self.wrappers = {
            'H': ExtraHeaderFields,
            'P': ExtendedPatientRecord,
            'O': ExtendedOrderRecord,
            'R': ExtendedResultRecord,
            'C': ExtendedCommentRecord,
            # 'Q': QueryRecord,
            'L': TerminatorRecord
        }
        self.dispatch['M'] = self.my_handler

    def my_handler(self, record):
        print("Received Machine Record:", record)

    def on_header(self, record):
        print("Received Header:", record)

    def on_patient(self, record):
        print("Received Patient:", record)

    def on_order(self, record):
        print("Received Order:", record)

    def on_result(self, record):
        print("Received Result:", record)

    def on_comment(self, record):
        print("Received Comment:", record)

    def on_terminator(self, record):
        print("Received Terminator:", record)

    def on_unknown(self, record):
        print("Unknown record type:", record)

    def _default_handler(self, record):
        print("Unhandled record:", record)
