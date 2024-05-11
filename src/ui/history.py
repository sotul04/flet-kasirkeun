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
        self.height = 100
        self.transaction = transaction
        self.content = ft.Container(
            content=ft.ListTile(
                leading=ft.FloatingActionButton(
                    icon=ft.icons.SHOPPING_BASKET,
                    on_click= lambda e: self.button_onclick(e)
                ),
                title=ft.Text(f"Nomor Transaksi: {self.transaction.get_idTransaction}"),
                subtitle=ft.Text(f"{self.transaction.get_datetime}"),
                trailing=ft.Text(f"Rp {self.transaction.get_totalPrice}")
            )
        )
    
    def button_onclick(self, _):
        trc = TransactionController.getTransaction(self.transaction.get_idTransaction)
        self.father.change_details(trc)

class DetailGoods(ft.Card):

    good : Triple

    quantityLabel : ft.Text

    def __init__(self, good : Triple, padding = 15):
        super().__init__()
        self.height = 120
        self.good = good
        self.__init_quantityLabel()
        self.content = ft.Container(
            margin=10,
            padding=padding,
            content= ft.ListTile(
                leading=ft.Image(
                    src_base64=self.good.get_first.get_imgSource if self.good.get_first.get_imgSource != "" else Good.image_default,
                    width=60,
                    height=60,
                    fit=ft.ImageFit.CONTAIN
                ),
                title=ft.Text(self.good.get_first.get_name),
                subtitle=ft.Text(f"Rp {self.good.get_third}"),
                trailing=ft.Text(f"{self.good.get_second}")
            ),
        )
    
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
                self.couponDetails = ft.Text(f"Coupon: {self.transaction.get_couponFree} (Kupon Gratis), {self.transaction.get_couponDiscount} (Kupon Diskon)")
            elif self.transaction.get_couponFree != None:
                self.couponDetails = ft.Text(f"Coupon: {self.transaction.get_couponFree} (Kupon Gratis)")
            else:
                self.couponDetails = ft.Text(f"Coupon: {self.transaction.get_couponDiscount} (Kupon Diskon)")
        self.content = ft.Column(
            [
                ft.Text(f"Detail", size=40),
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
                    width=300,
                    content=ft.Column(
                        [
                            ft.Column(
                                [
                                    ft.Text(f"Nomor Transaksi: {self.transaction.get_idTransaction}"),
                                    ft.Text(f"Waktu: {self.transaction.get_datetime}"),
                                ],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                            ft.Column(
                                [
                                    self.couponDetails,
                                    ft.Text(f"{self.getTotalItem()} Produk"),
                                    ft.Text(f"Rp {self.transaction.get_totalPrice}"),
                                    ft.Text(f"Diskon -Rp {self.transaction.get_discount}", color=ft.colors.GREEN),
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
            content=ft.Text("Tidak ada transaksi dipilih", size=40, color=ft.colors.GREY),
        )
    
    def init_search(self):
        self.searchTransaction = ft.Container(
            padding=ft.Padding(37.5,0,37.5,0),
            content=ft.TextField(
                label="Search",
                height=60,
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
            on_change= lambda e: self.onchange_filter(e),
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


