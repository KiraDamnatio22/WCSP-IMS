import io
import unicodedata
import customtkinter as ctk
import hashlib
import logging

from PIL import Image
from rapidfuzz.fuzz import ratio
from pop_ups.notifs import CustomMessageBox
from test_backend import retrieve_display_data, delete_data
from admin_features.new_item import CreateItem
from admin_features.edit_item import EditItem

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class InventoryAdmin(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ADMIN Viewing Feature")
        # self.geometry("1180x500+186+202")
        self.geometry("1180x500+166+182")
        self.resizable(False, False)
        self.configure(fg_color="#ffffff")
        # self.overrideredirect(True)

        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger(__name__)

        # CONSTANTS
        self.LOW_STOCK_MULTIPLIER = 2

        # OTHER VARIABLES
        self.toplevel_window = None
        self.product_frames = []
        self.products = {}
        self.frame_cache = {}
        self.image_cache = {}
        self.data_cache = None
        self.toast_label = None
        self.last_added_product_id = None
        self.no_result_label = None
        self.delete_msgbox = None
        self.refresh_counter = 0

        self.column_configs = [
            {"text": "Photo", "width": 50, "padx": (22, 30)},
            {"text": "Code", "width": 60, "padx": (0, 15), "textlength": 100},
            {"text": "Name", "width": 115, "padx": (0, 15), "textlength": 100},
            {"text": "Category", "width": 95, "padx": (0, 15), "textlength": 100},
            {"text": "Price", "width": 85, "padx": (0, 15), "textlength": 55},
            {"text": "Type", "width": 60, "padx": (0, 15), "textlength": 50},
            {"text": "Brand", "width": 80, "padx": (0, 15), "textlength": 50},
            {"text": "Unit", "width": 50, "padx": (0, 10), "textlength": 50},
            {"text": "Stock", "width": 60, "padx": (0, 5), "textlength": 100},
            {"text": "Min", "width": 60, "padx": (0, 5), "textlength": 100},
            {"text": "Stock Status", "width": 120, "padx": (0, 10)},
            {"text": "Actions", "width": 125, "padx": (0, 15), "textlength": 100},
        ]

        self.empty_image = self.load_image("icons/empty_2.png", (200, 200))

        self.fallback_image = ctk.CTkImage(
            light_image=Image.open("icons/placeholder_image_original.png").resize((50, 50)),
            size=(50, 50)
        )

        self.icon_in_stock = ctk.CTkImage(Image.open("icons/in_stock_emoji.png"), size=(16, 16))
        self.icon_low_stock = ctk.CTkImage(Image.open("icons/low_stock_emoji.png"), size=(16, 16))
        self.icon_out_stock = ctk.CTkImage(Image.open("icons/out_of_stock_emoji.png"), size=(16, 16))

        self.search_frame = ctk.CTkFrame(self, fg_color="#e8e8e8", corner_radius=5)
        self.search_frame.pack(fill='x', padx=(16, 19), pady=(10, 8))

        self.content_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=0)
        self.content_frame.pack(fill="both", expand=True)

        self.header_frame = ctk.CTkFrame(self.content_frame, fg_color="#298753", corner_radius=10)
        self.header_frame.pack(fill="x", padx=(16, 20))

        self.scrollable_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="#FFFFFF", height=276, width=1143, border_color="#ccc", border_width=2)
        self.scrollable_frame.pack(padx=(5, 5), pady=(0, 5), expand=True, fill="both")

        # (MouseBindings)
        self.scrollable_frame._parent_canvas.bind_all("<MouseWheel>", self.on_mouse_scroll)
        
        # Keyboard Shortcuts (KeyboardBindings)
        self.create_keyboard_shortcut(self, f"<Control-{"R".lower()}>", lambda event: self.refresh_inventory(force_refresh=True))
        self.create_keyboard_shortcut(self, f"<Control-{"T".lower()}>", lambda event: self.scroll_to_top())
        self.create_keyboard_shortcut(self, f"<Control-{"B".lower()}>", lambda event: self.scroll_to_bottom())
        self.create_keyboard_shortcut(self, f"<Control-{"S".lower()}>", lambda event: self.search_pane_focus())
        self.create_keyboard_shortcut(self, "<Control-BackSpace>", lambda event: self.search_pane.delete(0, "end"))
        self.create_keyboard_shortcut(self, "<Escape>", lambda event: self.unfocus_search())

        self.setup_searchbar()
        self.scroll_controls()
        self.setup_headers()
        self.refresh_inventory()

    def create_keyboard_shortcut(self, master, shortcut, fn):
        master.bind(shortcut, fn)

    def search_pane_focus(self):
        self.search_pane.focus()
        self.search_pane.configure(border_color="#298753")

    def on_mouse_scroll(self, event):
        ''' Scroll only if scrollable frame has overflow content '''
        canvas = self.scrollable_frame._parent_canvas
        scroll_region = canvas.bbox("all")
        if scroll_region is None:
            return

        content_height = scroll_region[3] - scroll_region[1]
        canvas_height = canvas.winfo_height()

        if content_height > canvas_height:
            scroll_speed = 10
            canvas.yview_scroll(-1 * (event.delta // 120) * scroll_speed, "units")

    def setup_headers(self):
        ''' This function setups the headers for the inventory product table. '''
        for col_index, col in enumerate(self.column_configs):
            if col_index == 10:
                header_label = ctk.CTkLabel(
                self.header_frame,
                text=col["text"],
                font=("Arial", 14, "bold"),
                text_color="#ffffff",
                width=col["width"],
                anchor="center",
                wraplength=60,
                # fg_color="lightgreen",
                )
                header_label.grid(row=0, column=col_index, padx=col["padx"], pady=8)
                continue

            header_label = ctk.CTkLabel(
                self.header_frame,
                text=col["text"],
                font=("Arial", 14, "bold"),
                text_color="#ffffff",
                width=col["width"],
                anchor="center",
                wraplength=90,
                # fg_color="lightgreen",
            )
            header_label.grid(row=0, column=col_index, padx=col["padx"], pady=8)
            self.header_frame.grid_columnconfigure(col_index, minsize=col["width"])

    def delayed_filter(self, *args):
        if hasattr(self, "_search_after_id"):
            self.after_cancel(self._search_after_id)
        self._search_after_id = self.after(250, self.filter_and_sort_products)

    def unfocus_search(self, event=None):
        if self.search_pane and self.search_pane.winfo_exists():
            if event:
                if self.search_pane.winfo_rootx() <= event.x_root <= self.search_pane.winfo_rootx() + self.search_pane.winfo_width() and \
                self.search_pane.winfo_rooty() <= event.y_root <= self.search_pane.winfo_rooty() + self.search_pane.winfo_height():
                    self.search_pane.configure(border_color='#298753')
                    return

            # Unfocus the search entry 
            self.search_pane.focus_set()
            self.focus_force()
            self.search_pane.configure(border_color='#979da2')

    def setup_searchbar(self):
        ''' This setups the searchbar for the fast retrieval of a specific item on the table. '''

        self.search_pane = ctk.CTkEntry(
            self.search_frame, 
            fg_color='#ffffff', 
            placeholder_text='Search code, name, category, type, or brand',
            placeholder_text_color='gray',
            width=350, 
            height=30, 
            font=('Poppins', 14), 
            text_color="black")
        self.search_pane.pack(pady=10, padx=10, anchor="w", side="left")
        self.search_pane.bind('<KeyRelease>', self.delayed_filter)

        self.bind("<Button-1>", self.unfocus_search)

        self.sort_by_var = ctk.StringVar(value="Sort by")
        sort_by_values = ["Name", "Category", "Price", "Type", "Unit", "Current stock"]
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
        sort_by_menu.pack(pady=10, padx=(0, 10), side="left")

        self.status_var = ctk.StringVar(value="Status")
        status_values = ["In Stock", "Low Stock", "Out of Stock"]
        status_sort_menu = ctk.CTkOptionMenu(
            master=self.search_frame,
            values=status_values,
            variable=self.status_var,
            height=33,
            width=135,
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
            image=ctk.CTkImage(light_image=Image.open("./icons/new_item_20.png"), size=(18, 18)),
            compound="left",
            border_spacing=4,
            anchor="center",
            command=self.open_create_item
        )
        self.new_item_btn.pack(pady=10, padx=(0, 10), side="right")

        self.sort_order_var = ctk.StringVar(value="ASCEND ↑")
        self.sort_order_btn = ctk.CTkButton(
            self.search_frame,
            width=90,
            height=33,
            textvariable=self.sort_order_var,
            font=('Poppins', 14),
            fg_color="gray",
            text_color="#ffffff",
            corner_radius=6,
            command=self.toggle_sort_order,
            state="disabled",
        )
        self.sort_order_btn.pack(pady=10, padx=(0, 10), side="left")

        self.reset_searchbar_button = ctk.CTkButton(
            self.search_frame,
            text="Reset",
            width=55,
            height=33,
            font=('Poppins', 14),
            fg_color="gray",
            text_color="#ffffff",
            corner_radius=6,
            command=self.reset_button_on_searchbar,
            state="disabled",
        )
        self.reset_searchbar_button.pack(pady=10, padx=(0, 10), side="left")

    def reset_button_on_searchbar(self):
        self.search_pane.delete(0, ctk.END)
        self.sort_by_var.set("Sort by")
        self.status_var.set("Status")
        self.sort_order_var.set("ASCEND ↑")
        self.filter_and_sort_products()

    def normalize(self, text):
        """Removes accents, lowercases, and trims whitespace."""
        text = unicodedata.normalize('NFKD', text)
        return ''.join(c for c in text if not unicodedata.combining(c)).strip().lower()

    def is_fuzzy_match(self, query, target):
        """Avoid fuzzy match on short strings unless very close."""
        if len(query) < 4:
            return False  # Prevent false positives on short strings
        similarity = ratio(query, target)
        if len(query) < 6:
            return similarity >= 85  # Require high match for medium strings
        return similarity >= 70  # More relaxed threshold for longer queries

    def clear_no_result_ui(self):
        if self.no_result_label:
            self.no_result_label.destroy()
            self.caption_label.destroy()
            self.no_result_label = None

    def activate_reset_button(self):
        self.reset_searchbar_button.configure(fg_color="#E63946", hover_color="#C92A3F", state="normal")

    def filter_and_sort_products(self):
        query = self.normalize(self.search_pane.get())
        sort_by = self.sort_by_var.get()
        status = self.status_var.get()
        order = self.sort_order_var.get() == "DESCEND ↓"

        # Sorting, Status, Descend, Ascend, Reset Switching
        if sort_by != "Sort by":
            self.sort_order_btn.configure(fg_color="#298753", hover_color="#4BAC76", state="normal")
            self.activate_reset_button()
        elif status != "Status":
            self.activate_reset_button()
        elif query != "":
            self.activate_reset_button()
        else:
            self.sort_order_btn.configure(state="disabled", fg_color="gray")
            self.reset_searchbar_button.configure(state="disabled", fg_color="gray")

        # Clear "no result" display if it exists
        self.clear_no_result_ui()

        sort_index = {
            "Name": 3,
            "Category": 4,
            "Price": 5,
            "Type": 6,
            "Unit": 8,
            "Current stock": 9,
        }.get(sort_by, None)

        filtered = [(p[1], p) for p, _ in self.product_frames]

        if query:
            self.scroll_to_top()
            # ABLE TO SEARCH: code, name, category, type, brand
            searchable_fields = [2, 3, 4, 6, 7]  
            filtered = []

            for pid, p in [(p[1], p) for p, _ in self.product_frames]:
                for i in searchable_fields:
                    field_value = self.normalize(str(p[i]))
                    similarity = ratio(query, field_value)
                    # print(f"Checking: query='{query}' vs field='{field_value}' → similarity: {similarity:.2f}")

                    # Strong matches
                    if query == field_value:
                        filtered.append((pid, p))
                        break
                    elif field_value.startswith(query):
                        filtered.append((pid, p))
                        break
                    elif query in field_value:
                        filtered.append((pid, p))
                        break
                    elif self.is_fuzzy_match(query, field_value):
                        filtered.append((pid, p))
                        break

            if filtered:
                self.show_toast(f"{len(filtered)} matching item(s) found", duration=1500, fgcolor="#298753")

            # Handle no results
            if not filtered:
                for _, frame in self.product_frames:
                    frame.pack_forget()

                self.no_result_label = ctk.CTkLabel(self.scrollable_frame, text="", image=self.empty_image)

                self.caption_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text="No matching item/s found.",
                    font=("Poppins", 15)
                )
                self.no_result_label.pack(pady=(45, 20))
                self.caption_label.pack(pady=10)
                return

        # Continue with filter by status and sorting...
        if status != "Status":
            self.scroll_to_top()
            filtered = [(pid, p) for pid, p in filtered if p[11] == status]

        if sort_index is not None:
            self.scroll_to_top()
            def sort_key(item):
                value = item[1][sort_index]
                if isinstance(value, str):
                    value = value.replace(",", "")
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return value.lower() if isinstance(value, str) else value

            filtered.sort(key=sort_key, reverse=order)

        # Hide all product frames
        self.clear_product_frames()

        # Show only filtered ones
        for x in range(len(filtered)):
            pid = filtered[x][1][0]
            frame = self.frame_cache.get(str(pid))
            if frame:
                frame.pack(fill="x", padx=(5, 0), pady=5)
            else:
                print(f"Warning: Frame for product ID {pid} not found in cache.")

    def clear_product_frames(self):
        for _, frame in self.product_frames:
            frame.pack_forget()

    def toggle_sort_order(self):
        current = self.sort_order_var.get()
        new_value = "DESCEND ↓" if current == "ASCEND ↑" else "ASCEND ↑"
        self.sort_order_var.set(new_value)
        # print(f"Sort order changed to: {new_value}")
        self.filter_and_sort_products()

    def show_toast(self, message, duration=2000, fgcolor="#444"):
        if self.toast_label:
            self.toast_label.destroy()
        self.toast_label = ctk.CTkLabel(self, text=message, fg_color=fgcolor, font=("Roboto", 14), text_color="white", corner_radius=5, padx=5)
        self.toast_label.place(relx=0.5, rely=0.9, anchor="s", y=-5)
        self.after(duration, self.toast_label.destroy)

    def diff_inventory(self, old, new):
        old_dict = {p[0]: p for p in old}
        new_dict = {p[0]: p for p in new}

        added = [p for pid, p in new_dict.items() if pid not in old_dict]

        removed = [pid for pid in old_dict if pid not in new_dict]

        updated = [p for pid, p in new_dict.items() if pid in old_dict and p != old_dict[pid]]

        return added, removed, updated

    def convert_blob_to_image(self, blob_data, product_id):
        try:
            if not blob_data:
                raise ValueError("No image data provided.")

            blob_hash = self.get_blob_hash(blob_data)
            cache_key = f"{product_id}_{blob_hash}"

            if cache_key in self.image_cache:
                return self.image_cache[cache_key]

            image = Image.open(io.BytesIO(blob_data)).convert("RGBA")
            bg = Image.new("RGBA", image.size, (255, 255, 255, 0))
            diff = Image.alpha_composite(bg, image)
            bbox = diff.getbbox()
            if bbox:
                image = image.crop(bbox)
            image = image.resize((50, 50), Image.LANCZOS)

            final_img = ctk.CTkImage(light_image=image, dark_image=image, size=(50, 50))
            self.image_cache[cache_key] = final_img
            return final_img

        except Exception as e:
            print(f"[ERROR] Failed to convert image blob: {e}")

            # Handle fallback and ensure it's cached
            fallback_key = f"{product_id}_fallback"
            if fallback_key in self.image_cache:
                return self.image_cache[fallback_key]

            self.image_cache[fallback_key] = self.fallback_image
            return self.fallback_image

    def refresh_inventory(self, force_refresh=False):
        final_data = {}

        if self.data_cache is None or force_refresh:
            db_data = retrieve_display_data()
            self.data_cache = db_data
        else:
            db_data = self.data_cache

        for stock in db_data:
            stock = list(stock)
            product_id = str(stock[0])

            try:
                image_blob = stock[1]
                stock[1] = self.convert_blob_to_image(image_blob, product_id)
            except:
                pass

            stock[-2] = int(stock[-2]) if isinstance(stock[-2], str) and stock[-2].isdigit() else stock[-2]
            stock[-1] = int(stock[-1]) if isinstance(stock[-1], str) and stock[-1].isdigit() else stock[-1]
            q, t = stock[-2], stock[-1]
            low_stock = t * self.LOW_STOCK_MULTIPLIER

            stock_status = (
                "Out of Stock" if q <= t
                else "Low Stock" if q <= low_stock
                else "In Stock"
            )
            stock.append(stock_status)

            try:
                final_data[product_id] = stock
            except:
                pass

        print(f"\n[INFO] Total products loaded: {len(final_data)}\n")

        old_data = list(self.products.values())
        new_data = list(final_data.values())

        added, removed, updated = self.diff_inventory(old_data, new_data)

        for pid in removed:
            pid = str(pid)
            if pid in self.frame_cache:
                self.frame_cache[pid].destroy()
                del self.frame_cache[pid]
            self.products.pop(pid, None)
        
        for product in updated:
            pid = str(product[0])
            self.products[pid] = product

            if pid in self.frame_cache:
                self.frame_cache[pid].destroy()

            frame = self.create_product_frame(product)
            self.frame_cache[pid] = frame

        for product in added:
            pid = str(product[0])
            self.products[pid] = product
            frame = self.create_product_frame(product)
            self.frame_cache[pid] = frame

        self.product_frames = [(p, self.frame_cache[str(p[0])]) for p in self.products.values()]

        if self.last_added_product_id:
            print(f"Highlighting product: {self.last_added_product_id}")
            self.highlight_and_scroll_to(str(self.last_added_product_id))
            self.last_added_product_id = None

        self.filter_and_sort_products()
        self.show_toast("Refreshed", duration=1500, fgcolor="#298753")

    def create_product_frame(self, product):
        frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10, fg_color="#e0e0e0")

        for col_index, (value, col) in enumerate(zip(product[1:], self.column_configs)):
            # print(f"col index: [{col_index}], value: {value}, col: {col}")
            if col_index == 0:
                image = product[1]
                if not isinstance(image, ctk.CTkImage):
                    print(f"[WARN] Invalid image at index 0: {image}")
                    continue
                label = ctk.CTkLabel(
                    frame,
                    text="",
                    image=image,
                    width=col["width"],
                    anchor="center",
                )
            elif col_index == 10:
                # Stock Status column — add icon based on status
                stock_status = value
                stock_icon = (
                    self.icon_out_stock if stock_status == "Out of Stock"
                    else self.icon_low_stock if stock_status == "Low Stock"
                    else self.icon_in_stock
                )
                label = ctk.CTkLabel(
                    frame,
                    text=stock_status,
                    image=stock_icon,
                    compound="left",
                    text_color="black",
                    font=('Segoe UI Emoji', 14),
                    width=col["width"],
                    anchor="center",
                    padx=5,
                )
            elif col_index == 5:
                label = ctk.CTkLabel(
                    frame,
                    text=value,
                    text_color="black",
                    font=('Segoe UI Emoji', 14),
                    width=col["width"],
                    anchor="center",
                    wraplength=col["textlength"],
                )
            else:
                # All other text columns
                label = ctk.CTkLabel(
                    frame,
                    text=value,
                    text_color="black",
                    font=('Segoe UI Emoji', 14),
                    width=col["width"],
                    anchor="center",
                    wraplength=col["textlength"],
                )
            label.grid(row=0, column=col_index, padx=col["padx"], pady=15)

        button_frame = ctk.CTkFrame(frame, fg_color="transparent", corner_radius=0, height=45, width=128)
        button_frame.grid(row=0, column=11)
        button_frame.grid_propagate(False)

        ctk.CTkButton(
            button_frame,
            text="EDIT",
            font=("Poppins", 13, "bold"),
            text_color="#FFFFFF",
            width=50,
            height=25,
            cursor="hand2",
            command=lambda i=product[0]: self.edit_window(str(i)),
        ).grid(row=0, column=0, sticky="nsew", pady=(8, 0), padx=(6, 7))

        ctk.CTkButton(
            button_frame, 
            text="DELETE",
            font=("Poppins", 13, "bold"),
            text_color="#FFFFFF",
            width=40,
            height=25,
            cursor="hand2",
            fg_color="#E63946",
            hover_color="#C92A3F",
            command=lambda i=product[0]: self.ask_delete(str(i)),
        ).grid(row=0, column=1, sticky="nsew", pady=(8, 0))

        frame.pack()
        return frame

    def highlight_and_scroll_to(self, product_id):
        frame = self.frame_cache.get(product_id)
        if not frame:
            print(f"[WARN] Frame not found for product_id: {product_id}")
            return

        def scroll_to_frame():
            self.update_idletasks()
            frame_y = frame.winfo_y()
            scroll_region_height = max(1, self.scrollable_frame.winfo_height())
            self.scrollable_frame._parent_canvas.yview_moveto(frame_y / scroll_region_height)

        # Delay scrolling to ensure layout is updated
        self.after(50, scroll_to_frame)

        def pulse(count=0):
            if count >= 8:
                frame.configure(border_width=0)
                return
            color = "#3B8ED0" if count % 2 == 0 else frame.cget("fg_color")
            frame.configure(border_width=2, border_color=color)
            self.after(260, lambda: pulse(count + 1))

        pulse()

    def scroll_controls(self):
        button_frame = ctk.CTkFrame(self.search_frame, fg_color="transparent")
        button_frame.pack(side="right", padx=(0, 10))

        to_top_btn = ctk.CTkButton(button_frame, text="↑ Top", width=60, command=self.scroll_to_top)
        to_bottom_btn = ctk.CTkButton(button_frame, text="↓ Bottom", width=80, command=self.scroll_to_bottom)

        to_top_btn.pack(side="left", padx=(5, 3))
        to_bottom_btn.pack(side="left", padx=(3, 5))

    def scroll_to_top(self):
        self.scrollable_frame._parent_canvas.yview_moveto(0)

    def scroll_to_bottom(self):
        self.scrollable_frame._parent_canvas.yview_moveto(1)

    def ask_delete(self, item_id):
        if self.delete_msgbox and self.delete_msgbox.winfo_exists():
            self.delete_msgbox.focus_force()
            return

        def confirm_delete():
            self.log.debug(f"Deleting item_id: {item_id}")
            delete_data(self, item_id)
            if self.delete_msgbox and self.delete_msgbox.winfo_exists():
                self.delete_msgbox.destroy()
                self.refresh_inventory(force_refresh=True)

        self.delete_msgbox = CustomMessageBox(
            self,
            title="Delete Item",
            message="Are you sure you want to delete the item?",
            on_confirm=confirm_delete
        )

    def open_create_item(self):
        def after_add(product_id):
            self.last_added_product_id = product_id
            self.refresh_inventory(force_refresh=True)

        CreateItem(self, on_add_callback=after_add)

    def edit_window(self, product_id):
        def after_update():
            # self.image_cache.pop(product_id, None)
            self.refresh_inventory(force_refresh=True)

        EditItem(self, item_id=product_id, on_update_callback=after_update)

    def load_image(self, path, size):
        """Load and resize a PNG image using PIL and return a CTkImage."""
        image = Image.open(path)
        image = image.resize(size, Image.LANCZOS)
        return ctk.CTkImage(light_image=image, dark_image=image, size=size)
    
    def get_blob_hash(self, blob):
        return hashlib.md5(blob).hexdigest() if blob else None


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
            fg_color="#E63946", 
            hover_color="#C92A3F",
            text_color="#FFFFFF",
            cursor="hand2",
            command=self.exit_main
        ).pack()

    def exit_main(self):
        main_window = self.master.winfo_toplevel()
        main_window.destroy()


app = InventoryAdmin()
app.mainloop()


