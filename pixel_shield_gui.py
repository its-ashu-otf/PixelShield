import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pixel_shield import encrypt_image, decrypt_image
import os
from PIL import Image, ImageTk
import io

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
            text="Secure Image Encryption Tool",
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
        
        # Create input frame
        input_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        input_frame.pack(fill=tk.X, pady=10)
        
        # Input file selection
        ttk.Label(input_frame, text="Input File:").pack(anchor=tk.W)
        input_container = ttk.Frame(input_frame)
        input_container.pack(fill=tk.X, pady=5)
        self.input_path = tk.StringVar()
        input_entry = ttk.Entry(input_container, textvariable=self.input_path)
        input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(input_container, text="Browse", command=self.browse_input).pack(side=tk.RIGHT)
        
        # Output file selection
        ttk.Label(input_frame, text="Output File:").pack(anchor=tk.W)
        output_container = ttk.Frame(input_frame)
        output_container.pack(fill=tk.X, pady=5)
        self.output_path = tk.StringVar()
        output_entry = ttk.Entry(output_container, textvariable=self.output_path)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(output_container, text="Browse", command=self.browse_output).pack(side=tk.RIGHT)
        
        # Password frame
        password_frame = ttk.LabelFrame(main_frame, text="Security", padding="10")
        password_frame.pack(fill=tk.X, pady=10)
        
        # Password entry
        ttk.Label(password_frame, text="Password:").pack(anchor=tk.W)
        self.password = tk.StringVar()
        password_entry = ttk.Entry(password_frame, textvariable=self.password, show="•")
        password_entry.pack(fill=tk.X, pady=5)
        
        # Operation buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        # Create custom styled buttons
        encrypt_btn = ttk.Button(
            button_frame,
            text="Encrypt Image",
            command=self.encrypt,
            style="Accent.TButton"
        )
        encrypt_btn.pack(side=tk.LEFT, padx=10)
        
        decrypt_btn = ttk.Button(
            button_frame,
            text="Decrypt Image",
            command=self.decrypt,
            style="Accent.TButton"
        )
        decrypt_btn.pack(side=tk.LEFT, padx=10)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.pack(fill=tk.X, pady=10)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack()
        
        # Configure custom styles
        style.configure("Accent.TButton", background="#3498db", foreground="white")
        
        # Bind enter key to encrypt
        self.root.bind('<Return>', lambda e: self.encrypt())
        
    def browse_input(self):
        filename = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp"),
                ("Encrypted files", "*.enc"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.input_path.set(filename)
            # Auto-set output filename
            if not self.output_path.get():
                base, ext = os.path.splitext(filename)
                if ext.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
                    self.output_path.set(base + '.enc')
                else:
                    self.output_path.set(base + '.jpg')
    
    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            title="Select Output File",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp"),
                ("Encrypted files", "*.enc"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.output_path.set(filename)
    
    def encrypt(self):
        if not self.validate_inputs():
            return
        try:
            self.status_var.set("Encrypting...")
            self.root.update()
            encrypt_image(self.input_path.get(), self.output_path.get(), self.password.get())
            self.status_var.set("Encryption successful!")
            messagebox.showinfo("Success", "Image encrypted successfully!")
        except Exception as e:
            self.status_var.set("Encryption failed!")
            messagebox.showerror("Error", f"Failed to encrypt image: {str(e)}")
    
    def decrypt(self):
        if not self.validate_inputs():
            return
        try:
            self.status_var.set("Decrypting...")
            self.root.update()
            decrypt_image(self.input_path.get(), self.output_path.get(), self.password.get())
            self.status_var.set("Decryption successful!")
            messagebox.showinfo("Success", "Image decrypted successfully!")
        except Exception as e:
            self.status_var.set("Decryption failed!")
            messagebox.showerror("Error", f"Failed to decrypt image: {str(e)}")
    
    def validate_inputs(self):
        if not self.input_path.get():
            messagebox.showerror("Error", "Please select an input file")
            return False
        if not self.output_path.get():
            messagebox.showerror("Error", "Please select an output file")
            return False
        if not self.password.get():
            messagebox.showerror("Error", "Please enter a password")
            return False
        return True

def main():
    root = tk.Tk()
    app = PixelShieldGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 