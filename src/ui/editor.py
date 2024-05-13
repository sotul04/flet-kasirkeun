from typing import List
import flet as ft
from models.Good import Good
from models.Coupon import DiscountCoupon, FreeCoupon
from controller.GoodController import GoodController
from controller.CouponController import CouponController

def isStringEmpty(s : str):
    return len(s)==0 or s.isspace()

class GoodEditor(ft.AlertDialog):

    page : ft.Page

    father : any

    good : Good

    nameField : ft.TextField
    priceField : ft.TextField
    stockField : ft.TextField

    imageField : ft.Container

    image_picker : ft.FilePicker

    frame : ft.Container

    def __init__(self, page : ft.Page, father : any, good : Good = None):
        super().__init__()
        self.good = good
        self.page = page
        self.father = father
        if good:
            self.init_edit()
        else:
            self.init_add()
        self.content = self.frame
    
    def init_component_edit(self):
        self.image_picker = ft.FilePicker(
            on_result= lambda e: self.image_result(e),
        )
        self.nameField = ft.TextField(
            label="Nama Produk",
            value=self.good.get_name,
            height=60,
            border_radius=30,
        )
        self.priceField = ft.TextField(
            label="Harga",
            value=self.good.get_price,
            prefix_text="Rp ",
            height=60,
            border_radius=30,
            input_filter=ft.NumbersOnlyInputFilter(),
        )
        self.stockField = ft.TextField(
            label="Stok",
            value=self.good.get_stock,
            height=60,
            border_radius=30,
            input_filter=ft.NumbersOnlyInputFilter(),
        )
        self.imageField = ft.Container(
            content=ft.Image(
                src_base64= Good.image_default if self.good.get_imgSource == "" else self.good.get_imgSource,
                height=178,
                width=178,
                fit=ft.ImageFit.CONTAIN
            ),
            height=180,
            width=180,
            ink=True,
            on_click= lambda _: self.image_change()
        )
    
    def init_component_add(self):
        self.image_picker = ft.FilePicker(
            on_result= lambda e: self.image_result(e),
        )
        self.nameField = ft.TextField(
            label="Nama Produk",
            max_length=255,
            border_radius=30,
        )
        self.priceField = ft.TextField(
            label="Harga",
            prefix_text="Rp ",
            height=60,
            border_radius=30,
            input_filter=ft.NumbersOnlyInputFilter(),
        )
        self.stockField = ft.TextField(
            label="Stok",
            height=60,
            border_radius=30,
            input_filter=ft.NumbersOnlyInputFilter(),
        )
        self.imageField = ft.Container(
            content=ft.Image(
                src_base64= Good.image_default,
                height=178,
                width=178,
                fit=ft.ImageFit.CONTAIN
            ),
            height=180,
            width=180,
            ink=True,
            on_click= lambda _: self.image_change()
        )
    
    def init_edit(self):
        self.init_component_edit()
        self.page.overlay.append(self.image_picker)
        self.frame = ft.Container(
            width=600,
            height=400,
            content= ft.Column(
                [
                    ft.Card(
                        content=ft.Container(
                            padding=10,
                            content=ft.Row(
                                [
                                    self.imageField,
                                    ft.Column(
                                        [
                                            self.nameField,
                                            self.priceField,
                                            self.stockField,
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        width=300,
                                    ),
                                ],
                                ft.MainAxisAlignment.SPACE_AROUND,
                            )
                        ),
                        height = 300,
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                text="Simpan",
                                on_click= lambda _: self.save_change_edit()
                            ),
                            ft.ElevatedButton(
                                text="Batal",
                                on_click= lambda _: self.close_editor()
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                expand=True,
            )
        )
    
    def init_add(self):
        self.init_component_add()
        self.page.overlay.append(self.image_picker)
        self.frame = ft.Container(
            width=600,
            height=400,
            content= ft.Column(
                [
                    ft.Card(
                        content=ft.Container(
                            padding=10,
                            content=ft.Row(
                                [
                                    self.imageField,
                                    ft.Column(
                                        [
                                            self.nameField,
                                            self.priceField,
                                            self.stockField,
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        width=300,
                                    ),
                                ],
                                ft.MainAxisAlignment.SPACE_AROUND,
                            )
                        ),
                        height = 300,
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                text="Tambah",
                                on_click= lambda _: self.save_add()
                            ),
                            ft.ElevatedButton(
                                text="Batal",
                                on_click= lambda _: self.close_editor()
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                expand=True,
            )
        )

    def image_change(self):
        self.image_picker.pick_files(
            file_type=ft.FilePickerFileType.IMAGE,
        )

    
    def image_result(self, e : ft.FilePickerResultEvent):
        if e.files:
            newbase64 = Good.image_to_base64(e.files[0].path)
            self.imageField.content.src_base64 = newbase64
            self.imageField.update()
        else:
            print("Cancelled")
    
    def show_editor(self):
        self.page.dialog = self
        self.open = True
        self.page.update()
    
    def close_editor(self):
        self.open = False
        self.page.overlay.remove(self.image_picker)
        self.page.update()
    
    def save_change_edit(self):
        name = self.nameField.value if (self.nameField.value != None and not isStringEmpty(self.nameField.value)) else None
        price = float(self.priceField.value) if (self.priceField.value != None and self.priceField.value != "") else None
        stock = int(self.stockField.value) if (self.stockField.value != None and self.stockField.value != "") else None
        if name and price and stock:
            GoodController.setEditedGood(Good(self.good.get_idItem, name, stock, price, self.imageField.content.src_base64))
            self.close_editor()
            self.father.refresh_view()
            self.father.father.update_interface()
    
    def save_add(self):
        name = self.nameField.value if (self.nameField.value != None and not isStringEmpty(self.nameField.value)) else None
        price = float(self.priceField.value) if (self.priceField.value != None and self.priceField.value != "") else None
        stock = int(self.stockField.value) if (self.stockField.value != None and self.stockField.value != "") else None
        if name and price and stock:
            GoodController.addItem(Good(0, name, stock, price, self.imageField.content.src_base64))
            self.close_editor()
            self.father.update_interface()
    

class DiscountCouponEditor(ft.AlertDialog):

    coupon : DiscountCoupon

    codeField : ft.TextField
    minbuyField : ft.TextField
    percentField : ft.TextField
    maxdiscField : ft.TextField

    page : ft.Page

    frame : ft.Container

    father : any

    def __init__(self, page : ft.Page, father : any, coupon : DiscountCoupon = None):
        super().__init__()
        self.page = page
        self.coupon = coupon
        self.father = father
        if coupon:
            self.init_edit()
        else:
            self.init_add()
        self.content = self.frame
    
    def init_component_add(self):
        self.codeField = ft.TextField(
            label="Kode kupon",
            max_length=10,
            # height=60,
            border_radius=30,
            on_change= lambda _: self.change_code()
        )
        self.minbuyField = ft.TextField(
            label="Minimal Pembelian",
            prefix_text="Rp ",
            height=60,
            border_radius=30,
            input_filter=ft.NumbersOnlyInputFilter(),
        )
        self.percentField = ft.TextField(
            label="Persen Diskon",
            suffix_text="%",
            height=60,
            border_radius=30,
            input_filter=ft.NumbersOnlyInputFilter(),
            on_change= lambda _: self.change_percent()
        )
        self.maxdiscField = ft.TextField(
            label="Diskon Maksimal",
            prefix_text="Rp ",
            height=60,
            border_radius=30,
            input_filter=ft.NumbersOnlyInputFilter(),
        )
    
    def init_component_edit(self):
        self.minbuyField = ft.TextField(
            label="Minimal Pembelian",
            prefix_text="Rp ",
            value=self.coupon.get_minBuy,
            height=60,
            border_radius=30,
            input_filter=ft.NumbersOnlyInputFilter(),
        )
        self.percentField = ft.TextField(
            label="Persen Diskon",
            suffix_text="%",
            value=self.coupon.get_percentage,
            height=60,
            border_radius=30,
            input_filter=ft.NumbersOnlyInputFilter(),
            on_change= lambda _: self.change_percent()
        )
        self.maxdiscField = ft.TextField(
            label="Diskon Maksimal",
            prefix_text="Rp ",
            value=self.coupon.get_maxDiscount,
            height=60,
            border_radius=30,
            input_filter=ft.NumbersOnlyInputFilter(),
        )
    
    def check_code(self):
        code = self.codeField.value
        value = False
        usedBefore = CouponController.isCodeAlreadyUsed(code)
        if code == None or isStringEmpty(code) or usedBefore:
            self.codeField.prefix_text = "Invalid  "
            self.codeField.prefix_style = ft.TextStyle(foreground=ft.Paint(color=ft.colors.RED))
        else:
            self.codeField.prefix_text = None
            self.codeField.prefix_style = None
            value = True
        self.codeField.update()
        return value
    
    def change_code(self):
        self.check_code()
    
    def check_percent(self):
        percent = self.percentField.value
        if percent == None or percent == "":
            self.percentField.prefix_text = "Invalid  "
            self.percentField.prefix_style = ft.TextStyle(foreground=ft.Paint(color=ft.colors.RED))
            self.percentField.update()
            return False
        if int(percent) <= 0 or int(percent)> 100:
            self.percentField.prefix_text = "Invalid  "
            self.percentField.prefix_style = ft.TextStyle(foreground=ft.Paint(color=ft.colors.RED))
            self.percentField.update()
            return False
        self.percentField.prefix_text = None
        self.percentField.prefix_style = None
        self.percentField.update()
        return True
    
    def change_percent(self):
        self.check_percent()
    
    def show_editor(self):
        self.page.dialog = self
        self.open = True
        self.page.update()
    
    def close_editor(self):
        self.open = False
        self.page.update()
    
    def save_change_edit(self):
        minbuy = float(self.minbuyField.value) if (self.minbuyField.value != None and self.minbuyField.value != "") else None
        percent = int(self.percentField.value) if (self.percentField.value != None and self.percentField.value != "") else None
        maxDisc = float(self.maxdiscField.value) if (self.maxdiscField.value != None and self.maxdiscField.value != "") else None
        percentValid = self.check_percent()
        if minbuy and percent and maxDisc and percentValid:
            CouponController.setEditedDiscountCoupon(DiscountCoupon(self.coupon.get_idCoupon,self.coupon.get_code,minbuy, percent, maxDisc))
            self.close_editor()
            self.father.refresh_view()
            self.father.father.update_interface()
        
    def save_change_add(self):
        notused = self.check_code()
        code = self.codeField.value
        minbuy = float(self.minbuyField.value) if (self.minbuyField.value != None and self.minbuyField.value != "") else None
        percent = int(self.percentField.value) if (self.percentField.value != None and self.percentField.value != "") else None
        maxDisc = float(self.maxdiscField.value) if (self.maxdiscField.value != None and self.maxdiscField.value != "") else None
        percentValid = self.check_percent()
        if notused and code and minbuy and percent and maxDisc and percentValid:
            CouponController.addDiscountCoupon(DiscountCoupon(0,self.codeField.value,minbuy, percent, maxDisc))
            self.close_editor()
            self.father.update_interface()
    
    def init_add(self):
        self.init_component_add()
        self.frame = ft.Container(
            width=500,
            height=380,
            content= ft.Column(
                [
                    ft.Card(
                        content=ft.Container(
                            padding=ft.Padding(30,20,30,20),
                            content=ft.Column(
                                [
                                    self.codeField,
                                    self.minbuyField,
                                    self.percentField,
                                    self.maxdiscField,
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ),
                        height=340,
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                text="Tambah",
                                on_click= lambda _: self.save_change_add()
                            ),
                            ft.ElevatedButton(
                                text="Batal",
                                on_click= lambda _: self.close_editor()
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY
            )
        )
    
    def init_edit(self):
        self.init_component_edit()
        self.frame = ft.Container(
            width=500,
            height=320,
            content= ft.Column(
                [
                    ft.Card(
                        content=ft.Container(
                            padding=ft.Padding(30,20,30,20),
                            content=ft.Column(
                                [
                                    self.minbuyField,
                                    self.percentField,
                                    self.maxdiscField,
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ),
                        height=260,
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                text="Simpan",
                                on_click= lambda _: self.save_change_edit()
                            ),
                            ft.ElevatedButton(
                                text="Batal",
                                on_click= lambda _: self.close_editor()
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY
            )
        )


class FreeCouponEditor(ft.AlertDialog):

    coupon : FreeCoupon

    codeField : ft.TextField
    itemField : ft.Dropdown
    itemCount : ft.TextField
    freeField : ft.Dropdown
    freeCount : ft.TextField

    listItem : List[Good]

    page : ft.Page

    frame : ft.Container

    father : any

    def __init__(self, page : ft.Page, father : any, coupon : FreeCoupon = None):
        super().__init__()
        self.page = page
        self.coupon = coupon
        self.father = father
        if coupon:
            self.init_edit()
        else:
            self.init_add()
        self.content = self.frame
    
    def check_code(self):
        code = self.codeField.value
        value = False
        usedBefore = CouponController.isCodeAlreadyUsed(code)
        if code == None or isStringEmpty(code) or usedBefore:
            self.codeField.prefix_text = "Invalid  "
            self.codeField.prefix_style = ft.TextStyle(foreground=ft.Paint(color=ft.colors.RED))
        else:
            self.codeField.prefix_text = None
            self.codeField.prefix_style = None
            value = True
        self.codeField.update()
        return value
    
    def change_code(self):
        self.check_code()
    
    def show_editor(self):
        self.page.dialog = self
        self.open = True
        self.page.update()
    
    def close_editor(self):
        self.open = False
        self.page.update()
    
    def init_listItem(self):
        self.listItem = GoodController.getAllGoods()
        self.itemField = ft.Dropdown(
            label="Produk yang harus dibeli",
            options=[
                ft.dropdown.Option(key=f"{item.get_idItem}", text=f"{item.get_name}") for item in self.listItem
            ],
            width=300,
        )
        self.freeField = ft.Dropdown(
            label="Produk gratis",
            options=[
                ft.dropdown.Option(key=f"{item.get_idItem}", text=f"{item.get_name}") for item in self.listItem
            ],
            width=300,
        )
    
    def init_component_add(self):
        self.init_listItem()
        self.itemField.value = str(self.listItem[0].get_idItem)
        self.freeField.value = str(self.listItem[0].get_idItem)
        self.codeField = ft.TextField(
            label="Kode kupon",
            max_length=10,
            # height=60,
            border_radius=30,
            on_change= lambda _: self.change_code()
        )
        self.itemCount = ft.TextField(
            label="Jumlah produk",
            height=60,
            width=150,
            border_radius=30,
            input_filter=ft.NumbersOnlyInputFilter(),
        )
        self.freeCount = ft.TextField(
            label="Jumlah produk gratis",
            height=60,
            width=150,
            border_radius=30,
            input_filter=ft.NumbersOnlyInputFilter(),
        )
    
    def init_component_edit(self):
        self.init_listItem()
        self.itemField.value = str(self.coupon.get_idItem)
        self.freeField.value = str(self.coupon.get_idFree)
        self.itemCount = ft.TextField(
            label="Jumlah produk",
            height=60,
            width=130,
            value=str(self.coupon.get_nItem),
            border_radius=30,
            input_filter=ft.NumbersOnlyInputFilter(),
        )
        self.freeCount = ft.TextField(
            label="Jumlah produk gratis",
            height=60,
            width=130,
            value=str(self.coupon.get_nFree),
            border_radius=30,
            input_filter=ft.NumbersOnlyInputFilter(),
        )
    
    def init_add(self):
        self.init_component_add()
        self.frame = ft.Container(
            width=600,
            height=300,
            content= ft.Column(
                [
                    ft.Card(
                        content=ft.Container(
                            padding=ft.Padding(30,20,30,20),
                            content=ft.Column(
                                [
                                    self.codeField,
                                    ft.Row(
                                        [
                                            self.itemField,
                                            self.itemCount,
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_AROUND
                                    ),
                                    ft.Row(
                                        [
                                            self.freeField,
                                            self.freeCount,
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_AROUND
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ),
                        height=260,
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                text="Tambah",
                                on_click= lambda _: self.save_change_add()
                            ),
                            ft.ElevatedButton(
                                text="Batal",
                                on_click= lambda _: self.close_editor()
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY
            )
        )
    
    def init_edit(self):
        self.init_component_edit()
        self.frame = ft.Container(
            width=500,
            height=270,
            content= ft.Column(
                [
                    ft.Card(
                        content=ft.Container(
                            padding=ft.Padding(30,20,30,20),
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            self.itemField,
                                            ft.Text("  "),
                                            self.itemCount,
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_AROUND
                                    ),
                                    ft.Row(
                                        [
                                            self.freeField,
                                            ft.Text("  "),
                                            self.freeCount,
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_AROUND
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ),
                        height=240,
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                text="Simpan",
                                on_click= lambda _: self.save_change_edit()
                            ),
                            ft.ElevatedButton(
                                text="Batal",
                                on_click= lambda _: self.close_editor()
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY
            )
        )
    
    def save_change_add(self):
        notused = self.check_code()
        code = self.codeField.value
        iditem = int(self.itemField.value)
        nitem = 0 if (self.itemCount.value == None or self.itemCount.value == "") else int(self.itemCount.value)
        idfree = int(self.freeField.value)
        nfree = 0 if (self.freeCount.value == None or self.freeCount.value == "") else int(self.freeCount.value)

        if notused and code:
            CouponController.addFreeCoupon(FreeCoupon(0,code,iditem, nitem, idfree, nfree))
            self.close_editor()
            self.father.update_interface()
    
    def save_change_edit(self):
        iditem = int(self.itemField.value)
        nitem = 0 if (self.itemCount.value == None or self.itemCount.value == "") else int(self.itemCount.value)
        idfree = int(self.freeField.value)
        nfree = 0 if (self.freeCount.value == None or self.freeCount.value == "") else int(self.freeCount.value)
        CouponController.setEditedFreeCoupon(FreeCoupon(self.coupon.get_idCoupon, self.coupon.get_code, iditem, nitem, idfree, nfree))
        self.close_editor()
        self.father.refresh_view()
        self.father.father.update_interface()
