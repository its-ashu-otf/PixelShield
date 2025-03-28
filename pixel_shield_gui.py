import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pixel_shield import encrypt_image, decrypt_image, SUPPORTED_FORMATS
import os
from PIL import Image, ImageTk
import io

# Get all supported extensions
SUPPORTED_EXTENSIONS = [ext for formats in SUPPORTED_FORMATS.values() for ext in formats]

class PixelShieldGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PixelShield - Image Encryption Tool")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")
        
        # Create main container
        container = ttk.Frame(root)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Create banner frame
        banner_frame = tk.Frame(container, bg="#3498db", height=150)
        banner_frame.pack(fill=tk.X, pady=(0, 20))
        banner_frame.pack_propagate(False)
        
        # Create banner text
        banner_text = tk.Label(
            banner_frame,
            text="PixelShield",
            font=("Helvetica", 36, "bold"),
            fg="white",
            bg="#3498db"
        )
        banner_text.pack(pady=20)
        
        # Create subtitle
        subtitle_text = tk.Label(
            banner_frame,
            text=f"Secure Image Encryption Tool - Supporting {len(SUPPORTED_FORMATS)} Image Formats",
            font=("Helvetica", 14),
            fg="white",
            bg="#3498db"
        )
        subtitle_text.pack()
        
        # Create main content frame
        main_frame = ttk.Frame(container, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Style configuration
        style = ttk.Style()
        style.configure("TButton", padding=10, font=("Helvetica", 10))
        style.configure("TLabel", padding=5, font=("Helvetica", 10))
        style.configure("TEntry", padding=5)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create encryption tab
        encrypt_tab = ttk.Frame(notebook)
        notebook.add(encrypt_tab, text="Encrypt")
        
        # Create decryption tab
        decrypt_tab = ttk.Frame(notebook)
        notebook.add(decrypt_tab, text="Decrypt")
        
        # Encryption tab content
        encrypt_frame = ttk.LabelFrame(encrypt_tab, text="Encryption", padding="10")
        encrypt_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Input file selection for encryption
        ttk.Label(encrypt_frame, text="Input Image:").pack(anchor=tk.W)
        input_container = ttk.Frame(encrypt_frame)
        input_container.pack(fill=tk.X, pady=5)
        self.input_path = tk.StringVar()
        input_entry = ttk.Entry(input_container, textvariable=self.input_path)
        input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(input_container, text="Browse", command=self.browse_input).pack(side=tk.RIGHT)
        
        # Output file selection for encryption
        ttk.Label(encrypt_frame, text="Output File:").pack(anchor=tk.W)
        output_container = ttk.Frame(encrypt_frame)
        output_container.pack(fill=tk.X, pady=5)
        self.output_path = tk.StringVar()
        output_entry = ttk.Entry(output_container, textvariable=self.output_path)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(output_container, text="Browse", command=self.browse_output).pack(side=tk.RIGHT)
        
        # Encryption password
        ttk.Label(encrypt_frame, text="Encryption Password:").pack(anchor=tk.W)
        self.encrypt_password = tk.StringVar()
        encrypt_password_entry = ttk.Entry(encrypt_frame, textvariable=self.encrypt_password, show="•")
        encrypt_password_entry.pack(fill=tk.X, pady=5)
        
        # Encryption button
        encrypt_btn = ttk.Button(
            encrypt_frame,
            text="Encrypt Image",
            command=self.encrypt,
            style="Accent.TButton"
        )
        encrypt_btn.pack(pady=10)
        
        # Decryption tab content
        decrypt_frame = ttk.LabelFrame(decrypt_tab, text="Decryption", padding="10")
        decrypt_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Input file selection for decryption
        ttk.Label(decrypt_frame, text="Encrypted File:").pack(anchor=tk.W)
        decrypt_input_container = ttk.Frame(decrypt_frame)
        decrypt_input_container.pack(fill=tk.X, pady=5)
        self.decrypt_input_path = tk.StringVar()
        decrypt_input_entry = ttk.Entry(decrypt_input_container, textvariable=self.decrypt_input_path)
        decrypt_input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(decrypt_input_container, text="Browse", command=self.browse_decrypt_input).pack(side=tk.RIGHT)
        
        # Output file selection for decryption
        ttk.Label(decrypt_frame, text="Output Image:").pack(anchor=tk.W)
        decrypt_output_container = ttk.Frame(decrypt_frame)
        decrypt_output_container.pack(fill=tk.X, pady=5)
        self.decrypt_output_path = tk.StringVar()
        decrypt_output_entry = ttk.Entry(decrypt_output_container, textvariable=self.decrypt_output_path)
        decrypt_output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(decrypt_output_container, text="Browse", command=self.browse_decrypt_output).pack(side=tk.RIGHT)
        
        # Decryption password
        ttk.Label(decrypt_frame, text="Decryption Password:").pack(anchor=tk.W)
        self.decrypt_password = tk.StringVar()
        decrypt_password_entry = ttk.Entry(decrypt_frame, textvariable=self.decrypt_password, show="•")
        decrypt_password_entry.pack(fill=tk.X, pady=5)
        
        # Decryption button
        decrypt_btn = ttk.Button(
            decrypt_frame,
            text="Decrypt Image",
            command=self.decrypt,
            style="Accent.TButton"
        )
        decrypt_btn.pack(pady=10)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.pack(fill=tk.X, pady=10)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack()
        
        # Configure custom styles
        style.configure("Accent.TButton", background="#3498db", foreground="white")
        
        # Bind enter key to appropriate function based on active tab
        self.root.bind('<Return>', lambda e: self.encrypt() if notebook.select() == notebook.tabs()[0] else self.decrypt())
        
    def browse_input(self):
        filename = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=[
                ("All supported images", "*" + " *".join(SUPPORTED_EXTENSIONS)),
                ("Encrypted files", "*.enc"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.input_path.set(filename)
            # Auto-set output filename
            if not self.output_path.get():
                base, ext = os.path.splitext(filename)
                if ext.lower() in SUPPORTED_EXTENSIONS:
                    self.output_path.set(base + '.enc')
                else:
                    self.output_path.set(base + '.jpg')
    
    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            title="Select Output File",
            filetypes=[
                ("All supported images", "*" + " *".join(SUPPORTED_EXTENSIONS)),
                ("Encrypted files", "*.enc"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.output_path.set(filename)
    
    def browse_decrypt_input(self):
        filename = filedialog.askopenfilename(
            title="Select Encrypted File",
            filetypes=[
                ("Encrypted files", "*.enc"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.decrypt_input_path.set(filename)
            # Auto-set output filename
            if not self.decrypt_output_path.get():
                base, ext = os.path.splitext(filename)
                self.decrypt_output_path.set(base + '.jpg')
    
    def browse_decrypt_output(self):
        filename = filedialog.asksaveasfilename(
            title="Select Output Image",
            filetypes=[
                ("All supported images", "*" + " *".join(SUPPORTED_EXTENSIONS)),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.decrypt_output_path.set(filename)
    
    def encrypt(self):
        if not self.validate_encrypt_inputs():
            return
        try:
            self.status_var.set("Encrypting...")
            self.root.update()
            encrypt_image(self.input_path.get(), self.output_path.get(), self.encrypt_password.get())
            self.status_var.set("Encryption successful!")
            messagebox.showinfo("Success", "Image encrypted successfully!")
        except Exception as e:
            self.status_var.set("Encryption failed!")
            messagebox.showerror("Error", f"Failed to encrypt image: {str(e)}")
    
    def decrypt(self):
        if not self.validate_decrypt_inputs():
            return
        try:
            self.status_var.set("Decrypting...")
            self.root.update()
            decrypt_image(self.decrypt_input_path.get(), self.decrypt_output_path.get(), self.decrypt_password.get())
            self.status_var.set("Decryption successful!")
            messagebox.showinfo("Success", "Image decrypted successfully!")
        except Exception as e:
            self.status_var.set("Decryption failed!")
            messagebox.showerror("Error", f"Failed to decrypt image: {str(e)}")
    
    def validate_encrypt_inputs(self):
        if not self.input_path.get():
            messagebox.showerror("Error", "Please select an input image")
            return False
        if not self.output_path.get():
            messagebox.showerror("Error", "Please select an output file")
            return False
        if not self.encrypt_password.get():
            messagebox.showerror("Error", "Please enter an encryption password")
            return False
            
        # Validate file existence
        if not os.path.exists(self.input_path.get()):
            messagebox.showerror("Error", f"Input file '{self.input_path.get()}' does not exist")
            return False
            
        # Validate file size
        if os.path.getsize(self.input_path.get()) == 0:
            messagebox.showerror("Error", f"Input file '{self.input_path.get()}' is empty")
            return False
            
        # Validate file format
        ext = os.path.splitext(self.input_path.get())[1].lower()
        if ext not in SUPPORTED_EXTENSIONS:
            messagebox.showerror("Error", f"Unsupported file format '{ext}'. Please select a supported image format.")
            return False
            
        return True
    
    def validate_decrypt_inputs(self):
        if not self.decrypt_input_path.get():
            messagebox.showerror("Error", "Please select an encrypted file")
            return False
        if not self.decrypt_output_path.get():
            messagebox.showerror("Error", "Please select an output image")
            return False
        if not self.decrypt_password.get():
            messagebox.showerror("Error", "Please enter a decryption password")
            return False
            
        # Validate file existence
        if not os.path.exists(self.decrypt_input_path.get()):
            messagebox.showerror("Error", f"Encrypted file '{self.decrypt_input_path.get()}' does not exist")
            return False
            
        # Validate file size
        if os.path.getsize(self.decrypt_input_path.get()) == 0:
            messagebox.showerror("Error", f"Encrypted file '{self.decrypt_input_path.get()}' is empty")
            return False
            
        return True

def main():
    root = tk.Tk()
    app = PixelShieldGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 