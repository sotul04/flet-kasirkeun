import models.Good
from typing import List
from dataclasses import dataclass
import copy

@dataclass
class Triple:
    
    first : models.Good.Good
    second : int
    third : float

    def __init__(
        self,
        first : any = None,
        second : any  = None,
        third : any  = None,
    ) -> None:
        self.first = first
        self.second = second
        self.third = third

    @property
    def get_first(self):
        return self.first
    
    @get_first.setter
    def set_first(self, value):
        self.first = value

    @property
    def get_second(self):
        return self.second

    @get_second.setter
    def set_second(self, value):
        self.second = value

    @property
    def get_third(self):
        return self.third

    @get_third.setter
    def set_third(self, value):
        self.third = value
    
    def copy(self):
        return copy.deepcopy(self)

@dataclass
class Transaction:

    idTransaction : int
    couponFree : int | None
    couponDiscount : int | None
    items : List[Triple]
    totalPrice : float
    datetime : str
    discount : float

    def __init__(
        self,
        idTransaction : int = 0,
        couponFree : int = None,
        couponDiscount : int = None,
        items : List[Triple] = [],
        totalPrice : float = 0.0,
        datetime : str = "",
        discount : float = 0.0
    ) -> None:
        self.idTransaction = idTransaction
        self.couponFree = couponFree
        self.couponDiscount = couponDiscount
        self.items = items
        self.totalPrice = totalPrice
        self.datetime = datetime
        self.discount = discount

    @property
    def get_idTransaction(self):
        return self.idTransaction

    @get_idTransaction.setter
    def set_idTransaction(self, value):
        self.idTransaction = value

    @property
    def get_couponFree(self):
        return self.couponFree

    @get_couponFree.setter
    def set_couponFree(self, value):
        self.couponFree = value

    @property
    def get_couponDiscount(self):
        return self.couponDiscount

    @get_couponDiscount.setter
    def set_couponDiscount(self, value):
        self.couponDiscount = value

    @property
    def get_items(self):
        return self.items

    @get_items.setter
    def set_items(self, value):
        self.items = value

    @property
    def get_totalPrice(self):
        return self.totalPrice

    @get_totalPrice.setter
    def set_totalPrice(self, value):
        self.totalPrice = value

    @property
    def get_datetime(self):
        return self.datetime

    @get_datetime.setter
    def set_datetime(self, value):
        self.datetime = value

    @property
    def get_discount(self):
        return self.discount

    @get_discount.setter
    def set_discount(self, value):
        self.discount = value

    def getItem(self, index : int):
        return self.get_items[index]
    
    def getItemGood(self, index : int) -> models.Good.Good:
        return self.getItem(index).get_first

    def getItemQuantity(self, index : int) -> int:
        return self.getItem(index).get_second
    
    def getItemPrices(self, index : int) -> float:
        return self.getItem(index).get_third

    def setItem(self, index : int, item : Triple):
        self.totalPrice -= self.get_items[index].get_third
        self.items[index] = item
        self.totalPrice += item.get_third
    
    def getItemPosition(self, item : models.Good.Good) -> int :
        length = len(self.items)
        for i in range(length):
            if (self.getItemGood(i).equals(item)):
                return i
        return -1

    def addItem(self, item : Triple):
        pos = self.getItemPosition(item.get_first)
        added_price = item.get_third
        if pos < 0:
            self.items.append(item)
        else:
            quantity = item.get_second + self.getItemQuantity(pos)
            prices = item.get_third + self.getItemPrices(pos)
            newItem = Triple(item.get_first, quantity, prices)
            self.items[pos] = newItem
        self.totalPrice += added_price
    
    def add(self, good : models.Good.Good, quantity : int, prices : float):
        newItem = Triple(good, quantity, prices)
        self.addItem(newItem)
    
    def cancelOneItem(self, item : models.Good.Good) -> bool:
        pos = self.getItemPosition(item)
        if pos >= 0:
            stock = self.items[pos].get_second
            if stock > 1:
                minus = item.get_price
                self.totalPrice -= minus
                self.items[pos].third -= minus
                self.items[pos].second -= 1
            else:
                self.totalPrice -= self.items[pos].get_third
                self.items.pop(pos)
            return True
        return False

