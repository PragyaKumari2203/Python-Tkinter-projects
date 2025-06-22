# import tkinter as tk
# from tkinter import messagebox, simpledialog
# import sqlite3
# import re
# from tkinter import ttk


# # ========== DATABASE ========== #
# def init_db():
#     conn = sqlite3.connect('contacts.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS contacts (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             store_name TEXT NOT NULL,
#             phone TEXT NOT NULL UNIQUE,
#             email TEXT,
#             address TEXT
#         )
#     ''')
#     conn.commit()
#     conn.close()

# # ========== VALIDATIONS ========== #
# def is_valid_phone(phone):
#     return phone.isdigit() and len(phone) == 10

# def is_valid_email(email):
#     return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# # ========== DATABASE OPS ========== #
# def add_contact(store_name, phone, email, address):
#     conn = sqlite3.connect('contacts.db')
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO contacts (store_name, phone, email, address) VALUES (?, ?, ?, ?)",
#                    (store_name, phone, email, address))
#     conn.commit()
#     conn.close()

# def view_contacts():
#     conn = sqlite3.connect('contacts.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM contacts")
#     rows = cursor.fetchall()
#     conn.close()
#     return rows

# def search_contacts(keyword):
#     conn = sqlite3.connect('contacts.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM contacts WHERE store_name LIKE ? OR phone LIKE ?", 
#                    (f'%{keyword}%', f'%{keyword}%'))
#     rows = cursor.fetchall()
#     conn.close()
#     return rows

# def update_contact(contact_id, store_name, phone, email, address):
#     conn = sqlite3.connect('contacts.db')
#     cursor = conn.cursor()
#     cursor.execute("UPDATE contacts SET store_name=?, phone=?, email=?, address=? WHERE id=?",
#                    (store_name, phone, email, address, contact_id))
#     conn.commit()
#     conn.close()

# def delete_contact(contact_id):
#     conn = sqlite3.connect('contacts.db')
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
#     conn.commit()
#     conn.close()

# # ========== GUI FUNCTIONS ========== #
# def refresh_list():
#     tree.delete(*tree.get_children())
#     for contact in view_contacts():
#         tree.insert('', 'end', iid=contact[0], values=(contact[1], contact[2], contact[3], contact[4]))
#     back_button.pack_forget()


# def add_new():
#     while True:
#         store_name = simpledialog.askstring("Input", "Store Name:")
#         if store_name is None or store_name.strip() == "":
#             messagebox.showwarning("Warning", "Store name is required.")
#             continue

#         phone = simpledialog.askstring("Input", "Phone Number:")
#         if phone is None or phone.strip() == "":
#             messagebox.showwarning("Warning", "Phone number is required.")
#             continue

#         if not is_valid_phone(phone):
#             messagebox.showerror("Invalid Phone", "Phone number must be 10 digits.")
#             continue

#         email = simpledialog.askstring("Input", "Email:")
#         if email:
#             while not is_valid_email(email):
#                 messagebox.showerror("Invalid Email", "Please enter a valid email address.")
#                 email = simpledialog.askstring("Input", "Email (re-enter):")
#                 if email is None:
#                     email = ""  # Let them skip if they cancel on re-entry
#                     break

#         address = simpledialog.askstring("Input", "Address:")
#         if address is None:
#             address = ""

#         try:
#             add_contact(store_name, phone, email, address)
#             refresh_list()
#             messagebox.showinfo("Success", "Contact added successfully.")
#             break  # success, exit loop
#         except sqlite3.IntegrityError:
#             messagebox.showerror("Error", "Phone number already exists. Try a different one.")

# def search():
#     keyword = simpledialog.askstring("Search", "Enter store name or phone number:")
#     if keyword:
#         tree.delete(*tree.get_children())
#         for contact in search_contacts(keyword):
#             tree.insert('', 'end', iid=contact[0], values=(contact[1], contact[2], contact[3], contact[4]))
#         back_button.pack(pady=5)
#     else:
#         refresh_list()


# def delete_selected():
#     selected = tree.selection()
#     if not selected:
#         messagebox.showinfo("Info", "Please select a contact to delete.")
#         return

