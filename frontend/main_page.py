import tkinter as tk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from login_page    import LoginPage
from home_page     import HomePage
from Dashboard_page import DashboardPage
from page_two      import PageTwo


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bristol Pink Cafe")
        self.geometry("1280x820")
        self.minsize(960, 640)
        self.configure(bg="#111111")

        # Shared data store : Dashboard writes here; PageTwo reads it
        self.shared_data = None

        # Centre on screen
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        w, h = 1280, 820
        self.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

        # Show login first; main app loads on successful authentication
        self._show_login()

        # Keyboard shortcuts (active after login)
        self.bind("<Control-q>", lambda e: self.destroy())
        self.bind("<F1>", lambda e: self.show_page("HomePage"))
        self.bind("<F2>", lambda e: self.show_page("DashboardPage"))
        self.bind("<F3>", lambda e: self.show_page("PageTwo"))

    # Login gate
    def _show_login(self):
        """Display the login screen, covering the full window."""
        self.login_frame = LoginPage(self, on_success=self._on_login_success)
        self.login_frame.place(relwidth=1, relheight=1)

    def _on_login_success(self):
        """Called by LoginPage when credentials are accepted."""
        self.login_frame.destroy()
        self._build_main_app()

    # Main application
    def _build_main_app(self):
        """Instantiate all pages and show the home page."""
        self.container = tk.Frame(self, bg="#111111")
        self.container.pack(fill="both", expand=True)

        self.pages = {}
        for PageClass in (HomePage, DashboardPage, PageTwo):
            page = PageClass(self.container, self)
            self.pages[PageClass.__name__] = page
            page.place(relwidth=1, relheight=1)

        self.show_page("HomePage")

    def show_page(self, page_name: str):
        page = self.pages.get(page_name)
        if page is None:
            return
        page.tkraise()

        titles = {
            "HomePage":      "Bristol Pink Cafe Home",
            "DashboardPage": "Bristol Pink Cafe Sales Forecasting",
            "PageTwo":       "Bristol Pink Cafe Business Intelligence",
        }
        self.title(titles.get(page_name, "Bristol Pink Cafe"))

        if hasattr(page, "navbar"):
            page.navbar.set_active(page_name)

        if page_name == "PageTwo" and hasattr(page, "refresh_analytics"):
            page.refresh_analytics()


if __name__ == "__main__":
    app = App()
    app.mainloop()
