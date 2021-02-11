from firebase import fs


def get_all_categories():
    categories = fs.collection('categories').stream()
    result = [dict(id=c.id,**c.to_dict()) for c in categories]
    return dict(data=result)


class Category:
    def __init__(self, title, description, products=[], sub_categories=[]):
        self.title = title
        self.description = description
        self.products = products
        self.sub_categories = sub_categories

