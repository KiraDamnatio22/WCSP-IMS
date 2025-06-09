import customtkinter as ctk
from PIL import Image

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class SidebarApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Wintercool Inventory Management")
        self.geometry("1200x700+200+55")
        self.iconbitmap("icons/wcsp_logo.ico")

        self.active_button = None
        self.nav_items = {}

        # Load icons
        self.icons = {
            "Home": ctk.CTkImage(light_image=Image.open("icons/home.png"), size=(20, 20)),
            "Inventory": ctk.CTkImage(light_image=Image.open("icons/inventory.png"), size=(20, 20)),
            "Sales": ctk.CTkImage(light_image=Image.open("icons/sales.png"), size=(20, 20)),
            "Purchases": ctk.CTkImage(light_image=Image.open("icons/purchases.png"), size=(20, 20)),
            "Reports": ctk.CTkImage(light_image=Image.open("icons/reports.png"), size=(20, 20)),
            "Documents": ctk.CTkImage(light_image=Image.open("icons/documents.png"), size=(20, 20)),
        }

        # Load top logo image
        self.logo_image = ctk.CTkImage(light_image=Image.open("icons/inventory_main_logo.png"), size=(30, 30))

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        # Top Logo and Label section
        self.logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.logo_frame.pack(pady=20, anchor="w")

        self.logo_label = ctk.CTkLabel(self.logo_frame, image=self.logo_image, text="", width=30)
        self.logo_label.pack(side="left", padx=(6, 0))

        self.title_label = ctk.CTkLabel(self.logo_frame,  text="Inventory", font=("Arial", 20, "bold"))
        self.title_label.pack(side="left")

        # Main Content
        self.main_content = ctk.CTkFrame(self)
        self.main_content.pack(side="right", expand=True, fill="both")

        # Pages
        self.pages = {}
        self.create_pages()

        # Navigation items
        nav_labels = list(self.icons.keys())
        for label in nav_labels:
            btn = ctk.CTkButton(
                self.sidebar, 
                text=label, 
                image=self.icons[label],
                anchor="w", 
                width=200, 
                height=40, 
                font=("Arial", 14),
                fg_color="transparent",
                text_color="black",
                hover_color="#1f6aa5",
                command=lambda l=label: self.select_nav(l))
            btn.pack(pady=2, fill="x")
            self.nav_items[label] = btn

        self.select_nav("Home")

    def create_pages(self):
        for label in self.icons:
            frame = ctk.CTkFrame(self.main_content)
            ctk.CTkLabel(frame, text=f"This is the {label} page", font=("Arial", 24)).pack(pady=50)
            self.pages[label] = frame

    def select_nav(self, selected_label):
        for label, btn in self.nav_items.items():
            btn.configure(fg_color="#1f6aa5" if label == selected_label else "transparent")

        # Show the selected page
        for label, frame in self.pages.items():
            frame.pack_forget()

        self.pages[selected_label].pack(fill="both", expand=True)

if __name__ == "__main__":
    app = SidebarApp()
    app.mainloop()
