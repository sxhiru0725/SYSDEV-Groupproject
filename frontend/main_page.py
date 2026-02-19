import tkinter as tk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from home_page import HomePage
from Dashboard_page import DashboardPage
from page_two import PageTwo

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Bristol Pink Cafe")
        self.geometry("1280x820")
        self.minsize(960, 640)
        self.configure(bg="#111111")

        # Shared data store- Dashboard writes here; PageTwo reads it
        self.shared_data = None

        # Centre on screen
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        w, h = 1280, 820
        self.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

        # Container
        self.container = tk.Frame(self, bg="#111111")
        self.container.pack(fill="both", expand=True)

        # Instantiate all pages
        self.pages = {}
        for PageClass in (HomePage, DashboardPage, PageTwo):
            page = PageClass(self.container, self)
            self.pages[PageClass.__name__] = page
            page.place(relwidth=1, relheight=1)

        # Start on home
        self.show_page("HomePage")

        # Keyboard shortcuts
        self.bind("<Control-q>", lambda e: self.destroy())
        self.bind("<F1>", lambda e: self.show_page("HomePage"))
        self.bind("<F2>", lambda e: self.show_page("DashboardPage"))
        self.bind("<F3>", lambda e: self.show_page("PageTwo"))

    def show_page(self, page_name: str):
        page = self.pages[page_name]
        page.tkraise()

        titles = {
            "HomePage":      "Bristol Pink Cafe Home",
            "DashboardPage": "Bristol Pink Cafe Sales Forecasting",
            "PageTwo":       "Bristol Pink Cafe Business Intelligence",
        }
        self.title(titles.get(page_name, "Bristol Pink Cafe"))

        # Update navbar active highlight
        if hasattr(page, "navbar"):
            page.navbar.set_active(page_name)

        # Auto-refresh PageTwo whenever it's shown, so it picks up new CSV data
        if page_name == "PageTwo" and hasattr(page, "refresh_analytics"):
            page.refresh_analytics()


if __name__ == "__main__":
    app = App()
    app.mainloop()


