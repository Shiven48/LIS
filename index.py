import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import threading
import serial
import socket
import time
import requests
import json
import config

class MiddlewareGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analyzer Middleware")
        self.root.geometry("900x700")
        
        # Connection status variables
        self.serial_connected = False
        self.tcp_connected = False
        self.serial_connection = None
        self.tcp_connection = None
        
        # Data aggregation variables
        self.serial_data_buffer = []
        self.network_data_buffer = []
        self.data_received = False
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        
        # Create tabs
        self.serial_tab = ttk.Frame(self.notebook)
        self.network_tab = ttk.Frame(self.notebook)
        self.logs_tab = ttk.Frame(self.notebook)
        
        # Add tabs to notebook
        self.notebook.add(self.serial_tab, text='Serial Mode')
        self.notebook.add(self.network_tab, text='Network Mode')
        self.notebook.add(self.logs_tab, text='Logs')
        
        self.notebook.pack(expand=1, fill='both', padx=10, pady=10)
        
        # Setup all tabs
        self.setup_serial_tab()
        self.setup_network_tab()
        self.setup_logs_tab()
        
        # Log initial startup
        self.log_event("Analyzer Middleware started")

    def setup_serial_tab(self):
        # Main frame for serial tab
        main_frame = ttk.Frame(self.serial_tab)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Connection settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Serial Connection Settings")
        settings_frame.pack(fill='x', pady=(0, 10))
        
        # Port setting
        ttk.Label(settings_frame, text="Port:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.serial_port = ttk.Entry(settings_frame, width=20)
        self.serial_port.grid(row=0, column=1, padx=5, pady=5)
        self.serial_port.insert(0, config.DEFAULT_SERIAL_PORT)  
        
        # Baud rate setting
        ttk.Label(settings_frame, text="Baud Rate:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.baud_rate = ttk.Combobox(settings_frame, width=17, values=[9600, 19200, 38400, 57600, 115200])
        self.baud_rate.grid(row=1, column=1, padx=5, pady=5)
        self.baud_rate.set(config.DEFAULT_BAUD_RATE)  
        
        # Data bits setting
        ttk.Label(settings_frame, text="Data Bits:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.data_bits = ttk.Combobox(settings_frame, width=17, values=[7, 8])
        self.data_bits.grid(row=2, column=1, padx=5, pady=5)
        self.data_bits.set(config.DEFAULT_DATA_BITS)
        
        # Parity setting
        ttk.Label(settings_frame, text="Parity:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.parity = ttk.Combobox(settings_frame, width=17, values=["None", "Even", "Odd"])
        self.parity.grid(row=0, column=3, padx=5, pady=5)
        self.parity.set(config.DEFAULT_PARITY)
        
        # Stop bits setting
        ttk.Label(settings_frame, text="Stop Bits:").grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.stop_bits = ttk.Combobox(settings_frame, width=17, values=[1, 2])
        self.stop_bits.grid(row=1, column=3, padx=5, pady=5)
        self.stop_bits.set(config.DEFAULT_STOP_BITS)
        
        # Connection buttons
        button_frame = ttk.Frame(settings_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        self.serial_connect_btn = ttk.Button(button_frame, text="Connect", command=self.handle_serial_connection)
        self.serial_connect_btn.pack(side='left', padx=5)
        
        self.serial_disconnect_btn = ttk.Button(button_frame, text="Disconnect", command=self.disconnect_serial, state='disabled')
        self.serial_disconnect_btn.pack(side='left', padx=5)
        
        # Status label
        self.serial_status = ttk.Label(button_frame, text="Disconnected", foreground='red')
        self.serial_status.pack(side='left', padx=10)
        
        # API endpoint frame for serial
        api_frame_serial = ttk.LabelFrame(main_frame, text="API Endpoint Configuration")
        api_frame_serial.pack(fill='x', pady=(0, 10))
        
        ttk.Label(api_frame_serial, text="API Endpoint:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.serial_api_endpoint = ttk.Entry(api_frame_serial, width=40)
        self.serial_api_endpoint.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.serial_api_endpoint.insert(0, "http://localhost:8000/app/analyzer/parse")
        
        # API send button
        self.serial_send_api_btn = ttk.Button(api_frame_serial, text="Send to API", 
                                            command=self.send_serial_data_to_api, state='disabled')
        self.serial_send_api_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Clear buffer button
        self.serial_clear_buffer_btn = ttk.Button(api_frame_serial, text="Clear Buffer", 
                                                command=self.clear_serial_buffer)
        self.serial_clear_buffer_btn.grid(row=1, column=0, padx=5, pady=5)
        
        # Buffer status label
        self.serial_buffer_status = ttk.Label(api_frame_serial, text="Buffer: 0 messages")
        self.serial_buffer_status.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        # Configure column weight
        api_frame_serial.columnconfigure(1, weight=1)
        
        # Monitor frame
        monitor_frame = ttk.LabelFrame(main_frame, text="Serial Data Monitor (ASTM/HL7)")
        monitor_frame.pack(fill='both', expand=True)
        
        # Text widget with scrollbar
        text_frame = ttk.Frame(monitor_frame)
        text_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.serial_monitor = tk.Text(text_frame, height=15, wrap='word')
        serial_scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=self.serial_monitor.yview)
        self.serial_monitor.configure(yscrollcommand=serial_scrollbar.set)
        
        self.serial_monitor.pack(side='left', fill='both', expand=True)
        serial_scrollbar.pack(side='right', fill='y')
        
        # Clear button
        clear_serial_btn = ttk.Button(monitor_frame, text="Clear Monitor", command=lambda: self.serial_monitor.delete(1.0, tk.END))
        clear_serial_btn.pack(pady=5)

    def setup_network_tab(self):
        # Main frame for network tab
        main_frame = ttk.Frame(self.network_tab)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Connection settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Network Connection Settings")
        settings_frame.pack(fill='x', pady=(0, 10))
        
        # IP Address setting
        ttk.Label(settings_frame, text="IP Address:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.ip_address = ttk.Entry(settings_frame, width=20)
        self.ip_address.grid(row=0, column=1, padx=5, pady=5)
        self.ip_address.insert(0, "192.168.1.100")  # Default value
        
        # Port setting
        ttk.Label(settings_frame, text="Port:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.tcp_port = ttk.Entry(settings_frame, width=20)
        self.tcp_port.grid(row=1, column=1, padx=5, pady=5)
        self.tcp_port.insert(0, "2575")  # Default HL7 port
        
        # Connection type
        ttk.Label(settings_frame, text="Connection Type:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.connection_type = ttk.Combobox(settings_frame, width=17, values=["TCP Client", "TCP Server"])
        self.connection_type.grid(row=2, column=1, padx=5, pady=5)
        self.connection_type.set("TCP Client")  # Default value
        
        # Connection buttons
        button_frame = ttk.Frame(settings_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        self.tcp_connect_btn = ttk.Button(button_frame, text="Connect", command=self.handle_tcp_connection)
        self.tcp_connect_btn.pack(side='left', padx=5)
        
        self.tcp_disconnect_btn = ttk.Button(button_frame, text="Disconnect", command=self.disconnect_tcp, state='disabled')
        self.tcp_disconnect_btn.pack(side='left', padx=5)
        
        # Status label
        self.tcp_status = ttk.Label(button_frame, text="Disconnected", foreground='red')
        self.tcp_status.pack(side='left', padx=10)
        
        # API endpoint frame for network
        api_frame_network = ttk.LabelFrame(main_frame, text="API Endpoint Configuration")
        api_frame_network.pack(fill='x', pady=(0, 10))
        
        ttk.Label(api_frame_network, text="API Endpoint:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.network_api_endpoint = ttk.Entry(api_frame_network, width=40)
        self.network_api_endpoint.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.network_api_endpoint.insert(0, "http://localhost:8000/app/analyzer/parse")
        
        # API send button
        self.network_send_api_btn = ttk.Button(api_frame_network, text="Send to API", 
                                             command=self.send_network_data_to_api, state='disabled')
        self.network_send_api_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Clear buffer button
        self.network_clear_buffer_btn = ttk.Button(api_frame_network, text="Clear Buffer", 
                                                 command=self.clear_network_buffer)
        self.network_clear_buffer_btn.grid(row=1, column=0, padx=5, pady=5)
        
        # Buffer status label
        self.network_buffer_status = ttk.Label(api_frame_network, text="Buffer: 0 messages")
        self.network_buffer_status.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        # Configure column weight
        api_frame_network.columnconfigure(1, weight=1)
        
        # Monitor frame
        monitor_frame = ttk.LabelFrame(main_frame, text="Network Data Monitor (ASTM/HL7)")
        monitor_frame.pack(fill='both', expand=True)
        
        # Text widget with scrollbar
        text_frame = ttk.Frame(monitor_frame)
        text_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.network_monitor = tk.Text(text_frame, height=15, wrap='word')
        network_scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=self.network_monitor.yview)
        self.network_monitor.configure(yscrollcommand=network_scrollbar.set)
        
        self.network_monitor.pack(side='left', fill='both', expand=True)
        network_scrollbar.pack(side='right', fill='y')
        
        # Clear button
        clear_network_btn = ttk.Button(monitor_frame, text="Clear Monitor", command=lambda: self.network_monitor.delete(1.0, tk.END))
        clear_network_btn.pack(pady=5)

    def setup_logs_tab(self):
        # Main frame for logs tab
        main_frame = ttk.Frame(self.logs_tab)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Logs frame
        logs_frame = ttk.LabelFrame(main_frame, text="System Logs")
        logs_frame.pack(fill='both', expand=True)
        
        # Text widget with scrollbar
        text_frame = ttk.Frame(logs_frame)
        text_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.logs = tk.Text(text_frame, height=20, wrap='word')
        logs_scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=self.logs.yview)
        self.logs.configure(yscrollcommand=logs_scrollbar.set)
        
        self.logs.pack(side='left', fill='both', expand=True)
        logs_scrollbar.pack(side='right', fill='y')
        
        # Control buttons
        button_frame = ttk.Frame(logs_frame)
        button_frame.pack(fill='x', pady=5)
        
        ttk.Button(button_frame, text="Clear Logs", command=self.clear_logs).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Save Logs", command=self.save_logs).pack(side='left', padx=5)

    def log_event(self, message):
        """Add a timestamped message to the logs"""
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        log_message = f"{timestamp} {message}\n"
        
        # Add to logs tab
        self.logs.insert(tk.END, log_message)
        self.logs.see(tk.END)
        
        # Also print to console for debugging
        print(log_message.strip())

    def handle_serial_connection(self):
        """Handle serial connection"""
        if not self.serial_connected:
            try:
                port = self.serial_port.get()
                baud = int(self.baud_rate.get())
                databits = int(self.data_bits.get())
                
                # Convert parity setting
                parity_map = {"None": serial.PARITY_NONE, "Even": serial.PARITY_EVEN, "Odd": serial.PARITY_ODD}
                parity = parity_map[self.parity.get()]
                
                stopbits = int(self.stop_bits.get())
                
                self.log_event(f"Attempting to connect to Serial Port {port} at {baud} baud...")
                
                # Create serial connection
                self.serial_connection = serial.Serial(
                    port=port,
                    baudrate=baud,
                    bytesize=databits,
                    parity=parity,
                    stopbits=stopbits,
                    timeout=1
                )
                
                self.serial_connected = True
                self.serial_status.config(text="Connected", foreground='green')
                self.serial_connect_btn.config(state='disabled')
                self.serial_disconnect_btn.config(state='normal')
                
                self.log_event(f"Successfully connected to Serial Port {port}")
                
                # Start reading thread
                self.serial_thread = threading.Thread(target=self.read_serial_data, daemon=True)
                self.serial_thread.start()
                
            except Exception as e:
                self.log_event(f"Serial connection failed: {str(e)}")
                messagebox.showerror("Connection Error", f"Failed to connect to serial port: {str(e)}")

    def disconnect_serial(self):
        """Disconnect from serial port"""
        if self.serial_connected and self.serial_connection:
            self.serial_connected = False
            self.serial_connection.close()
            self.serial_connection = None
            
            self.serial_status.config(text="Disconnected", foreground='red')
            self.serial_connect_btn.config(state='normal')
            self.serial_disconnect_btn.config(state='disabled')
            
            # Disable API button when disconnected
            self.serial_send_api_btn.config(state='disabled')
            
            self.log_event("Serial connection disconnected")

    def read_serial_data(self):
        """Read data from serial connection in a separate thread"""
        while self.serial_connected and self.serial_connection:
            try:
                if self.serial_connection.in_waiting > 0:
                    data = self.serial_connection.readline().decode('utf-8', errors='ignore')
                    if data:
                        # Add to buffer
                        self.serial_data_buffer.append({
                            'timestamp': datetime.now().isoformat(),
                            'data': data.strip()
                        })
                        
                        # Update GUI in main thread
                        self.root.after(0, lambda: self.update_serial_monitor(data))
                        # Enable API button and update buffer status
                        self.root.after(0, lambda: self.update_serial_api_status())
                time.sleep(0.1)
            except Exception as e:
                self.root.after(0, lambda: self.log_event(f"Serial read error: {str(e)}"))
                break

    def update_serial_monitor(self, data):
        """Update serial monitor with new data"""
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        formatted_data = f"{timestamp} {data}"
        self.serial_monitor.insert(tk.END, formatted_data)
        self.serial_monitor.see(tk.END)

    def update_serial_api_status(self):
        """Update serial API button status and buffer count"""
        buffer_count = len(self.serial_data_buffer)
        self.serial_buffer_status.config(text=f"Buffer: {buffer_count} messages")
        
        # Enable API button if there's data and connection is active
        if buffer_count > 0 and self.serial_connected:
            self.serial_send_api_btn.config(state='normal')

    def send_serial_data_to_api(self):
        """Send aggregated serial data to API endpoint"""
        if not self.serial_data_buffer:
            messagebox.showwarning("No Data", "No ASTM data available to send")
            return
        
        endpoint = self.serial_api_endpoint.get().strip()
        if not endpoint:
            messagebox.showerror("Invalid Endpoint", "Please enter a valid API endpoint")
            return
        
        try:
            # Prepare payload
            payload = {
                'source': 'serial',
                'connection_info': {
                    'port': self.serial_port.get(),
                    'baud_rate': self.baud_rate.get(),
                    'data_bits': self.data_bits.get(),
                    'parity': self.parity.get(),
                    'stop_bits': self.stop_bits.get()
                },
                'data': self.serial_data_buffer.copy(),
                'total_messages': len(self.serial_data_buffer)
            }
            
            self.log_event(f"Sending {len(self.serial_data_buffer)} ASTM messages to {endpoint}")
            
            # Send POST request
            response = requests.post(
                endpoint,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                self.log_event(f"Successfully sent data to API. Response: {response.status_code}")
                
                # Clear buffer after successful send
                self.serial_data_buffer.clear()
                self.update_serial_api_status()
                
                # Show success message with response
                try:
                    response_data = response.json()
                    messagebox.showinfo("Success", f"Data sent successfully!\nMessages processed: {response_data.get('processed', 'N/A')}")
                except:
                    messagebox.showinfo("Success", f"Data sent successfully!\nResponse: {response.status_code}")
                    
            else:
                self.log_event(f"API request failed with status {response.status_code}: {response.text}")
                messagebox.showerror("API Error", f"Failed to send data. Status: {response.status_code}")
                
        except requests.exceptions.Timeout:
            self.log_event("API request timed out")
            messagebox.showerror("Timeout Error", "Request timed out. Please check the endpoint URL and try again.")
        except requests.exceptions.ConnectionError:
            self.log_event("Failed to connect to API endpoint")
            messagebox.showerror("Connection Error", "Failed to connect to API endpoint. Please check the URL and network connection.")
        except Exception as e:
            self.log_event(f"Error saving logs: {str(e)}")
            messagebox.showerror("Error", f"Failed to save logs: {str(e)}")

    def on_closing(self):
        """Handle application closing"""
        if self.serial_connected:
            self.disconnect_serial()
        if self.tcp_connected:
            self.disconnect_tcp()
        self.root.destroy()

    def clear_serial_buffer(self):
        """Clear the serial data buffer"""
        self.serial_data_buffer.clear()
        self.update_serial_api_status()
        self.log_event("Serial data buffer cleared")

    def handle_tcp_connection(self):
        """Handle TCP connection"""
        if not self.tcp_connected:
            try:
                ip = self.ip_address.get()
                port = int(self.tcp_port.get())
                conn_type = self.connection_type.get()
                
                self.log_event(f"Attempting to connect to TCP {ip}:{port} as {conn_type}...")
                
                # Create socket
                self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.tcp_socket.settimeout(5)
                
                if conn_type == "TCP Client":
                    self.tcp_socket.connect((ip, port))
                    self.tcp_connection = self.tcp_socket
                else:  # TCP Server
                    self.tcp_socket.bind((ip, port))
                    self.tcp_socket.listen(1)
                    self.log_event(f"Waiting for connection on {ip}:{port}...")
                    self.tcp_connection, addr = self.tcp_socket.accept()
                    self.log_event(f"Client connected from {addr}")
                
                self.tcp_connected = True
                self.tcp_status.config(text="Connected", foreground='green')
                self.tcp_connect_btn.config(state='disabled')
                self.tcp_disconnect_btn.config(state='normal')
                
                self.log_event(f"Successfully connected to TCP {ip}:{port}")
                
                # Start reading thread
                self.tcp_thread = threading.Thread(target=self.read_tcp_data, daemon=True)
                self.tcp_thread.start()
                
            except Exception as e:
                self.log_event(f"TCP connection failed: {str(e)}")
                messagebox.showerror("Connection Error", f"Failed to connect via TCP: {str(e)}")

    def disconnect_tcp(self):
        """Disconnect from TCP"""
        if self.tcp_connected:
            self.tcp_connected = False
            if self.tcp_connection:
                self.tcp_connection.close()
            if hasattr(self, 'tcp_socket'):
                self.tcp_socket.close()
            
            self.tcp_status.config(text="Disconnected", foreground='red')
            self.tcp_connect_btn.config(state='normal')
            self.tcp_disconnect_btn.config(state='disabled')
            
            # Disable API button when disconnected
            self.network_send_api_btn.config(state='disabled')
            
            self.log_event("TCP connection disconnected")

    def read_tcp_data(self):
        """Read data from TCP connection in a separate thread"""
        while self.tcp_connected and self.tcp_connection:
            try:
                data = self.tcp_connection.recv(1024).decode('utf-8', errors='ignore')
                if data:
                    # Add to buffer
                    self.network_data_buffer.append({
                        'timestamp': datetime.now().isoformat(),
                        'data': data.strip()
                    })
                    
                    # Update GUI in main thread
                    self.root.after(0, lambda: self.update_network_monitor(data))
                    # Enable API button and update buffer status
                    self.root.after(0, lambda: self.update_network_api_status())
                else:
                    # Connection closed by remote
                    break
                time.sleep(0.1)
            except Exception as e:
                self.root.after(0, lambda: self.log_event(f"TCP read error: {str(e)}"))
                break

    def update_network_monitor(self, data):
        """Update network monitor with new data"""
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        formatted_data = f"{timestamp} {data}\n"
        self.network_monitor.insert(tk.END, formatted_data)
        self.network_monitor.see(tk.END)

    def update_network_api_status(self):
        """Update network API button status and buffer count"""
        buffer_count = len(self.network_data_buffer)
        self.network_buffer_status.config(text=f"Buffer: {buffer_count} messages")
        
        # Enable API button if there's data and connection is active
        if buffer_count > 0 and self.tcp_connected:
            self.network_send_api_btn.config(state='normal')

    def send_network_data_to_api(self):
        """Send aggregated network data to API endpoint"""
        if not self.network_data_buffer:
            messagebox.showwarning("No Data", "No ASTM data available to send")
            return
        
        endpoint = self.network_api_endpoint.get().strip()
        if not endpoint:
            messagebox.showerror("Invalid Endpoint", "Please enter a valid API endpoint")
            return
        
        try:
            # Prepare payload
            payload = {
                'source': 'network',
                'connection_info': {
                    'ip_address': self.ip_address.get(),
                    'port': self.tcp_port.get(),
                    'connection_type': self.connection_type.get()
                },
                'data': self.network_data_buffer.copy(),
                'total_messages': len(self.network_data_buffer)
            }
            
            self.log_event(f"Sending {len(self.network_data_buffer)} ASTM messages to {endpoint}")
            
            # Send POST request
            response = requests.post(
                endpoint,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                self.log_event(f"Successfully sent data to API. Response: {response.status_code}")
                
                # Clear buffer after successful send
                self.network_data_buffer.clear()
                self.update_network_api_status()
                
                # Show success message with response
                try:
                    response_data = response.json()
                    messagebox.showinfo("Success", f"Data sent successfully!\nMessages processed: {response_data.get('processed', 'N/A')}")
                except:
                    messagebox.showinfo("Success", f"Data sent successfully!\nResponse: {response.status_code}")
                    
            else:
                self.log_event(f"API request failed with status {response.status_code}: {response.text}")
                messagebox.showerror("API Error", f"Failed to send data. Status: {response.status_code}")
                
        except requests.exceptions.Timeout:
            self.log_event("API request timed out")
            messagebox.showerror("Timeout Error", "Request timed out. Please check the endpoint URL and try again.")
        except requests.exceptions.ConnectionError:
            self.log_event("Failed to connect to API endpoint")
            messagebox.showerror("Connection Error", "Failed to connect to API endpoint. Please check the URL and network connection.")
        except Exception as e:
            self.log_event(f"Error sending data to API: {str(e)}")
            messagebox.showerror("Error", f"Failed to send data to API: {str(e)}")

    def clear_network_buffer(self):
        """Clear the network data buffer"""
        self.network_data_buffer.clear()
        self.update_network_api_status()
        self.log_event("Network data buffer cleared")

    def clear_logs(self):
        """Clear the logs"""
        self.logs.delete(1.0, tk.END)
        self.log_event("Logs cleared")

    def save_logs(self):
        """Save logs to file"""
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'w') as f:
                    f.write(self.logs.get(1.0, tk.END))
                self.log_event(f"Logs saved to {filename}")
                messagebox.showinfo("Success", f"Logs saved to {filename}")
        except Exception as e:
            self.log_event(f"Error saving logs: {str(e)}")
            messagebox.showerror("Error", f"Failed to save logs: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MiddlewareGUI(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    root.mainloop()