import customtkinter as ctk
from PIL import Image

from .admin_features.new_item import CreateItem

class InventoryAdmin():
    def __init__(self, master):
        self.master = master
        self.counter_label = None
        self.toplevel_window = None

        """ NEW ITEM TOP LEVEL WINDOW """
        # CreateItem(self.master)

        self.products = [
            ['Photo', 'Copper Tube 3/4', '10000', 'Copper', 'Hailang', 'PCS','CompanyA', 5, 5,'Out of Stock'],
            ['Photo', 'Silver Rod 5mm', '8000','Silver', 'Metro', 'PCS', 'CompanyB', 8, 5, 'Low Stock']
        ]

        # self.products = []

        # Column config — widths and horizontal padding
        self.column_configs = [
            {"text": "Photo", "width": 60, "padx": (40, 0)},
            {"text": "Item Name", "width": 150, "padx": (20, 10)},
            {"text": "Price", "width": 65, "padx": 15},
            {"text": "Type", "width": 95, "padx": 15},
            {"text": "Brand", "width": 65, "padx": 15},
            {"text": "Unit", "width": 55, "padx": 15},
            {"text": "Supplier", "width": 65, "padx": (15, 20)},
            {"text": "Current stock", "width": 120, "padx": 10},
            {"text": "Threshold", "width": 80, "padx": 10},
            {"text": "Stock status", "width": 100, "padx": 10},
        ]

        # Title label frame
        # self.title_frame = ctk.CTkFrame(self.master, fg_color="green", corner_radius=0)
        self.title_frame = ctk.CTkFrame(self.master, fg_color="#ffffff", corner_radius=0)
        self.title_frame.pack(fill='x', ipady=15)

        # Status bar frame
        # self.status_frame = ctk.CTkFrame(self.master, fg_color="lightblue", corner_radius=0)
        self.status_frame = ctk.CTkFrame(self.master, fg_color="#ffffff", corner_radius=0)
        self.status_frame.pack(fill='x', pady=(0, 15))

        # Search bar frame
        # self.search_frame = ctk.CTkFrame(self.master, fg_color="green", corner_radius=5)
        self.search_frame = ctk.CTkFrame(self.master, fg_color="#e8e8e8", corner_radius=5)
        self.search_frame.pack(fill='x', padx=(16, 19), pady=(0, 17))

        # Main content frame
        # self.content_frame = ctk.CTkFrame(self.master, fg_color="green", corner_radius=0)
        self.content_frame = ctk.CTkFrame(self.master, fg_color="#ffffff", corner_radius=0)
        self.content_frame.pack(fill="both", expand=True)

        # Header frame
        self.header_frame = ctk.CTkFrame(self.content_frame, fg_color="#298753", corner_radius=10)
        self.header_frame.pack(fill="x", padx=(16, 20))

        # Scrollable frame for product data
        self.scrollable_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="gray")
        self.scrollable_frame.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        self.scrollable_frame._parent_canvas.bind_all("<MouseWheel>", self.on_mouse_scroll)

        self.setup_title()
        self.setup_searchbar()
        self.setup_headers()
        self.view_inventory()
        self.setup_status_bar()
        self.update_total_item_counter()

    def setup_title(self):
        inv_label = ctk.CTkLabel(self.title_frame, text='As of Month-Day-Year', font=('Raleway', 14, 'bold'), bg_color="transparent", anchor="n")
        inv_label.pack(side='right', anchor='s', padx=(0, 25), pady=(0, 4))

    def filter_and_sort_products(self):
        search_query = self.search_var.get().lower()
        sort_by = self.sort_by_var.get()
        status_filter = self.status_var.get()

        # Map sort column to index
        sort_index = {
            "Item Name": 1, "Price": 2, "Type": 3, "Brand": 4,
            "Unit": 5, "Supplier": 6
        }.get(sort_by, None)

        # Clear current view (hide frames)
        for product, frame in self.product_frames:
            frame.pack_forget()

        # Filter and sort products
        filtered = []
        for product, frame in self.product_frames:
            if search_query and search_query not in product[1].lower():
                continue
            if status_filter != "Status" and product[9] != status_filter:
                continue
            filtered.append((product, frame))

        if sort_index is not None:
            filtered.sort(key=lambda x: x[0][sort_index])

        # Show filtered, sorted frames
        for product, frame in filtered:
            frame.pack(fill="x", padx=5, pady=5)

        # Update item counters
        # self.total_item_count.configure(text=len(filtered))

    def setup_searchbar(self):
        ''' This setups the searchbar for the fast retrieval of a specific item on the table. '''
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.filter_and_sort_products())

        search_pane = ctk.CTkEntry(self.search_frame, fg_color='#ffffff', placeholder_text=' Search item', width=350, height=30, font=('Poppins', 14), border_color="#298753", textvariable=self.search_var)
        search_pane.pack(pady=10, padx=(17, 10), anchor="w", side="left")

        self.sort_by_var = ctk.StringVar(value="Sort by")
        sort_by_values = ["Item Name", "Price", "Type", "Brand", "Unit", "Supplier"]
        status_values = ["In Stock", "Low Stock", "Out of Stock"]
        sort_by_menu = ctk.CTkOptionMenu(
            master=self.search_frame,
            values=sort_by_values,
            variable=self.sort_by_var,
            height=33,
            width=145,
            font=('Poppins', 14),
            text_color="black",
            button_color="#298753",
            button_hover_color="#4BAC76",
            fg_color="white",
            dropdown_fg_color="#298753",
            dropdown_text_color="#ffffff",
            dropdown_font=('Poppins', 13),
            dropdown_hover_color="#4BAC76",
            command=lambda _: self.filter_and_sort_products()
        )
        # sort_by_menu.set("Sort by")
        sort_by_menu.pack(pady=10, padx=(0, 10), side="left")

        self.status_var = ctk.StringVar(value="Status")
        status_sort_menu = ctk.CTkOptionMenu(
            master=self.search_frame,
            values=status_values,
            variable=self.status_var,
            height=33,
            width=145,
            font=('Poppins', 14),
            text_color="black",
            button_color="#298753",
            button_hover_color="#4BAC76",
            fg_color="white",
            dropdown_fg_color="#298753",
            dropdown_text_color="#ffffff",
            dropdown_font=('Poppins', 13),
            dropdown_hover_color="#4BAC76",
            command=lambda _: self.filter_and_sort_products()
        )
        # status_sort_menu.set("Status")
        status_sort_menu.pack(pady=10, padx=(0, 10), side="left")

        self.new_item_btn = ctk.CTkButton(
            self.search_frame,
            width=120,
            fg_color="#298753",
            hover_color="#4BAC76",
            text_color="#ffffff",
            text="New Item",
            font=("Poppins", 14, "bold"),
            cursor="hand2",
            image=ctk.CTkImage(light_image=Image.open("icons/new_item_20.png"), size=(18, 18)),
            compound="left",
            border_spacing=4,
            anchor="center",
            command=self.open_new_item_window
        )
        self.new_item_btn.pack(pady=10, padx=(0, 10), side="right")

    def setup_headers(self):
        ''' This function setups the headers for the inventory product table. '''
        for col_index, col in enumerate(self.column_configs):
            header_label = ctk.CTkLabel(
                self.header_frame,
                text=col["text"],
                font=("Arial", 14, "bold"),
                text_color="#ffffff",
                width=col["width"],
                anchor="center",
                wraplength=90,
            )
            header_label.grid(row=0, column=col_index, padx=col["padx"], pady=8)
            self.header_frame.grid_columnconfigure(col_index, minsize=col["width"])

    def create_product_frame(self, product):
        frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)

        for col_index, (value, col) in enumerate(zip(product, self.column_configs)):
            label = ctk.CTkLabel(
                    frame,
                    text=value,
                    font=('Roboto', 14),
                    width=col["width"],
                    anchor="center",
                    wraplength=90,
            )
            frame.configure(fg_color="#c4c3c3" if col_index % 2 == 0 else "#e0e0e0", )
            label.grid(row=0, column=col_index, padx=col["padx"], pady=15)
        frame.pack(fill="x", padx=5, pady=5)
        return frame

    def view_inventory(self):
        ''' This function builds the entire table for the inventory products. '''   
        self.product_frames = []

        for product in self.products:
            frame = self.create_product_frame(product)
            self.product_frames.append((product, frame))

        # for row_index, product in enumerate(self.products * 4):
        #     product_frame = ctk.CTkFrame(
        #         self.scrollable_frame, 
        #         fg_color="#c4c3c3" if row_index % 2 == 0 else "#e0e0e0", 
        #         # fg_color="#d5d5d5" if row_index % 2 == 0 else "#e0e0e0", 
        #         corner_radius=10)
        #     product_frame.pack(fill="x", padx=5, pady=5)

        #     for col_index, (value, col) in enumerate(zip(product, self.column_configs)):
        #         label = ctk.CTkLabel(
        #             product_frame,
        #             text=value,
        #             font=('Roboto', 14),
        #             width=col["width"],
        #             anchor="center",
        #             wraplength=90,
        #         )
        #         label.grid(row=0, column=col_index, padx=col["padx"], pady=15)
        #         product_frame.grid_columnconfigure(col_index, minsize=col["width"])

    def setup_status_bar(self):
        ctk.CTkLabel(self.status_frame, text='View Inventory', font=('Poppins', 25, 'bold'), text_color="#298753").grid(row=0, column=0, padx=(36, 67), pady=(0, 15))

