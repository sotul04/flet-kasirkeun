from data import cursor, commit
from models.Coupon import FreeCoupon, DiscountCoupon
from random import randint

COUPON_ID = 0
COUPON_CODE = 1
COUPON_FREE_ID_ITEM = 3
COUPON_FREE_N_ITEM = 4
COUPON_FREE_ID_FREE = 5
COUPON_FREE_N_FREE = 6

COUPON_DISCOUNT_MIN_BUY = 3
COUPON_DISCOUNT_PERCENTAGE = 4
COUPON_DISCOUNT_MAX_DISCOUNT = 5

class CouponController:

    @staticmethod
    def isFreeCouponExist(code : str) -> bool:
        result = cursor.execute(f"SELECT * from coupon NATURAL JOIN free_coupon WHERE code='{code}'")
        row = result.fetchone()
        if row:
            return True
        return False
    
    @staticmethod
    def isDiscountCouponExist(code : str) -> bool:
        result = cursor.execute(f"SELECT * FROM coupon NATURAL JOIN discount_coupon WHERE code='{code}'")
        row = result.fetchone()
        if row:
            return True
        return False

    @staticmethod
    def getFreeCoupon(code : str) -> FreeCoupon:
        result = cursor.execute(f"SELECT * FROM coupon NATURAL JOIN free_coupon WHERE code='{code}'")
        row = result.fetchone()
        return FreeCoupon(
            int(row[COUPON_ID]),
            row[COUPON_CODE], 
            int(row[COUPON_FREE_ID_ITEM]), 
            int(row[COUPON_FREE_N_ITEM]), 
            int(row[COUPON_FREE_ID_FREE]), 
            int(row[COUPON_FREE_N_FREE])
        )

    @staticmethod
    def getDiscountCoupon(code : str) -> DiscountCoupon:
        result = cursor.execute(f"SELECT * FROM coupon NATURAL JOIN discount_coupon WHERE code='{code}'")
        row = result.fetchone()
        return DiscountCoupon(
            int(row[COUPON_ID]),
            row[COUPON_CODE],
            float(row[COUPON_DISCOUNT_MIN_BUY]),
            int(row[COUPON_DISCOUNT_PERCENTAGE]),
            float(row[COUPON_DISCOUNT_MAX_DISCOUNT])
        )
    
    @staticmethod
    def deleteByCode(code : str) -> bool:
        result = cursor.execute(f"SELECT id_coupon, type FROM coupon WHERE code='{code}'")
        row = result.fetchone()
        if row:
            id = row[COUPON_ID]
            type = row[1]
            if type == "free_coupon":
                cursor.execute(f"DELETE FROM free_coupon WHERE id_coupon={id}")
            else:
                cursor.execute(f"DELETE FROM discount_coupon WHERE id_coupon={id}")
            cursor.execute(f"DELETE FROM coupon WHERE id_coupon={id}")
            commit()
            return True
        return False
    
    @staticmethod
    def deleteByID(idc : int) -> bool:
        result = cursor.execute(f"SELECT id_coupon, type FROM coupon WHERE id_coupon={idc}")
        row = result.fetchone()
        if row:
            id = row[COUPON_ID]
            type = row[1]
            if type == "free_coupon":
                cursor.execute(f"DELETE FROM free_coupon WHERE id_coupon={id}")
            else:
                cursor.execute(f"DELETE FROM discount_coupon WHERE id_coupon={id}")
            cursor.execute(f"DELETE FROM coupon WHERE id_coupon={id}")
            commit()
            return True
        return False

    @staticmethod
    def isCodeAlreadyUsed(code : str) -> bool:
        result = cursor.execute(f"SELECT * FROM coupon WHERE code='{code}'")
        row = result.fetchone()
        if row:
            return True
        return False

    @staticmethod
    def generateCouponCode() -> str:
        length = 6 + randint(0,4)
        code = ""
        for i in range(length):
            code += chr(ord('A') + randint(0,25))
        return code

    @staticmethod
    def addFreeCoupon(coupon : FreeCoupon):
        code = CouponController.generateCouponCode()
        while CouponController.isCodeAlreadyUsed(code):
            code = CouponController.generateCouponCode()
        cursor.execute(f"INSERT INTO coupon(code,type) VALUES ('{code}', 'free_coupon')")
        commit()
        result = cursor.execute(f"SELECT id_coupon FROM coupon WHERE code='{code}'")
        row = result.fetchone()
        cursor.execute(f"INSERT INTO free_coupon(id_coupon,id_item,n_item,id_free,n_free) VALUES ({row[0]},{coupon.get_idItem},{coupon.get_nItem},{coupon.get_idFree},{coupon.get_nFree})")
        commit()
    
    @staticmethod
    def addDiscountCoupon(coupon : DiscountCoupon):
        code = CouponController.generateCouponCode()
        while CouponController.isCodeAlreadyUsed(code):
            code = CouponController.generateCouponCode()
        cursor.execute(f"INSERT INTO coupon(code,type) VALUES ('{code}', 'discount_coupon')")
        commit()
        result = cursor.execute(f"SELECT id_coupon FROM coupon WHERE code='{code}'")
        row = result.fetchone()
        cursor.execute(f"INSERT INTO discount_coupon(id_coupon,min_buy,percentage,max_discount) VALUES ({row[0]},{coupon.get_minBuy},{coupon.get_percentage},{coupon.get_maxDiscount})")
        commit()

    @staticmethod
    def getAllCoupon() -> any:
        result = cursor.execute("SELECT * FROM coupon")
        rows = result.fetchall()
        return rows
    
    @staticmethod
    def setEditedFreeCoupon(coupon : FreeCoupon):
        cursor.execute(f"UPDATE free_coupon SET id_item={coupon.get_idItem}, n_item={coupon.get_nItem}, id_free={coupon.get_idFree}, n_free={coupon.get_nFree} WHERE id_coupon={coupon.get_idCoupon}")
        commit()
    
    @staticmethod
    def setEditedDiscountCoupon(coupon : DiscountCoupon):
        cursor.execute(f"UPDATE discount_coupon SET min_buy={coupon.get_minBuy}, percentage={coupon.get_percentage}, max_discount={coupon.get_maxDiscount} WHERE id_coupon={coupon.get_idCoupon}")
        commit()
