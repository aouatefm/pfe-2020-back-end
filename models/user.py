from settings import DEFAULT_AVATAR_URL


class User:

    def __init__(self, uid: str, email: str, **kwargs):
        self.uid = uid
        self.email = email
        self.first_name = kwargs.get('first_name', "")
        self.last_name = kwargs.get('last_name', "")
        self.display_name = kwargs.get('display_name', f"{self.first_name} {self.last_name}")
        self.phone_number = kwargs.get('phone_number', None)
        self.billing_address = kwargs.get('billing_address', None)
        self.shipping_address = kwargs.get('shipping_address', None)
        self.store_id = kwargs.get('store_id', None)
        self.avatar: str = kwargs.get('avatar', DEFAULT_AVATAR_URL)
        self.role: str = kwargs.get('role', None)

    uid: str
    email: str
    first_name: str
    last_name: str
    display_name: str
    phone_number: str
    billing_address: str
    shipping_address: str
    store_id: str
    avatar: str
    role: str