#     contact_id = int(selected[0])
#     values = tree.item(contact_id, 'values')
#     store_name, phone = values[0], values[1]

#     confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete:\n{store_name} ({phone})?")
#     if not confirm:
#         return

#     delete_contact(contact_id)
#     refresh_list()
#     messagebox.showinfo("Deleted", f"✅ Contact deleted:\n{store_name} ({phone})")

# def show_contact_details(event):
#     selection = listbox.curselection()
#     if not selection:
#         return
#     index = selection[0]
#     contacts = view_contacts()
#     if index >= len(contacts):
#         return
#     contact = contacts[index]
#     contact_id, store_name, phone, email, address = contact

#     messagebox.showinfo("Contact Details",
#                         f"Store Name: {store_name}\n"
#                         f"Phone: {phone}\n"
#                         f"Email: {email or 'N/A'}\n"
#                         f"Address: {address or 'N/A'}")


# # def update_selected():
# #     selection = listbox.curselection()
# #     if not selection:
# #         messagebox.showinfo("Info", "Please select a contact to update.")
# #         return

# #     index = int(selection[0])
# #     contact_line = listbox.get(index)
# #     contact_id = int(contact_line.split('|')[0])

# #     conn = sqlite3.connect('contacts.db')
# #     cursor = conn.cursor()
# #     cursor.execute("SELECT store_name, phone, email, address FROM contacts WHERE id=?", (contact_id,))
# #     result = cursor.fetchone()
# #     conn.close()

# #     if not result:
# #         messagebox.showerror("Error", "Contact not found.")
# #         return

# #     current_store, current_phone, current_email, current_address = result

# #     field_options = {
# #         "1": "Store Name",
# #         "2": "Phone",
# #         "3": "Email",
# #         "4": "Address"
# #     }

# #     choice = simpledialog.askstring(
# #         "Update Field",
# #         "Which field do you want to update?\n1 - Store Name\n2 - Phone\n3 - Email\n4 - Address"
# #     )

# #     if not choice or choice not in field_options:
# #         messagebox.showinfo("Info", "Invalid choice or cancelled.")
# #         return

# #     field_name = field_options[choice]
# #     new_value = simpledialog.askstring("Input", f"Enter new {field_name}:")

# #     if not new_value:
# #         messagebox.showwarning("Warning", f"{field_name} cannot be empty.")
# #         return

# #     if choice == "2" and not is_valid_phone(new_value):
# #         messagebox.showerror("Invalid Phone", "Phone number must be 10 digits.")
# #         return

# #     if choice == "3" and not is_valid_email(new_value):
# #         messagebox.showerror("Invalid Email", "Please enter a valid email address.")
# #         return

# #     # Apply the update selectively
# #     updated_store = current_store if choice != "1" else new_value
# #     updated_phone = current_phone if choice != "2" else new_value
# #     updated_email = current_email if choice != "3" else new_value
# #     updated_address = current_address if choice != "4" else new_value

# #     try:
# #         update_contact(contact_id, updated_store, updated_phone, updated_email, updated_address)
# #         refresh_list()
# #         messagebox.showinfo("Success", f"{field_name} updated successfully.")
# #     except sqlite3.IntegrityError:
# #         messagebox.showerror("Error", "Phone number already exists.")
# def update_selected():
#     selected = tree.selection()
#     if not selected:
#         messagebox.showinfo("Info", "Please select a contact to update.")
#         return

#     contact_id = int(selected[0])
#     contact = next((c for c in view_contacts() if c[0] == contact_id), None)

#     if not contact:
#         messagebox.showerror("Error", "Contact not found.")
#         return

#     current_store, current_phone, current_email, current_address = contact[1], contact[2], contact[3], contact[4]

#     field_options = {
#         "1": "Store Name",
#         "2": "Phone",
#         "3": "Email",
#         "4": "Address"
#     }

#     while True:
#         choice = simpledialog.askstring(
#             "Update Field",
#             "Which field do you want to update?\n1 - Store Name\n2 - Phone\n3 - Email\n4 - Address\n(Cancel to exit)"
#         )

#         if not choice or choice not in field_options:
#             messagebox.showinfo("Info", "Update cancelled or invalid choice.")
#             return