# ======================== BOX ONEEEEEEEE =============================
        total_item_status_frame = ctk.CTkFrame(self.status_frame, fg_color="#298753", width=250, height=70)
        total_item_status_frame.grid(row=0, column=1, padx=15, pady=(0, 15))
        total_item_status_frame.grid_propagate(False)

        total_item_icon = ctk.CTkLabel(
            total_item_status_frame, 
            text='', 
            image=ctk.CTkImage(light_image=Image.open("icons/total.png"), size=(48, 48)),
        )
        total_item_icon.grid(row=0, column=0, rowspan=2, pady=(1, 0), padx=(18, 0))

        total_item_label = ctk.CTkLabel(
            total_item_status_frame, 
            text='Total  Items',
            # text_color="#ffffff",
            text_color="black",
            font=("Roboto", 16, "bold"),
            fg_color="#298753",
        )
        total_item_label.grid(row=0, column=1, padx=(10, 0), pady=(6, 0))

        total_items = len(self.scrollable_frame.winfo_children())

        self.total_item_count = ctk.CTkLabel(
            total_item_status_frame, 
            text=total_items, 
            text_color="#ffffff",
            font=("Poppins", 21, "bold"),
            fg_color="#298753",
        )
        self.total_item_count.grid(row=1, column=1, padx=(11, 0), sticky="w")


