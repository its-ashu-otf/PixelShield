import customtkinter as ctk  # Ensure you have installed customtkinter

class PixelShieldGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PixelShield - Secure Image Encryption")
        self.geometry("800x600")
        self.minsize(600, 400)

        # Create menu bar
        self.create_menu()

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        for row in range(5):
            self.grid_rowconfigure(row, weight=1)

        # Header
        header_frame = ctk.CTkFrame(self, corner_radius=10)
        header_frame.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="nsew")

        title_label = ctk.CTkLabel(header_frame, text="PixelShield", font=("Helvetica", 32, "bold"))
        title_label.grid(row=0, column=0, padx=20, pady=(10, 0))

        # ✅ Initialize process_btn before calling set_color_scheme
        self.process_btn = ctk.CTkButton(self, text="Process", command=self.process_file, height=40)
        self.process_btn.grid(row=2, column=0, pady=10, padx=20, sticky="ew")

        # ✅ Now it's safe to call set_color_scheme
        self.set_color_scheme()
        
        # At the end of __init__, after creating the menu:
        self.update_menu_style()

    def set_color_scheme(self):
        """Set the color scheme safely, ensuring widgets exist before modifying them."""
        if ctk.get_appearance_mode() == "Dark":
            btn_fg = "black"
            btn_text = "white"
        else:
            btn_fg = "white"
            btn_text = "black"

        # ✅ Ensure the button exists before modifying it
        if hasattr(self, 'process_btn') and isinstance(self.process_btn, ctk.CTkButton):
            self.process_btn.configure(fg_color=btn_fg, text_color=btn_text)

    def create_menu(self):
        """Placeholder for menu creation."""
        pass  # Implement this later

    def process_file(self):
        """Placeholder for file processing."""
        print("Processing file...")

if __name__ == "__main__":
    app = PixelShieldGUI()
    app.mainloop()

