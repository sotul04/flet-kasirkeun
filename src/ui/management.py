from typing import List
import flet as ft
from models.Good import Good
from models.Coupon import FreeCoupon, DiscountCoupon, Coupon
from controller.CouponController import CouponController
from controller.GoodController import GoodController
from ui.editor import *
from ui.alert import DialogAlert

class GoodBox(ft.Card):
    
    good : Good

    father : 'GoodManager'

    def __init__(self, good : Good, father : 'GoodManager'):
        super().__init__()
        self.height = 140
        self.good = good
        self.father = father
        self.stockLabel = ft.Text(value=f"Stok: {self.good.get_stock}")
        self.content = ft.Container(
            margin=10,
            content=ft.Column(
                [
                    ft.ListTile(
                        leading=ft.Image(
                            src_base64=self.good.get_imgSource if self.good.get_imgSource != "" else Good.image_default,
                            width=60,
                            height=60,
                            fit=ft.ImageFit.CONTAIN
                        ),
                        title=ft.Text(self.good.get_name, weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(f"Rp {self.good.get_price:,.1f}")
                    ),
                    ft.Row(
                        [
                            ft.Container(
                                content= self.stockLabel,
                                padding=ft.Padding(30,0,0,0)
                            )
                        ]
                    )
                ]
            ),
            ink=True,
            on_click= lambda _: self.onclick_container()
        )

    def onclick_container(self):
        self.father.select_item(self.good)

class GoodView(ft.Container):

    good : Good

    page : ft.Page

    frame : ft.Container

    father : 'GoodManager'
    
    def __init__(self, good : Good, page : ft.Page, father : 'GoodManager'):
        super().__init__()
        self.good = good
        self.page = page
        self.father = father
        self.init_view()
    
    def init_view(self):
        self.frame = ft.Container(
            expand=True,
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Card(
                                width=500,
                                content=ft.Container(
                                    padding=10,
                                    content=ft.Row(
                                        [
                                            ft.Container(
                                                content=ft.Image(
                                                    src_base64= Good.image_default if self.good.get_imgSource == "" else self.good.get_imgSource,
                                                    height=178,
                                                    width=178,
                                                    fit=ft.ImageFit.CONTAIN
                                                ),
                                                height=180,
                                                width=180,
                                                ink=True,
                                            ),
                                            ft.Container(width=10),
                                            ft.Column(
                                                [
                                                    ft.TextField(
                                                        label="Nama Produk",
                                                        height=60,
                                                        border_radius=30,
                                                        value=self.good.get_name,
                                                        read_only=True,
                                                    ),
                                                    ft.TextField(
                                                        label="ID",
                                                        height=60,
                                                        border_radius=30,
                                                        value=self.good.get_idItem,
                                                        read_only=True,
                                                    ),
                                                    ft.TextField(
                                                        label="Harga",
                                                        height=60,
                                                        prefix_text="Rp ",
                                                        border_radius=30,
                                                        value=self.good.get_price,
                                                        read_only=True,
                                                    ),
                                                    ft.TextField(
                                                        label="Stok Barang",
                                                        height=60,
                                                        border_radius=30,
                                                        value=self.good.get_stock,
                                                        read_only=True,
                                                    ),
                                                ],
                                                alignment=ft.MainAxisAlignment.CENTER,
                                                width=200,
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    )
                                )
                            ),
                            ft.Row(
                                [
                                    ft.Container(width=5),
                                    ft.ElevatedButton(
                                        text="Edit",
                                        on_click= lambda _: self.edit_onclick()
                                    ),
                                    ft.ElevatedButton(
                                        text="Hapus",
                                        bgcolor=ft.colors.RED_200,
                                        color=ft.colors.RED,
                                        on_click= lambda _: self.delete_onclick()
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.END,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        self.content = self.frame

    def refresh_view(self):
        self.good = GoodController.getItem(self.good.get_idItem)
        self.init_view()
        self.update()
    
    def edit_onclick(self):
        GoodEditor(self.page, self, self.good).show_editor()
    
    def delete_onclick(self):
        GoodController.deleteItem(self.good.get_idItem)
        self.father.deselect_item()
        self.father.update_interface()

class GoodManager(ft.Container):
    
    listItem : List[Good]
    itemField : ft.Column

    emptyBox: ft.Container
    
    searchField : ft.Container

    page : ft.Page

    left : ft.Container
    right : ft.Container

    def __init__(self, page : ft.Page):
        super().__init__()
        self.page = page
        self.expand= True
        self.init_component()

    def init_itemField(self):
        self.listItem = GoodController.getAllGoods()
        self.itemField = ft.Column(
            [
                GoodBox(good, self) for good in self.listItem
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )
        if len(self.listItem) == 0:
            self.itemField.controls = [ft.Container(
                content=ft.Text("Tidak ada barang", size=16),
                padding=ft.Padding(0,40,0,0)
            )]
    
    def init_component(self):
        self.init_itemField()
        self.emptyBox = ft.Container(
            expand=True,
            content=ft.Text("Tidak ada item dipilih", size=30, color=ft.colors.GREY),
            alignment=ft.alignment.center
        )
        self.searchField = ft.Container(
            content= ft.TextField(
                label="Search",
                height=60,
                border_radius=30,
                on_change= lambda e: self.onchangeSearch(e),
            ),
            padding=ft.Padding(50,0,50,0),
        )
        self.left = ft.Container(
            expand=True,
            content=ft.Column(
                [
                    ft.Container(height=10),
                    self.searchField,
                    ft.Row(
                        [
                            ft.Text("List Barang Jualan", size=16),
                            ft.ElevatedButton(
                                text="Tambah",
                                on_click= lambda _: self.add_item()
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Divider(thickness=2),
                    self.itemField,
                ],
            )
        )
        self.right = ft.Container(
            expand=True,
            content=self.emptyBox
        )
        self.content = ft.Container(
            expand=True,
            content=ft.Row(
                [
                    self.left,
                    ft.VerticalDivider(width=1, thickness=2),
                    self.right,
                ]
            )
        )
    
    def onchangeSearch(self, e : ft.ControlEvent):
        self.listItem = GoodController.getSomeGoods(e.control.value)
        children = [GoodBox(good, self) for good in self.listItem]
        self.itemField.controls = children
        if len(self.listItem) == 0:
            self.itemField.controls = [ft.Container(
                content=ft.Text("Tidak ada barang", size=16),
                padding=ft.Padding(0,40,0,0)
            )]
        self.itemField.update()
    
    def update_interface(self):
        self.listItem = GoodController.getSomeGoods(self.searchField.content.value)
        children = [GoodBox(good, self) for good in self.listItem]
        self.itemField.controls = children
        if len(self.listItem) == 0:
            self.itemField.controls = [ft.Container(
                content=ft.Text("Tidak ada barang", size=16),
                padding=ft.Padding(0,40,0,0)
            )]
        self.itemField.update()
    
    def deselect_item(self):
        self.right.content = self.emptyBox
        self.right.update()
    
    def select_item(self, good : Good):
        self.right.content = GoodView(good, self.page, self)
        self.right.update()
    
    def add_item(self):
        GoodEditor(self.page, self).show_editor()

class CouponBox(ft.Card):

    coupon : FreeCoupon | DiscountCoupon

    father : 'CouponManager'

    def __init__(self, coupon : FreeCoupon | DiscountCoupon, father : 'CouponManager'):
        super().__init__()
        self.coupon = coupon
        self.father = father
        self.height = 100
        self.init_view()

    def init_view(self):
        self.content = ft.Container(
            margin=10,
            content=ft.ListTile(
                leading= ft.FloatingActionButton(
                    icon=ft.icons.CABLE
                ),
                title=ft.Text(f"ID Kupon: {self.coupon.get_idCoupon}", weight=ft.FontWeight.BOLD),
                subtitle=ft.Text(f"{"Kupon Gratis" if isinstance(self.coupon, FreeCoupon) else "Kupon Diskon"}"),
                trailing=ft.Text(f"{self.coupon.get_code}")
            ),
            ink=True,
            on_click= lambda _: self.onclick_container()
        )
    
    def onclick_container(self):
        self.father.select_item(self.coupon)

class CouponView(ft.Container):

    coupon : FreeCoupon | DiscountCoupon

    page : ft.Page
    frame : ft.Container
    father : 'GoodManager'

    def __init__(self, coupon : FreeCoupon | DiscountCoupon, page : ft.Page, father : 'GoodManager'):
        super().__init__()
        self.coupon = coupon
        self.page = page
        self.father = father
        if isinstance(self.coupon, FreeCoupon):
            self.init_view_freecoupon()
        else:
            self.init_view_discountcoupon()
    
    def init_view_freecoupon(self):
        self.frame = ft.Container(
            expand=True,
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Card(
                                width=500,
                                content=ft.Container(
                                    padding=10,
                                    content=ft.Column(
                                        [
                                            ft.TextField(
                                                label="ID Kupon",
                                                height=60,
                                                border_radius=30,
                                                value=self.coupon.get_idCoupon,
                                                read_only=True,
                                            ),
                                            ft.TextField(
                                                label="Jenis Kupon",
                                                height=60,
                                                border_radius=30,
                                                value=f"Kupon Gratis",
                                                read_only=True,
                                            ),
                                            ft.TextField(
                                                label="Kode Kupon",
                                                height=60,
                                                border_radius=30,
                                                value=self.coupon.get_code,
                                                read_only=True,
                                            ),
                                            ft.TextField(
                                                label="Produk yang harus dibeli",
                                                height=60,
                                                border_radius=30,
                                                value=GoodController.getItem(self.coupon.get_idItem).get_name,
                                                read_only=True,
                                            ),
                                            ft.TextField(
                                                label="Jumlah produk minimal",
                                                height=60,
                                                border_radius=30,
                                                value=self.coupon.get_nItem,
                                                read_only=True,
                                            ),
                                            ft.TextField(
                                                label="Produk gratis",
                                                height=60,
                                                border_radius=30,
                                                value=GoodController.getItem(self.coupon.get_idFree).get_name,
                                                read_only=True,
                                            ),
                                            ft.TextField(
                                                label="Jumlah produk gratis",
                                                height=60,
                                                border_radius=30,
                                                value=self.coupon.get_nFree,
                                                read_only=True,
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        width=300,
                                    )
                                )
                            ),
                            ft.Row(
                                [
                                    ft.Container(width=5),
                                    ft.ElevatedButton(
                                        text="Edit",
                                        on_click= lambda _: self.edit_onclick()
                                    ),
                                    ft.ElevatedButton(
                                        text="Hapus",
                                        bgcolor=ft.colors.RED_200,
                                        color=ft.colors.RED,
                                        on_click= lambda _: self.delete_onclick()
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.END
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        self.content = self.frame
    
    def init_view_discountcoupon(self):
        self.frame = ft.Container(
            expand=True,
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Card(
                                width=500,
                                content=ft.Container(
                                    padding=10,
                                    content=ft.Column(
                                        [
                                            ft.TextField(
                                                label="ID Kupon",
                                                height=60,
                                                border_radius=30,
                                                value=self.coupon.get_idCoupon,
                                                read_only=True,
                                            ),
                                            ft.TextField(
                                                label="Jenis Kupon",
                                                height=60,
                                                border_radius=30,
                                                value=f"Kupon Diskon",
                                                read_only=True,
                                            ),
                                            ft.TextField(
                                                label="Kode Kupon",
                                                height=60,
                                                border_radius=30,
                                                value=self.coupon.get_code,
                                                read_only=True,
                                            ),
                                            ft.TextField(
                                                label="Minimal Pembelian",
                                                height=60,
                                                border_radius=30,
                                                value=f"{self.coupon.get_minBuy:,.1f}",
                                                read_only=True,
                                                prefix_text="Rp ",
                                            ),
                                            ft.TextField(
                                                label="Persen Diskon",
                                                height=60,
                                                border_radius=30,
                                                value=f"{self.coupon.get_percentage}",
                                                read_only=True,
                                                suffix_text="%",
                                            ),
                                            ft.TextField(
                                                label="Diskon Maksimal",
                                                height=60,
                                                border_radius=30,
                                                value=f"{self.coupon.get_maxDiscount:,.1f}",
                                                read_only=True,
                                                prefix_text="Rp "
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        width=300,
                                    )
                                )
                            ),
                            ft.Row(
                                [
                                    ft.Container(width=5),
                                    ft.ElevatedButton(
                                        text="Edit",
                                        on_click= lambda _: self.edit_onclick()
                                    ),
                                    ft.ElevatedButton(
                                        text="Hapus",
                                        bgcolor=ft.colors.RED_200,
                                        color=ft.colors.RED,
                                        on_click= lambda _: self.delete_onclick()
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.END
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        self.content = self.frame
    
    def refresh_view(self):
        if isinstance(self.coupon, FreeCoupon):
            self.coupon = CouponController.getFreeCoupon(self.coupon.get_code)
            self.init_view_freecoupon()
        else:
            self.coupon = CouponController.getDiscountCoupon(self.coupon.get_code)
            self.init_view_discountcoupon()
        self.update()
    
    def edit_onclick(self):
        if isinstance(self.coupon, FreeCoupon):
            FreeCouponEditor(self.page, self, self.coupon).show_editor()
        else:
            DiscountCouponEditor(self.page, self, self.coupon).show_editor()
    
    def delete_onclick(self):
        CouponController.deleteByCode(self.coupon.get_code)
        self.father.deselect_item()
        self.father.update_interface()

class CouponManager(ft.Container):

    listCoupon : List[FreeCoupon | DiscountCoupon]
    itemField : ft.Column

    emptyBox : ft.Container

    searchField : ft.Container

    page : ft.Page

    left : ft.Container
    right : ft.Container

    def __init__(self, page : ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.init_component()
    
    def init_itemField(self):
        self.listCoupon = CouponController.getAll()
        self.itemField = ft.Column(
            [
                CouponBox(coupon, self) for coupon in self.listCoupon
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )
        if len(self.listCoupon) == 0:
            self.itemField.controls = [ft.Container(
                content=ft.Text("Tidak ada kupon", size=16),
                padding=ft.Padding(0,40,0,0)
            )]
    
    def init_component(self):
        self.init_itemField()
        self.emptyBox = ft.Container(
            expand=True,
            content=ft.Text("Tidak ada item dipilih", size=30, color=ft.colors.GREY),
            alignment=ft.alignment.center
        )
        self.searchField = ft.Container(
            content= ft.TextField(
                label="Search",
                height=60,
                border_radius=30,
                on_change= lambda e: self.onchangeSearch(e),
            ),
            padding=ft.Padding(50,0,50,0),
        )
        self.left = ft.Container(
            expand=True,
            content=ft.Column(
                [
                    ft.Container(height=10),
                    self.searchField,
                    ft.Row(
                        [
                            ft.Text("List Kupon", size=16),
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.TextButton(
                                            text="Kupon Diskon",
                                            icon=ft.icons.ADD,
                                            on_click= lambda _: self.add_discountcoupon()
                                        ),
                                        ft.TextButton(
                                            text="Kupon Gratis",
                                            icon=ft.icons.ADD,
                                            on_click= lambda _: self.add_freecoupon()
                                        )
                                    ]
                                )
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Divider(thickness=2),
                    self.itemField,
                ],
            )
        )
        self.right = ft.Container(
            expand=True,
            content=self.emptyBox
        )
        self.content = ft.Container(
            expand=True,
            content=ft.Row(
                [
                    self.left,
                    ft.VerticalDivider(width=1, thickness=2),
                    self.right,
                ]
            )
        )
    
    def onchangeSearch(self, e : ft.ControlEvent):
        self.listCoupon = CouponController.getSomeCoupon(e.control.value)
        children = [CouponBox(coupon, self) for coupon in self.listCoupon]
        self.itemField.controls = children
        if len(self.listCoupon) == 0:
            self.itemField.controls = [ft.Container(
                content=ft.Text("Tidak ada kupon", size=16),
                padding=ft.Padding(0,40,0,0)
            )]
        self.itemField.update()
    
    def update_interface(self):
        self.listCoupon = CouponController.getSomeCoupon(self.searchField.content.value)
        children = [CouponBox(coupon, self) for coupon in self.listCoupon]
        self.itemField.controls = children
        if len(self.listCoupon) == 0:
            self.itemField.controls = [ft.Container(
                content=ft.Text("Tidak ada kupon", size=16),
                padding=ft.Padding(0,40,0,0)
            )]
        self.itemField.update()
    
    def deselect_item(self):
        self.right.content = self.emptyBox
        self.right.update()
    
    def select_item(self, coupon : FreeCoupon | DiscountCoupon):
        self.right.content = CouponView(coupon, self.page, self)
        self.right.update()
    
    def add_freecoupon(self):
        listGoods = GoodController.getAll()
        if len(listGoods) == 0:
            DialogAlert(self.page, "Tidak dapat menambah kupon gratis untuk saat ini\nSilahkan berpindah ke manajemen produk untuk menambah produk", "List Produk masih kosong").open_dlg()
        FreeCouponEditor(self.page, self).show_editor()
    
    def add_discountcoupon(self):
        DiscountCouponEditor(self.page, self).show_editor()

class ManagementUI(ft.Container):

    page : ft.Page

    isCoupon : bool

    goodManager : GoodManager
    couponManager : CouponManager

    button : ft.FloatingActionButton

    def __init__(self, page : ft.Page):
        super().__init__()
        self.page = page
        self.isCoupon = False
        self.goodManager = GoodManager(self.page)
        self.couponManager = CouponManager(self.page)
        self.content = ft.Container(
            expand=True,
            content=self.goodManager
        )
        self.button = ft.FloatingActionButton(
            text="Produk", 
            bgcolor=ft.colors.BLUE_300, 
            on_click=lambda _: self.change_floating_onclick(),
            foreground_color=ft.colors.WHITE,
            height=50,
            width=120,
            hover_elevation=10
        )
        self.page.floating_action_button = self.button
    
    def change_floating_onclick(self):
        if self.isCoupon:
            self.isCoupon = not self.isCoupon
            self.content = self.goodManager
            self.button.text = "Produk"
            self.button.update()
            self.update()
            self.goodManager.update()
        else:
            self.isCoupon = not self.isCoupon
            self.content = self.couponManager
            self.button.text = "Kupon"
            self.button.update()
            self.update()
            self.couponManager.update()