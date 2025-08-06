import os, sys, sqlite3
from pop_ups.notifs import Toast


def get_app_dir():
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.abspath(os.path.dirname(__file__))

def connect_db():
    db_path = os.path.join(get_app_dir(), "test_backend.db")
    conn = sqlite3.connect(db_path)
    curr = conn.cursor()
    return conn, curr

def insert_to_database(master, *data):
    conn, curr = connect_db()

    # Unpack fields
    (
        photo, name, _type, brand, price,
        quantity, threshold, unit, category, supplier
    ) = data

    # Determine prefix
    prefix_map = {
        "Consumables": "C",
        "Tools": "T",
        "Equipment": "E"
    }
    normalized_category = category.strip().title()
    print(f"Category: {normalized_category}")
    prefix = prefix_map.get(normalized_category, "X")

    # prefix = prefix_map.get(category, "X")  # Fallback to X if unknown

    # Get next ID in sequence for the prefix
    curr.execute("SELECT code FROM items WHERE code LIKE ? ORDER BY id DESC LIMIT 1", (f"{prefix}%",))
    last_code_row = curr.fetchone()
    if last_code_row:
        last_num = int(last_code_row[0][1:])  # Remove prefix and convert
        new_num = last_num + 1
    else:
        new_num = 1

    new_code = f"{prefix}{new_num:03d}"

    # Insert into database
    curr.execute("""
        INSERT INTO items (
            code, photo, name, _type, brand, price,
            quantity, threshold, unit, category, supplier
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (new_code, photo, name, _type, brand, price, quantity, threshold, unit, category, supplier))

    item_id = curr.lastrowid
    conn.commit()
    conn.close()

    Toast(master, "✅ Item Added!", duration=2800)
    return item_id, new_code


def retrieve_display_data():
    conn, curr = connect_db()
    rows = curr.execute("SELECT id, photo, code, name, category, price, _type, brand, unit, quantity, threshold FROM items").fetchall()
    conn.close()
    return rows

def retrieve_item_data_from_db(item_id):
    conn, curr = connect_db()
    rows = curr.execute("SELECT photo, name, price, _type, brand, unit, supplier, quantity, threshold, category FROM items WHERE id = ?", (item_id,)).fetchone()
    conn.close()  
    return rows

def delete_data(master, item_id):
    print(f"Deleting {item_id, type(item_id)}")
    conn, curr = connect_db()
    curr.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    Toast(master, "✅ Item Deleted!", duration=2800)

def update_data(master, item_id, photo_data, new_values):
    # print(f"PARENT WIDGET: {master}")
    # print(f"ITEM ID: {item_id}")
    # # print(f"ITEM PHOTO: {photo_data}")

    # headers = ["Item Name", "Category", "Price", "Type", "Brand", "Unit", "Quantity", "Threshold", "Supplier"]
    # print("ITEM DETAILS:")
    # for idx, value in enumerate(new_values):
    #     print(f"\t- {headers[idx]}: {value}")
    # print()
    conn, curr = connect_db()
    curr.execute("""
        UPDATE items 
        SET photo = ?, name = ?, category = ?, price = ?, _type = ?, brand = ?, unit = ?, quantity = ?, threshold = ?, supplier = ?
        WHERE id = ?
    """, (photo_data, *new_values, item_id))
    conn.commit()
    conn.close()
    Toast(master, "✅ Item Updated!", duration=2800)

def remove_entire_db_table():
    conn, curr = connect_db()
    curr.execute("""DROP TABLE IF EXISTS items;""")
    conn.commit()
    conn.close()
    print("\n\n Table removal success.")

def create_table():
    conn, curr = connect_db()
    curr.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT,
            photo BLOB,
            name TEXT,
            _type TEXT,
            brand TEXT,
            price REAL,
            quantity INTEGER,
            threshold INTEGER,
            unit TEXT,
            category TEXT,
            supplier TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("\n Table creation done!")


'''Create the table'''
# create_table()

'''Delete the table'''
# remove_entire_db_table()

