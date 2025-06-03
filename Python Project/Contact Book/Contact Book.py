import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os

class ContactBookGUI:
    def __init__(self, master):
        self.master = master
        master.title("Contact Book")
        master.geometry("600x400")

        self.contacts = self.load_contacts()

        self.create_widgets()
        self.update_contact_list()

    def load_contacts(self, filename="contacts.json"):
        """Loads contacts from a JSON file."""
        contacts = []
        try:
            with open(filename, "r") as f:
                contacts = json.load(f)
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error decoding contacts file.")
        return contacts

    def save_contacts(self, filename="contacts.json"):
        """Saves contacts to a JSON file."""
        try:
            with open(filename, "w") as f:
                json.dump(self.contacts, f, indent=4)
            messagebox.showinfo("Success", "Contacts saved successfully!")
        except IOError:
            messagebox.showerror("Error", "Error saving contacts.")

    def create_widgets(self):
        # --- Contact List Frame ---
        self.list_frame = tk.Frame(self.master)
        self.list_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.contact_list = ttk.Treeview(self.list_frame, columns=("Name", "Phone"), show="headings")
        self.contact_list.heading("Name", text="Name")
        self.contact_list.heading("Phone", text="Phone Number")
        self.contact_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.contact_list.bind('<<TreeviewSelect>>', self.show_contact_details)

        self.scrollbar = tk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.contact_list.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.contact_list.config(yscrollcommand=self.scrollbar.set)

        # --- Details Frame ---
        self.details_frame = tk.Frame(self.master)
        self.details_frame.pack(padx=10, pady=5, fill=tk.X)

        self.details_labels = {
            "Name:": tk.Label(self.details_frame, text="Name:"),
            "Phone:": tk.Label(self.details_frame, text="Phone:"),
            "Email:": tk.Label(self.details_frame, text="Email:"),
            "Address:": tk.Label(self.details_frame, text="Address:")
        }
        self.details_values = {
            "Name:": tk.StringVar(),
            "Phone:": tk.StringVar(),
            "Email:": tk.StringVar(),
            "Address:": tk.StringVar()
        }

        row = 0
        for label_text, label_widget in self.details_labels.items():
            label_widget.grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
            value_label = tk.Label(self.details_frame, textvariable=self.details_values[label_text], anchor=tk.W)
            value_label.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=2)
            row += 1

        # --- Button Frame ---
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(pady=10)

        tk.Button(self.button_frame, text="Add Contact", command=self.add_contact).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="View All", command=self.update_contact_list).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Search Contact", command=self.search_contact).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Update Contact", command=self.update_contact).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Delete Contact", command=self.delete_contact).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Save Contacts", command=self.save_contacts).pack(side=tk.LEFT, padx=5)

    def update_contact_list(self, search_results=None):
        """Updates the contact list Treeview."""
        for item in self.contact_list.get_children():
            self.contact_list.delete(item)

        contacts_to_display = search_results if search_results is not None else self.contacts

        for contact in contacts_to_display:
            self.contact_list.insert("", tk.END, values=(contact.get("name", ""), contact.get("phone", "")))

    def show_contact_details(self, event):
        """Displays detailed information of the selected contact."""
        selected_item = self.contact_list.selection()
        if selected_item:
            selected_name = self.contact_list.item(selected_item[0])['values'][0]
            for contact in self.contacts:
                if contact.get("name") == selected_name:
                    self.details_values["Name:"].set(contact.get("name", ""))
                    self.details_values["Phone:"].set(contact.get("phone", ""))
                    self.details_values["Email:"].set(contact.get("email", ""))
                    self.details_values["Address:"].set(contact.get("address", ""))
                    return

        # Clear details if no contact is selected
        for var in self.details_values.values():
            var.set("")

    def add_contact(self):
        """Opens a dialog to add a new contact."""
        add_window = tk.Toplevel(self.master)
        add_window.title("Add New Contact")

        labels = ["Name:", "Phone:", "Email:", "Address:"]
        entries = {}

        for i, label_text in enumerate(labels):
            tk.Label(add_window, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
            entry = tk.Entry(add_window, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky=tk.EW)
            entries[label_text[:-1].lower()] = entry

        def save_new_contact():
            new_contact = {key: entry.get().strip() for key, entry in entries.items()}
            if not new_contact["name"] or not new_contact["phone"]:
                messagebox.showerror("Error", "Name and Phone are required.")
                return
            self.contacts.append(new_contact)
            self.update_contact_list()
            add_window.destroy()

        tk.Button(add_window, text="Save Contact", command=save_new_contact).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def search_contact(self):
        """Opens a dialog to search for a contact."""
        search_window = tk.Toplevel(self.master)
        search_window.title("Search Contact")

        tk.Label(search_window, text="Search by Name or Phone:").pack(padx=10, pady=5)
        search_entry = tk.Entry(search_window, width=30)
        search_entry.pack(padx=10, pady=5)

        def perform_search():
            search_term = search_entry.get().strip().lower()
            results = []
            for contact in self.contacts:
                if search_term in contact.get("name", "").lower() or search_term in contact.get("phone", "").lower():
                    results.append(contact)
            self.update_contact_list(results)

        tk.Button(search_window, text="Search", command=perform_search).pack(pady=10)

    def update_contact(self):
        """Opens a dialog to update the selected contact."""
        selected_item = self.contact_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a contact to update.")
            return

        selected_name = self.contact_list.item(selected_item[0])['values'][0]
        original_index = -1
        for i, contact in enumerate(self.contacts):
            if contact.get("name") == selected_name:
                original_index = i
                break

        if original_index == -1:
            messagebox.showerror("Error", "Selected contact not found in data.")
            return

        update_window = tk.Toplevel(self.master)
        update_window.title("Update Contact")

        labels = ["Name:", "Phone:", "Email:", "Address:"]
        entries = {}

        current_contact = self.contacts[original_index]

        for i, label_text in enumerate(labels):
            tk.Label(update_window, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
            entry = tk.Entry(update_window, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky=tk.EW)
            entry.insert(0, current_contact.get(label_text[:-1].lower(), ""))
            entries[label_text[:-1].lower()] = entry

        def save_updated_contact():
            updated_contact = {key: entry.get().strip() for key, entry in entries.items()}
            if not updated_contact["name"] or not updated_contact["phone"]:
                messagebox.showerror("Error", "Name and Phone are required.")
                return
            self.contacts[original_index] = updated_contact
            self.update_contact_list()
            self.show_contact_details(None) # Refresh details view
            update_window.destroy()

        tk.Button(update_window, text="Save Updates", command=save_updated_contact).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def delete_contact(self):
        """Deletes the selected contact after confirmation."""
        selected_item = self.contact_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a contact to delete.")
            return

        selected_name = self.contact_list.item(selected_item[0])['values'][0]
        index_to_delete = -1
        for i, contact in enumerate(self.contacts):
            if contact.get("name") == selected_name:
                index_to_delete = i
                break

        if index_to_delete == -1:
            messagebox.showerror("Error", "Selected contact not found in data.")
            return

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{selected_name}'?"):
            del self.contacts[index_to_delete]
            self.update_contact_list()
            # Clear details view after deletion
            for var in self.details_values.values():
                var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    contact_book = ContactBookGUI(root)
    root.mainloop()