#         field_name = field_options[choice]

#         while True:
#             new_value = simpledialog.askstring("Input", f"Enter new {field_name}:")
#             if new_value is None:
#                 messagebox.showinfo("Cancelled", f"{field_name} update cancelled.")
#                 return

#             if not new_value.strip():
#                 messagebox.showwarning("Warning", f"{field_name} cannot be empty.")
#                 continue

#             if choice == "2" and not is_valid_phone(new_value):
#                 messagebox.showerror("Invalid Phone", "Phone number must be 10 digits.")
#                 continue

#             if choice == "3" and not is_valid_email(new_value):
#                 messagebox.showerror("Invalid Email", "Please enter a valid email address.")
#                 continue

#             break

#         updated_store = current_store if choice != "1" else new_value
#         updated_phone = current_phone if choice != "2" else new_value
#         updated_email = current_email if choice != "3" else new_value
#         updated_address = current_address if choice != "4" else new_value

#         try:
#             update_contact(contact_id, updated_store, updated_phone, updated_email, updated_address)
#             refresh_list()
#             messagebox.showinfo("Success", f"{field_name} updated successfully.")
#         except sqlite3.IntegrityError:
#             messagebox.showerror("Error", "Phone number already exists. Try another.")
#             continue

#         break

# # ========== MAIN GUI ========== #
# if __name__ == "__main__":
#     init_db()

#     root = tk.Tk()
#     root.title("📇 Contact Management System")
#     root.geometry("750x500")
#     root.configure(bg="#f0f4f7")

#     title_label = tk.Label(root, text="Contact Management System", bg="#f0f4f7",
#                            font=("Helvetica", 20, "bold"), fg="#333")
#     title_label.pack(pady=10)

#     list_frame = tk.Frame(root, bg="#f0f4f7")
#     list_frame.pack(pady=10)

#     tree = ttk.Treeview(list_frame, columns=("Store", "Phone", "Email", "Address"), show='headings', height=15)

#     # Define columns
#     tree.heading("Store", text="Store Name")
#     tree.heading("Phone", text="Phone")
#     tree.heading("Email", text="Email")
#     tree.heading("Address", text="Address")

#     tree.column("Store", width=150)
#     tree.column("Phone", width=100)
#     tree.column("Email", width=180)
#     tree.column("Address", width=220)

#     tree.pack(side="left", fill="both")
#     scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
#     scrollbar.pack(side="right", fill="y")
#     tree.configure(yscrollcommand=scrollbar.set)


#     btn_font = ("Segoe UI", 11, "bold")

#     button_frame = tk.Frame(root, bg="#f0f4f7")
#     button_frame.pack(pady=10)

#     tk.Button(button_frame, text="Add Contact", font=btn_font, bg="#4CAF50", fg="white",
#               width=15, command=add_new).grid(row=0, column=0, padx=5, pady=5)
#     tk.Button(button_frame, text="Search Contact", font=btn_font, bg="#2196F3", fg="white",
#               width=15, command=search).grid(row=0, column=1, padx=5, pady=5)
#     tk.Button(button_frame, text="Update Contact", font=btn_font, bg="#FFC107", fg="black",
#               width=15, command=update_selected).grid(row=0, column=2, padx=5, pady=5)
#     tk.Button(button_frame, text="Delete Contact", font=btn_font, bg="#F44336", fg="white",
#               width=15, command=delete_selected).grid(row=0, column=3, padx=5, pady=5)

#     back_button = tk.Button(root, text="⬅ Back to Home", font=btn_font, bg="#9E9E9E", fg="white",
#                             command=refresh_list)

#     refresh_list()
#     root.mainloop()














# import tkinter as tk
# from tkinter import messagebox, simpledialog, ttk
# import sqlite3
# import re

# # ========== DATABASE ========== #
# def init_db():
#     conn = sqlite3.connect('contacts.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS contacts (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             store_name TEXT NOT NULL,
#             phone TEXT NOT NULL UNIQUE,
#             email TEXT,
#             address TEXT
#         )
#     ''')
#     conn.commit()
#     conn.close()

