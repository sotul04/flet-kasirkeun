import flet as ft

class DialogAlert(ft.AlertDialog):

    info : str 
    option : bool
    page : ft.Page

    def __init__(self, page : ft.Page, info : str = "Alert", title : str = "Alert", option : bool = False):
        super().__init__()
        self.page = page
        self.info = info
        self.title = ft.Text(title)
        self.option = option
        if option:
            self.modal = True
        self.content = ft.Text(info)
        if self.option:
            self.actions=[
                ft.TextButton("Ya", on_click= lambda e: self.close_dlg(e)),
                ft.TextButton("Batal", on_click= lambda e: self.close_dlg(e))
            ]
        self.on_dismiss=lambda e : None
    
    def close_dlq(self, e):
        self.open = False
        self.page.update()
    
    def open_dlg(self):
        self.page.dialog = self
        self.open = True
        self.page.update()