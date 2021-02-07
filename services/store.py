from firebase import fs, COLLECTIONS as COL
from models.store import Store
from services.user import get_user_by_id, update_user_profile


def check_store_exist(store_id: str) -> bool:
    store = fs.collection(COL['stores']).document(store_id).get()
    return store.exists


def get_store_by_id(store_id: str) -> (Store, str) or (None, str):
    store = fs.collection(COL['stores']).document(store_id).get()
    if store.exists:
        return Store(**store.to_dict()), "store found"
    else:
        return None, "store not found!"


def create_store(name: str, owner_id: str, **kwargs) -> (Store, str) or (None, str):
    store_id = name.replace(' ', '-'.lower())
    if check_store_exist(store_id):
        return None, "store already exists"

    user, detail = get_user_by_id(owner_id)
    if user.store_id is not None:
        return None, "user already have a store!"

    store = Store(name, owner_id, **kwargs)
    # create new store for the user
    fs.collection(COL['stores']).document(store_id).set(store.__dict__)
    # update user  with the newly created store id
    fs.collection(COL['users']).document(owner_id).set(dict(store_id=store_id), merge=True)

    return store, "store created."


def update_store(store_id, **kwargs) -> (bool, str):
    if not check_store_exist(store_id):
        return None, "store doest not exist."
    forbidden_fields = ['store_id', 'owner_id']
    for k in forbidden_fields:
        try:
            kwargs.pop(k)
        except KeyError:
            pass
    fs.collection(COL['stores']).document(store_id).set(kwargs, merge=True)
    return True, "store updated."


def delete_store(store_id: str) -> (bool, str):
    store = fs.collection(COL['stores']).document(store_id).get()
    if not store.exists:
        return False, "store not found."
    else:
        store = store.to_dict()

    fs.collection(COL['users']).document(store.get('owner_id')).set(dict(store_id=None), merge=True)
    fs.collection(COL['stores']).document(store_id).delete()
    return True, "store deleted."


def get_stores_list() -> [dict]:
    stores = fs.collection(COL['stores']).stream()
    return [s.to_dict() for s in stores]
