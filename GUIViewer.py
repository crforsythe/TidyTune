import tkinter as tk
from tkinter import ttk
from BaseSearcher import search_by_keyword
from BaseViewer import print_tab_from_url

def donothing():
   x = 0

class SongTabApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tidy Tune")

        # Create and place the widgets
        self.search_label = tk.Label(root, text="Enter a song title:")
        self.search_label.pack()

        self.search_entry = tk.Entry(root)
        self.search_entry.pack()

        self.search_button = tk.Button(root, text="Search", command=self.search_and_populate_list)
        self.search_button.pack()

        self.song_treeview = ttk.Treeview(root, columns=("Title", "Artist", "Rating", "Tab Type", "URL"),
                                          displaycolumns=(0, 1, 2, 3), height=5, show='headings')  # Adjust the height as needed
        self.song_treeview.heading("#1", text="Title")
        self.song_treeview.heading("#2", text="Artist")
        self.song_treeview.heading("#3", text="Rating")
        self.song_treeview.heading("#4", text="Tab Type")
        self.song_treeview.pack()

        # Create a custom tag to set text color to black
        self.song_treeview.tag_configure('black_text', foreground='black')

        self.text_panel = tk.Text(root, wrap=tk.NONE)
        self.text_panel.pack(fill=tk.BOTH, expand=True)  # Make the Text widget fill and expand in both directions

        # Current page label
        self.current_page_label = tk.Label(root, text="Page: 1")
        self.current_page_label.pack()

        # Current transposition label
        self.current_transposition_label = tk.Label(root, text="Transposition: 0")
        self.current_transposition_label.pack()

        # Left and right page navigation buttons
        self.prev_page_button = tk.Button(root, text="Prev Page", command=self.prev_page)
        self.prev_page_button.pack(side=tk.LEFT)

        self.next_page_button = tk.Button(root, text="Next Page", command=self.next_page)
        self.next_page_button.pack(side=tk.LEFT)

        # Relative transposition elements

        self.increase_transposition_button = tk.Button(root, text="+", command=self.increase_transposition)
        self.increase_transposition_button.pack(side=tk.RIGHT)

        self.transposition_value = tk.IntVar()
        self.transposition_value.set(0)
        self.transposition_display = tk.Label(root, text='Transpose')
        self.transposition_display.pack(side=tk.RIGHT)

        self.decrease_transposition_button = tk.Button(root, text="-", command=self.decrease_transposition)
        self.decrease_transposition_button.pack(side=tk.RIGHT)

        # Initialize page number
        self.current_page = 1

        # Initialize transposition value
        self.transposition_amount = 0

        # Configure the Treeview to call select_song when an item is selected
        self.song_treeview.bind("<<TreeviewSelect>>", self.select_song)


        #Menu bar
        #https://www.tutorialspoint.com/python/tk_menu.htm
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=donothing)
        filemenu.add_command(label="Open", command=donothing)
        filemenu.add_command(label="Save", command=donothing)
        filemenu.add_command(label="Save as...", command=donothing)
        filemenu.add_command(label="Close", command=donothing)

        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=donothing)
        editmenu.add_separator()
        editmenu.add_command(label="Cut", command=donothing)
        editmenu.add_command(label="Copy", command=donothing)
        editmenu.add_command(label="Paste", command=donothing)
        editmenu.add_command(label="Delete", command=donothing)
        editmenu.add_command(label="Select All", command=donothing)

        menubar.add_cascade(label="Edit", menu=editmenu)
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=donothing)
        helpmenu.add_command(label="About...", command=donothing)
        menubar.add_cascade(label="Help", menu=helpmenu)

        root.config(menu=menubar)

    def search_and_populate_list(self, results=None):
        search_term = self.search_entry.get()
        search_term = search_term.lower()
        if results is None:
            results = search_by_keyword(search_term, page_number=self.current_page)  # Use current page number
        self.song_treeview.delete(*self.song_treeview.get_children())  # Clear existing data

        for result in results:
            title = result['title']
            artist = result.get('artist', 'N/A')
            rating = result.get('rating', 'N/A')
            tab_type = result.get('type', 'N/A')
            url = result.get('tab_url', '')  # Get the URL
            self.song_treeview.insert("", "end", values=(title, artist, rating, tab_type, url))

            # Update the Treeview style to have black text for all items
        style = ttk.Style()
        style.configure("Treeview", foreground='black', background="white")
    def select_song(self, event):
        selected_song_item = self.song_treeview.selection()
        if selected_song_item:
            selected_song_url = self.song_treeview.item(selected_song_item, "values")[
                4]  # Get the URL from the fifth column
            selected_song_tab = print_tab_from_url(selected_song_url, self.transposition_amount)

            self.text_panel.delete(1.0, tk.END)
            if selected_song_tab:
                self.text_panel.insert(tk.END, selected_song_tab)
            else:
                self.text_panel.insert(tk.END, "Error fetching tablature.")

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.current_page_label.config(text=f"Page: {self.current_page}")
            self.search_and_populate_list()

    def next_page(self):
        # You may want to add logic to determine the total number of pages
        # and prevent going beyond the last page.
        search_term = self.search_entry.get()
        search_term = search_term.lower()
        search_results = search_by_keyword(search_term, page_number=self.current_page + 1)
        if search_results:
            self.current_page += 1
            self.current_page_label.config(text=f"Page: {self.current_page}")
            self.search_and_populate_list(results=search_results)

    def decrease_transposition(self):
        self.transposition_amount -= 1
        self.transposition_value.set(self.transposition_amount)
        self.current_transposition_label.config(text=f"Transposition: {self.transposition_amount}")
        self.select_song(None)  # Call select_song to update the displayed tab

    def increase_transposition(self):
        self.transposition_amount += 1
        self.transposition_value.set(self.transposition_amount)
        self.current_transposition_label.config(text=f"Transposition: {self.transposition_amount}")
        self.select_song(None)  # Call select_song to update the displayed tab


if __name__ == "__main__":
    root = tk.Tk()
    app = SongTabApp(root)
    root.mainloop()
