import tkinter as tk
from tkinter import scrolledtext
import serial
import threading
import time
import socket
import logging
import re

log = logging.getLogger(__name__)

ENQ = b'\x05'
ACK = b'\x06'
NAK = b'\x15'
EOT = b'\x04'
STX = b'\x02'
ETX = b'\x03'

control_map = {
    0x05: 'ENQ',
    0x06: 'ACK',
    0x15: 'NAK',
    0x04: 'EOT',
    0x02: 'STX',
    0x03: 'ETX'
}

CONTROL_CHAR_TO_BYTE = {
    'ENQ': b'\x05',
    'ACK': b'\x06',
    'NAK': b'\x15',
    'EOT': b'\x04',
    'STX': b'\x02',
    'ETX': b'\x03'
}


class ASTMAnalyzerGUI:
    def __init__(self, master):
        self.master = master
        master.title("ASTM Analyzer Simulator")
        master.geometry("1000x700")
        master.configure(bg='#f0f0f0')
    
        # Initialize variables
        self.ser = None
        self.sock = None
        self.read_thread = None
        self.reading = False
        self.port = 'COM2'
        self.baud_rate = 9600
        self.tcp_host = '127.0.0.1'
        self.tcp_port = 15200
    
        # Create main container
        main_container = tk.Frame(master, bg='#f0f0f0')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top control frame
        self.top_frame = tk.Frame(main_container, bg='#e6e6e6', relief=tk.RAISED, bd=2)
        self.top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Connection controls
        connection_frame = tk.Frame(self.top_frame, bg='#e6e6e6')
        connection_frame.pack(pady=10)
        
        tk.Label(connection_frame, text="Port:", bg='#e6e6e6', font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        tk.Label(connection_frame, text=self.port, bg='#e6e6e6', font=('Arial', 10)).pack(side=tk.LEFT, padx=(5, 15))
        
        tk.Label(connection_frame, text="Baud:", bg='#e6e6e6', font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.baud_var = tk.StringVar()
        self.baud_var.set(str(self.baud_rate))
        baud_menu = tk.OptionMenu(connection_frame, self.baud_var, "9600", "19200", "115200")
        baud_menu.configure(bg='white', font=('Arial', 9))
        baud_menu.pack(side=tk.LEFT, padx=(5, 15))
    
        # Connection buttons
        self.connect_btn = tk.Button(connection_frame, text="Connect", command=self.connect, 
                                    bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'),
                                    relief=tk.RAISED, bd=2, padx=15)
        self.connect_btn.pack(side=tk.LEFT, padx=5)
        
        self.disconnect_btn = tk.Button(connection_frame, text="Disconnect", command=self.disconnect,
                                    bg='#f44336', fg='white', font=('Arial', 10, 'bold'),
                                    relief=tk.RAISED, bd=2, padx=15)
        self.disconnect_btn.pack(side=tk.LEFT, padx=5)
        
        # Status indicator
        self.status_frame = tk.Frame(self.top_frame, bg='#e6e6e6')
        self.status_frame.pack(side=tk.RIGHT, padx=10, pady=5)
        
        tk.Label(self.status_frame, text="Status:", bg='#e6e6e6', font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.status_label = tk.Label(self.status_frame, text="Disconnected", bg='#e6e6e6', 
                                    fg='red', font=('Arial', 10, 'bold'))
        self.status_label.pack(side=tk.LEFT, padx=5)
    
        # Middle frame for log windows
        self.middle_frame = tk.Frame(main_container)
        self.middle_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Left panel for general logs
        self.logs_frame = tk.LabelFrame(self.middle_frame, text="General Logs", 
                                    font=('Arial', 11, 'bold'), bg='#f0f0f0')
        self.logs_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Log text area with scrollbar
        self.log_text = scrolledtext.ScrolledText(self.logs_frame, width=40, height=25,
                                                font=('Consolas', 9), bg='white', fg='black',
                                                wrap=tk.WORD, relief=tk.SUNKEN, bd=2)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Right panel for error logs
        self.errors_frame = tk.LabelFrame(self.middle_frame, text="Error Logs", 
                                        font=('Arial', 11, 'bold'), bg='#f0f0f0')
        self.errors_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Error text area with scrollbar
        self.error_text = scrolledtext.ScrolledText(self.errors_frame, width=40, height=25,
                                                font=('Consolas', 9), bg='#fff8f8', fg='#d32f2f',
                                                wrap=tk.WORD, relief=tk.SUNKEN, bd=2)
        self.error_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Bottom frame for input controls
        self.bottom_frame = tk.Frame(main_container, bg='#e6e6e6', relief=tk.RAISED, bd=2)
        self.bottom_frame.pack(fill=tk.X, pady=(0, 5))
    
        # Input frame
        self.input_frame = tk.Frame(self.bottom_frame, bg='#e6e6e6')
        self.input_frame.pack(pady=10)
        
        tk.Label(self.input_frame, text="Message:", bg='#e6e6e6', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 5))
        self.input_entry = tk.Entry(self.input_frame, width=60, font=('Arial', 10),
                                relief=tk.SUNKEN, bd=2)
        self.input_entry.pack(side=tk.LEFT, padx=5)
        
        self.send_btn = tk.Button(self.input_frame, text="Send", command=self.send_text,
                                bg='#2196F3', fg='white', font=('Arial', 10, 'bold'),
                                relief=tk.RAISED, bd=2, padx=15)
        self.send_btn.pack(side=tk.LEFT, padx=5)
        
        # ENQ button frame
        self.enq_frame = tk.Frame(self.bottom_frame, bg='#e6e6e6')
        self.enq_frame.pack(pady=(0, 10))
        
        self.enq_btn = tk.Button(self.enq_frame, text="Send ENQ", command=self.send_enq,
                                bg='#FF9800', fg='white', font=('Arial', 10, 'bold'),
                                relief=tk.RAISED, bd=2, padx=20)
        self.enq_btn.pack()
        
        # Control buttons frame
        self.control_frame = tk.Frame(self.bottom_frame, bg='#e6e6e6')
        self.control_frame.pack(pady=(0, 10))
        
        # Clear buttons
        self.clear_logs_btn = tk.Button(self.control_frame, text="Clear Logs", 
                                    command=self.clear_logs, bg='#9E9E9E', fg='white',
                                    font=('Arial', 9), relief=tk.RAISED, bd=2, padx=10)
        self.clear_logs_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_errors_btn = tk.Button(self.control_frame, text="Clear Errors", 
                                        command=self.clear_errors, bg='#9E9E9E', fg='white',
                                        font=('Arial', 9), relief=tk.RAISED, bd=2, padx=10)
        self.clear_errors_btn.pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to send message
        self.input_entry.bind('<Return>', lambda event: self.send_text())
        
        # Configure text widget tags for different message types
        self.log_text.tag_configure("timestamp", foreground="#1D1D1D", font=('Consolas', 8))
        self.log_text.tag_configure("sent", foreground="#0066CC", font=('Consolas', 9, 'bold'))
        self.log_text.tag_configure("received", foreground="#009900", font=('Consolas', 9, 'bold'))
        self.log_text.tag_configure("info", foreground="#1D1D1D")
        
        self.error_text.tag_configure("error", foreground="#d32f2f", font=('Consolas', 9, 'bold'))
        self.error_text.tag_configure("warning", foreground="#ff9800", font=('Consolas', 9, 'bold'))
        self.error_text.tag_configure("timestamp", foreground="#1D1D1D", font=('Consolas', 8))

    def clear_logs(self):
        """Clear all content from the general logs window"""
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, "--- General logs cleared ---\n", "info")

    def clear_errors(self):
        """Clear all content from the error logs window"""
        self.error_text.delete(1.0, tk.END)
        self.error_text.insert(tk.END, "--- Error logs cleared ---\n", "info")

    def clear_all_logs(self):
        """Clear both log windows"""
        self.clear_logs()
        self.clear_errors()

    def log(self, message, msg_type="info"):
        """
        Add a message to the general logs window
        msg_type: 'info', 'sent', 'received', 'timestamp'
        """
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        self.log_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.log_text.insert(tk.END, f"{message}\n", msg_type)
        self.log_text.see(tk.END)  # Auto-scroll to bottom

    def log_error(self, error_message, error_type="error"):
        """
        Add an error message to the error logs window
        error_type: 'error', 'warning'
        """
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        self.error_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.error_text.insert(tk.END, f"{error_message}\n", error_type)
        self.error_text.see(tk.END)

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, int(self.baud_var.get()), timeout=1)
            self.log(f"[Analyzer] Connected to {self.port} at {self.baud_var.get()} baud")
            
            # Check if socket connection succeeds
            if self.connectSocket():
                self.reading = True
                self.read_thread = threading.Thread(target=self.read_socket)
                self.read_thread.daemon = True
                self.read_thread.start()
            else:
                self.log_error("[Error] Failed to connect to socket", "error")
            
        except serial.SerialException as e:
            self.log_error(f"[Error] {e}", "error")

    def connectSocket(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setblocking(True)
            sock.connect((self.tcp_host,self.tcp_port))
            self.log(f"Successfully connected to {self.tcp_host}:{self.tcp_port}")
            self.sock = sock
            return True
        except socket.gaierror as e:
            self.log_error(f"Address-related error connecting to {self.tcp_host}:{self.tcp_port} - {e}")
        except socket.timeout as e:
            self.log_error(f"Connection to {self.tcp_host}:{self.tcp_port} timed out - {e}")
        except ConnectionRefusedError as e:
            self.log_error(f"Connection to {self.tcp_host}:{self.tcp_port} refused - {e}")
        except socket.error as e:
            self.log_error(f"Socket error while connecting to {self.tcp_host}:{self.tcp_port} - {e}")
        except Exception as e:
            self.log_error(f"Unexpected error during socket connection")
        
        return False

    def disconnect(self):
        self.reading = False
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.log("[Analyzer] Serial port disconnected")

    def read_socket(self):
        while self.reading and self.sock:
            try:
                self.sock.settimeout(1.0)
                data = self.sock.recv(4096)
            
                if data:
                    # decoded = data.decode(errors='ignore', encoding='latin-1').strip()
                    for b in data:
                        if b in control_map:
                            self.log(f"[CONTROL] - {control_map[b]}", "recv")
                        else:
                            self.log(f"[RECEIVED BYTE] - {chr(b)}", "recv")
                else:
                    self.log("[INFO] Socket connection closed by remote", "info")
                    break
                
            except socket.timeout:
                continue
            except socket.error as e:
                self.log_error(f"[Socket Error] {e}", "error")
                break
            except Exception as e:
                self.log_error(f"[Unexpected Error] {e}", "error")
                break
            
            time.sleep(0.3)
    
        # if self.sock:
        #     try:
        #         self.sock.close()
        #     except:
        #         pass
        #     self.sock = None

    def send_text(self):
        user_input = self.input_entry.get()
        try:
            parsed_msg = self.parse_input_with_control_chars(user_input)
            self.sock.sendall(parsed_msg)
            pretty = self.preetyLogger(parsed_msg)
            self.log(pretty, "send")
        except (ConnectionAbortedError, BrokenPipeError):
            self.log_error("[Error] Socket connection aborted. Please reconnect.", "error")
        except Exception as e:
            self.log_error(f"[Unexpected Error] {e}", "error")


    def parse_input_with_control_chars(self, input_str: str) -> bytes:
        """
        Converts human-friendly input like "[STX]data[ETX]" into proper ASTM bytes.
        """
        result = bytearray()
    
        # Replace known escape sequences manually
        input_str = input_str.replace('\\r', '\r').replace('\\n', '\n')
        
        # Find all parts like [STX], data, [ETX]
        tokens = re.split(r'(\[[A-Z]+\])', input_str)
    
        for token in tokens:
            match = re.match(r'\[([A-Z]+)\]', token)
            if match:
                ctrl = match.group(1)
                if ctrl in CONTROL_CHAR_TO_BYTE:
                    result.extend(CONTROL_CHAR_TO_BYTE[ctrl])
            else:
                result.extend(token.encode('latin-1'))
        
        return bytes(result)


    def preetyLogger(self, bdata: bytes):
        output_lines = []
        buffer = []
        in_astm_block = False

        for b in bdata:
            if b in control_map:
                label = control_map[b]

                if label == 'STX':
                    # Start capturing ASTM block
                    in_astm_block = True
                    buffer.append(f"[{label}]")
                elif label == 'ETX':
                    buffer.append(f"[{label}]")
                    in_astm_block = False
                else:
                    # Flush current ASTM block if exists
                    if buffer:
                        output_lines.append(''.join(buffer))
                        buffer = []
                    output_lines.append(f" - [{label}]")
            elif b == 13:  # \r (CR)
                buffer.append("[CR]")
            elif b == 10:  # \n (LF)
                buffer.append("[LF]")
            else:
                try:
                    buffer.append(chr(b))
                except:
                    buffer.append(f"[0x{b:02X}]")  # fallback for unknown byte

        if buffer:
            output_lines.append(''.join(buffer))

        return "\n".join(output_lines)

    
    def buffer_to_lines(self, buffer):
        try:
            return bytes(buffer).decode('latin-1', errors='ignore').replace('\r', '')
        except Exception:
            return repr(buffer)

    def send_enq(self):
        if self.ser and self.ser.is_open:
            self.sock.sendall(ENQ)
            b = 0x05
            self.log(f"[Sent] {control_map[b]}", "send")

if __name__ == '__main__':
    root = tk.Tk()
    app = ASTMAnalyzerGUI(root)
    root.mainloop()