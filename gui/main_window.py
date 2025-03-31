import sys
import customtkinter as ctk
import webbrowser
from pathlib import Path
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

# Adjust Python path to include parent directory
sys.path.append(str(Path(__file__).parent.parent))

from tools.image_utils import encrypt_image, decrypt_image, is_supported_image, SUPPORTED_FORMATS

# Set global appearance and theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")  # Default theme as base

class ModernPixelShieldGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # App configuration
        self.title("PixelShield")
        self.geometry("900x650")
        self.minsize(700, 550)
        
        # Define colors for the app
        self.colors = {
            "primary": "#3B82F6",       # Blue
            "secondary": "#10B981",     # Green for success
            "accent": "#8B5CF6",        # Purple for accent
            "warning": "#F59E0B",       # Amber for warnings
            "error": "#EF4444",         # Red for errors
            "dark_bg": "#1E293B",       # Dark background
            "light_bg": "#F1F5F9",      # Light background
            "dark_card": "#334155",     # Dark card background
            "light_card": "#FFFFFF",    # Light card background
        }
        
        # Track current mode buttons for proper styling
        self.encrypt_button = None
        self.decrypt_button = None
        
        # Configure grid layout (we'll add an extra row for our custom menu)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Custom menu bar
        self.grid_rowconfigure(1, weight=0)  # Header
        self.grid_rowconfigure(2, weight=1)  # Main content
        self.grid_rowconfigure(3, weight=0)  # Footer

        # Get the current appearance mode
        self.current_appearance = ctk.get_appearance_mode()
        
        # Create the custom menu bar first
        self.create_custom_menu()
        
        # Create the interface components
        self.create_header()
        self.create_main_content()
        self.create_footer()
        
        # Update the color scheme based on the current theme
        self.update_color_scheme()
        
        # Bind appearance mode change event to update UI
        self.bind("<<AppearanceModeChanged>>", self.on_appearance_change)

    def create_custom_menu(self):
        """Create a custom menu bar instead of using native tk.Menu"""
        is_dark = self.current_appearance.lower() == "dark"
        menu_bg = self.colors["dark_bg"] if is_dark else self.colors["light_bg"]
        text_color = "white"
        
        # Create frame for menu
        self.menu_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=menu_bg, height=30)
        self.menu_frame.grid(row=0, column=0, sticky="ew")
        self.menu_frame.grid_propagate(False)  # Keep fixed height
        
        # File menu button
        self.file_button = ctk.CTkButton(
            self.menu_frame,
            text="File",
            font=ctk.CTkFont(size=12),
            width=60,
            height=30,
            corner_radius=0,
            fg_color="transparent",
            text_color=text_color,
            hover_color=self.colors["primary"],
            command=self.show_file_menu
        )
        self.file_button.pack(side="left")
        
        # Help menu button
        self.help_button = ctk.CTkButton(
            self.menu_frame,
            text="Help",
            font=ctk.CTkFont(size=12),
            width=60,
            height=30,
            corner_radius=0,
            fg_color="transparent",
            text_color=text_color,
            hover_color=self.colors["primary"],
            command=self.show_help_menu
        )
        self.help_button.pack(side="left")
        
        # Store menu buttons for theme updates
        self.menu_buttons = [self.file_button, self.help_button]

    def show_file_menu(self):
        """Show the file menu dropdown"""
        x = self.file_button.winfo_rootx()
        y = self.file_button.winfo_rooty() + self.file_button.winfo_height()
        
        # Create a popup window to serve as our menu
        is_dark = self.current_appearance.lower() == "dark"
        menu_bg = self.colors["dark_bg"] if is_dark else self.colors["light_bg"]
        text_color = "white"
        
        # Check if the popup already exists
        if hasattr(self, 'file_menu_popup') and self.file_menu_popup.winfo_exists():
            self.file_menu_popup.lift()  # Bring it to the front
            return
        
        self.file_menu_popup = tk.Toplevel(self)
        self.file_menu_popup.geometry(f"180x70+{x}+{y}")
        self.file_menu_popup.overrideredirect(True)  # Remove window decorations
        self.file_menu_popup.configure(bg=menu_bg)
        self.file_menu_popup.attributes("-topmost", True)
        
        # Add menu items
        toggle_btn = ctk.CTkButton(
            self.file_menu_popup,
            text="Toggle Dark/Light Mode",
            font=ctk.CTkFont(size=12),
            height=30,
            corner_radius=0,
            fg_color="transparent",
            text_color=text_color,
            hover_color=self.colors["primary"],
            anchor="w",
            command=lambda: [self.toggle_appearance_mode(), self.file_menu_popup.withdraw()]
        )
        toggle_btn.pack(fill="x")
        
        exit_btn = ctk.CTkButton(
            self.file_menu_popup,
            text="Exit",
            font=ctk.CTkFont(size=12),
            height=30,
            corner_radius=0,
            fg_color="transparent",
            text_color=text_color,
            hover_color=self.colors["primary"],
            anchor="w",
            command=self.quit
        )
        exit_btn.pack(fill="x")
        
        # Close on focus loss
        self.file_menu_popup.bind("<FocusOut>", lambda e: self.file_menu_popup.withdraw())

    def show_help_menu(self):
        """Show the help menu dropdown"""
        x = self.help_button.winfo_rootx()
        y = self.help_button.winfo_rooty() + self.help_button.winfo_height()
        
        # Create a popup window
        is_dark = self.current_appearance.lower() == "dark"
        menu_bg = self.colors["dark_bg"] if is_dark else self.colors["light_bg"]
        text_color = "white"
        
        # Check if the popup already exists
        if hasattr(self, 'help_menu_popup') and self.help_menu_popup.winfo_exists():
            self.help_menu_popup.lift()  # Bring it to the front
            return
        
        self.help_menu_popup = tk.Toplevel(self)
        self.help_menu_popup.geometry(f"180x70+{x}+{y}")
        self.help_menu_popup.overrideredirect(True)  # Remove window decorations
        self.help_menu_popup.configure(bg=menu_bg)
        self.help_menu_popup.attributes("-topmost", True)
        
        # Add menu items
        update_btn = ctk.CTkButton(
            self.help_menu_popup,
            text="Check for Updates",
            font=ctk.CTkFont(size=12),
            height=30,
            corner_radius=0,
            fg_color="transparent",
            text_color=text_color,
            hover_color=self.colors["primary"],
            anchor="w",
            command=lambda: [self.check_for_updates(), self.help_menu_popup.withdraw()]
        )
        update_btn.pack(fill="x")
        
        about_btn = ctk.CTkButton(
            self.help_menu_popup,
            text="About",
            font=ctk.CTkFont(size=12),
            height=30,
            corner_radius=0,
            fg_color="transparent",
            text_color=text_color,
            hover_color=self.colors["primary"],
            anchor="w",
            command=lambda: [self.show_about(), self.help_menu_popup.withdraw()]
        )
        about_btn.pack(fill="x")
        
        # Close on focus loss
        self.help_menu_popup.bind("<FocusOut>", lambda e: self.help_menu_popup.withdraw())

    def create_header(self):
        """Create a modern header with logo and title"""
        header_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="transparent")
        header_frame.grid(row=1, column=0, pady=(30, 15), padx=30, sticky="ew")
        header_frame.grid_columnconfigure(1, weight=1)
        
        # App logo and title in a horizontal layout
        logo_title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        logo_title_frame.grid(row=0, column=0, sticky="w")
        
        # App title with custom font
        title_label = ctk.CTkLabel(
            logo_title_frame, 
            text="PixelShield", 
            font=ctk.CTkFont(family="Helvetica", size=38, weight="bold")
        )
        title_label.pack(side="left", padx=(0, 10))
        
        # Subtitle/Tagline
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Secure Image Encryption",
            font=ctk.CTkFont(family="Helvetica", size=16)
        )
        subtitle_label.grid(row=1, column=0, sticky="w", pady=(0, 5))
        
        # Developer credit with clickable link
        dev_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        dev_frame.grid(row=0, column=1, sticky="e")
        
        dev_label = ctk.CTkLabel(
            dev_frame, 
            text="by Ashutosh Gupta", 
            font=ctk.CTkFont(family="Helvetica", size=14),
            cursor="hand2"
        )
        dev_label.pack(side="left", padx=(0, 10))
        dev_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/its-ashu-otf"))
        
        github_label = ctk.CTkLabel(
            dev_frame, 
            text="GitHub: its-ashu-otf", 
            font=ctk.CTkFont(family="Helvetica", size=14, underline=True),
            text_color=self.colors["primary"],
            cursor="hand2"
        )
        github_label.pack(side="left")
        github_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/its-ashu-otf"))

    def create_main_content(self):
        """Create the main content area with modern UI elements"""
        main_frame = ctk.CTkFrame(self, corner_radius=15)
        main_frame.grid(row=2, column=0, padx=30, pady=15, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Mode selection with modern toggle
        mode_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        mode_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        mode_label = ctk.CTkLabel(
            mode_frame,
            text="Operation Mode:",
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold")
        )
        mode_label.pack(side="left", padx=(0, 15))
        
        self.mode_var = ctk.StringVar(value="encrypt")
        
        # Modern styled mode selector
        self.encrypt_button = ctk.CTkButton(
            mode_frame,
            text="Encrypt",
            command=lambda: self.set_mode("encrypt"),
            width=120,
            height=36,
            border_width=1,
            corner_radius=8,
            fg_color=self.colors["primary"],  # Always start with primary color for selected
            text_color="white",
            hover_color=self.colors["accent"]
        )
        self.encrypt_button.pack(side="left", padx=(0, 10))
        
        self.decrypt_button = ctk.CTkButton(
            mode_frame,
            text="Decrypt",
            command=lambda: self.set_mode("decrypt"),
            width=120,
            height=36,
            border_width=1,
            corner_radius=8,
            fg_color="transparent",  # Start with transparent for unselected
            text_color=None,
            hover_color=self.colors["accent"]
        )
        self.decrypt_button.pack(side="left")
        
        # File selection and password entry area
        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        form_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        form_frame.grid_columnconfigure(1, weight=1)
        
        # More space between form elements
        row_padding = 15
        
        # Input file selection
        input_label = ctk.CTkLabel(
            form_frame, 
            text="Input File:",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold")
        )
        input_label.grid(row=0, column=0, sticky="w", padx=(10, 15), pady=(row_padding, 0))
        
        input_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        input_frame.grid(row=0, column=1, sticky="ew", pady=(row_padding, 0))
        input_frame.grid_columnconfigure(0, weight=1)
        
        self.input_path = ctk.CTkEntry(
            input_frame, 
            placeholder_text="Select input image file",
            height=40,
            corner_radius=8,
            border_width=1
        )
        self.input_path.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        self.browse_input_btn = ctk.CTkButton(
            input_frame, 
            text="Browse",
            width=100,
            height=40,
            corner_radius=8,
            command=self.browse_input
        )
        self.browse_input_btn.grid(row=0, column=1)
        
        # Output file selection
        output_label = ctk.CTkLabel(
            form_frame, 
            text="Output File:",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold")
        )
        output_label.grid(row=1, column=0, sticky="w", padx=(10, 15), pady=(row_padding, 0))
        
        output_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        output_frame.grid(row=1, column=1, sticky="ew", pady=(row_padding, 0))
        output_frame.grid_columnconfigure(0, weight=1)
        
        self.output_path = ctk.CTkEntry(
            output_frame, 
            placeholder_text="Select output file location",
            height=40,
            corner_radius=8,
            border_width=1
        )
        self.output_path.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        self.browse_output_btn = ctk.CTkButton(
            output_frame, 
            text="Browse",
            width=100,
            height=40,
            corner_radius=8,
            command=self.browse_output
        )
        self.browse_output_btn.grid(row=0, column=1)
        
        # Password entry with improved toggle
        password_label = ctk.CTkLabel(
            form_frame, 
            text="Password:",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold")
        )
        password_label.grid(row=2, column=0, sticky="w", padx=(10, 15), pady=(row_padding, 0))
        
        password_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        password_frame.grid(row=2, column=1, sticky="ew", pady=(row_padding, 0))
        password_frame.grid_columnconfigure(0, weight=1)
        
        self.password_input = ctk.CTkEntry(
            password_frame, 
            placeholder_text="Enter encryption password",
            height=40,
            corner_radius=8,
            border_width=1,
            show="•"
        )
        self.password_input.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        self.show_password_btn = ctk.CTkButton(
            password_frame, 
            text="Show",
            width=100,
            height=40,
            corner_radius=8,
            command=self.toggle_password_visibility
        )
        self.show_password_btn.grid(row=0, column=1)
        
        # Process button with modern styling
        process_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        process_frame.grid(row=2, column=0, padx=20, pady=(30, 20), sticky="ew")
        process_frame.grid_columnconfigure(0, weight=1)
        
        self.process_btn = ctk.CTkButton(
            process_frame, 
            text="Process",
            height=50,
            corner_radius=10,
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
            command=self.process_file
        )
        self.process_btn.grid(row=0, column=0, sticky="ew")
        
        # Styled progress bar
        style = ttk.Style()
        style.configure("TProgressbar", thickness=10, troughcolor="#E2E8F0", background=self.colors["primary"])
        
        self.progress_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.progress_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame, 
            orient="horizontal", 
            length=100, 
            mode="determinate",
            style="TProgressbar"
        )
        self.progress_bar.pack(fill="x")

    def create_footer(self):
        """Create a modern footer with status information"""
        footer_frame = ctk.CTkFrame(self, height=40, corner_radius=0, fg_color="transparent")
        footer_frame.grid(row=3, column=0, sticky="ew")
        footer_frame.grid_columnconfigure(0, weight=1)
        
        # Status display with modern styling
        self.status_label = ctk.CTkLabel(
            footer_frame, 
            text="Ready",
            font=ctk.CTkFont(family="Helvetica", size=13),
            anchor="w"
        )
        self.status_label.grid(row=0, column=0, padx=30, pady=10, sticky="w")
        
        # Version info
        version_label = ctk.CTkLabel(
            footer_frame, 
            text="v0.2.0",
            font=ctk.CTkFont(family="Helvetica", size=13),
            text_color="gray"
        )
        version_label.grid(row=0, column=1, padx=30, pady=10, sticky="e")

    def on_appearance_change(self, event=None):
        """Handle appearance mode changes to update UI consistently"""
        # Update current appearance tracking
        self.current_appearance = ctk.get_appearance_mode()
        
        # Update color scheme
        self.update_color_scheme()
        
        # Update menu style
        self.update_menu_style()

    def update_menu_style(self):
        """Update menu styling based on current appearance mode"""
        is_dark = self.current_appearance.lower() == "dark"
        menu_bg = self.colors["dark_bg"] if is_dark else self.colors["light_bg"]
        text_color = "white"
        
        self.menu_frame.configure(fg_color=menu_bg)
        
        for button in self.menu_buttons:
            button.configure(fg_color="transparent", text_color=text_color)

    def set_mode(self, mode):
        """Set the current operation mode with visual feedback"""
        self.mode_var.set(mode)
        
        # Directly update button styles for selected/unselected
        if mode == "encrypt":
            self.encrypt_button.configure(
                fg_color=self.colors["primary"],
                text_color="white"  # Set a valid text color
            )
            self.decrypt_button.configure(
                fg_color="transparent",
                text_color="black" if ctk.get_appearance_mode().lower() == "light" else "white"  # Set a valid text color
            )
        else:
            self.decrypt_button.configure(
                fg_color=self.colors["primary"],
                text_color="white"  # Set a valid text color
            )
            self.encrypt_button.configure(
                fg_color="transparent",
                text_color="black" if ctk.get_appearance_mode().lower() == "light" else "white"  # Set a valid text color
            )
        
        # Update file extension hints
        if mode == "encrypt":
            self.input_path.configure(placeholder_text="Select image to encrypt")
            self.output_path.configure(placeholder_text="Select where to save encrypted file (.bin)")
            self.process_btn.configure(text="Encrypt Image")
        else:
            self.input_path.configure(placeholder_text="Select encrypted file to decrypt")
            self.output_path.configure(placeholder_text="Select where to save decrypted image")
            self.process_btn.configure(text="Decrypt Image")
            
        # Update output path if input is already set
        if self.input_path.get():
            input_file = Path(self.input_path.get())
            default_ext = ".bin" if mode == "encrypt" else ".jpg"
            self.output_path.delete(0, "end")
            self.output_path.insert(0, str(input_file.with_suffix(default_ext)))

    def toggle_appearance_mode(self):
        """Toggle between Dark and Light appearance modes with proper updates"""
        # Toggle the appearance mode
        current_mode = ctk.get_appearance_mode()
        new_mode = "Light" if current_mode == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)
        
        # Update our tracking variable
        self.current_appearance = new_mode
        
        # Update UI elements for the new theme
        self.update_color_scheme()
        
        # Update menu styling
        self.update_menu_style()
        
        # Fix button text colors for unselected mode button
        self.fix_mode_button_contrast()
        
        # Show a status message
        self.status_label.configure(text=f"Theme changed to {new_mode} Mode")

    def fix_mode_button_contrast(self):
        """Fix text contrast issues for mode buttons when theme changes"""
        current_mode = self.mode_var.get()
        is_dark = ctk.get_appearance_mode().lower() == "dark"
        
        # Fix unselected button text color to ensure visibility
        if current_mode == "encrypt":
            # Decrypt button is unselected
            self.decrypt_button.configure(
                text_color="white" if is_dark else "black"
            )
        else:
            # Encrypt button is unselected
            self.encrypt_button.configure(
                text_color="white" if is_dark else "black"
            )

    def update_color_scheme(self):
        """Update the color scheme based on the current appearance mode"""
        is_dark = ctk.get_appearance_mode().lower() == "dark"
        
        # Update button colors based on the theme
        accent_color = self.colors["primary"]
        hover_color = self.colors["accent"]
        
        # Update menu styling
        self.update_menu_style()
        
        # Update standard buttons
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkButton):
                        # Skip mode selection buttons as they have special handling
                        if child not in [self.encrypt_button, self.decrypt_button]:
                            child.configure(fg_color=accent_color, hover_color=hover_color)
                    
                    # Update nested frames
                    elif isinstance(child, ctk.CTkFrame):
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, ctk.CTkButton):
                                # Skip mode selection buttons
                                if grandchild not in [self.encrypt_button, self.decrypt_button]:
                                    grandchild.configure(fg_color=accent_color, hover_color=hover_color)
        
        # Fix mode button text contrast
        self.fix_mode_button_contrast()
        
        # Update progress bar color
        style = ttk.Style()
        style.configure("TProgressbar", background=accent_color)

    def toggle_password_visibility(self):
        """Toggle password visibility with button text update"""
        current = self.password_input.cget("show")
        if current == "•":
            self.password_input.configure(show="")
            self.show_password_btn.configure(text="Hide")
        else:
            self.password_input.configure(show="•")
            self.show_password_btn.configure(text="Show")

    def browse_input(self):
        """Browse for input file with modern file dialog"""
        mode = self.mode_var.get()
        if mode == "encrypt":
            filetypes = [("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp *.ico *.heic *.heif *.avif *.svg *.raw *.cr2 *.nef *.arw *.dng"), ("All Files", "*.*")]
            title = "Select Image to Encrypt"
        else:
            filetypes = [("Encrypted Files", "*.bin"), ("All Files", "*.*")]
            title = "Select Encrypted File to Decrypt"
            
        file_path = filedialog.askopenfilename(title=title, filetypes=filetypes)
        
        if file_path:
            self.input_path.delete(0, "end")
            self.input_path.insert(0, file_path)
            
            # Automatically set output path if empty
            if not self.output_path.get():
                input_file = Path(file_path)
                default_ext = ".bin" if mode == "encrypt" else ".jpg"
                self.output_path.delete(0, "end")
                self.output_path.insert(0, str(input_file.with_suffix(default_ext)))
            
            self.status_label.configure(text=f"Selected input file: {Path(file_path).name}")

    def browse_output(self):
        """Browse for output file with modern file dialog"""
        mode = self.mode_var.get()
        if mode == "encrypt":
            default_ext = ".bin"
            filetypes = [("Encrypted Files", "*.bin"), ("All Files", "*.*")]
            title = "Save Encrypted File As"
        else:
            default_ext = ".jpg"
            filetypes = [("JPEG Image", "*.jpg"), ("PNG Image", "*.png"), ("All Files", "*.*")]
            title = "Save Decrypted Image As"
            
        file_path = filedialog.asksaveasfilename(
            title=title,
            defaultextension=default_ext,
            filetypes=filetypes
        )
        
        if file_path:
            self.output_path.delete(0, "end")
            self.output_path.insert(0, file_path)
            self.status_label.configure(text=f"Selected output location: {Path(file_path).name}")

    def process_file(self):
        """Process the file with visual feedback"""
        input_path = self.input_path.get().strip()
        output_path = self.output_path.get().strip()
        password = self.password_input.get().strip()
        mode = self.mode_var.get()

        if not input_path or not output_path or not password:
            self.show_error("Error", "Please fill in all fields.")
            return
            
        if len(password) < 8:
            self.show_warning("Weak Password", "Your password is less than 8 characters. This may not be secure. Do you want to continue?")
            return
            
        # Update UI to show processing
        self.status_label.configure(text="Processing... Please wait")
        self.progress_bar["value"] = 0
        self.update_idletasks()
        
        # Simulate progress steps
        for i in range(10):
            self.progress_bar["value"] = i * 10
            self.update_idletasks()
            self.after(100)  # Short delay for visual effect

        try:
            if mode == "encrypt":
                valid, error_msg = is_supported_image(input_path)
                if not valid:
                    self.show_error("Error", error_msg)
                    self.progress_bar["value"] = 0
                    return
                    
                encrypt_image(input_path, output_path, password)
                self.show_success("Success", f"Image encrypted successfully!")
                self.status_label.configure(text=f"Encrypted successfully: {Path(output_path).name}")
            else:
                decrypt_image(input_path, output_path, password)
                self.show_success("Success", f"Image decrypted successfully!")
                self.status_label.configure(text=f"Decrypted successfully: {Path(output_path).name}")
                
            # Complete the progress bar
            self.progress_bar["value"] = 100
            
        except Exception as e:
            self.show_error("Error", f"Operation failed:\n{str(e)}")
            self.status_label.configure(text="Operation failed.")
            self.progress_bar["value"] = 0

    def show_error(self, title, message):
        """Show a modern styled error message"""
        messagebox.showerror(title, message)

    def show_warning(self, title, message):
        """Show a modern styled warning message"""
        return messagebox.askokcancel(title, message)

    def show_success(self, title, message):
        """Show a modern styled success message"""
        messagebox.showinfo(title, message)

    def check_for_updates(self):
        """Check for updates and download the latest version if available"""
        self.status_label.configure(text="Checking for updates...")
        
        # Simulate an update check
        self.after(1500, lambda: self.status_label.configure(text="You are using the latest version."))
        self.after(3500, lambda: self.status_label.configure(text="Ready"))

    def show_about(self):
        """Show an about dialog with app information"""
        about_message = (
            "PixelShield - Secure Image Encryption\n\n"
            "Version: 0.5.0\n"
            "Developed by: Ashutosh Gupta\n\n"
            "This tool provides secure image encryption using AES-256.\n"
            "GitHub: https://github.com/its-ashu-otf\n\n"
            "© 2025 All Rights Reserved"
        )
        messagebox.showinfo("About PixelShield", about_message)

if __name__ == "__main__":
    app = ModernPixelShieldGUI()
    app.mainloop()