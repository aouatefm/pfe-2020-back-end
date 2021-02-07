from firebase_admin import auth
from firebase_admin._auth_utils import UserNotFoundError
from firebase_admin.auth import UserRecord
from firebase_admin.exceptions import FirebaseError
from firebase import fs, COLLECTIONS as COL
from firebase import fs
from models.user import User


def get_user_by_id(uid) -> (User, str) or (None, str):
    try:
        auth.get_user(uid)
    except UserNotFoundError:
        return None, "user does not exist in firebase auth"

    user_snapshot = fs.collection(COL['users']).document(uid).get()
    if user_snapshot.exists:
        user_data = user_snapshot.to_dict()
        user = User(**user_data)
        return user, "user found"
    else:
        return None, "user does not exist"


def check_user_exists_by_email(email: str) -> bool:
    try:
        auth.get_user_by_email(email=email)
        return True
    except UserNotFoundError:
        return False


def create_user(email: str, password: str, **kwargs) -> (User, str) or (None, str):
    if check_user_exists_by_email(email=email):
        return None, "user already exists"

    # remove store_id and uid from request payload if sent
    for k in ['store_id', 'uid']:
        try:
            kwargs.pop(k)
        except KeyError:
            pass

    # creating user in the firebase auth
    user_record: UserRecord = auth.create_user(email=email, password=password)
    user = User(uid=user_record.uid, email=email, **kwargs)
    user.role = 'user'  # set default user role to user
    fs.collection(COL['users']).document(user_record.uid).set(user.__dict__)
    return user, "User created"


def get_all_users() -> [dict]:
    users = fs.collection(COL['users']).stream()
    return [u.to_dict() for u in users]


def delete_user(uid) -> (bool, str):
    try:
        auth.delete_user(uid)
        fs.collection(COL['users']).document(uid).delete()
        return True, "user deleted"
    except UserNotFoundError as e:
        return False, str(e)


def update_user_profile(uid: str, **kwargs) -> (bool, str):
    if not get_user_by_id(uid):
        return False, "user not found!"

    # remove unwanted fields from request payload if sent
    for k in ['store_id', 'uid', 'email', 'password', 'role']:
        try:
            kwargs.pop(k)
        except KeyError:
            pass

    # update user in firestore
    fs.collection(COL['users']).document(uid).set(kwargs, merge=True)
    return True, "User Updated"


def update_user_password(uid: str, password: str) -> (bool, str):
    # update user password in firebase auth
    # TODO: test if password hash changes after login
    try:
        auth.update_user(uid, **dict(password=password))
        return True, "User password Updated successfully."
    except (ValueError, FirebaseError) as e:
        return False, str(e)


def update_user_email(uid: str, email: str) -> (bool, str):
    # check if email exists
    if check_user_exists_by_email(email):
        return False, "Email not available."

    try:
        auth.update_user(uid, **dict(email=email))  # update user email in firebase auth
        fs.collection(COL['users']).document(uid).set(dict(email=email), merge=True)  # update user email in firestore
        return True, "User email Updated successfully."
    except (ValueError, FirebaseError) as e:
        return False, str(e)
