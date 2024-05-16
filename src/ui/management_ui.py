from models.Good import Good
from controller.CouponController import CouponController
from controller.GoodController import GoodController
from models.DiscountCoupon import DiscountCoupon
from models.FreeCoupon import FreeCoupon
import flet as ft
from typing import List
from typing import Union

class CouponCard(ft.Card):
    coups: Union[FreeCoupon,DiscountCoupon]
    father: 'ManajemenUI'
    def __init__(self, coupons: Union[FreeCoupon,DiscountCoupon], daddy: 'ManajemenUI' = None):
        super().__init__()
        self.coups = coupons
        self.father = daddy
        self.height = 90
        self.content = ft.Container(
            content=ft.ListTile(
                leading=ft.FloatingActionButton(
                    icon=ft.icons.AIRPLANE_TICKET,
                    on_click= lambda e: self.got_onclick(e),
                ),
                title=ft.Text("Free Coupon") if self.coups.__class__.__name__ == "FreeCoupon" else ft.Text("Discount Coupon"),
                subtitle = ft.Text(f"Buy {self.coups.getNBuy()} {GoodController.getItem(self.coups.getIDToBuy()).get_name}, Get {self.coups.getNFree()} {GoodController.getItem(self.coups.getIDFreeItem()).get_name}") if self.coups.__class__.__name__ == "FreeCoupon" else ft.Text(f"Discount {self.coups.getPercentage()}% off"),
                trailing = ft.Text(f"{self.coups.getCode()}"),
            ),
            ink=True,
            on_click= lambda e: self.got_onclick(e),
        )

    def got_onclick(self,_):
        self.father.gotten_coupon = CouponController.getCoupon(self.coups.getCode())

