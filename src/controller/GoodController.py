from typing import List
from data import cursor, commit
from models import Good

GOOD_ID = 0
GOOD_NAME = 1
GOOD_STOCK = 2
GOOD_PRICE = 3
GOOD_IMG = 4

class GoodController:

    @staticmethod
    def isItemExist(id : int) -> bool:
        result = cursor.execute(f"SELECT * FROM goods WHERE id_item={id}")
        row = result.fetchone()
        if row:
            return True
        return False
    
    @staticmethod
    def getItem(id : int) -> Good:
        result = cursor.execute(f"SELECT * from goods WHERE id_item={id}")
        row = result.fetchone()
        if row:
            return Good(
                int(row[GOOD_ID]),
                row[GOOD_NAME],
                int(row[GOOD_STOCK]),
                float(row[GOOD_PRICE]),
                row[GOOD_IMG]
            )
        else:
            return Good()

    @staticmethod
    def setEditedGood(target : Good):
        cursor.execute(f"UPDATE goods SET name='{target.get_name}', stock={target.get_stock}, price={target.get_price}, img_source='{target.get_imgSource}' WHERE id_item={target.get_idItem}")
        commit()
    
    @staticmethod
    def deleteItem(id : int):
        cursor.execute(f"DELETE FROM goods WHERE id_item={id}")
        commit()
    
    @staticmethod
    def addItem(good: Good):
        image = good.get_imgSource
        if image == "":
            image = Good.image_default
        cursor.execute(f"INSERT INTO goods(name,stock,price,img_source) VALUES ('{good.get_name}',{good.get_stock},{good.get_price},'{image}')")
        commit()

    @staticmethod
    def getAll() -> any:
        result = cursor.execute("SELECT * FROM goods")
        rows = result.fetchall()
        return rows
    
    @staticmethod
    def getSome(likes : str) -> any:
        result = cursor.execute(f"SELECT * FROM goods WHERE name LIKE '%{likes}%' OR id_item LIKE '%{likes}%'")
        rows = result.fetchall()
        return rows
    
    @staticmethod
    def getAllGoods() -> List[Good]:
        rows = GoodController.getAll()
        goods = []
        for row in rows:
            goods.append(Good(
                int(row[0]),
                row[1],
                int(row[2]),
                float(row[3]),
                row[4]
            ))
        return goods
    
    @staticmethod
    def getSomeGoods(likes : str) -> List[Good]:
        rows = GoodController.getSome(likes)
        goods = []
        for row in rows:
            goods.append(Good(
                int(row[0]),
                row[1],
                int(row[2]),
                float(row[3]),
                row[4]
            ))
        return goods
    
    @staticmethod
    def sellOneGood(id : int) -> bool:
        result = cursor.execute(f"SELECT stock FROM goods WHERE id_item={id}")
        row = result.fetchone()
        if int(row[0]) > 0:
            cursor.execute(f"UPDATE goods SET stock={row[0]-1} WHERE id_item={id}")
            commit()
            return True
        return False
    
    @staticmethod
    def cancelOneGood(id : int):
        result = cursor.execute(f"SELECT stock FROM goods WHERE id_item={id}")
        row = result.fetchone()
        cursor.execute(f"UPDATE goods SET stock={row[0]+1} WHERE id_item={id}")
        commit()