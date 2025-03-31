import sys
import customtkinter as ctk
import webbrowser
from pathlib import Path
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox

# Adjust Python path to include parent directory
sys.path.append(str(Path(__file__).parent.parent))

from tools.image_utils import encrypt_image, decrypt_image, is_supported_image, SUPPORTED_FORMATS

# Set global appearance before widget creation
ctk.set_appearance_mode("System")  # System default
ctk.set_default_color_theme("blue")  # Minimal blue theme

class PixelShieldGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PixelShield - Secure Image Encryption")
        self.geometry("800x600")
        self.minsize(600, 400)

        # Configure grid layout (1 column, 3 rows)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Header Frame
        header_frame = ctk.CTkFrame(self, corner_radius=10)
        header_frame.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="nsew")
        header_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(header_frame, text="PixelShield", font=("Helvetica", 32, "bold"), text_color="#4A90E2")
        title_label.grid(row=0, column=0, padx=20, pady=(10, 0))
        dev_label = ctk.CTkLabel(header_frame, text="Developed by Ashutosh Gupta | GitHub: its-ashu-otf", font=("Helvetica", 12))
        dev_label.grid(row=1, column=0, padx=20, pady=(0, 10))
        dev_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/its-ashu-otf"))

        # Main Content Frame
        content_frame = ctk.CTkFrame(self, corner_radius=10)
        content_frame.grid(row=1, column=0, pady=10, padx=20, sticky="nsew")
        content_frame.grid_columnconfigure(1, weight=1)

        # Mode Selection (Encrypt/Decrypt)
        self.mode_var = ctk.StringVar(value="encrypt")
        mode_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        mode_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")
        encrypt_radio = ctk.CTkRadioButton(mode_frame, text="Encrypt", variable=self.mode_var, value="encrypt", text_color="#4A90E2")
        decrypt_radio = ctk.CTkRadioButton(mode_frame, text="Decrypt", variable=self.mode_var, value="decrypt", text_color="#4A90E2")
        encrypt_radio.pack(side="left", padx=10)
        decrypt_radio.pack(side="left", padx=10)

        # File Input
        input_label = ctk.CTkLabel(content_frame, text="Input File:", anchor="w")
        input_label.grid(row=1, column=0, sticky="ew", padx=(20, 5), pady=5)
        self.input_path = ctk.CTkEntry(content_frame, placeholder_text="Select input file")
        self.input_path.grid(row=1, column=1, sticky="ew", padx=(5, 20), pady=5)
        browse_input_btn = ctk.CTkButton(content_frame, text="Browse", command=self.browse_input)
        browse_input_btn.grid(row=1, column=2, sticky="ew", padx=5, pady=5)

        # File Output
        output_label = ctk.CTkLabel(content_frame, text="Output File:", anchor="w")
        output_label.grid(row=2, column=0, sticky="ew", padx=(20, 5), pady=5)
        self.output_path = ctk.CTkEntry(content_frame, placeholder_text="Select output file")
        self.output_path.grid(row=2, column=1, sticky="ew", padx=(5, 20), pady=5)
        browse_output_btn = ctk.CTkButton(content_frame, text="Browse", command=self.browse_output)
        browse_output_btn.grid(row=2, column=2, sticky="ew", padx=5, pady=5)

        # Password Entry with toggle
        password_label = ctk.CTkLabel(content_frame, text="Password:", anchor="w")
        password_label.grid(row=3, column=0, sticky="ew", padx=(20, 5), pady=5)
        self.password_input = ctk.CTkEntry(content_frame, placeholder_text="Enter password", show="•")
        self.password_input.grid(row=3, column=1, sticky="ew", padx=(5, 20), pady=5)
        self.show_password_btn = ctk.CTkButton(content_frame, text="Show", width=80, command=self.toggle_password_visibility)
        self.show_password_btn.grid(row=3, column=2, sticky="ew", padx=5, pady=5)

        # Process Button
        process_btn = ctk.CTkButton(self, text="Process", command=self.process_file, height=40, fg_color="#4A90E2", text_color="white")
        process_btn.grid(row=2, column=0, pady=10, padx=20, sticky="ew")

        # Status Bar at the bottom
        self.status_label = ctk.CTkLabel(self, text="", anchor="w", text_color="#4A90E2")
        self.status_label.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew")

    def toggle_password_visibility(self):
        current = self.password_input.cget("show")
        if current == "•":
            self.password_input.configure(show="")
            self.show_password_btn.configure(text="Hide")
        else:
            self.password_input.configure(show="•")
            self.show_password_btn.configure(text="Show")

    def browse_input(self):
        file_path = filedialog.askopenfilename(title="Select Input File", filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp *.ico *.heic *.heif *.avif *.svg *.raw *.cr2 *.nef *.arw *.dng"), ("All Files", "*.*")])
        if file_path:
            self.input_path.delete(0, "end")
            self.input_path.insert(0, file_path)
            # Automatically set output path if empty
            if not self.output_path.get():
                input_file = Path(file_path)
                default_ext = ".bin" if self.mode_var.get() == "encrypt" else ".jpg"
                self.output_path.delete(0, "end")
                self.output_path.insert(0, str(input_file.with_suffix(default_ext)))

    def browse_output(self):
        def_ext = ".bin" if self.mode_var.get() == "encrypt" else ".jpg"
        file_path = filedialog.asksaveasfilename(title="Select Output File", defaultextension=def_ext, filetypes=[("All Files", "*.*")])
        if file_path:
            self.output_path.delete(0, "end")
            self.output_path.insert(0, file_path)

    def process_file(self):
        input_path = self.input_path.get().strip()
        output_path = self.output_path.get().strip()
        password = self.password_input.get().strip()

        if not input_path or not output_path or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            if self.mode_var.get() == "encrypt":
                valid, error_msg = is_supported_image(input_path)
                if not valid:
                    messagebox.showerror("Error", error_msg)
                    return
                encrypt_image(input_path, output_path, password)  # Removed algorithm argument
                self.status_label.configure(text=f"Encrypted successfully: {output_path}")
            else:
                decrypt_image(input_path, output_path, password)  # Removed algorithm argument
                self.status_label.configure(text=f"Decrypted successfully: {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Operation failed:\n{e}")
            self.status_label.configure(text="Operation failed.")

if __name__ == "__main__":
    app = PixelShieldGUI()
    app.mainloop()