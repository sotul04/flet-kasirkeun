import flet as ft
from controller.CouponController import CouponController
from controller.GoodController import GoodController
from controller.TransactionController import TransactionController
from models.Coupon import FreeCoupon, DiscountCoupon
from models.Good import *
from models.Transaction import Transaction, Triple
from ui.transaction_ui import TransactionUI, GoodCart, GoodBox
from ui.history import HistoryUI
from ui.management import ManagementUI

class MainPage:

    sideBar : ft.Column
    railNav : ft.NavigationRail
    logo : ft.Image
    mainFrame : ft.Row
    rightFrame : ft.Container
    modeButton : ft.Switch
    page : ft.Page

    transaction = TransactionUI
    history = HistoryUI
    management = ManagementUI

    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.__init_mainFrame()
        self.page.add(self.mainFrame)
        self.page.update()

    def __init_mainFrame(self):
        self.transaction = TransactionUI(self.page)
        self.history = HistoryUI()
        self.management = ManagementUI(self.page)
        self.page.floating_action_button.visible = False
        self.__init_sideBar()
        self.__init_rightFrame()
        self.mainFrame = ft.Row(
            [
                self.sideBar,
                ft.VerticalDivider(width=1, thickness=2),
                self.rightFrame,
            ],
            expand=True,
        )
    
    def on_change_sideBar(self, e : ft.ControlEvent):
        if e.control.selected_index == 0:
            print("Transaksi")
            self.rightFrame.content = self.transaction
            self.page.floating_action_button.visible = False
            self.rightFrame.update()
            self.transaction.left.update_interface()
            self.page.update()
        elif e.control.selected_index == 1:
            print("Manajemen")
            self.page.floating_action_button.visible = True
            self.rightFrame.content = self.management
            self.rightFrame.update()
            self.page.update()
        else:
            print("Riwayat")
            self.rightFrame.content = self.history
            self.page.floating_action_button.visible = False
            self.rightFrame.update()
            self.page.update()
            self.history.onchange_filter(None)

    def on_theme_change(self, e):
        if e.control.value:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.modeButton.label = "Dark"
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.modeButton.label = "Light"
        self.page.update()

    def __init_sideBar(self):
        self.__init_logo()
        self.modeButton = ft.Switch(label="Light", on_change=lambda e: self.on_theme_change(e), width=80, height=30)
        self.railNav=ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            leading=self.logo,
            extended=True,
            expand=True,
            group_alignment=-0.96,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.TROLLEY, 
                    selected_icon=ft.icons.TROLLEY, 
                    label_content=ft.Text("Transaksi"),
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.MANAGE_SEARCH_OUTLINED),
                    selected_icon_content=ft.Icon(ft.icons.MANAGE_SEARCH),
                    label="Manajemen",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.HISTORY_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.HISTORY),
                    label_content=ft.Text("Riwayat"),
                ),
            ],
            on_change=lambda e: self.on_change_sideBar(e)
        )
        self.sideBar = ft.Column(
            [
                self.railNav,
                self.modeButton,
            ],
            width=180,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
    def __init_logo(self):
        self.logo = ft.Image(src=f"src/assets/logo.png", width=170, height=80, fit=ft.ImageFit.CONTAIN)
    
    def __init_rightFrame(self):
        self.rightFrame = ft.Container(expand=True)
        self.rightFrame.content = self.transaction

app = ft.app(target=MainPage, name="Kasirkeun", assets_dir="assets")
