import customtkinter as ctk

from main_window import IMSApp
from utility.tools import resize_image

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class LoginPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Wintercool PMS Login")
        self.geometry("800x500+260+100")
        self.iconbitmap('icons/wcsp_logo.ico')
        self.resizable(False, False)
        # self.overrideredirect(True)

        self.grid_columnconfigure((1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.selected_role = None

        self.left_frame = ctk.CTkFrame(self, width=450, height=500, corner_radius=0)
        self.left_frame.grid(row=0, column=0)
        # left_frame.grid(row=0, column=0, sticky="nsew")
        self.left_frame.grid_propagate(False)

        bg_image = resize_image("icons/login/WCSP-IMS-BG.png", (400, 500))

        image_label = ctk.CTkLabel(self.left_frame, text="", image=bg_image)
        image_label.pack(fill="both", expand=True)

        self.right_frame = ctk.CTkFrame(self, width=450, height=500, corner_radius=0, fg_color='white')
        self.right_frame.grid(row=0, column=1, sticky="nsew", )
        self.right_frame.grid_propagate(False)
        

        # Widgets inside right frame
        ctk.CTkLabel(self.right_frame, text="Welcome Back!", font=ctk.CTkFont(size=26, weight="bold")).pack(pady=(65, 8))
        ctk.CTkLabel(self.right_frame, text="Sign in to your account", font=ctk.CTkFont(size=14)).pack(pady=(0, 30))

        ctk.CTkLabel(self.right_frame, text="Username", font=('Roboto', 16, 'bold')).pack(fill='x', padx=40)
        self.username_entry = ctk.CTkEntry(self.right_frame, placeholder_text="Enter username", width=200, font=('Arial', 14))
        self.username_entry.pack(padx=40, pady=(0, 15))

        ctk.CTkLabel(self.right_frame, text="Password", font=('Roboto', 16, 'bold')).pack(fill="x", padx=40)
        self.password_entry = ctk.CTkEntry(self.right_frame, placeholder_text="Enter password", show="●", width=200, font=('Arial', 14))
        self.password_entry.pack(padx=40, pady=(0, 20))

        dropdown = ctk.CTkOptionMenu(
            master=self.right_frame,
            values=["Admin", "Owner/Manager", "Technician"],
            height=25,
            width=105,
            font=('Segoe UI', 13, 'bold'),
            anchor='center',
            fg_color="#298753",
            button_color="#298753",
            button_hover_color="#4BAC76",
            dropdown_fg_color="#298753",
            dropdown_text_color="#dce4ee",
            dropdown_hover_color="#4BAC76",
            dropdown_font=('Segoe UI', 13, 'bold'),
            command=self.selection_change
        )
        dropdown.set("Select role")
        dropdown.pack(pady=(0, 20))

        ctk.CTkButton(self.right_frame, text="Login", fg_color="#6300EE", hover_color="#4B00B5", width=120, font=('Roboto', 14), command=self.authenticate_login).pack(padx=40)

        ctk.CTkLabel(
            self.right_frame, 
            text='Forget password?',
            text_color='red',
            font=('Raleway', 14,),
            cursor='hand2').pack(pady=(15, 0))

        # WIDGET BINDINGS
        self.username_entry.bind("<FocusIn>", lambda event: self.on_entry_focus_in(self.username_entry))
        self.password_entry.bind("<FocusIn>", lambda event: self.on_entry_focus_in(self.password_entry))

        self.right_frame.bind('<Button-1>', lambda event: self.on_entry_focus_out([self.username_entry, self.password_entry]))

    def selection_change(self, role):
        self.selected_role = role.lower()

    def authenticate_login(self):
        user = self.username_entry.get()
        pasw = self.password_entry.get()

        if user == 'admin' and pasw == '123':
            self.destroy()
            main_app = IMSApp()
            main_app.mainloop()
        else:
            print('Login Error!')

    def on_entry_focus_in(self, entry):
        entry.configure(border_color='#4B00B5')

    def on_entry_focus_out(self, entries):
        for entry in entries:
            entry.configure(border_color='#D9D9D9')

    def exit(self):
        self.destroy()


# app = LoginPage()
# app.mainloop()
