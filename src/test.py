# 

# import flet as ft

# def main(page):
#     page.title = "Card Example"
#     page.add(
#         ft.Card(
#             content=ft.Container(
#                 content=ft.Column(
#                     [
#                         ft.ListTile(
#                             leading=ft.Icon(ft.icons.ALBUM),
#                             title=ft.Text("The Enchanted Nightingale"),
#                             subtitle=ft.Text(
#                                 "Music by Julie Gable. Lyrics by Sidney Stein."
#                             ),
#                         ),
#                         ft.Row(
#                             [ft.TextButton("Buy tickets"), ft.TextButton("Listen")],
#                             alignment=ft.MainAxisAlignment.END,
#                         ),
#                     ]
#                 ),
#                 width=400,
#                 padding=10,
#             )
#         )
#     )

# ft.app(target=main)


import flet as ft

from ui.editor import GoodEditor, DiscountCouponEditor, FreeCouponEditor
from models.Good import Good
from models.Coupon import DiscountCoupon, FreeCoupon

def main(page: ft.Page):

    page.theme_mode = ft.ThemeMode.LIGHT

    def show(_):
        editor = GoodEditor(page)
        editor.show_editor()
    
    def show2(_):
        editor = FreeCouponEditor(page, FreeCoupon(51, "FREEDOM", 9, 3, 8, 2))
        editor.show_editor()

    page.add(
        ft.ElevatedButton(text="Press", on_click=show),
        ft.ElevatedButton(text="Discount", on_click=show2)
    )


ft.app(target=main)

# import flet as ft

# def main(page: ft.Page):
#     def dropdown_changed(e):
#         t.value = f"Dropdown changed to {dd.value}"
#         print(e.control.value)
#         page.update()

#     t = ft.Text()
#     dd = ft.Dropdown(
#         on_change=dropdown_changed,
#         options=[
#             ft.dropdown.Option(f"Nomor: {i+1}", "Anjing") for i in range (100)
#         ],
#         width=200,
#     )
#     page.add(dd, t)

# ft.app(target=main)