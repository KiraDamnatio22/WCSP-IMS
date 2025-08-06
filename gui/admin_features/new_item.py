import io, os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import customtkinter as ctk

from PIL import Image
from tkinter import filedialog
from test_backend import insert_to_database
from pop_ups.notifs import Toast


class CreateItem(ctk.CTkToplevel):
    def __init__(self, master, on_add_callback=None):
        super().__init__(master)

        self.master = master
        self.on_add_callback = on_add_callback

        self.title("Add New Item")
        self.geometry("1000x572+205+100")
        self.resizable(False, False)
        self.configure(fg_color="#ffffff")
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.overrideredirect(True)
        self.grab_set()

        self.actual_item_photo = None

        border_frame = ctk.CTkFrame(self, fg_color="lightgray", corner_radius=8)
        border_frame.pack(expand=True, fill="both")

        self.mainframe = ctk.CTkFrame(border_frame, fg_color="#ffffff", corner_radius=0)
        self.mainframe.pack(fill="both", expand=True, padx=1.5, pady=1.5)

        self.entry_frame = ctk.CTkFrame(self.mainframe, fg_color="#ffffff", corner_radius=0)
        self.entry_frame.pack(fill="both", expand=True, padx=70, pady=20)

        # WINDOW TITLE
        self.window_title = ctk.CTkLabel(
            self.entry_frame,
            text="New Item",
            font=('Poppins', 30, 'bold'),
            text_color="#298753",
        )
        self.window_title.grid(row=0, column=0, sticky="w", pady=(12, 0))

        self.frame_one_main = ctk.CTkFrame(self.entry_frame, fg_color="#ffffff", corner_radius=0, width=856, height=79)
        self.frame_one_main.grid(row=1, column=0, sticky="w")
        self.frame_one_main.grid_propagate(False)

        self.frame_one = ctk.CTkFrame(self.frame_one_main, fg_color="#ffffff", corner_radius=0, width=435, height=60)
        self.frame_one.grid(row=0, column=0, sticky="nsew")
        self.frame_one.grid_propagate(False)

        self.frame_one_half = ctk.CTkFrame(self.frame_one_main, fg_color="#ffffff", corner_radius=0, width=300, height=65)
        self.frame_one_half.grid(row=0, column=1, pady=(13, 0))
        self.frame_one_half.grid_propagate(False)

        self.frame_two = ctk.CTkFrame(self.entry_frame, fg_color="#ffffff", corner_radius=0, height=345, width=700)
        self.frame_two.grid(row=2, column=0, sticky="w")
        self.frame_two.grid_propagate(False)

        self.frame_three = ctk.CTkFrame(self.entry_frame, fg_color="#ffffff", corner_radius=0)
        self.frame_three.grid(row=3, column=0, sticky="e")

        self.setup_all_fields()  
    
    def setup_all_fields(self):
        # ITEM PHOTO
        ctk.CTkLabel(self.frame_one, text="Item Photo", font=("Poppins", 20), text_color="#298753", bg_color="transparent", anchor="center").grid(row=0, column=0, pady=(10, 0))
        self.photo_entry = ctk.CTkButton(
            self.frame_one,
            text="Upload Photo",
            font=("Poppins", 14),
            fg_color="#298753",
            text_color="#ffffff",
            hover_color="#4BAC76",
            border_color="#ffffff",
            width=100,
            cursor="hand2",
            command=self.upload_item_image
        )
        self.photo_entry.grid(row=0, column=1, padx=(10, 0), pady=(10, 0))

        # ITEM PHOTO PREVIEW
        self.item_photo_preview = ctk.CTkLabel(self.frame_one, text="", font=("Poppins", 20), text_color="black", bg_color="transparent", height=70)
        self.item_photo_preview.grid(row=0, column=2, padx=(20, 100), pady=(10, 0))

        # ITEM NAME
        ctk.CTkLabel(self.frame_two, text="Item Name", font=("Poppins", 20), text_color="#298753", bg_color="transparent", anchor="s").grid(row=0, column=0, sticky="w", padx=(0, 185), ipady=6)
        self.item_name_entry = ctk.CTkEntry(
            self.frame_two,
            width=250,
            height=30,
            fg_color="#e8e8e8",
            font=("Poppins", 13)
        )
        self.item_name_entry.grid(row=1, column=0, padx=(0, 185), sticky="w")

        # ITEM PRICE
        ctk.CTkLabel(self.frame_one_half, text="Price", font=("Poppins", 20), text_color="#298753", bg_color="transparent").grid(row=0, column=0, sticky="w", pady=(0, 0))
        self.price_entry = ctk.CTkEntry(
            self.frame_one_half,
            fg_color="#e8e8e8",
            width=122,
        )
        self.price_entry.grid(row=1, column=0)

        # ITEM TYPE
        ctk.CTkLabel(self.frame_two, text="Type", font=("Poppins", 20), text_color="#298753", bg_color="transparent").grid(row=2, column=0, sticky="w")
        self.type_entry = ctk.CTkEntry(
            self.frame_two,
            fg_color="#e8e8e8",
            height=30,
            font=("Poppins", 13),
        )
        self.type_entry.grid(row=3, column=0, sticky="w")

        # ITEM BRAND
        ctk.CTkLabel(self.frame_two, text="Brand", font=("Poppins", 20), text_color="#298753", bg_color="transparent", anchor="s").grid(row=4, column=0, sticky="w", pady=(10, 0))
        self.brand_entry = ctk.CTkEntry(
            self.frame_two,
            fg_color="#e8e8e8",
            height=30,
            font=("Poppins", 13),
        )
        self.brand_entry.grid(row=5, column=0, sticky="w")

        # ITEM UNIT
        ctk.CTkLabel(self.frame_two, text="Unit", font=("Poppins", 20), text_color="#298753", bg_color="transparent", anchor="s").grid(row=0, column=1, sticky="w", ipady=6)

        unit_values = ["box", "pc/s", "roll", "ft", "in", "ft", "m", "cm", "mm", "kg", "g"]

        self.unit_entry = ctk.CTkOptionMenu(
            master=self.frame_two,
            values=unit_values,
            height=33,
            width=120,
            font=('Poppins', 14),
            text_color="black",
            button_color="#298753",
            button_hover_color="#4BAC76",
            fg_color="#e8e8e8",
            dropdown_fg_color="#e8e8e8",
            dropdown_text_color="black",
            dropdown_font=('Poppins', 14),
            dropdown_hover_color="#298753",
            command=lambda e: self.clear_focus(e)
        )
        self.unit_entry.set("Select unit")
        self.unit_entry.grid(row=1, column=1, sticky="w")
        
        # ITEM SUPPLIER
        self.supplier_entry = ctk.CTkEntry(self.entry_frame)
        ctk.CTkLabel(self.frame_two, text="Supplier", font=("Poppins", 20), text_color="#298753", bg_color="transparent").grid(row=6, column=0, sticky="w", pady=(10, 0))
        self.supplier_entry = ctk.CTkEntry(
            self.frame_two,
            width=250,
            fg_color="#e8e8e8",
            height=30,
            font=("Poppins", 13),
        )
        self.supplier_entry.grid(row=7, column=0, sticky="w")

        # ITEM CURRENT STOCK
        ctk.CTkLabel(self.frame_two, text="Quantity", font=("Poppins", 20), text_color="#298753", bg_color="transparent").grid(row=2, column=1, sticky="w", pady=(10, 0))
        self.current_stock_entry = ctk.CTkEntry(
            self.frame_two,
            width=50,
            fg_color="#e8e8e8",
        )
        self.current_stock_entry.grid(row=3, column=1, sticky="w")
        
        # ITEM THRESHOLD
        ctk.CTkLabel(self.frame_two, text="Set Threshold", font=("Poppins", 20), text_color="#298753", bg_color="transparent").grid(row=4, column=1, sticky="w", pady=(10, 0))
        self.threshold_entry = ctk.CTkEntry(
            self.frame_two,
            width=50,
            fg_color="#e8e8e8",
        )
        self.threshold_entry.grid(row=5, column=1, sticky="w")

        # ITEM CATEGORY
        ctk.CTkLabel(self.frame_two, text="Category", font=("Poppins", 20), text_color="#298753", bg_color="transparent", anchor="s").grid(row=6, column=1, sticky="w", pady=(10, 0))

        unit_values = ["Equipment", "Tools", "Consumables"]

        self.category_entry = ctk.CTkOptionMenu(
            master=self.frame_two,
            values=unit_values,
            height=33,
            width=155,
            font=('Poppins', 14),
            text_color="black",
            button_color="#298753",
            button_hover_color="#4BAC76",
            fg_color="#e8e8e8",
            dropdown_fg_color="#e8e8e8",
            dropdown_text_color="black",
            dropdown_font=('Poppins', 14),
            dropdown_hover_color="#298753",
            command=lambda e: self.clear_focus(e)
        )
        self.category_entry.set("Select category")
        self.category_entry.grid(row=7, column=1, sticky="w")

        self.entry_fields = [
            self.item_name_entry,
            self.type_entry,
            self.brand_entry,
            self.price_entry,
            self.current_stock_entry,
            self.threshold_entry,
            self.supplier_entry,
        ]
        
        self.option_menus = [
            self.unit_entry,
            self.category_entry,
        ]
        
        self.new_item_details = [
            self.item_name_entry,
            self.type_entry,
            self.brand_entry,
            self.price_entry,
            self.current_stock_entry,
            self.threshold_entry,
            self.unit_entry,
            self.category_entry,
            self.supplier_entry,
        ]
        # print(self.new_item_details)

        # ADD BUTTON
        self.add_button = ctk.CTkButton(
            self.frame_three,
            text="Add",
            font=("Poppins", 14, "bold"),
            text_color="#ffffff",
            width=200,
            height=35,
            fg_color="#298753",
            hover_color="#4BAC76",
            cursor="hand2",
            command=lambda: self.add_item_to_database(self.new_item_details)
        )
        self.add_button.pack(side="right", anchor="s")

        # BACK BUTTON
        self.back_button = ctk.CTkButton(
            self.frame_three,
            text="Back",
            font=("Poppins", 14, "bold"),
            text_color="#298753",
            width=200,
            fg_color="#ffffff",
            border_color="#298753",
            border_width=2.5,
            border_spacing=0,
            hover_color="#e8e8e8",
            cursor="hand2",
            command=self.close_window
        )
        self.back_button.pack(side="right", anchor="s", padx=(0, 20))

        # for widget in self.entry_fields:
        #     widget.bind("<FocusIn>", lambda e, w=widget: w.configure(border_color='#298753'))
        #     widget.bind("<FocusOut>", lambda e, w=widget: w.configure(border_color='#979da2'))

        other_widgets = [
            self.mainframe,
            self.entry_frame,
            self.frame_one,
            self.frame_two,
            self.frame_one_main,
            self.frame_one_half,
        ]

        for menu in other_widgets:
            menu.bind("<Button-1>", self.clear_focus)

        # self.show_widget_fg_color()

    def clear_focus(self, event):
        self.focus()

    def show_widget_fg_color(self):
        self.mainframe.configure(fg_color="yellow")
        self.entry_frame.configure(fg_color="blue")
        self.frame_one_main.configure(fg_color="lightblue")
        self.frame_one.configure(fg_color="lightgreen")
        self.frame_one_half.configure(fg_color="red")
        self.frame_two.configure(fg_color="lightyellow")
        self.frame_three.configure(fg_color="brown")

    def upload_item_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg *.gif")])
        if file_path:
            image = Image.open(file_path)
            image = image.resize((100, 100))
            self.actual_item_photo = self.convert_image_to_blob(file_path)

            ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(60, 60))

            self.item_photo_preview.configure(image=ctk_image)
            self.item_photo_preview.image = ctk_image

    def convert_image_to_blob(self, image_path):
        with open(image_path, 'rb') as file:
            profile_blob = file.read()
        return profile_blob

    def close_window(self):
        self.destroy()

    def validate_inputs(self):
        for entry in self.entry_fields:
            if not entry.get().strip():
                return False, "Some fields are empty"          

        try:
            float(self.price_entry.get())
            int(self.current_stock_entry.get())
            int(self.threshold_entry.get())
        except ValueError:
            return False, "Price and quantity must be numbers"
        
        if self.option_menus[0].get() == "Select unit":
            return False, "Select first a UNIT"
        if self.option_menus[1].get() == "Select category":
            return False, "Select first a CATEGORY"

        return True, ""


    def add_item_to_database(self, details):
        print(details)
        validation_result, message = self.validate_inputs()
        
        if validation_result:
            item_id, code = insert_to_database(
                self.master,
                self.actual_item_photo,
                details[0].get(),  # name
                details[1].get(),  # type
                details[2].get(),  # brand
                details[3].get(),  # price
                details[4].get(),  # quantity
                details[5].get(),  # threshold
                details[6].get(),  # unit
                details[7].get(),  # category
                details[8].get(),  # supplier
            )

            if self.on_add_callback:
                self.after(100, self.destroy)

            new_product = [
                self.actual_item_photo,
                code,
                details[0].get(),
                details[7].get(),
                float(details[3].get()),
                details[1].get(),
                details[2].get(),
                details[6].get(),
                int(details[4].get()),
                int(details[5].get()),
            ]

            q, t = new_product[8], new_product[9]
            low_stock = t * 2
            status = (
                "Out of Stock" if q <= t else
                "Low Stock" if q <= low_stock else
                "In Stock"
            )
            new_product.append(status)

            new_product[0] = self.master.convert_blob_to_image(new_product[0], str(new_product[1]))

            # print(item_id, type(item_id))
            self.on_add_callback(item_id)  # 🔥 Key Line

            self.add_button.pack_forget()
            self.back_button.pack_forget()
            self.photo_entry.grid_forget()
            self.close_add_window_and_refresh()

        else:
            Toast(self, message, duration=2800, x=713, y=125, bg_color="#E63946", font=("Poppins", 16, "bold"))
     
    def close_add_window_and_refresh(self):
        self.master.refresh_inventory()
        self.after(1000, self.destroy)
