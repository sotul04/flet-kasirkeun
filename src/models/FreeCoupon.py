from dataclasses import dataclass
from models.Coupon import Coupon

@dataclass
class FreeCoupon(Coupon):
    __id_item_to_buy : int
    __n_item : int
    __id_free_item : int
    __n_free : int

    def __init__ (self, couponID: int, name: str, boughtID: int, nItem: int, freeID: int, nFree: int):
        super().__init__(couponID,name)
        self.__id_item_to_buy = boughtID
        self.__n_item = nItem
        self.__id_free_item = freeID
        self.__n_free = nFree

    def getIDToBuy (self) -> int:
        return self.__id_item_to_buy
    
    def getNBuy (self) -> int:
        return self.__n_item
    
    def setNBuy (self, newN: int):
        self.__n_item = newN

    def getIDFreeItem (self) -> int:
        return self.__id_free_item
    
    def getNFree (self) -> int:
        return self.__n_free
    
    def setNFree (self, newN: int):
        self.__n_free = newN