# ======================== BOX TWOOOOOOOO =============================
        low_stock_alerts_frame = ctk.CTkFrame(self.status_frame, fg_color="#298753", width=250, height=70)
        low_stock_alerts_frame.grid(row=0, column=2, padx=35, pady=(0, 15))
        low_stock_alerts_frame.grid_propagate(False)

        low_stock_alerts_icon = ctk.CTkLabel(
            low_stock_alerts_frame, 
            text='', 
            image=ctk.CTkImage(light_image=Image.open("icons/stock_alerts.png"), size=(52, 52)),
            # fg_color="white"
        )
        low_stock_alerts_icon.grid(row=0, column=0, rowspan=2, pady=(5, 0), padx=(15, 0))

        low_stock_alerts_label = ctk.CTkLabel(
            low_stock_alerts_frame, 
            text='Low Stock Alerts',
            # text_color="#ffffff",
            text_color="black",
            font=("Roboto", 16, "bold"),
            fg_color="#298753",
            # fg_color="yellow"
        )
        low_stock_alerts_label.grid(row=0, column=1, padx=(10, 0), pady=(6, 0), sticky="w")

        # Place out of stock data here

        self.low_stock_alerts_count = ctk.CTkLabel(
            low_stock_alerts_frame, 
            text="4 items running low", 
            text_color="#ffffff",
            font=("Poppins", 15, "bold"),
            fg_color="#298753",
            # fg_color="blue"
        )
        self.low_stock_alerts_count.grid(row=1, column=1, pady=(5, 0), padx=(10, 0), sticky="w")


# ======================== BOX THREEEEEEE =============================
        out_of_stock_frame = ctk.CTkFrame(self.status_frame, fg_color="#298753", width=250, height=70)
        out_of_stock_frame.grid(row=0, column=3, padx=15, pady=(0, 15))
        out_of_stock_frame.grid_propagate(False)

        out_of_stock_icon = ctk.CTkLabel(
            out_of_stock_frame, 
            text='', 
            image=ctk.CTkImage(light_image=Image.open("icons/out_of_stock.png"), size=(55, 55)),
        )
        out_of_stock_icon.grid(row=0, column=0, rowspan=2, pady=(5, 0), padx=(18, 0))

        out_of_stock_label = ctk.CTkLabel(
            out_of_stock_frame, 
            text='Out of Stock',
            # text_color="#ffffff",
            text_color="black",
            font=("Roboto", 16, "bold"),
            fg_color="#298753",
        )
        out_of_stock_label.grid(row=0, column=1, padx=(13, 0), pady=(6, 0))

        # Place out of stock data here

        self.out_of_stock_count = ctk.CTkLabel(
            out_of_stock_frame, 
            text=4, 
            text_color="#ffffff",
            font=("Poppins", 21, "bold"),
            fg_color="#298753",
        )
        self.out_of_stock_count.grid(row=1, column=1, padx=(14, 0), sticky="w")

    def open_new_item_window(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = CreateItem(self.master)
        else:
            self.toplevel_window.focus()

    def update_total_item_counter(self):
        if self.counter_label:
            total_items = len(self.scrollable_frame.winfo_children())
            self.total_item_count.configure(text=total_items)

    def on_mouse_scroll(self, event):
        ''' This function is intended to change the speed of the mouse scroll on the scrollable frame. '''
    
        scroll_speed = 6  # The higher the faster
        
        if event.num == 4:  # For Linux
            self.scrollable_frame._parent_canvas.yview_scroll(-scroll_speed, "units")
        elif event.num == 5:  # For Linux
            self.scrollable_frame._parent_canvas.yview_scroll(scroll_speed, "units")
        else:  # For Windows & macOS
            self.scrollable_frame._parent_canvas.yview_scroll(-1 * (event.delta // 120) * scroll_speed, "units")


class AccountAdmin():
    def __init__(self, master):
        self.master = master

        ctk.CTkLabel(
            self.master,
            text="Account Panel", 
            font=("Arial", 24),
        ).pack(pady=50)

        ctk.CTkButton(
            self.master, 
            text="Logout", 
            font=("Poppins", 14),
            fg_color="#C92A3F",
            hover_color="#E63946", 
            text_color="#FFFFFF",
            cursor="hand2",
            command=self.exit_main
        ).pack()

    def exit_main(self):
        main_window = self.master.winfo_toplevel()
        main_window.destroy()
