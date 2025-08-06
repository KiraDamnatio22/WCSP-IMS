import io, os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import customtkinter as ctk

from PIL import Image
from tkinter import filedialog
from test_backend import update_data, retrieve_item_data_from_db
from pop_ups.notifs import Toast

class EditItem(ctk.CTkToplevel):
    def __init__(self, master, item_id, on_update_callback=None):
        super().__init__(master)
        self.title("Update Item")
        self.geometry("1000x572+205+100")
        self.resizable(False, False)
        self.configure(fg_color="#ffffff")
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.overrideredirect(True)
        self.grab_set()

        self.master = master
        self.on_add_callback = on_update_callback
        self.item_id = item_id
        self.new_threshold = 0
        self.actual_item_photo = None

        border_frame = ctk.CTkFrame(self, fg_color="lightgray", corner_radius=8)
        border_frame.pack(expand=True, fill="both")

        # self.mainframe = ctk.CTkFrame(border_frame, fg_color="#ffffff", corner_radius=0)
        # self.mainframe.pack(fill="both", expand=True, padx=1.5, pady=1.5)

        # self.entry_frame = ctk.CTkFrame(self.mainframe, fg_color="#ffffff", corner_radius=0)
        # self.entry_frame.pack(fill="both", expand=True, padx=70, pady=20)

        # # WINDOW TITLE
        # self.window_title = ctk.CTkLabel(
        #     self.entry_frame,
        #     text="Edit Item",
        #     font=('Poppins', 30, 'bold'),
        #     text_color="#298753",
        # )
        # self.window_title.grid(row=0, column=0, sticky="w", pady=(12, 0))

        # # frame_one_main = ctk.CTkFrame(self.entry_frame, fg_color="lightblue", corner_radius=0, width=856, height=79)
        # frame_one_main = ctk.CTkFrame(self.entry_frame, fg_color="#ffffff", corner_radius=0, width=856, height=79)
        # frame_one_main.grid(row=1, column=0, sticky="w")
        # frame_one_main.grid_propagate(False)

        # # self.frame_one = ctk.CTkFrame(frame_one_main, fg_color="lightgreen", corner_radius=0, width=435, height=60)
        # self.frame_one = ctk.CTkFrame(frame_one_main, fg_color="#ffffff", corner_radius=0, width=435, height=60)
        # self.frame_one.grid(row=0, column=0, sticky="nsew")
        # self.frame_one.grid_propagate(False)

        # # self.frame_one_half = ctk.CTkFrame(frame_one_main, fg_color="lightyellow", corner_radius=0, width=300, height=65)
        # self.frame_one_half = ctk.CTkFrame(frame_one_main, fg_color="#ffffff", corner_radius=0, width=300, height=65)
        # self.frame_one_half.grid(row=0, column=1, pady=(13, 0))
        # self.frame_one_half.grid_propagate(False)

        # # self.frame_two = ctk.CTkFrame(self.entry_frame, fg_color="lightgray", corner_radius=0, height=345, width=800)
        # self.frame_two = ctk.CTkFrame(self.entry_frame, fg_color="#ffffff", corner_radius=0, height=345, width=700)
        # self.frame_two.grid(row=2, column=0, sticky="w")
        # self.frame_two.grid_propagate(False)

        # self.frame_three = ctk.CTkFrame(self.entry_frame, fg_color="#ffffff", corner_radius=0)
        # self.frame_three.grid(row=3, column=0, sticky="e")

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

    def reset_to_default_threshold(self, default_value):
        self.toggle_threshold_btn.configure(state="normal", fg_color="#298753", hover_color="#4BAC76",)
        self.reset_to_default_threshold_btn.configure(state="disabled", fg_color="gray")

        self.threshold_entry.delete(0, "end")
        self.threshold_entry.insert(0, default_value)
        self.threshold_entry.configure(state="disabled", fg_color="#e8e8e8", text_color="black")
        self.new_threshold = default_value

    def set_new_threshold(self):
        self.toggle_threshold_btn.configure(state="disabled", fg_color="gray")
        self.reset_to_default_threshold_btn.configure(state="normal", fg_color="#E63946", hover_color="#C92A3F",)

        self.reset_to_default_threshold_btn.grid(row=5, column=3, sticky="w", padx=(15, 0))
        self.threshold_entry.configure(state="normal")
        self.threshold_entry.delete(0, "end")
        self.threshold_entry.focus()
        self.new_threshold = self.threshold_entry.get()

    def setup_all_fields(self):
        datas = retrieve_item_data_from_db(self.item_id)
        blob_img = datas[0]
        item_photo_image = self.convert_blob_to_image(blob_img)

        # ITEM PHOTO
        ctk.CTkLabel(self.frame_one, text="Item Photo", font=("Poppins", 20), text_color="#298753", bg_color="transparent", anchor="center").grid(row=0, column=0, pady=(10, 0))
        self.photo_entry = ctk.CTkButton(
            self.frame_one,
            text="Upload New Photo",
            font=("Poppins", 14),
            fg_color="#298753",
            text_color="#ffffff",
            hover_color="#4BAC76",
            border_color="#ffffff",
            width=100,
            cursor="hand2",
            command=self.upload_item_image
        )
        self.photo_entry.grid(row=0, column=2, padx=(20, 100), pady=(10, 0))

        # ITEM PHOTO PREVIEW
        self.item_photo_preview = ctk.CTkLabel(self.frame_one, text="", font=("Poppins", 20), text_color="black", bg_color="transparent", height=70)
        self.item_photo_preview.grid(row=0, column=1, padx=(15, 0), pady=(10, 0))

        self.item_photo_preview.configure(image=item_photo_image)
        self.item_photo_preview.image = item_photo_image

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
        self.item_name_entry.insert(0, datas[1])
        
        # ITEM PRICE
        ctk.CTkLabel(self.frame_one_half, text="Price", font=("Poppins", 20), text_color="#298753", bg_color="transparent").grid(row=0, column=0, sticky="w", pady=(0, 0))
        self.price_entry = ctk.CTkEntry(
            self.frame_one_half,
            fg_color="#e8e8e8",
            width=122,
        )
        self.price_entry.grid(row=1, column=0)
        self.price_entry.insert(0, datas[2])

        # ITEM TYPE
        ctk.CTkLabel(self.frame_two, text="Type", font=("Poppins", 20), text_color="#298753", bg_color="transparent").grid(row=2, column=0, sticky="w")
        self.type_entry = ctk.CTkEntry(
            self.frame_two,
            fg_color="#e8e8e8",
            height=30,
            font=("Poppins", 13),
        )
        self.type_entry.grid(row=3, column=0, sticky="w")
        self.type_entry.insert(0, datas[3])

        # ITEM BRAND
        ctk.CTkLabel(self.frame_two, text="Brand", font=("Poppins", 20), text_color="#298753", bg_color="transparent", anchor="s").grid(row=4, column=0, sticky="w", pady=(10, 0))
        self.brand_entry = ctk.CTkEntry(
            self.frame_two,
            fg_color="#e8e8e8",
            height=30,
            font=("Poppins", 13),
        )
        self.brand_entry.grid(row=5, column=0, sticky="w")
        self.brand_entry.insert(0, datas[4])

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
        self.unit_entry.set(datas[5])
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
        self.supplier_entry.insert(0, datas[6])

        # ITEM CURRENT STOCK
        ctk.CTkLabel(self.frame_two, text="Quantity", font=("Poppins", 20), text_color="#298753", bg_color="transparent").grid(row=2, column=1, sticky="w", pady=(10, 0))
        self.current_stock_entry = ctk.CTkEntry(
            self.frame_two,
            width=50,
            fg_color="#e8e8e8",
        )
        self.current_stock_entry.grid(row=3, column=1, sticky="w")
        self.current_stock_entry.insert(0, datas[7])

        # ITEM THRESHOLD
        threshold = ctk.StringVar(value=datas[8])

        ctk.CTkLabel(self.frame_two, text="Set Threshold", font=("Poppins", 20), text_color="#298753", bg_color="transparent").grid(row=4, column=1, sticky="w", pady=(10, 0))

        # Threshold Entry
        self.threshold_entry = ctk.CTkEntry(
            self.frame_two,
            width=50,
            fg_color="#e8e8e8",
            state="readonly",
            textvariable=threshold
        )
        self.threshold_entry.insert(0, threshold)
        self.threshold_entry.grid(row=5, column=2)

        self.toggle_threshold_btn = ctk.CTkButton(
            self.frame_two,
            text="New Threshold",
            font=("Poppins", 14),
            text_color="#ffffff",
            fg_color="#298753",
            hover_color="#4BAC76",
            border_color="#ffffff",
            width=100,
            command=self.set_new_threshold,
        )
        self.toggle_threshold_btn.grid(row=5, column=1, sticky="w")
        
        self.reset_to_default_threshold_btn = ctk.CTkButton(
            self.frame_two,
            text="reset",
            font=("Poppins", 14),
            fg_color="gray",
            text_color="#ffffff",
            border_color="#ffffff",
            width=50,
            command=lambda t=threshold.get(): self.reset_to_default_threshold(t),
            state="disabled"
        )
        
        # ITEM CATEGORY
        ctk.CTkLabel(self.frame_two, text="Category", font=("Poppins", 20), text_color="#298753", bg_color="transparent", anchor="s").grid(row=6, column=1, sticky="w", pady=(10, 0))

        unit_values = ["Equipment", "Tools", "Consumables"]

        self.category_entry = ctk.CTkOptionMenu(
            master=self.frame_two,
            values=unit_values,
            height=33,
            width=145,
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
        self.category_entry.set(datas[9])
        self.category_entry.grid(row=7, column=1, sticky="w")

        item_new_details = [
            self.item_name_entry,
            self.category_entry,
            self.price_entry,
            self.type_entry,
            self.brand_entry,
            self.unit_entry,
            self.current_stock_entry,
            self.threshold_entry,
            self.supplier_entry,
        ]

        # UDPATE BUTTON
        self.update_button = ctk.CTkButton(
            self.frame_three,
            text="Update",
            font=("Poppins", 14, "bold"),
            text_color="#ffffff",
            width=200,
            height=35,
            fg_color="#298753",
            hover_color="#4BAC76",
            cursor="hand2",
            command=lambda item_img=blob_img, datas=item_new_details: self.update_item_from_database(item_img, datas)
        )
        self.update_button.pack(side="right", anchor="s")

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

        for widget in self.entry_fields:
            widget.bind("<FocusIn>", lambda e, w=widget: w.configure(border_color='#298753'))
            widget.bind("<FocusOut>", lambda e, w=widget: w.configure(border_color='#979da2'))

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

    def convert_blob_to_image(self, blob_data):
        image = Image.open(io.BytesIO(blob_data))
        image = image.resize((50, 50))  # Resize image for UI
        return ctk.CTkImage(light_image=image, dark_image=image, size=(60, 60))

    def close_window(self):
        self.destroy()

    def update_item_from_database(self, item_image, new_item_details):
        final_item_img = None
        updated_item_values = [item.get() for item in new_item_details]

        # UPLOAD NOTHING. SAME IMAGE
        if self.actual_item_photo == None:
            final_item_img = item_image

        # UPLOAD SOMETHING. SAME IMAGE
        elif self.actual_item_photo == item_image:
            final_item_img = item_image

        # UPLOAD SOMETHING. DIFFERENT IMAGE
        else:
            final_item_img = self.actual_item_photo

        update_data(self.master, self.item_id, final_item_img, updated_item_values)
        self.close_add_window_and_refresh()
     
    def close_add_window_and_refresh(self):
        self.master.refresh_inventory(force_refresh=True)
        self.after(600, self.destroy)