# # ========== VALIDATIONS ========== #
# def is_valid_phone(phone):
#     return phone.isdigit() and len(phone) == 10

# def is_valid_email(email):
#     return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# # ========== DATABASE OPS ========== #
# def add_contact(store_name, phone, email, address):
#     conn = sqlite3.connect('contacts.db')
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO contacts (store_name, phone, email, address) VALUES (?, ?, ?, ?)",
#                    (store_name, phone, email, address))
#     conn.commit()
#     conn.close()

# def view_contacts():
#     conn = sqlite3.connect('contacts.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM contacts")
#     rows = cursor.fetchall()
#     conn.close()
#     return rows

# def search_contacts(keyword):
#     conn = sqlite3.connect('contacts.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM contacts WHERE store_name LIKE ? OR phone LIKE ?", 
#                    (f'%{keyword}%', f'%{keyword}%'))
#     rows = cursor.fetchall()
#     conn.close()
#     return rows

# def update_contact(contact_id, store_name, phone, email, address):
#     conn = sqlite3.connect('contacts.db')
#     cursor = conn.cursor()
#     cursor.execute("UPDATE contacts SET store_name=?, phone=?, email=?, address=? WHERE id=?",
#                    (store_name, phone, email, address, contact_id))
#     conn.commit()
#     conn.close()

# def delete_contact(contact_id):
#     conn = sqlite3.connect('contacts.db')
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
#     conn.commit()
#     conn.close()

# # ========== GUI FUNCTIONS ========== #
# def refresh_list():
#     tree.delete(*tree.get_children())
#     for contact in view_contacts():
#         tree.insert('', 'end', iid=contact[0], values=(contact[1],))  # Only show store_name
#     back_button.config(state=tk.DISABLED)


# def show_contact_details(event):
#     selected = tree.selection()
#     if not selected:
#         return
#     contact_id = int(selected[0])
#     contact = next((c for c in view_contacts() if c[0] == contact_id), None)

#     if not contact:
#         return

#     _, store, phone, email, address = contact
#     messagebox.showinfo("Contact Details", f"📌 Store: {store}\n📞 Phone: {phone}\n📧 Email: {email or 'N/A'}\n🏠 Address: {address or 'N/A'}")

# def open_add_form():
#     form_window = tk.Toplevel(root)
#     form_window.title("Add New Contact")
#     form_window.geometry("350x300")

#     def save_new_contact():
#         store = store_entry.get()
#         phone = phone_entry.get()
#         email = email_entry.get()
#         address = address_entry.get()

#         if not store.strip():
#             messagebox.showerror("Error", "Store name is required.")
#             return
#         if not phone.strip() or not is_valid_phone(phone):
#             messagebox.showerror("Error", "Phone must be 10 digits.")
#             return
#         if email and not is_valid_email(email):
#             messagebox.showerror("Error", "Invalid email.")
#             return

#         try:
#             add_contact(store, phone, email, address)
#             refresh_list()
#             form_window.destroy()
#             messagebox.showinfo("Success", "Contact added successfully.")
#         except sqlite3.IntegrityError:
#             messagebox.showerror("Error", "Phone number already exists.")

#     # Labels and Inputs
#     tk.Label(form_window, text="Store Name:").pack(pady=5)
#     store_entry = tk.Entry(form_window, width=40)
#     store_entry.pack()

#     tk.Label(form_window, text="Phone:").pack(pady=5)
#     phone_entry = tk.Entry(form_window, width=40)
#     phone_entry.pack()

#     tk.Label(form_window, text="Email:").pack(pady=5)
#     email_entry = tk.Entry(form_window, width=40)
#     email_entry.pack()

#     tk.Label(form_window, text="Address:").pack(pady=5)
#     address_entry = tk.Entry(form_window, width=40)
#     address_entry.pack()

#     tk.Button(form_window, text="Save", bg="#4CAF50", fg="white", command=save_new_contact).pack(pady=10)

# def update_selected():
#     selected = tree.selection()
#     if not selected:
#         messagebox.showinfo("Info", "Select a contact to update.")
#         return

#     contact_id = int(selected[0])
#     contact = next((c for c in view_contacts() if c[0] == contact_id), None)
#     if not contact:
#         return

