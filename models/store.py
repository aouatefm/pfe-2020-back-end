from firebase import fs


class Store:
    def __init__(self, name: str, owner_id: str, **kwargs):
        self.store_id = kwargs.get('store_id', name.replace(' ', '-').lower())
        self.owner_id = owner_id
        self.address = kwargs.get('address', "")
        self.lat = kwargs.get('lat', "")
        self.lng = kwargs.get('lng', "")
        self.phone_number = kwargs.get('phone_number', "")
        self.description = kwargs.get('description', "")
        self.cover_image = kwargs.get('cover_image', "")
        self.logo = kwargs.get('logo', "")
        self.name = name
        self.socials = kwargs.get('socials', dict(facebook="", instagram="", youtube=""))
        self.is_active = False

    store_id: str
    address: str
    owner_id: str
    phone_number: str
    description: str
    cover_image: str
    logo: str
    name: str
    socials: dict
    is_active: bool
