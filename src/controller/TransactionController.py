from models.Transaction import Transaction, Triple
from controller.CouponController import CouponController
from models.Good import Good
from data import cursor, commit
from typing import List

class TransactionController:

    SORT_BY_TOTALPRICE_ASC = 0
    SORT_BY_TOTALPRICE_DESC = 1
    SORT_BY_DATE_ASC = 2
    SORT_BY_DATE_DESC = 3
    
    @staticmethod
    def getDetails(id : int):
        result = cursor.execute(f"SELECT * FROM sold_goods WHERE id_transaction={id}")
        rows = result.fetchall()
        return rows

    @staticmethod
    def getSoldGoods(id : int) -> List[Triple]:
        result = cursor.execute(f"SELECT * FROM sold_goods LEFT NATURAL JOIN goods WHERE id_transaction={id}")
        rows = result.fetchall()
        items = []
        for row in rows:
            items.append(Triple(
                Good(
                    0 if row[1] == None else int(row[1]),
                    None if row[4] == None else row[4],
                    0 if row[5] == None else int(row[5]),
                    0.0 if row[6] == None else float(row[6]),
                    Good.image_default if row[7] == None else row[7]
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
        cursor.execute(f"INSERT INTO transactions (id_free_coupon, id_discount_coupon, total_price, datetime, discount) VALUES ({tsc.get_couponFree if tsc.get_couponFree != None else 'NULL'},{tsc.get_couponDiscount if tsc.get_couponDiscount != None else 'NULL'},{tsc.get_totalPrice},datetime('now','localtime'),{tsc.get_discount})")
        id = cursor.lastrowid
        for trip in tsc.get_items:
            TransactionController.saveDetails(id, trip)
        if tsc.get_couponFree != None:
            CouponController.deleteByID(tsc.get_couponFree)
        if tsc.get_couponDiscount != None:
            CouponController.deleteByID(tsc.get_couponDiscount)
        commit()
    
    @staticmethod
    def getAll(sorted : int = SORT_BY_DATE_DESC):
        if sorted == TransactionController.SORT_BY_DATE_DESC:
            result = cursor.execute("SELECT * FROM transactions ORDER BY datetime DESC")
            rows = result.fetchall()
            return rows
        elif sorted == TransactionController.SORT_BY_DATE_ASC:
            result = cursor.execute("SELECT * FROM transactions ORDER BY datetime ASC")
            rows = result.fetchall()
            return rows
        elif sorted == TransactionController.SORT_BY_TOTALPRICE_DESC:
            result = cursor.execute("SELECT * FROM transactions ORDER BY total_price DESC")
            rows = result.fetchall()
            return rows
        else:
            result = cursor.execute("SELECT * FROM transactions ORDER BY total_price ASC")
            rows = result.fetchall()
            return rows
    
    @staticmethod
    def getRawTransaction(sorted : int = SORT_BY_DATE_DESC) -> List[Transaction]:
        rows = TransactionController.getAll(sorted=sorted)
        data = []
        for row in rows:
            data.append(Transaction(
                idTransaction= int(row[0]),
                couponFree= None if row[1] == None else int(row[1]),
                couponDiscount= None if row[2] == None else int(row[2]),
                totalPrice= float(row[3]),
                datetime=row[4],
                discount= float(row[5])
            ))
        return data
    
    @staticmethod
    def getSome(likes : str, sorted : int = SORT_BY_DATE_DESC):
        if sorted == TransactionController.SORT_BY_DATE_DESC:
            result = cursor.execute(f"SELECT * FROM transactions WHERE id_transaction LIKE '%{likes}%' OR total_price LIKE '%{likes}%' ORDER BY datetime DESC")
            rows = result.fetchall()
            return rows
        elif sorted == TransactionController.SORT_BY_DATE_ASC:
            result = cursor.execute(f"SELECT * FROM transactions WHERE id_transaction LIKE '%{likes}%' OR total_price LIKE '%{likes}%' ORDER BY datetime ASC")
            rows = result.fetchall()
            return rows
        elif sorted == TransactionController.SORT_BY_TOTALPRICE_DESC:
            result = cursor.execute(f"SELECT * FROM transactions WHERE id_transaction LIKE '%{likes}%' OR total_price LIKE '%{likes}%' ORDER BY total_price DESC")
            rows = result.fetchall()
            return rows
        else:
            result = cursor.execute(f"SELECT * FROM transactions WHERE id_transaction LIKE '%{likes}%' OR total_price LIKE '%{likes}%' ORDER BY total_price ASC")
            rows = result.fetchall()
            return rows
    
    @staticmethod
    def getSomeRawTransaction(likes : str, sorted : int = SORT_BY_DATE_DESC) -> List[Transaction]:
        rows = TransactionController.getSome(likes,sorted=sorted)
        data = []
        for row in rows:
            data.append(Transaction(
                idTransaction= int(row[0]),
                couponFree= None if row[1] == None else int(row[1]),
                couponDiscount= None if row[2] == None else int(row[2]),
                totalPrice= float(row[3]),
                datetime=row[4],
                discount= float(row[5])
            ))
        return data