class ManajemenUI(ft.Container):

    coupon_list: List[Union[DiscountCoupon,FreeCoupon]]
    goods_list: List[Good]
    search_bar: ft.Container
    goods_button: ft.ElevatedButton
    coupon_button: ft.ElevatedButton
    management_field: ft.Column
    controller_area: ft.Container
    coupon_of_choice: ft.Dropdown
    gotten_coupon: Union[DiscountCoupon,FreeCoupon]
    is_goods: bool

    def __init__ (self):
        super().__init__()
        self.gotten_coupon = DiscountCoupon(0,"DUMMY-",1,1,1) # DUMMY
        self.is_goods = True
        self.init_list()
        self.init_search()
        self.init_choice()
        self.init_controller()
        self.init_button()
        self.expand = True
        self.content = ft.Row([
            ft.Container(
                expand=True,
                content=ft.Column([
                    ft.Container(height=20),
                    self.search_bar,
                    ft.Row([
                        self.goods_button,
                        ft.Container(height=30),
                        self.coupon_button,
                        ft.Container(height=30),
                        self.coupon_of_choice,
                        ft.Container(height=30),
                    ]),
                    ft.Divider(height=4),
                    self.management_field,
                ])
            ),
            ft.VerticalDivider(width=3),
            self.controller_area,
        ])

    def init_list (self):
        if (not self.is_goods):
            self.coupon_list = CouponController.getAllCoupons()
            self.goods_list = GoodController.getAllGoods()
            self.management_field = ft.Column([
                CouponCard(coupons,self) for coupons in self.coupon_list
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            )
        else:
            self.management_field = ft.Column([
                ft.Text(value="Goodies")
            ])

    def init_search(self):
        self.search_bar = ft.Container(
            padding=ft.Padding(37.5,0,37.5,0),
            content=ft.TextField(
                label="Search",
                height=70,
                border_radius=30,
                on_change= lambda e: self.onchange_filter(e)
            )
        )

    def init_choice(self):
        self.coupon_of_choice = ft.Dropdown(
            label="Choose Coupon Type",
            options=[
                ft.dropdown.Option("Any"),
                ft.dropdown.Option("Free Coupon"),
                ft.dropdown.Option("Discount Coupon"),
            ],
            width=200,
            height=50,
            on_change= lambda e: self.onchange_filter(e),
            text_size=12,
            icon_size=20,
            border_radius=30,
        )

    def init_controller(self):
        self.controller_area = ft.Container(
            content=ft.Column(
                [
                    ft.ElevatedButton(text="Add"),
                    ft.ElevatedButton(text="Edit"),
                    ft.ElevatedButton(text="Delete"),
                ]
            ),
            expand=True,
        )

    def init_button(self):
        self.goods_button = ft.ElevatedButton(text="Goods", on_click=lambda e: self.switch_status(e))
        self.coupon_button = ft.ElevatedButton(text="Coupon", on_click=lambda e: self.switch_status(e))

    def switch_status(self,_):
        self.is_goods = not self.is_goods
        if (self.is_goods):
            self.management_field.controls = ["Goodies" for i in range(5)]
            self.management_field.update()
        else:
            self.coupon_list = CouponController.getAllCoupons()
            self.goods_list = GoodController.getAllGoods()
            self.management_field.controls = [CouponCard(coupons,self) for coupons in self.coupon_list]
            self.management_field.update()

    def onchange_filter(self, _):
        tipe = self.coupon_of_choice.value
        if (not self.is_goods):
            sorter = self.search_bar.content.value
            self.coupon_list = CouponController.getSomeCoupons(sorter,tipe)
            self.management_field.controls = [CouponCard(item, self) for item in self.coupon_list]
            self.management_field.update()

class ManajemenEditor(ft.Container):
    discount_bar: ft.Container
    min_buy_bar: ft.Container
    percentage_bar: ft.Container
    bought_choice: ft.Dropdown
    bought_amount: ft.Container
    free_choice: ft.Dropdown
    free_amount: ft.Container
    ok_button: ft.ElevatedButton
    choice_coupon: ft.Dropdown
    father: 'ManajemenUI'
    status: str

    def __init__ (self, daddy: 'ManajemenUI' = None):
        super().__init__()
        self.status = "Blank"
        self.father = daddy
        self.init_choice_coupon()
        self.init_discount()
        self.init_min_buy()
        self.init_percentage()
        self.init_bought_choice()
        self.init_bought_amount()
        self.init_free_choice()
        self.init_free_amount()
        self.init_ok()
        self.content = ft.Column(
            [
                self.choice_coupon,
                ft.Row(
                    [
                        self.discount_bar if self.choice_coupon.value == "Discount Coupon" else self.bought_choice,
                        self.min_buy_bar if self.choice_coupon.value == "Discount Coupon" else self.bought_amount,
                    ]
                ),
                ft.Row(
                    [
                       self.percentage_bar if self.choice_coupon.value == "Discount Coupon" else self.free_choice,
                       self.free_amount if self.choice_coupon.value == "Free Coupon" else ft.Container(),
                    ]
                ),
                ft.Divider(height=3),
                self.init_ok,
            ]
        )
    
    def init_discount (self):
        self.discount_bar = ft.Container(
            padding=ft.Padding(20,20,0,0),
            content=ft.TextField(
                label="Insert Max Discount",
                height=50,
                border_radius=10, 
                # on_change= lambda e: self.onchange_filter(e),
            ),
        )

    def init_min_buy (self):
        self.min_buy_bar = ft.Container(
            padding=ft.Padding(20,20,0,0),
            content=ft.TextField(
                label="Insert Minimal Buying Amount",
                height=50,
                border_radius=10, 
                # on_change= lambda e: self.onchange_filter(e),
            ),
        )

    def init_percentage (self):
        self.percentage_bar = ft.Container(
            padding=ft.Padding(20,20,0,0),
            content=ft.TextField(
                label="Insert Percentage",
                height=50,
                border_radius=10,
                # on_change= lambda e: self.onchange_filter(e),
            ),
        )

    def init_bought_choice (self):
        liste = GoodController.getAllGoods()
        self.bought_choice = ft.Dropdown(
            label="Item Bought",
            options=[ft.dropdown.Option(item.get_name) for item in liste],
            width=200,
            height=50,
            # on_change= lambda e: self.onchange_filter(e),
            text_size=12,
            icon_size=20,
            border_radius=30,
        )

    def init_bought_amount (self):
        self.bought_amount = ft.Container(
            padding=ft.Padding(20,20,0,0),
            content=ft.TextField(
                label="Insert Amount Bought",
                height=50,
                border_radius=10,
                # on_change= lambda e: self.onchange_filter(e),
            ),
        )

    def init_free_choice (self):
        liste = GoodController.getAllGoods()
        self.free_choice = ft.Dropdown(
            label="Item Bought",
            options=[ft.dropdown.Option(item.get_name) for item in liste],
            width=200,
            height=50,
            # on_change= lambda e: self.onchange_filter(e),
            text_size=12,
            icon_size=20,
            border_radius=30,
        )

    def init_free_amount (self):
        self.free_amount = ft.Container(
            padding=ft.Padding(20,20,0,0),
            content=ft.TextField(
                label="Insert Amount Bought",
                height=50,
                border_radius=10,
                # on_change= lambda e: self.onchange_filter(e),
            ),
        )

    def init_choice_coupon(self):
        self.choice_coupon = ft.Dropdown(
            label="Choose Coupon Type",
            options=[
                ft.dropdown.Option("Free Coupon"),
                ft.dropdown.Option("Discount Coupon"),
            ],
            width=200,
            height=50,
            text_size=12,
            icon_size=20,
            border_radius=30,
        )

    def init_ok (self):
        self.ok_button = ft.ElevatedButton(
            text="OK",
            on_click=lambda e: self.onclick_OK(e),
        )

    def onclick_OK(self,_):
        if (self.status == "Delete" and self.father.gotten_coupon.getCode() != "DUMMY!"):
            CouponController.deleteCouponByCode(self.father.gotten_coupon.getCode())
            print("Coupon succesfully deleted")
            return
        if (self.choice_coupon.value == "Discount Coupon"):
            got_max_discount = self.discount_bar.content.value
            got_min_buy = self.min_buy_bar.content.value
            got_percentage = self.percentage_bar.content.value
            new_coupon = DiscountCoupon(1,CouponController.generateCouponCode(),got_min_buy,got_percentage,got_max_discount)
            if (self.status == "Add"):
                CouponController.createCoupon(new_coupon)
                print("Coupon successfully created")
            elif (self.status == "Edit" and self.father.gotten_coupon.getCode() != "DUMMY!"):
                CouponController.editCoupon(new_coupon)
                print("Coupon successfully edited")
        elif (self.choice_coupon.value == "Free Coupon"):
            got_bought_id = GoodController.getItemByName(self.bought_choice.value).get_idItem
            got_bought_amount = int(self.bought_amount.content.value)
            got_free_id = GoodController.getItemByName(self.free_choice.value).get_idItem
            got_free_amount = int(self.free_amount.content.value)
            new_coupon = FreeCoupon(1,CouponController.generateCouponCode(),got_bought_id,got_bought_amount,got_free_id,got_free_amount)
            if (self.status == "Add"):
                CouponController.createCoupon(new_coupon)
                print("Coupon successfully created")
            elif (self.status == "Edit" and self.father.gotten_coupon.getCode() != "DUMMY!"):
                CouponController.editCoupon(new_coupon)
                print("Coupon successfully edited")