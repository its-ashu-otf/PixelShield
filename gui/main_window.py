import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import os
import webbrowser
from datetime import datetime

from gui.scaling import setup_dpi_awareness, setup_scaling, get_scaled_size
from pixel_shield import encrypt_image, decrypt_image, is_supported_image, SUPPORTED_FORMATS

class PixelShieldGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PixelShield - Secure Image Encryption")
        
        # Set up DPI awareness and scaling
        setup_dpi_awareness()
        self.fonts = setup_scaling(self.root)
        
        # Configure window
        self.root.geometry("900x700")
        self.root.minsize(700, 500)
        
        # Set theme
        style = ttk.Style()
        style.theme_use('clam')  # Use clam theme for better cross-platform appearance
        
        # Configure styles
        style.configure('Title.TLabel', font=self.fonts['heading'])
        style.configure('Text.TLabel', font=self.fonts['text'])
        style.configure('Accent.TButton', font=self.fonts['text'])
        style.configure('TRadiobutton', font=self.fonts['text'])
        style.configure('TCheckbutton', font=self.fonts['text'])
        style.configure('TLabelframe.Label', font=self.fonts['text'])
        
        # Create main container
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self._create_widgets()
        self._setup_layout()
        
        # Center the window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def _create_widgets(self):
        """Create all GUI widgets."""
        # Title and version
        title_frame = ttk.Frame(self.main_frame)
        
        title_label = ttk.Label(
            title_frame,
            text="PixelShield",
            style='Title.TLabel'
        )
        
        version_label = ttk.Label(
            title_frame,
            text="v0.2.0",
            style='Text.TLabel'
        )
        
        # Developer info
        dev_frame = ttk.Frame(self.main_frame)
        
        dev_label = ttk.Label(
            dev_frame,
            text="Developed by Ashutosh Gupta",
            style='Text.TLabel'
        )
        
        github_link = ttk.Label(
            dev_frame,
            text="GitHub: its-ashu-otf",
            style='Text.TLabel',
            foreground="blue",
            cursor="hand2"
        )
        github_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/its-ashu-otf"))
        github_link.bind("<Enter>", lambda e: github_link.configure(underline=True))
        github_link.bind("<Leave>", lambda e: github_link.configure(underline=False))
        
        # Mode selection with better styling
        mode_frame = ttk.LabelFrame(self.main_frame, text="Operation Mode", padding="10")
        
        self.mode_var = tk.StringVar(value="encrypt")
        
        ttk.Radiobutton(
            mode_frame,
            text="Encrypt Image",
            variable=self.mode_var,
            value="encrypt",
            command=self._on_mode_change
        ).pack(side=tk.LEFT, padx=20)
        
        ttk.Radiobutton(
            mode_frame,
            text="Decrypt Image",
            variable=self.mode_var,
            value="decrypt",
            command=self._on_mode_change
        ).pack(side=tk.LEFT, padx=20)
        
        # File selection with better styling
        file_frame = ttk.LabelFrame(self.main_frame, text="File Selection", padding="10")
        
        self.input_path = tk.StringVar()
        ttk.Entry(
            file_frame,
            textvariable=self.input_path,
            width=60,
            font=self.fonts['text']
        ).grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Button(
            file_frame,
            text="Browse",
            command=self._browse_input,
            style='Accent.TButton'
        ).grid(row=0, column=1, padx=5, pady=5)
        
        # Password entry with show/hide toggle
        password_frame = ttk.LabelFrame(self.main_frame, text="Password", padding="10")
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(
            password_frame,
            textvariable=self.password_var,
            show="•",
            width=60,
            font=self.fonts['text']
        )
        self.password_entry.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        self.show_password = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            password_frame,
            text="Show Password",
            variable=self.show_password,
            command=self._toggle_password_visibility
        ).grid(row=0, column=1, padx=5, pady=5)
        
        # Output path with better styling
        output_frame = ttk.LabelFrame(self.main_frame, text="Output Location", padding="10")
        
        self.output_path = tk.StringVar()
        ttk.Entry(
            output_frame,
            textvariable=self.output_path,
            width=60,
            font=self.fonts['text']
        ).grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Button(
            output_frame,
            text="Browse",
            command=self._browse_output,
            style='Accent.TButton'
        ).grid(row=0, column=1, padx=5, pady=5)
        
        # Process button with better styling
        self.process_button = ttk.Button(
            self.main_frame,
            text="Process",
            command=self._process_file,
            style='Accent.TButton'
        )
        
        # Status label with better styling
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(
            self.main_frame,
            textvariable=self.status_var,
            wraplength=800,
            style='Text.TLabel'
        )
        
        # Store widgets for layout
        self.widgets = {
            'title_frame': title_frame,
            'title': title_label,
            'version': version_label,
            'dev_frame': dev_frame,
            'dev_label': dev_label,
            'github_link': github_link,
            'mode_frame': mode_frame,
            'file_frame': file_frame,
            'password_frame': password_frame,
            'output_frame': output_frame,
            'process_button': self.process_button,
            'status': self.status_label
        }
        
    def _setup_layout(self):
        """Set up the layout of widgets."""
        # Title and version
        self.widgets['title_frame'].grid(row=0, column=0, pady=(0, 10))
        self.widgets['title'].pack(side=tk.LEFT, padx=5)
        self.widgets['version'].pack(side=tk.LEFT, padx=5)
        
        # Developer info
        self.widgets['dev_frame'].grid(row=1, column=0, pady=(0, 20))
        self.widgets['dev_label'].pack(side=tk.LEFT, padx=5)
        self.widgets['github_link'].pack(side=tk.LEFT, padx=5)
        
        # Mode selection
        self.widgets['mode_frame'].grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # File selection
        self.widgets['file_frame'].grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Password
        self.widgets['password_frame'].grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Output location
        self.widgets['output_frame'].grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Process button
        self.widgets['process_button'].grid(row=6, column=0, pady=(0, 10))
        
        # Status label
        self.widgets['status'].grid(row=7, column=0, sticky=(tk.W, tk.E))
        
    def _toggle_password_visibility(self):
        """Toggle password visibility."""
        if self.show_password.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="•")
            
    def _on_mode_change(self):
        """Handle mode change between encrypt and decrypt."""
        mode = self.mode_var.get()
        self.process_button.config(
            text="Encrypt" if mode == "encrypt" else "Decrypt"
        )
        
    def _browse_input(self):
        """Open file dialog for input file selection."""
        mode = self.mode_var.get()
        if mode == "encrypt":
            filetypes = [("Image files", "*" + " *".join([ext for formats in SUPPORTED_FORMATS.values() for ext in formats]))]
        else:
            filetypes = [("Encrypted files", "*.bin")]
            
        filename = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=filetypes
        )
        if filename:
            self.input_path.set(filename)
            # Set default output path
            if not self.output_path.get():
                input_path = Path(filename)
                if mode == "encrypt":
                    output_path = input_path.with_suffix('.bin')
                else:
                    # Try to determine original extension
                    output_path = input_path.with_suffix('.jpg')
                self.output_path.set(str(output_path))
                
    def _browse_output(self):
        """Open file dialog for output file selection."""
        mode = self.mode_var.get()
        if mode == "encrypt":
            filetypes = [("Encrypted files", "*.bin")]
        else:
            filetypes = [("Image files", "*" + " *".join([ext for formats in SUPPORTED_FORMATS.values() for ext in formats]))]
            
        filename = filedialog.asksaveasfilename(
            title="Select Output Location",
            filetypes=filetypes,
            defaultextension=".bin" if mode == "encrypt" else ".jpg"
        )
        if filename:
            self.output_path.set(filename)
            
    def _process_file(self):
        """Process the file (encrypt or decrypt)."""
        input_path = self.input_path.get()
        output_path = self.output_path.get()
        password = self.password_var.get()
        
        if not input_path or not output_path or not password:
            messagebox.showerror(
                "Error",
                "Please fill in all fields"
            )
            return
            
        try:
            mode = self.mode_var.get()
            if mode == "encrypt":
                # Validate input file
                is_valid, error_msg = is_supported_image(input_path)
                if not is_valid:
                    messagebox.showerror("Error", error_msg)
                    return
                    
                encrypt_image(input_path, output_path, password)
                self.status_var.set(f"Successfully encrypted: {output_path}")
            else:
                decrypt_image(input_path, output_path, password)
                self.status_var.set(f"Successfully decrypted: {output_path}")
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def run(self):
        """Start the GUI application."""
        self.root.mainloop() 