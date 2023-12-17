from django.db import models
from cryptography.fernet import Fernet
import uuid

def generate_order_id():
    return str(uuid.uuid4())

class OrderHeader(models.Model):
    ORDER_ID = models.CharField(max_length=40, primary_key=True, default=generate_order_id)
    ORDER_NAME = models.CharField(max_length=255, null=True, blank=True)
    PLACED_DATE = models.DateTimeField(null=True, blank=True)
    APPROVED_DATE = models.DateTimeField(null=True, blank=True)
    STATUS_ID = models.CharField(max_length=40, null=True, blank=True)
    CURRENCY_UOM_ID = models.CharField(max_length=40, null=True, blank=True)
    PRODUCT_STORE_ID = models.CharField(max_length=40, null=True, blank=True)
    SALES_CHANNEL_ENUM_ID = models.CharField(max_length=40, null=True, blank=True)
    GRAND_TOTAL = models.DecimalField(max_digits=24, decimal_places=4, null=True, blank=True)
    COMPLETED_DATE = models.DateTimeField(null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super(OrderHeader, self).__init__(*args, **kwargs)
        self.CREDIT_CARD_KEY = Fernet.generate_key()
        self.cipher_suite = Fernet(self.CREDIT_CARD_KEY)

    def set_credit_card(self, credit_card_number):
        encrypted_credit_card = self.cipher_suite.encrypt(credit_card_number.encode())
        self.credit_card = encrypted_credit_card.decode()

    def get_credit_card(self):
        if self.credit_card:
            decrypted_credit_card = self.cipher_suite.decrypt(self.credit_card.encode())
            return decrypted_credit_card.decode()
        return None

class Party(models.Model):
    PARTY_ID = models.CharField(max_length=40, primary_key=True)
    PARTY_TYPE_ENUM_ID = models.CharField(max_length=40, null=True, blank=True)

class Person(models.Model):
    PARTY_ID = models.CharField(max_length=40, primary_key=True)
    SALUTATION = models.CharField(max_length=255, null=True, blank=True)
    FIRST_NAME = models.CharField(max_length=255, null=True, blank=True)
    MIDDLE_NAME = models.CharField(max_length=255, null=True, blank=True)
    LAST_NAME = models.CharField(max_length=255, null=True, blank=True)
    GENDER = models.CharField(max_length=1, null=True, blank=True)
    BIRTH_DATE = models.DateField(null=True, blank=True)
    MARITAL_STATUS_ENUM_ID = models.CharField(max_length=40, null=True, blank=True)
    EMPLOYMENT_STATUS_ENUM_ID = models.CharField(max_length=40, null=True, blank=True)
    OCCUPATION = models.CharField(max_length=255, null=True, blank=True)
    PARTY_ID = models.ForeignKey(Party, on_delete=models.CASCADE)

class OrderPart(models.Model):
    ORDER_PART_SEQ_ID = models.CharField(max_length=40)
    PART_NAME = models.CharField(max_length=255, null=True, blank=True)
    STATUS_ID = models.CharField(max_length=40, null=True, blank=True)
    VENDOR_PARTY_ID = models.CharField(max_length=40, null=True, blank=True)
    CUSTOMER_PARTY_ID = models.CharField(max_length=40, null=True, blank=True)
    PART_TOTAL = models.DecimalField(max_digits=24, decimal_places=4, null=True, blank=True)
    FACILITY_ID = models.CharField(max_length=40, null=True, blank=True)
    SHIPMENT_METHOD_ENUM_ID = models.CharField(max_length=40, null=True, blank=True)
    ORDER_ID = models.ForeignKey(OrderHeader, on_delete=models.CASCADE)
    CUSTOMER_PARTY_ID = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='order_part_customer')

class Product(models.Model):
    PRODUCT_ID = models.CharField(max_length=40, primary_key=True)
    OWNER_PARTY_ID = models.CharField(max_length=40, null=True, blank=True)
    PRODUCT_NAME = models.CharField(max_length=255, null=True, blank=True)
    DESCRIPTION = models.CharField(max_length=4095, null=True, blank=True)
    CHARGE_SHIPPING = models.CharField(max_length=1, null=True, blank=True)
    RETURNABLE = models.CharField(max_length=1, null=True, blank=True)
    OWNER_PARTY_ID = models.ForeignKey(Party, on_delete=models.CASCADE)

