import customtkinter as ctk

class CustomMessageBox(ctk.CTkToplevel):
    def __init__(self, parent, title, message, on_confirm):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x200+890+465")
        self.resizable(False, False)
        self.configure(fg_color="#F0F0F0")
        self.grab_set()
        self.overrideredirect(True)

        # Title label
        title_label = ctk.CTkLabel(
            self, 
            text=title, 
            font=("Poppins", 18, "bold"),
            text_color="white", 
            fg_color="#218838", 
            corner_radius=5, 
            pady=10,
            bg_color="#218838"
        )
        title_label.pack(fill="x")

        # Message label
        message_label = ctk.CTkLabel(
            self, text=message, font=("Poppins", 14),
            text_color="black", wraplength=350, pady=20
        )
        message_label.pack(pady=10)

        # Buttons frame
        button_frame = ctk.CTkFrame(self, fg_color="#F0F0F0")
        button_frame.pack(pady=10)

        ctk.CTkButton(
            button_frame, text="Cancel",
            fg_color="#979da2", hover_color="#7a7f85",
            font=("Poppins", 13, "bold"),
            text_color="white",
            bg_color="#F0F0F0",
            command=self.destroy
        ).grid(row=0, column=0, padx=8)

        ctk.CTkButton(
            button_frame, text="Yes, Delete",
            fg_color="#E63946", hover_color="#C92A3F",
            font=("Poppins", 13, "bold"),
            text_color="white",
            bg_color="#F0F0F0",
            command=on_confirm
        ).grid(row=0, column=1, padx=8)


class Toast(ctk.CTkToplevel):
    def __init__(self, parent, message, *, x=600, y=325, duration=1800, bg_color="#218838", fg_color="#ffffff", font=("Poppins", 14, "bold"), width=225, height=50):
        super().__init__(parent)
        self.overrideredirect(True)   # no titlebar
        self.lift()   # stay on top
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.0)   # start fully transparent

        self.x = x
        self.y = y

        # message label
        self.label = ctk.CTkLabel(
            self,
            text=message,
            text_color=fg_color,
            fg_color=bg_color,
            font=font,
            padx=15,
            pady=8,
            width=width,
            height=height,
            bg_color=bg_color,
        )
        self.label.pack()

        # position at bottom-right of parent
        self.update_idletasks()
        tw = self.winfo_reqwidth()
        th = self.winfo_reqheight()

        self.geometry(f"{tw}x{th}+{self.x}+{self.y}")

        # fade in
        self.attributes("-alpha", 0.0)
        self._fade(step=0.05, target=1.0, delay=10)

        # schedule fade-out
        self.after(duration, lambda: self._fade(step=-0.05,
                                                target=0.0,
                                                delay=10,
                                                on_done=self.destroy))

    def _fade(self, step, target, delay, on_done=None):
        alpha = self.attributes("-alpha") + step
        alpha = max(0.0, min(1.0, alpha))
        self.attributes("-alpha", alpha)
        if (step > 0 and alpha < target) or (step < 0 and alpha > target):
            self.after(delay, lambda: self._fade(step, target, delay, on_done))
        elif on_done:
            on_done()


# def ask_exit():
#     def confirm_exit():
#         app.destroy()

#     CustomMessageBox(
#         app, 
#         title="Delete Item",
#         message="Are you sure you want to delete the item?",
#         on_confirm=confirm_exit
#     )
#     # CustomMessageBox(
#     #     app, 
#     #     title="Exit Application",
#     #     message="Are you sure you want to quit?",
#     #     on_confirm=confirm_exit
#     # )

# app = ctk.CTk()
# app.geometry("400x200")
# ctk.set_appearance_mode("light")

# ctk.CTkButton(app, text="Quit", font=("Poppins", 14, "bold"), fg_color="#218838", text_color="white", command=ask_exit).pack(pady=50)
# app.mainloop()