#     current_store, current_phone, current_email, current_address = contact[1], contact[2], contact[3], contact[4]

#     field_options = {
#         "1": "Store Name",
#         "2": "Phone",
#         "3": "Email",
#         "4": "Address"
#     }

#     while True:
#         choice = simpledialog.askstring("Update", "Update which field?\n1 - Store\n2 - Phone\n3 - Email\n4 - Address")
#         if not choice or choice not in field_options:
#             messagebox.showinfo("Info", "Update cancelled.")
#             return

#         field_name = field_options[choice]
#         new_value = simpledialog.askstring("Input", f"Enter new {field_name}:")
#         if not new_value:
#             messagebox.showwarning("Warning", "Value cannot be empty.")
#             continue

#         if choice == "2" and not is_valid_phone(new_value):
#             messagebox.showerror("Error", "Phone must be 10 digits.")
#             continue
#         if choice == "3" and new_value and not is_valid_email(new_value):
#             messagebox.showerror("Error", "Invalid email.")
#             continue

#         updated_store = current_store if choice != "1" else new_value
#         updated_phone = current_phone if choice != "2" else new_value
#         updated_email = current_email if choice != "3" else new_value
#         updated_address = current_address if choice != "4" else new_value

#         try:
#             update_contact(contact_id, updated_store, updated_phone, updated_email, updated_address)
#             refresh_list()
#             messagebox.showinfo("Success", f"{field_name} updated.")
#         except sqlite3.IntegrityError:
#             messagebox.showerror("Error", "Phone number already exists.")
#         break

# def delete_selected():
#     selected = tree.selection()
#     if not selected:
#         messagebox.showinfo("Info", "Select a contact to delete.")
#         return
#     contact_id = int(selected[0])
#     contact = next((c for c in view_contacts() if c[0] == contact_id), None)
#     if not contact:
#         return

#     confirm = messagebox.askyesno("Confirm", f"Delete {contact[1]} ({contact[2]})?")
#     if confirm:
#         delete_contact(contact_id)
#         refresh_list()
#         messagebox.showinfo("Deleted", "Contact deleted.")

# def search():
#     keyword = simpledialog.askstring("Search", "Enter store name or phone:")
#     if keyword:
#         tree.delete(*tree.get_children())
#         for contact in search_contacts(keyword):
#             tree.insert('', 'end', iid=contact[0], values=(contact[1],))
#         back_button.config(state=tk.NORMAL)

#     else:
#         refresh_list()

# # ========== MAIN GUI ========== #
# if __name__ == "__main__":
#     init_db()

#     root = tk.Tk()
#     root.title("📇 Contact Management System")
#     root.geometry("600x450")
#     root.configure(bg="#f0f4f7")

#     title_label = tk.Label(root, text="Contact Management System", bg="#f0f4f7",
#                            font=("Helvetica", 20, "bold"), fg="#333")
#     title_label.pack(pady=10)

#     list_frame = tk.Frame(root, bg="#f0f4f7")
#     list_frame.pack(pady=10)

#     tree = ttk.Treeview(list_frame, columns=("Store",), show='headings', height=15)
#     tree.heading("Store", text="Store Name")
#     tree.column("Store", width=500)
#     tree.bind("<Double-1>", show_contact_details)
#     tree.pack(side="left", fill="both")

#     scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
#     scrollbar.pack(side="right", fill="y")
#     tree.configure(yscrollcommand=scrollbar.set)

#     button_frame = tk.Frame(root, bg="#f0f4f7")
#     button_frame.pack(pady=10)
#     nav_frame = tk.Frame(root, bg="#f0f4f7")
#     nav_frame.pack(pady=5)

#     btn_font = ("Segoe UI", 10, "bold")  # Declare this BEFORE using it

#     back_button = tk.Button(nav_frame, text="⬅ Back to All", font=btn_font,
#                         bg="#9E9E9E", fg="white", command=refresh_list)
#     back_button.pack()  # <-- THIS makes it visible



#     btn_font = ("Segoe UI", 10, "bold")