class OrderItem(models.Model):
    ORDER_ITEM_SEQ_ID = models.CharField(max_length=40)
    ORDER_PART_SEQ_ID = models.CharField(max_length=40, null=True, blank=True)
    PRODUCT_ID = models.CharField(max_length=40, null=True, blank=True)
    ITEM_DESCRIPTION = models.CharField(max_length=255, null=True, blank=True)
    QUANTITY = models.DecimalField(max_digits=26, decimal_places=6, null=True, blank=True)
    ITEM_TYPE_ENUM_ID = models.CharField(max_length=40, null=True, blank=True)
    UNIT_AMOUNT = models.DecimalField(max_digits=25, decimal_places=5, null=True, blank=True)
    PARENT_ITEM_SEQ_ID = models.CharField(max_length=40, null=True, blank=True)
    ORDER_ID = models.ForeignKey(OrderHeader, on_delete=models.CASCADE)
    PRODUCT_ID = models.ForeignKey(Product, on_delete=models.CASCADE)


# class OrderHeader(models.Model):
#     orderId = models.CharField(primary_key=True, max_length=40)
#     orderName = models.CharField(max_length=255, null=True, blank=True)
#     placedDate = models.DateField(null=True, blank=True)
#     approvedDate = models.DateField(null=True, blank=True)
#     statusId = models.CharField(max_length=40, null=True, blank=True)
#     currencyUomId = models.CharField(max_length=40, null=True, blank=True)
#     productStoreId = models.CharField(max_length=40, null=True, blank=True)
#     salesChannelEnumId = models.CharField(max_length=40, null=True, blank=True)
#     grandTotal = models.DecimalField(max_digits=24, decimal_places=4, null=True, blank=True)

# class Person(models.Model):
#     partyId = models.CharField(primary_key=True, max_length=40)
#     salutation = models.CharField(max_length=255, null=True, blank=True)
#     firstName = models.CharField(max_length=255, null=True, blank=True)
#     middleName = models.CharField(max_length=255, null=True, blank=True)
#     lastName = models.CharField(max_length=255, null=True, blank=True)
#     gender = models.CharField(max_length=1, null=True, blank=True)
#     birthDate = models.DateField(null=True, blank=True)
#     occupation = models.CharField(max_length=255, null=True, blank=True)
#     maritalStatusEnumId = models.CharField(max_length=40, null=True, blank=True)
#     employmentStatusEnumId = models.CharField(max_length=40, null=True, blank=True)

# class Product(models.Model):
#     productId = models.CharField(primary_key=True, max_length=40)
#     ownerPartyId = models.CharField(max_length=40, null=True, blank=True)
#     productName = models.CharField(max_length=255, null=True, blank=True)
#     description = models.TextField(null=True, blank=True)
#     chargeShipping = models.CharField(max_length=1, null=True, blank=True)
#     returnable = models.CharField(max_length=1, null=True, blank=True)

# class OrderPart(models.Model):
#     orderId = models.ForeignKey(OrderHeader, on_delete=models.CASCADE)
#     orderPartSeqId = models.CharField(max_length=40)
#     partName = models.CharField(max_length=255, null=True, blank=True)
#     statusId = models.CharField(max_length=40, null=True, blank=True)
#     vendorPartyId = models.CharField(max_length=40, null=True, blank=True)
#     customerPartyId = models.CharField(max_length=40, null=True, blank=True)
#     partTotal = models.DecimalField(max_digits=24, decimal_places=4, null=True, blank=True)
#     facilityId = models.CharField(max_length=40, null=True, blank=True)
#     shipmentMethodEnumId = models.CharField(max_length=40, null=True, blank=True)

# class OrderItem(models.Model):
#     orderId = models.ForeignKey(OrderHeader, on_delete=models.CASCADE)
#     orderItemSeqId = models.CharField(max_length=40)
#     orderPartSeqId = models.CharField(max_length=40, null=True, blank=True)
#     productId = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
#     itemDescription = models.CharField(max_length=255, null=True, blank=True)
#     quantity = models.DecimalField(max_digits=26, decimal_places=6, null=True, blank=True)
#     unitAmount = models.DecimalField(max_digits=25, decimal_places=5, null=True, blank=True)
#     itemTypeEnumId = models.CharField(max_length=40, null=True, blank=True)
#     parentItemSeqId = models.CharField(max_length=40, null=True, blank=True)

