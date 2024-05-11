from dataclasses import dataclass

@dataclass
class Coupon:

    idCoupon : int
    code : str

    def __init__(self, idCoupon : int = 0, code : str = "") -> None:
        self.idCoupon = idCoupon
        self.code = code

    @property
    def get_idCoupon(self):
        return self.idCoupon
    
    @property
    def set_idCoupon(self, value):
        self.idCoupon = value

    @property
    def get_code(self):
        return self.code
    
    @property
    def set_code(self, value):
        self.code = value

@dataclass
class FreeCoupon(Coupon):

    idItem : int
    nItem : int
    idFree : int
    nFree : int

    def __init__(
            self, 
            idCoupon: int = 0, 
            code: str = "",
            idItem : int = 0, 
            nItem : int = 0, 
            idFree : int = 0,
            nFree : int = 0
        ) -> None:
        super().__init__(idCoupon, code)
        self.idItem = idItem
        self.nItem = nItem
        self.idFree = idFree
        self.nFree = nFree

    @property
    def get_idItem(self):
        return self.idItem

    @get_idItem.setter
    def set_idItem(self, value):
        self.idItem = value

    @property
    def get_nItem(self):
        return self.nItem

    @get_nItem.setter
    def set_nItem(self, value):
        self.nItem = value

    @property
    def get_idFree(self):
        return self.idFree

    @get_idFree.setter
    def set_idFree(self, value):
        self.idFree = value

    @property
    def get_nFree(self):
        return self.nFree

    @get_nFree.setter
    def set_nFree(self, value):
        self.nFree = value

@dataclass
class DiscountCoupon(Coupon):

    minBuy : float
    percentage : int
    maxDiscount : float

    def __init__(
            self, 
            idCoupon: int = 0, 
            code: str = "",
            minBuy : float = 0.0,
            percentage : int = 0,
            maxDiscount : float = 0.0
        ) -> None:
        super().__init__(idCoupon, code)
        self.percentage = percentage
        self.minBuy = minBuy
        self.maxDiscount = maxDiscount

    @property
    def get_percentage(self):
        return self.percentage

    @get_percentage.setter
    def set_percentage(self, value):
        self.percentage = value

    @property
    def get_minBuy(self):
        return self.minBuy

    @get_minBuy.setter
    def set_minBuy(self, value):
        self.minBuy = value

    @property
    def get_maxDiscount(self):
        return self.maxDiscount

    @get_maxDiscount.setter
    def set_maxDiscount(self, value):
        self.maxDiscount = value

    def discount(self, price : float):
        disc = price*self.percentage
        if (disc > self.maxDiscount):
            disc = self.maxDiscount
        return disc