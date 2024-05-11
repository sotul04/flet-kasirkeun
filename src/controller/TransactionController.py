from models.Transaction import Transaction, Triple
from controller.CouponController import CouponController
from models.Good import Good
from data import cursor, commit
from typing import List

class TransactionController:

    @staticmethod
    def getAll():
        result = cursor.execute("SELECT * FROM transactions")
        rows = result.fetchall()
        return rows
    
    @staticmethod
    def getDetails(id : int):
        result = cursor.execute(f"SELECT * FROM sold_goods WHERE id_transaction={id}")
        rows = result.fetchall()
        return rows

    @staticmethod
    def getSoldGoods(id : int) -> List[Triple]:
        result = cursor.execute(f"SELECT * FROM sold_goods NATURAL JOIN goods WHERE id_transaction={id}")
        rows = result.fetchall()
        items = []
        for row in rows:
            items.append(Triple(
                Good(
                    int(row[1]),
                    row[4],
                    int(row[5]),
                    float(row[6]),
                    row[7]
                ),
                int(row[2]),
                float(row[3])
            ))
        return items

    @staticmethod
    def getTransaction(id : int) -> Transaction:
        item = TransactionController.getSoldGoods(id)
        result = cursor.execute(f"SELECT * FROM transactions WHERE id_transaction={id}")
        row = result.fetchone()
        print(row)
        return Transaction(
            idTransaction= int(row[0]),
            couponFree= None if row[1] == None else int(row[1]),
            couponDiscount= None if row[2] == None else int(row[2]),
            items=item,
            totalPrice=float(row[3]),
            datetime=row[4],
            discount=float(row[5])
        )
    
    @staticmethod
    def saveDetails(id : int, item : Triple):
        cursor.execute(f"INSERT INTO sold_goods(id_transaction, id_item, quantity, prices) VALUES ({id},{item.get_first.get_idItem},{item.get_second},{item.get_third})")
        commit()
    
    @staticmethod
    def addTransaction(tsc : Transaction):
        cursor.execute(f"INSERT INTO transactions (id_free_coupon, id_discount_coupon, total_price, datetime, discount) VALUES ({tsc.get_couponFree if tsc.get_couponFree != None else 'NULL'},{tsc.get_couponDiscount if tsc.get_couponDiscount != None else 'NULL'},{tsc.get_totalPrice},datetime('now','+7 hours'),{tsc.get_discount})")
        id = cursor.lastrowid
        for trip in tsc.get_items:
            TransactionController.saveDetails(id, trip)
        if tsc.get_couponFree != None:
            CouponController.deleteByID(tsc.get_couponFree)
        if tsc.get_couponDiscount != None:
            CouponController.deleteByID(tsc.get_couponDiscount)
        commit()