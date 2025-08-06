import customtkinter as ctk
from PIL import Image

from permissions import admin_access_list

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class IMSApp(ctk.CTk):
    def __init__(self, role="Guest", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Wintercool IMS")
        self.geometry("1350x650+8+20")
        self.iconbitmap("icons/wcsp_logo.ico")
        self.resizable(False, False)
        # self.overrideredirect(True)

        self.nav_items = {}
        self.role = role

        # Load icons
        self.icons = {
            "Home": ctk.CTkImage(light_image=Image.open("icons/navigation/home.png"), size=(20, 20)),
            "Inventory": ctk.CTkImage(light_image=Image.open("icons/navigation/inventory.png"), size=(20, 20)),
            "Requests": ctk.CTkImage(light_image=Image.open("icons/navigation/requests.png"), size=(20, 20)),
            "Purchases": ctk.CTkImage(light_image=Image.open("icons/navigation/purchases.png"), size=(20, 20)),
            "Suppliers": ctk.CTkImage(light_image=Image.open("icons/navigation/suppliers.png"), size=(20, 20)),
            "Reports": ctk.CTkImage(light_image=Image.open("icons/navigation/reports.png"), size=(20, 20)),
            "Manage User": ctk.CTkImage(light_image=Image.open("icons/navigation/user_management.png"), size=(20, 20)),
            "Settings": ctk.CTkImage(light_image=Image.open("icons/navigation/settings.png"), size=(20, 20)),
            "Help": ctk.CTkImage(light_image=Image.open("icons/navigation/help.png"), size=(20, 20)),
            "Account": ctk.CTkImage(light_image=Image.open("icons/navigation/profile-24.png"), size=(20, 20)),
        }

        self.logo_image = ctk.CTkImage(light_image=Image.open("icons/navigation/inventory_main_logo.png"), size=(30, 30))

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=170, corner_radius=0, fg_color='#298753')
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Top Logo and Title
        self.logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.logo_frame.pack(pady=20, anchor="w")

        self.logo_label = ctk.CTkLabel(
            self.logo_frame, 
            width=30, 
            text_color="#ffffff",
            text=" Inventory", 
            font=("Poppins", 23, "bold"),
            image=self.logo_image, 
            compound="left",
        )
        self.logo_label.pack(
            side="left", 
            padx=(6, 0), 
            pady=(0, 50)
        )

        # Main Content
        self.main_content = ctk.CTkFrame(self, corner_radius=0, fg_color='#ffffff')
        self.main_content.pack(side="right", expand=True, fill="both")

        self.main_content.grid_rowconfigure(0, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)

        # Page containers and setup registry
        self.pages = {}
        self.page_setup_registry = {}
        self.page_instances = {}

        self.create_pages()

        # Navigation items
        for label in self.icons.keys():
            if label == "Account":
                break

            btn = ctk.CTkButton(
                self.sidebar,
                text=label, 
                image=self.icons[label],
                anchor="w",
                width=200,
                height=40,
                font=("Poppins", 13, "bold"),
                fg_color="transparent",
                text_color="#ffffff",
                # hover_color="#ffffff",
                hover=False,
                command=lambda l=label: self.select_nav(l))
            btn.pack(padx=5, pady=2, fill="x")
            self.nav_items[label] = btn

        acc_btn = ctk.CTkButton(self.sidebar, text="Account", image=self.icons["Account"], anchor="w", width=200, height=40, font=("Poppins", 13, "bold"), fg_color="transparent", text_color="#ffffff", hover_color="#ffffff", command=lambda l="Account": self.select_nav(l), hover=False)
        acc_btn.pack(padx=5, pady=(0, 15), fill="x", side='bottom')
        self.nav_items["Account"] = acc_btn

            # btn.bind('<Enter>', lambda event, b=btn: self.on_mouse_hover_on_nav(b))
            # btn.bind('<Leave>', lambda event, b=btn: self.on_mouse_hover_off_nav(b))

        self.select_nav("Inventory")
        # self.view_existing_pages()

    def create_pages(self):
        for label in self.icons:
            frame = ctk.CTkFrame(self.main_content, fg_color='#ffffff')
            frame.grid(row=0, column=0, sticky="nsew")
            self.pages[label] = frame

        # Register page here
        self.page_setup_registry = {
            "Home": self.setup_home_page,
            "Inventory": self.setup_inventory_page,
            "Requests": self.setup_requests_page,
            "Purchases": self.setup_purchases_page,
            "Suppliers": self.setup_suppliers_page,
            "Reports": self.setup_reports_page,
            "Manage User": self.setup_user_management_page,
            "Settings": self.setup_settings_page,
            "Help": self.setup_help_page,
            "Account": self.setup_account_page,
        }
    
    def select_nav(self, selected_label):
        for label, btn in self.nav_items.items():
            if label == selected_label:
                btn.configure(fg_color="#ffffff", text_color='#298753')
            else:
                btn.configure(fg_color='transparent', text_color='#ffffff')

        selected_frame = self.pages[selected_label]
        selected_frame.lift()

        # Populate page only if it hasn't been created yet
        if not selected_frame.winfo_children():
            setup_func = self.page_setup_registry.get(selected_label)
            if setup_func:
                setup_func()

    # def on_mouse_hover_on_nav(self, btn):
    #     btn.configure(text_color='#298753', hover_color="#ffffff")

    # def on_mouse_hover_off_nav(self, btn):
    #     btn.configure(text_color='#ffffff', hover_color="#ffffff")

    # PAGE SETUP METHODS
    def setup_home_page(self):
        frame = self.pages["Home"]
        ctk.CTkLabel(frame, text="Welcome to Home Page", font=("Arial", 24)).pack(pady=50)

    def setup_inventory_page(self):
        frame = self.pages["Inventory"]
        if "Inventory" not in self.page_instances:
            self.page_instances["Inventory"] = admin_access_list["Inventory"](frame)

    def setup_requests_page(self):
        frame = self.pages["Requests"]
        ctk.CTkLabel(frame, text="Requests Management", font=("Arial", 24)).pack(pady=50)

    def setup_purchases_page(self):
        frame = self.pages["Purchases"]
        ctk.CTkLabel(frame, text="View Purchase Orders", font=("Arial", 24)).pack(pady=50)

    def setup_suppliers_page(self):
        frame = self.pages["Suppliers"]
        ctk.CTkLabel(frame, text="Suppliers List", font=("Arial", 24)).pack(pady=50)

    def setup_reports_page(self):
        frame = self.pages["Reports"]
        ctk.CTkLabel(frame, text="View / Export Reports", font=("Arial", 24)).pack(pady=50)

    def setup_user_management_page(self):
        frame = self.pages["Manage User"]
        ctk.CTkLabel(frame, text="Users Management", font=("Arial", 24)).pack(pady=50)

    def setup_settings_page(self):
        frame = self.pages["Settings"]
        ctk.CTkLabel(frame, text="Manage Settings", font=("Arial", 24)).pack(pady=50)

    def setup_help_page(self):
        frame = self.pages["Help"]
        ctk.CTkLabel(frame, text="Ask Help", font=("Arial", 24)).pack(pady=50)

    def setup_account_page(self):
        frame = self.pages["Account"]
        if "Account" not in self.page_instances:
            self.page_instances["Account"] = admin_access_list["Account"](frame)

    def view_existing_pages(self):
        print(f'\n SELF.PAGES\n\n {self.pages}')
        print(f'\n PAGE.INSTANCES\n\n {self.page_instances}')

    def mainwin_exit(self):
        self.destroy()



if __name__ == "__main__":
    app = IMSApp()
    app.mainloop()
    