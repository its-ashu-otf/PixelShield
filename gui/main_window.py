import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import webbrowser
import os
import ctypes
from tools.image_utils import encrypt_image, decrypt_image, is_supported_image


class PixelShieldApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure the main window
        self.title("PixelShield - Secure Image Encryption")
        self.geometry("800x600")
        self.minsize(700, 500)

        # Initialize state
        self.mode = "encrypt"
        self.dark_mode = self.detect_system_theme()  # Detect system theme

        # Apply styles
        self.style = ttk.Style(self)
        self.configure_styles()

        # Create UI components
        self.create_menu()
        self.create_header()
        self.create_mode_selection()
        self.create_file_selection()
        self.create_footer()

    def detect_system_theme(self):
        """Detect the system theme (dark or light)."""
        if os.name == "nt":  # Windows
            try:
                # Access the Windows registry to check the theme setting
                key = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
                registry = ctypes.windll.advapi32.RegOpenKeyExW
                query_value = ctypes.windll.advapi32.RegQueryValueExW
                close_key = ctypes.windll.advapi32.RegCloseKey

                # Open the registry key
                hkey = ctypes.c_void_p()
                if registry(0x80000001, key, 0, 0x20019, ctypes.byref(hkey)) == 0:
                    # Query the value of "AppsUseLightTheme"
                    value = ctypes.c_ulong()
                    value_size = ctypes.c_ulong(ctypes.sizeof(value))
                    if query_value(hkey, "AppsUseLightTheme", None, None, ctypes.byref(value), ctypes.byref(value_size)) == 0:
                        close_key(hkey)
                        return value.value == 0  # 0 means dark mode, 1 means light mode
                    close_key(hkey)
            except Exception:
                pass
        elif os.name == "posix":  # macOS/Linux
            try:
                # Check for dark mode on macOS
                if "AppleInterfaceStyle" in os.environ:
                    return os.environ["AppleInterfaceStyle"].lower() == "dark"
            except Exception:
                pass
        return False  # Default to dark mode if detection fails

    def configure_styles(self):
        """Configure styles for the application."""
        if self.dark_mode:
            self.configure(bg="#1E1E1E")
            self.style.theme_use("clam")
            self.style.configure("TLabel", background="#1E1E1E", foreground="#FFFFFF", font=("Helvetica", 12))
            self.style.configure("TButton", background="#333333", foreground="#FFFFFF", font=("Helvetica", 10))
            self.style.configure("TEntry", fieldbackground="#333333", foreground="#FFFFFF")
            self.style.configure("TFrame", background="#1E1E1E")
            self.style.configure("TProgressbar", troughcolor="#333333", background="#00FF00")
        else:
            self.configure(bg="#F7F7F7")
            self.style.theme_use("default")
            self.style.configure("TLabel", background="#F7F7F7", foreground="#000000", font=("Helvetica", 12))
            self.style.configure("TButton", background="#E0E0E0", foreground="#000000", font=("Helvetica", 10))
            self.style.configure("TEntry", fieldbackground="#FFFFFF", foreground="#000000")
            self.style.configure("TFrame", background="#F7F7F7")
            self.style.configure("TProgressbar", troughcolor="#E0E0E0", background="#0078D7")

    def toggle_dark_mode(self):
        """Toggle between dark and light modes."""
        self.dark_mode = not self.dark_mode
        self.configure_styles()

    def create_menu(self):
        """Create the menu bar."""
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Encrypt", command=lambda: self.set_mode("encrypt"))
        file_menu.add_command(label="Decrypt", command=lambda: self.set_mode("decrypt"))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        # View menu
        view_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Dark Mode", command=self.toggle_dark_mode)

        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Check for Updates", command=self.check_for_updates)

    def create_header(self):
        """Create the header section."""
        header_frame = ttk.Frame(self, padding=(10, 10))
        header_frame.pack(fill="x", pady=(10, 0))

        title_label = ttk.Label(header_frame, text="PixelShield", font=("Helvetica", 24, "bold"))
        title_label.pack(side="left", padx=(10, 20))

    def create_mode_selection(self):
        """Create the mode selection section."""
        mode_frame = ttk.Frame(self, padding=(10, 10))
        mode_frame.pack(fill="x", pady=(10, 0))

        mode_label = ttk.Label(mode_frame, text="Operation Mode:")
        mode_label.pack(side="left", padx=(10, 10))

        self.encrypt_button = ttk.Button(mode_frame, text="Encrypt", command=lambda: self.set_mode("encrypt"))
        self.encrypt_button.pack(side="left", padx=5)

        self.decrypt_button = ttk.Button(mode_frame, text="Decrypt", command=lambda: self.set_mode("decrypt"))
        self.decrypt_button.pack(side="left", padx=5)

    def create_file_selection(self):
        """Create the file selection section."""
        file_frame = ttk.Frame(self, padding=(10, 10))
        file_frame.pack(fill="both", expand=True, pady=(10, 0))

        # Input file selection
        ttk.Label(file_frame, text="Input File:").grid(row=0, column=0, sticky="w", pady=5)
        self.input_path = ttk.Entry(file_frame, width=50)
        self.input_path.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(file_frame, text="Browse", command=self.browse_input).grid(row=0, column=2, padx=5, pady=5)

        # Output file selection
        ttk.Label(file_frame, text="Output File:").grid(row=1, column=0, sticky="w", pady=5)
        self.output_path = ttk.Entry(file_frame, width=50)
        self.output_path.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(file_frame, text="Browse", command=self.browse_output).grid(row=1, column=2, padx=5, pady=5)

        # Password input
        ttk.Label(file_frame, text="Password:").grid(row=2, column=0, sticky="w", pady=5)
        self.password_input = ttk.Entry(file_frame, show="*", width=50)
        self.password_input.grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(file_frame, text="Show", command=self.toggle_password_visibility).grid(row=2, column=2, padx=5, pady=5)

        # Progress bar
        self.progress_bar = ttk.Progressbar(file_frame, length=400, mode="determinate")
        self.progress_bar.grid(row=3, column=0, columnspan=3, pady=10)

        # Process button
        ttk.Button(file_frame, text="Process", command=self.process_file).grid(row=4, column=0, columnspan=3, pady=10)

    def create_footer(self):
        """Create the footer section."""
        footer_frame = ttk.Frame(self, padding=(10, 10))
        footer_frame.pack(fill="x", pady=(10, 0))

        self.status_label = ttk.Label(footer_frame, text="Ready")
        self.status_label.pack(side="left", padx=10)

        version_label = ttk.Label(footer_frame, text="v1.0.0")
        version_label.pack(side="right", padx=10)

    def set_mode(self, mode):
        """Set the operation mode (encrypt or decrypt)."""
        self.mode = mode
        self.status_label.config(text=f"Mode: {mode.capitalize()}")

    def browse_input(self):
        """Browse for the input file."""
        filetypes = [("All Files", "*.*")]
        if self.mode == "encrypt":
            filetypes = [("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"), ("All Files", "*.*")]
        file_path = filedialog.askopenfilename(title="Select Input File", filetypes=filetypes)
        if file_path:
            self.input_path.delete(0, tk.END)
            self.input_path.insert(0, file_path)

    def browse_output(self):
        """Browse for the output file."""
        filetypes = [("All Files", "*.*")]
        if self.mode == "encrypt":
            filetypes = [("Encrypted Files", "*.bin"), ("All Files", "*.*")]
        else:
            filetypes = [("Image Files", "*.jpg *.jpeg *.png *.bmp"), ("All Files", "*.*")]
        file_path = filedialog.asksaveasfilename(title="Select Output File", filetypes=filetypes)
        if file_path:
            self.output_path.delete(0, tk.END)
            self.output_path.insert(0, file_path)

    def toggle_password_visibility(self):
        """Toggle the visibility of the password input."""
        if self.password_input.cget("show") == "*":
            self.password_input.config(show="")
        else:
            self.password_input.config(show="*")

    def process_file(self):
        """Process the file based on the selected mode."""
        input_path = self.input_path.get().strip()
        output_path = self.output_path.get().strip()
        password = self.password_input.get().strip()

        if not input_path or not output_path:
            messagebox.showerror("Error", "Please select input and output files.")
            return

        if not password:
            messagebox.showerror("Error", "Please enter a password.")
            return

        if len(password) < 8:
            if not messagebox.askyesno("Weak Password", "Your password is less than 8 characters. Do you want to continue?"):
                return

        self.status_label.config(text="Processing... Please wait")
        self.progress_bar["value"] = 10
        self.update_idletasks()

        try:
            if self.mode == "encrypt":
                valid, error_msg = is_supported_image(input_path)
                if not valid:
                    messagebox.showerror("Error", error_msg)
                    self.status_label.config(text="Ready")
                    self.progress_bar["value"] = 0
                    return

                encrypt_image(input_path, output_path, password)
                messagebox.showinfo("Success", f"Image encrypted successfully.\nSaved to: {output_path}")
            else:
                decrypt_image(input_path, output_path, password)
                messagebox.showinfo("Success", f"Image decrypted successfully.\nSaved to: {output_path}")

            self.progress_bar["value"] = 100
            self.status_label.config(text="Operation completed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Operation failed: {str(e)}")
            self.status_label.config(text="Operation failed.")
            self.progress_bar["value"] = 0

    def open_github(self):
        """Open the GitHub repository."""
        webbrowser.open("https://github.com/its-ashu-otf")

    def show_about(self):
        """Show the About dialog."""
        messagebox.showinfo(
            "About PixelShield",
            "PixelShield - Secure Image Encryption Tool\n"
            "Version 1.0.0\n"
            "Developed by Ashutosh Gupta\n\n"
            "GitHub: https://github.com/its-ashu-otf"
        )

    def check_for_updates(self):
        """Check for updates."""
        # Simulate checking for updates
        messagebox.showinfo("Check for Updates", "You are using the latest version of PixelShield.")


if __name__ == "__main__":
    app = PixelShieldApp()
    app.mainloop()