#     tk.Button(button_frame, text="➕ Add Contact", font=btn_font, bg="#4CAF50", fg="white",
#               width=15, command=open_add_form).grid(row=0, column=0, padx=5)
#     tk.Button(button_frame, text="🔍 Search", font=btn_font, bg="#2196F3", fg="white",
#               width=15, command=search).grid(row=0, column=1, padx=5)
#     tk.Button(button_frame, text="✏️ Update", font=btn_font, bg="#FFC107", fg="black",
#               width=15, command=update_selected).grid(row=0, column=2, padx=5)
#     tk.Button(button_frame, text="🗑️ Delete", font=btn_font, bg="#F44336", fg="white",
#               width=15, command=delete_selected).grid(row=0, column=3, padx=5)

#     refresh_list()
#     root.mainloop()





import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3
import re

# ========== DATABASE ========== #
def init_db():
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_name TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE,
            email TEXT,
            address TEXT
        )
    ''')
    conn.commit()
    conn.close()

# ========== VALIDATIONS ========== #
def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 10

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# ========== DATABASE OPS ========== #
def add_contact(store_name, phone, email, address):
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contacts (store_name, phone, email, address) VALUES (?, ?, ?, ?)",
                   (store_name, phone, email, address))
    conn.commit()
    conn.close()

def view_contacts():
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    conn.close()
    return rows

def search_contacts(keyword):
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts WHERE store_name LIKE ? OR phone LIKE ?", 
                   (f'%{keyword}%', f'%{keyword}%'))
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_contact(contact_id, store_name, phone, email, address):
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE contacts SET store_name=?, phone=?, email=?, address=? WHERE id=?",
                   (store_name, phone, email, address, contact_id))
    conn.commit()
    conn.close()

def delete_contact(contact_id):
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
    conn.commit()
    conn.close()

# ========== GUI FUNCTIONS ========== #
def refresh_list():
    tree.delete(*tree.get_children())
    for contact in view_contacts():
        tree.insert('', 'end', iid=contact[0], values=(contact[1],))
    back_button.pack_forget()  # Hide back button when not searching

def show_contact_details(event):
    selected = tree.selection()
    if not selected:
        return
    contact_id = int(selected[0])
    contact = next((c for c in view_contacts() if c[0] == contact_id), None)
    if not contact:
        return

    _, store, phone, email, address = contact
    messagebox.showinfo("Contact Details", f"📌 Store: {store}\n📞 Phone: {phone}\n📧 Email: {email or 'N/A'}\n🏠 Address: {address or 'N/A'}")

def open_add_form():
    form_window = tk.Toplevel(root)
    form_window.title("Add New Contact")
    form_window.geometry("350x300")

    def save_new_contact():
        store = store_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        address = address_entry.get()

        if not store.strip():
            messagebox.showerror("Error", "Store name is required.")
            return
        if not phone.strip() or not is_valid_phone(phone):
            messagebox.showerror("Error", "Phone must be 10 digits.")
            return
        if email and not is_valid_email(email):
            messagebox.showerror("Error", "Invalid email.")
            return

        try:
            add_contact(store, phone, email, address)
            refresh_list()
            form_window.destroy()
            messagebox.showinfo("Success", "Contact added successfully.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Phone number already exists.")

    tk.Label(form_window, text="Store Name:").pack(pady=5)
    store_entry = tk.Entry(form_window, width=40)
    store_entry.pack()

    tk.Label(form_window, text="Phone:").pack(pady=5)
    phone_entry = tk.Entry(form_window, width=40)
    phone_entry.pack()

    tk.Label(form_window, text="Email:").pack(pady=5)
    email_entry = tk.Entry(form_window, width=40)
    email_entry.pack()

    tk.Label(form_window, text="Address:").pack(pady=5)
    address_entry = tk.Entry(form_window, width=40)
    address_entry.pack()

    tk.Button(form_window, text="Save", bg="#4CAF50", fg="white", command=save_new_contact).pack(pady=10)

def update_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showinfo("Info", "Select a contact to update.")
        return

    contact_id = int(selected[0])
    contact = next((c for c in view_contacts() if c[0] == contact_id), None)
    if not contact:
        return

    current_store, current_phone, current_email, current_address = contact[1], contact[2], contact[3], contact[4]

    field_options = {
        "1": "Store Name",
        "2": "Phone",
        "3": "Email",
        "4": "Address"
    }

    while True:
        choice = simpledialog.askstring("Update", "Update which field?\n1 - Store\n2 - Phone\n3 - Email\n4 - Address")
        if not choice or choice not in field_options:
            messagebox.showinfo("Info", "Update cancelled.")
            return

        field_name = field_options[choice]
        new_value = simpledialog.askstring("Input", f"Enter new {field_name}:")
        if not new_value:
            messagebox.showwarning("Warning", "Value cannot be empty.")
            continue

        if choice == "2" and not is_valid_phone(new_value):
            messagebox.showerror("Error", "Phone must be 10 digits.")
            continue
        if choice == "3" and new_value and not is_valid_email(new_value):
            messagebox.showerror("Error", "Invalid email.")
            continue

        updated_store = current_store if choice != "1" else new_value
        updated_phone = current_phone if choice != "2" else new_value
        updated_email = current_email if choice != "3" else new_value
        updated_address = current_address if choice != "4" else new_value

        try:
            update_contact(contact_id, updated_store, updated_phone, updated_email, updated_address)
            refresh_list()
            messagebox.showinfo("Success", f"{field_name} updated.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Phone number already exists.")
        break

def delete_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showinfo("Info", "Select a contact to delete.")
        return
    contact_id = int(selected[0])
    contact = next((c for c in view_contacts() if c[0] == contact_id), None)
    if not contact:
        return

    confirm = messagebox.askyesno("Confirm", f"Delete {contact[1]} ({contact[2]})?")
    if confirm:
        delete_contact(contact_id)
        refresh_list()
        messagebox.showinfo("Deleted", "Contact deleted.")

def search():
    keyword = simpledialog.askstring("Search", "Enter store name or phone:")
    if keyword:
        tree.delete(*tree.get_children())
        results = search_contacts(keyword)
        for contact in results:
            tree.insert('', 'end', iid=contact[0], values=(contact[1],))
        if results:
            back_button.pack()  # Show back button if search returns anything
        else:
            messagebox.showinfo("No Results", "No matching contact found.")
            refresh_list()
    else:
        refresh_list()

# ========== MAIN GUI ========== #
if __name__ == "__main__":
    init_db()

    root = tk.Tk()
    root.title("📇 Contact Management System")
    root.geometry("600x450")
    root.configure(bg="#f0f4f7")

    btn_font = ("Segoe UI", 10, "bold")

    title_label = tk.Label(root, text="Contact Management System", bg="#f0f4f7",
                           font=("Helvetica", 20, "bold"), fg="#333")
    title_label.pack(pady=10)

    list_frame = tk.Frame(root, bg="#f0f4f7")
    list_frame.pack(pady=10)

    tree = ttk.Treeview(list_frame, columns=("Store",), show='headings', height=15)
    tree.heading("Store", text="Store Name")
    tree.column("Store", width=500)
    tree.bind("<Double-1>", show_contact_details)
    tree.pack(side="left", fill="both")

    scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    button_frame = tk.Frame(root, bg="#f0f4f7")
    button_frame.pack(pady=10)

    nav_frame = tk.Frame(root, bg="#f0f4f7")
    nav_frame.pack()

    back_button = tk.Button(nav_frame, text="⬅ Back to All", font=btn_font,
                            bg="#9E9E9E", fg="white", command=refresh_list)
    back_button.pack_forget()  # Initially hidden

    tk.Button(button_frame, text="➕ Add Contact", font=btn_font, bg="#4CAF50", fg="white",
              width=15, command=open_add_form).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="🔍 Search", font=btn_font, bg="#2196F3", fg="white",
              width=15, command=search).grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="✏️ Update", font=btn_font, bg="#FFC107", fg="black",
              width=15, command=update_selected).grid(row=0, column=2, padx=5)
    tk.Button(button_frame, text="🗑️ Delete", font=btn_font, bg="#F44336", fg="white",
              width=15, command=delete_selected).grid(row=0, column=3, padx=5)

    refresh_list()
    root.mainloop()
