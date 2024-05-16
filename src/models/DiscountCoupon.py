from dataclasses import dataclass
from models.Coupon import Coupon

@dataclass
class DiscountCoupon(Coupon):
    __min_buy : int
    __percentage : int
    __max_discount : float

    def __init__ (self, couponID: int, name: str, buy: int, percent: int, discount: float):
        super().__init__(couponID,name)
        self.__min_buy = buy
        self.__percentage = percent
        self.__max_discount = discount

    def getMinBuy (self) -> int:
        return self.__min_buy
    
    def setMinBuy (self, buy: int):
        self.__min_buy = buy

    def getPercentage (self) -> int:
        return self.__percentage
    
    def setPercentage (self, percent: int):
        self.__percentage = percent

    def getMaxDiscount (self) -> float:
        return self.__max_discount
    
    def setMaxDiscount (self, maxe: float):
        self.__max_discount = maxe

    def getDiscount (self, price: float) -> float:
        if (price*self.getPercentage()/100 > self.getMaxDiscount()):
            return self.getMaxDiscount()
        return price*self.getPercentage()