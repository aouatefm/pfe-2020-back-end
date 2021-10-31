from datetime import datetime

ORDER_STATUS = {'pending': 'pending',
                'processing': 'processing',
                'completed': 'completed',
                'cancelled': 'cancelled'}


class Order:
    def __init__(self, customer_id: str, store_id: str, products: [dict], **kwargs):
        self.order_id = kwargs.get('order_id')
        self.customer_id = customer_id
        self.store_id = store_id
        self.products = products
        self.status = kwargs.get('status', ORDER_STATUS["pending"])
        self.order_date = kwargs.get('order_date', datetime.now())
        self.billing_adr = kwargs.get('billing_adr', "")
        self.shipping_adr = kwargs.get('shipping_adr', "")
        self.contact_number = kwargs.get('contact_number', "")
        self.total_price = kwargs.get('total_price', 0)
        self.delivery = kwargs.get('delivery', 0)
        self.payment = kwargs.get('payment', 'cash')
        self.notes = kwargs.get('notes', '')
        self.second_contact_number = kwargs.get('second_contact_number', '')

    order_id: str
    customer_id: str
    store_id: str
    products: [dict]
    status: str
    order_date: datetime
    billing_adr: str
    shipping_adr: str
    contact_number: str
    total_price: float
    delivery: float
    payment: str
    notes: str

# TODO: add payment and delivery and notes to the creation of order
