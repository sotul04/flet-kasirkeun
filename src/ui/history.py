from typing import List
import flet as ft
from models.Transaction import Transaction, Triple
from models.Good import Good
from controller.TransactionController import TransactionController

class HistoryCard(ft.Card):

    transaction : Transaction
    father : 'HistoryUI'

    def __init__(self, transaction : Transaction, father : 'HistoryUI' = None):
        super().__init__()
        self.father = father
        self.height = 90
        self.transaction = transaction
        self.content = ft.Container(
            content=ft.ListTile(
                leading=ft.FloatingActionButton(
                    icon=ft.icons.SHOPPING_BASKET,
                    on_click= lambda e: self.button_onclick(e)
                ),
                title=ft.Text(f"Nomor Transaksi: {self.transaction.get_idTransaction}", weight=ft.FontWeight.BOLD),
                subtitle=ft.Text(f"{self.transaction.get_datetime}"),
                trailing=ft.Text(f"Rp {self.transaction.get_totalPrice:,.1f}", size=16)
            ),
            ink=True,
            on_click= lambda e: self.button_onclick(e)
        )
    
    def button_onclick(self, _):
        trc = TransactionController.getTransaction(self.transaction.get_idTransaction)
        self.father.change_details(trc)

class DetailGoods(ft.Card):

    good : Triple

    quantityLabel : ft.Text

    nameGood : ft.Text

    def __init__(self, good : Triple):
        super().__init__()
        self.height = 100
        self.good = good
        self.nameGood = ft.Text(self.good.get_first.get_name, weight=ft.FontWeight.BOLD)
        self.__init_quantityLabel()
        self.content = ft.Container(
            margin=10,
            content= ft.ListTile(
                leading=ft.Image(
                    src_base64=self.good.get_first.get_imgSource if self.good.get_first.get_imgSource != "" else Good.image_default,
                    width=60,
                    height=60,
                    fit=ft.ImageFit.CONTAIN
                ),
                title=self.nameGood,
                subtitle=ft.Text(f"Rp {self.good.get_third:,.1f}"),
                trailing=ft.Text(f"{self.good.get_second}", size=20)
            ),
        )
        if self.good.get_first.get_name == None:
            self.nameGood.value = "Unidentified Good"
            self.nameGood.color = ft.colors.RED
    
    def __init_quantityLabel(self):
        self.quantityLabel = ft.Text(str(self.good.get_second))

class TransactionDetail(ft.Container):

    transaction : Transaction
    couponDetails : ft.Text
    
    def __init__(self, transaction : Transaction):
        super().__init__()
        self.expand = True
        self.transaction = transaction
        if self.transaction.get_couponFree == None and self.transaction.get_couponDiscount == None:
            self.couponDetails = ft.Text("Tidak ada kupon yang digunakan")
        else:
            if self.transaction.get_couponFree != None and self.transaction.get_couponDiscount != None:
                self.couponDetails = ft.Text(f"Coupon: Kupon Gratis (ID: {self.transaction.get_couponFree}), Kupon Diskon (ID: {self.transaction.get_couponDiscount})")
            elif self.transaction.get_couponFree != None:
                self.couponDetails = ft.Text(f"Coupon: Kupon Gratis (ID: {self.transaction.get_couponFree})")
            else:
                self.couponDetails = ft.Text(f"Coupon: Kupon Diskon (ID: {self.transaction.get_couponDiscount})")
        self.content = ft.Column(
            [
                ft.Container(
                    content=ft.Text(f"Detail", size=40),
                    alignment=ft.alignment.center,
                    margin=ft.Margin(0,10,0,10)
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            DetailGoods(item) for item in self.transaction.items
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    ),
                    expand=True,
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text(f"Nomor Transaksi: {self.transaction.get_idTransaction}"),
                                        ft.Text(f"Waktu: {self.transaction.get_datetime}"),
                                    ],
                                    alignment=ft.MainAxisAlignment.END,
                                ),
                                alignment=ft.alignment.Alignment(1,0),
                            ),
                            ft.Divider(thickness=2),
                            ft.Column(
                                [
                                    self.couponDetails,
                                    ft.Text(f"{self.getTotalItem()} Produk"),
                                    ft.Text(f"Rp {self.transaction.get_totalPrice:,.1f}"),
                                    ft.Text(f"Diskon: Rp {self.transaction.get_discount:,.1f}", color=ft.colors.GREEN),
                                ],
                                alignment=ft.MainAxisAlignment.START
                            )
                        ]
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    
    def getTotalItem(self):
        count = 0
        for item in self.transaction.items:
            count += item.get_second
        return count

class HistoryUI(ft.Container):

    transaction_list : List[Transaction]

    # left
    searchTransaction : ft.Container
    filterer : ft.Dropdown

    transactionField : ft.Column

    #right
    emptyBox : ft.Container

    rightPanel : ft.Container

    def __init__(self):
        super().__init__()
        self.rightPanel = ft.Container(
            expand=True
        )
        self.init_list()
        self.init_search()
        self.init_dropdown()
        self.init_emptyBox()
        self.content = ft.Row(
            [
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        [
                            ft.Container(height=20),
                            self.searchTransaction,
                            ft.Row(
                                [
                                    self.filterer,
                                    ft.Container(width=30)
                                ],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                            ft.Divider(thickness=2),
                            self.transactionField,
                        ],
                    )
                ),
                ft.VerticalDivider(width=2, thickness=2),
                self.rightPanel,
            ]
        )
        self.rightPanel.content = self.emptyBox
    
    def init_list(self):
        self.transaction_list = TransactionController.getRawTransaction()
        self.transactionField = ft.Column(
            [
                HistoryCard(item, self) for item in self.transaction_list
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )
    
    def init_emptyBox(self):
        self.emptyBox = ft.Container(
            expand=True,
            content=ft.Text("Tidak ada transaksi dipilih", size=30, color=ft.colors.GREY),
            alignment=ft.alignment.center
        )
    
    def init_search(self):
        self.searchTransaction = ft.Container(
            padding=ft.Padding(37.5,0,37.5,0),
            content=ft.TextField(
                label="Search",
                height=70,
                border_radius=30,
                on_change= lambda e: self.onchange_filter(e)
            )
        )

    def init_dropdown(self):
        self.filterer = ft.Dropdown(
            label="Urutkan berdasarkan",
            options=[
                ft.dropdown.Option("Waktu - Acsending"),
                ft.dropdown.Option("Waktu - Descending"),
                ft.dropdown.Option("Harga Total - Ascending"),
                ft.dropdown.Option("Harga Total - Descending"),
            ],
            width=250,
            height=50,
            on_change= lambda e: self.onchange_filter(e),
            text_size=12,
            icon_size=20,
            border_radius=30,
        )

    # SORT_BY_TOTALPRICE_ASC = 0
    # SORT_BY_TOTALPRICE_DESC = 1
    # SORT_BY_DATE_ASC = 2
    # SORT_BY_DATE_DESC = 3
    
    def onchange_filter(self, _):
        type = 0
        if self.filterer.value == "Waktu - Acsending":
            type = 2
        elif self.filterer.value == "Waktu - Descending":
            type = 3
        elif self.filterer.value == "Harga Total - Descending":
            type = 1
        likes = self.searchTransaction.content.value
        self.transaction_list = TransactionController.getSomeRawTransaction(likes, type)
        self.transactionField.controls = [HistoryCard(item, self) for item in self.transaction_list]
        self.transactionField.update()
    
    def change_details(self, item : Transaction):
        self.rightPanel.content = TransactionDetail(item)
        self.rightPanel.update()


