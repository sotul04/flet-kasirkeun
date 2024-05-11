from typing import List
import flet as ft
from models.Good import Good
from models.Transaction import Transaction, Triple
from controller.TransactionController import TransactionController
from controller.GoodController import GoodController
from controller.CouponController import CouponController
from ui.alert import DialogAlert
from models.Coupon import *

class GoodBox(ft.Card):

    FOR_TRANSACTION = 0
    FOR_EDIT = 1
    
    good : Good
    addButton : ft.ElevatedButton
    editButton : ft.ElevatedButton
    removeButton : ft.ElevatedButton
    stockLabel : ft.Text

    page : ft.Page

    transactioninf : 'TransactionInterface'

    def __init__(self, good : Good, trainf : 'TransactionInterface', page : ft.Page = None, type: int = FOR_TRANSACTION, expand = False, padding = 15):
        super().__init__(expand=expand)
        self.page = page
        self.transactioninf = trainf
        self.height = 155
        self.good = good
        self.__init_addButton()
        self.__init_editButton()
        self.__init_removeButton()
        self.stockLabel = ft.Text(value=f"Stok: {self.good.get_stock}")
        self.content = ft.Container(
            margin=10,
            padding=padding,
            content=ft.Column(
                [
                    ft.ListTile(
                        leading=ft.Image(
                            src_base64=self.good.get_imgSource if self.good.get_imgSource != "" else Good.image_default,
                            width=60,
                            height=60,
                            fit=ft.ImageFit.CONTAIN
                        ),
                        title=ft.Text(self.good.get_name),
                        subtitle=ft.Text(f"Rp {self.good.get_price}")
                    ),
                    ft.Row(
                        [
                            ft.Container(
                                content= self.stockLabel,
                                padding=ft.Padding(30,0,0,0)
                            ),
                            ft.Row(
                                [
                                    self.addButton,
                                    self.editButton,
                                    self.removeButton
                                ],
                                alignment=ft.MainAxisAlignment.END,
                                expand=True
                            )
                        ]
                    )
                ]
            )
        )
        if type == GoodBox.FOR_TRANSACTION:
            self.editButton.visible = False
            self.removeButton.visible = False
            if self.good.get_stock <= 0:
                self.addButton.disabled = True
        else:
            self.addButton = False
    
    def __init_addButton(self):
        self.addButton = ft.ElevatedButton(
            text="Tambah",
            on_click=lambda e: self.add_onclick(e)
        )
    
    def __init_editButton(self):
        self.editButton = ft.ElevatedButton(
            text="Edit"
        )
    
    def __init_removeButton(self):
        self.removeButton = ft.ElevatedButton(
            text="Hapus"
        )
    
    def add_onclick(self, e):
        if GoodController.sellOneGood(self.good.get_idItem):
            self.good.set_stock = self.good.get_stock - 1
            self.stockLabel.value = self.good.get_stock
            self.transactioninf.add_item_outside(Triple(self.good, 1, self.good.get_price))
            self.update()

class GoodInterface(ft.Container):
    
    searchField : ft.Container
    goodField : ft.Column
    frame : ft.Column

    goods : List[Good]

    transactioninf : 'TransactionInterface'

    def __init__(self, page : ft.Page, trainf : 'TransactionInterface'):
        super().__init__()
        self.transactioninf = trainf
        self.page = page
        self.expand = True
        self.init_frame()
        self.content = self.frame
    
    def init_searchField(self):
        self.searchField = ft.Container(
            content= ft.TextField(
                label="Search",
                height=60,
                border_radius=30,
                on_change= lambda e: self.onchangeSearch(e),
            ),
            padding=ft.Padding(50,0,50,0),
        )
    
    def init_goodField(self):
        self.goods = GoodController.getAllGoods()
        children = [GoodBox(good, self.transactioninf) for good in self.goods]
        self.goodField = ft.Column(
            controls=children,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER
        )
        if len(self.goods) == 0:
            self.goodField.controls = [ft.Container(
                content=ft.Text("Tidak ada barang", size=16),
                padding=ft.Padding(0,40,0,0)
            )]

    def init_frame(self):
        self.init_searchField()
        self.init_goodField()
        self.frame = ft.Column(
            controls=[
                ft.Container(height=10),
                self.searchField,
                ft.Container(
                    content=ft.Text("List Barang Jualan", size=16, expand=True),
                ),
                ft.Divider(thickness=2),
                self.goodField,
            ],
        )

    def onchangeSearch(self, e : ft.ControlEvent):

        self.goods = GoodController.getSomeGoods(e.control.value)
        children = [GoodBox(good, self.transactioninf) for good in self.goods]
        self.goodField.controls = children
        if len(self.goods) == 0:
            self.goodField.controls = [ft.Container(
                content=ft.Text("Tidak ada barang", size=16),
                padding=ft.Padding(0,40,0,0)
            )]
        self.goodField.update()
    
    def update_interface(self):
        self.goods = GoodController.getSomeGoods(self.searchField.content.value)
        children = [GoodBox(good, self.transactioninf) for good in self.goods]
        self.goodField.controls = children
        if len(self.goods) == 0:
            self.goodField.controls = [ft.Container(
                content=ft.Text("Tidak ada barang", size=16),
                padding=ft.Padding(0,40,0,0)
            )]
        self.goodField.update()

class TransactionUI(ft.Container):

    left : GoodInterface
    right : 'TransactionInterface'

    page : ft.Page

    def __init__(self, page : ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.__init_right()
        self.__init_left()
        self.content = ft.Container(
            content= ft.Row(
                [
                    self.left,
                    ft.VerticalDivider(width=1, thickness=2),
                    self.right
                ],
                expand=True
            ),
            expand=True
        )

    def __init_left(self):
        self.left = GoodInterface(self.page, self.right)

    def __init_right(self):
        self.right = TransactionInterface(self.page)

class TransactionInterface(ft.Container):
    
    currentTrc : Transaction
    topBar : ft.Container
    listItem : ft.Column
    bottomBar : ft.Container

    discount : ft.Text
    couponButton : ft.ElevatedButton
    containerCoupon : ft.Container
    freeCoupon : ft.TextField
    discountCoupon : ft.TextField
    removeFreeCoupon : ft.ElevatedButton
    submitFreeCoupon : ft.ElevatedButton
    removeDiscountCoupon : ft.ElevatedButton
    submitDiscountCoupon : ft.ElevatedButton
    summary : ft.ListTile

    freeItem : Triple
    freeItemElement : 'GoodCart'

    currentDiscount : DiscountCoupon

    frame : ft.Column

    page : ft.Page

    def __init__(self, page : ft.Page):
        super().__init__()
        self.currentDiscount = None
        self.page = page
        self.expand = True
        self.init_mainFrame()
        self.content = self.frame

    def init_topBar(self):
        self.topBar = ft.Container(
            height=100,
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Row(
                            [
                                # ft.icons.TROLLEY,
                                ft.Image(src="my-flet-app/assets/trolley.png", width=70, height=70),
                                ft.Text(value="Keranjang", size=30),
                            ]
                        ),
                        expand=True,
                    ),
                    ft.ElevatedButton("Kosongkan", width=120, height=45, color=ft.colors.RED, bgcolor=ft.colors.RED_100, on_click= lambda e: self.empty_cart_onclick(e))
                ]
            )
        )
    
    def init_listItem(self):
        kaus = Good(2, "Kaus Kaki Ronaldo", 56, 300000)
        sumsang = Good(1, "sumsang s25 cross cross", 40, 30000000)

        self.currentTrc = Transaction(0, None, None, [Triple(kaus, 1, 300000), Triple(sumsang, 1, 30000000)], 30300000, "", 0.0)
        self.freeItem = None
        self.freeItemElement = None
        self.listItem = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        children = self.currentTrc.get_items
        view = [GoodCart(child.copy(), self) for child in children]
        self.listItem.controls = view

    
    def getTotalQuantity(self):
        counter = 0
        pos = 0
        for item in self.currentTrc.get_items:
            pos += 1
            counter += item.get_second
        return counter
    
    def init_bottomBar(self):
        self.discount = ft.Text()
        self.couponButton = ft.ElevatedButton(
            text="Pakai Kupon",
            on_click= lambda e: self.coupon_on_click(e)
        )
        self.summary = ft.ListTile(
            title=ft.Text(f"Rp {self.currentTrc.get_totalPrice}", color=ft.colors.WHITE, size=30),
            subtitle=ft.Text(f"{self.getTotalQuantity()} Produk", color=ft.colors.WHITE),
            trailing=ft.ElevatedButton(
                height=140,
                text="Bayar",
                color=ft.colors.BLACK,
                bgcolor=ft.colors.CYAN_200,
                on_click= lambda e: self.on_clik_bayar(e)
            ),
            bgcolor=ft.colors.BLUE,
        )
        self.freeCoupon = ft.TextField(
            width= 200,
            height= 50,
            label= "Free Coupon",
            border_radius=25,
        )
        self.discountCoupon =ft.TextField(
            width= 200,
            height= 50,
            label= "Discount Coupon",
            border_radius=25,
        )
        self.removeFreeCoupon = ft.ElevatedButton(
            text="Remove",
            visible=False,
            on_click=lambda e: self.removeFreeCoupon_onclick(e)
        )
        self.submitFreeCoupon = ft.ElevatedButton(
            text="Submit",
            on_click=lambda e: self.submitFreeCoupon_onclick(e)
        )
        self.removeDiscountCoupon = ft.ElevatedButton(
            text="Remove",
            visible=False,
            on_click=lambda e: self.removeDiscountCoupon_onclick(e)
        )
        self.submitDiscountCoupon = ft.ElevatedButton(
            text="Submit",
            on_click=lambda e: self.submitDiscountCoupon_onclick(e)
        )
        self.containerCoupon = ft.Container(
            height=120,
            visible=False,
            content= ft.Column(
                [
                    ft.Row(
                        [
                            self.freeCoupon,
                            self.removeFreeCoupon,
                            self.submitFreeCoupon,
                        ]
                    ),
                    ft.Row(
                        [
                            self.discountCoupon,
                            self.removeDiscountCoupon,
                            self.submitDiscountCoupon,
                        ]
                    ),
                ]
            )
        )
        self.bottomBar = ft.Container(
            height=120,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            self.discount,
                            self.couponButton
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    self.containerCoupon,
                    self.summary,
                ]
            )
        )
    
    def coupon_on_click(self, _):
        self.containerCoupon.visible = not self.containerCoupon.visible
        if self.containerCoupon.visible:
            self.bottomBar.height = 250
            self.couponButton.text = "Tutup"
        else:
            self.bottomBar.height = 120
            self.couponButton.text = "Pakai Kopun"
        self.bottomBar.update()
    
    def removeFreeCoupon_onclick(self, _):
        for _ in range(self.freeItem.get_second):
            GoodController.cancelOneGood(self.freeItem.get_first.get_idItem)
        self.freeItem = None
        self.currentTrc.set_couponFree = None
        self.listItem.controls.remove(self.freeItemElement)
        self.freeItemElement = None
        self.freeCoupon.value = ""
        self.submitFreeCoupon.visible = True
        self.removeFreeCoupon.visible = False
        self.update()
    
    def submitFreeCoupon_onclick(self, _):
        if not CouponController.isFreeCouponExist(self.freeCoupon.value):
            dialog = DialogAlert(self.page, info="Kupon tidak tersedia", title="Warning")
            dialog.open_dlg()
            return
        coupon = CouponController.getFreeCoupon(self.freeCoupon.value)
        pos = self.currentTrc.getItemPosition(Good(idItem=coupon.get_idItem))
        if pos < 0 or self.currentTrc.getItemQuantity(pos) < coupon.get_nItem:
            dialog = DialogAlert(self.page, info="Belum memenuhi syarat untuk memakai Kupon", title="Warning")
            dialog.open_dlg()
            return
        item_free = GoodController.getItem(coupon.get_idFree)
        if item_free.get_stock < coupon.get_nFree:
            dialog = DialogAlert(self.page, info="Jumlah barang yang tersedia tidak cukup", title="Warning")
            dialog.open_dlg()
            return
        self.currentTrc.set_couponFree = coupon.get_idCoupon
        self.freeItem = Triple(item_free, coupon.get_nFree, 0)
        self.freeItemElement = GoodCart(self.freeItem, self, isFree=True)
        dialog = DialogAlert(self.page, info="Berhasil memakai kupon", title="Success")
        dialog.open_dlg()
        self.removeFreeCoupon.visible = True
        self.submitFreeCoupon.visible = False
        self.update_all_transaction()
    
    def removeDiscountCoupon_onclick(self, _):
        self.removeDiscount()
        self.discountCoupon.value = ""
        self.submitDiscountCoupon.visible = True
        self.removeDiscountCoupon.visible = False
    
    def removeDiscount(self):
        self.currentTrc.discount = 0
        self.currentTrc.couponDiscount = None
        self.currentDiscount = None
        self.update_transaction()
    
    def updateDiscount(self):
        if self.currentDiscount != None:
            disc = self.currentTrc.get_totalPrice * self.currentDiscount.get_percentage
            self.currentTrc.discount = disc if disc <= self.currentDiscount.get_maxDiscount else self.currentDiscount.get_maxDiscount
            self.discount.value = f" - Rp {self.currentTrc.get_discount}"
        self.update()
    
    def submitDiscountCoupon_onclick(self, _):
        if not CouponController.isDiscountCouponExist(self.discountCoupon.value):
            dialog = DialogAlert(self.page, info="Kupon tidak tersedia", title="Warning")
            dialog.open_dlg()
            return
        coupon = CouponController.getDiscountCoupon(self.discountCoupon.value)
        if coupon.minBuy > self.currentTrc.get_totalPrice:
            dialog = DialogAlert(self.page, info="Batas minimum pembelian berlum tercapai", title="Warning")
            dialog.open_dlg()
            return
        self.currentDiscount = coupon
        dialog = DialogAlert(self.page, info="Berhasil memakai kupon", title="Success")
        dialog.open_dlg()
        self.currentTrc.couponDiscount = coupon.get_idCoupon
        self.removeDiscountCoupon.visible = True
        self.submitDiscountCoupon.visible = False
        self.updateDiscount()

    def init_mainFrame(self):
        self.init_topBar()
        self.init_listItem()
        self.init_bottomBar()
        self.frame = ft.Column(
            [
                self.topBar,
                ft.Container(
                    content=self.listItem,
                    expand=True,
                ),
                self.bottomBar,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
    
    def update_all_transaction(self):
        items = [GoodCart(item.copy(), self) for item in self.currentTrc.get_items]
        self.listItem.controls = items
        if self.freeItemElement != None:
            self.listItem.controls.append(self.freeItemElement)
        self.summary.title = ft.Text(f"Rp {self.currentTrc.get_totalPrice}", color=ft.colors.WHITE, size=30)
        self.summary.subtitle=ft.Text(f"{self.getTotalQuantity()} Produk", color=ft.colors.WHITE)
        self.updateDiscount()
    
    def update_transaction(self):
        self.summary.title = ft.Text(f"Rp {self.currentTrc.get_totalPrice}", color=ft.colors.WHITE, size=30)
        self.summary.subtitle=ft.Text(f"{self.getTotalQuantity()} Produk", color=ft.colors.WHITE)
        self.updateDiscount()

    def setTransaction(self, trc : Transaction):
        self.currentTrc = trc
    
    def on_clik_bayar(self, _ : ft.ControlEvent):
        if len(self.currentTrc.get_items) == 0:
            dialog = DialogAlert(self.page, info="Tidak ada barang yang dijual", title="Warning")
            dialog.open_dlg()
            return
        if self.freeItem != None:
            self.currentTrc.addItem(self.freeItem)
        if self.currentDiscount != None:
            if self.currentDiscount.get_minBuy > self.currentTrc.get_totalPrice:
                self.currentTrc.discount = 0
                self.currentTrc.couponDiscount = None
                self.currentDiscount = None
            else:
                self.currentTrc.totalPrice -= self.currentTrc.discount
        TransactionController.addTransaction(self.currentTrc)
        self.currentDiscount = None
        self.freeItem = None
        self. freeItemElement = None
        self.currentTrc = Transaction()
        self.update_all_transaction()
        dialog = DialogAlert(self.page ,info="Transaksi berhasil", title="Success")
        dialog.open_dlg()
    
    def add_item(self, item : Triple):
        self.currentTrc.addItem(item)
        self.update_transaction()
    
    def add_item_outside(self, item : Triple):
        self.currentTrc.addItem(item)
        self.update_all_transaction()
    
    def empty_cart_onclick(self, _):
        for item in self.currentTrc.items:
            for _ in range(item.get_second):
                GoodController.cancelOneGood(item.get_first.get_idItem)
        self.currentTrc = Transaction()
        self.freeItem = None
        self.freeItemElement = None
        self.currentDiscount = None
        self.update_all_transaction()
    
    def cancel_oneItem(self, item : Good):
        n_type_items = len(self.currentTrc.items)
        if self.currentTrc.cancelOneItem(item):
            if n_type_items > len(self.currentTrc.items):
                self.update_all_transaction()
            else:
                self.update_transaction()

class GoodCart(ft.Card):
    
    good : Triple

    subButton : ft.IconButton
    addButton : ft.IconButton

    quantityLabel : ft.Text

    father : TransactionInterface

    page : ft.Page

    def __init__(self, good : Triple, parents : TransactionInterface, page : ft.Page = None, isFree : bool = False, expand = False, padding = 15):
        super().__init__(expand=expand)
        self.father = parents
        self.page = page
        self.height = 120
        self.good = good
        self.__init_addButton()
        self.__init_subButton()
        self.__init_quantityLabel()
        self.content = ft.Container(
            margin=10,
            padding=padding,
            content=ft.Row(
                [
                    ft.ListTile(
                        leading=ft.Image(
                            src_base64=self.good.get_first.get_imgSource if self.good.get_first.get_imgSource != "" else Good.image_default,
                            width=60,
                            height=60,
                            fit=ft.ImageFit.CONTAIN
                        ),
                        title=ft.Text(self.good.get_first.get_name),
                        subtitle=ft.Text(f"Rp {self.good.get_third}"),
                        width=300,
                    ),
                    ft.Container(
                        content=ft.Row(
                            [
                                self.subButton,
                                self.quantityLabel,
                                self.addButton
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                        expand=True,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        if isFree:
            self.subButton.visible = False
            self.addButton.visible = False
            self.content.bgcolor = ft.colors.GREEN_300
            self.content.border_radius = 10
    
    def __init_addButton(self):
        self.addButton = ft.IconButton(
            icon=ft.icons.ADD,
            on_click= lambda e: self.add_onclick(e)
        )
    
    def __init_subButton(self):
        self.subButton = ft.IconButton(
            icon=ft.icons.REMOVE,
            on_click= lambda e: self.sub_onclick(e)
        )
    
    def __init_quantityLabel(self):
        self.quantityLabel = ft.Text(str(self.good.get_second))
    
    def add_onclick(self, _):
        if GoodController.sellOneGood(self.good.get_first.get_idItem):
            self.good.second += 1
            self.quantityLabel.value = str(self.good.get_second)
            self.good.set_third = self.good.get_third + self.good.get_first.get_price
            self.father.add_item(Triple(self.good.get_first, 1, self.good.get_first.get_price))
        self.update()
    
    def sub_onclick(self, _):
        self.father.cancel_oneItem(self.good.get_first)
        GoodController.cancelOneGood(self.good.get_first.get_idItem)
        self.good.set_second = self.good.get_second - 1
        self.quantityLabel.value = str(self.good.get_second)
        self.good.set_third = self.good.get_third - self.good.get_first.get_price
        if (self.good.set_second > 0):
            self.update()
        

