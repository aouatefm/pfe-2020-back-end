from collections import OrderedDict
from math import ceil
from operator import itemgetter
from pprint import pprint

from google.cloud import firestore

from firebase import fs, COLLECTIONS as COL
from services.product import get_all_products, get_products_by_store
from services.store import get_stores_list
from services.user import get_all_users


def get_general_stats(store_id: str = None) -> dict:
    result = dict()
    top_stores = dict()

    if store_id is None:
        result['total_products'] = len(get_all_products())
        result['total_stores'] = len(get_stores_list())
        result['total_users'] = len(get_all_users())
        result['top_stores'] = dict()


        orders = fs.collection(COL['orders']) \
            .order_by("order_date", direction=firestore.Query.DESCENDING).stream()
    else:
        result['total_products'] = len(get_products_by_store(store_id))

        orders = fs.collection(COL['orders']) \
            .where("store_id", "==", store_id) \
            .order_by("order_date", direction=firestore.Query.DESCENDING).stream()

    result['total_orders'] = 0
    result['total_sales'] = 0
    result['top_products'] = dict()
    daily_sales_products = {}
    monthly_sales_products = {}

    orders_docs = []

    for o in orders:
        o = o.to_dict()
        orders_docs.append(o)
        result['total_orders'] += 1
        result['total_sales'] += o.get('total_price')

        date_str = o.get('order_date').strftime("%d %b %Y")
        month_year = o.get('order_date').strftime("%b %Y")

        if date_str not in daily_sales_products:
            daily_sales_products[date_str] = dict(products=0, sales=0)
        daily_sales_products[date_str]['products'] += len(o.get('products'))
        daily_sales_products[date_str]['sales'] += o.get('total_price')

        if month_year not in monthly_sales_products:
            monthly_sales_products[month_year] = dict(products=0, sales=0)
        monthly_sales_products[month_year]['products'] += len(o.get('products'))
        monthly_sales_products[month_year]['sales'] += o.get('total_price')

        if store_id is None:
            if o.get('store_id') not in top_stores:
                top_stores[o['store_id']] = 0
            top_stores[o['store_id']] += o.get('total_price')

        # top_stores[o['store_id']]['orders'] += 1
    pprint(top_stores)
    # convert to chart format
    result['daily_sales_products'] = dict(dates=list(daily_sales_products.keys()), products=[], sales=[])
    result['monthly_sales_products'] = dict(dates=list(monthly_sales_products.keys()), products=[], sales=[])

    for k, v in daily_sales_products.items():
        result['daily_sales_products']['products'].append(v.get('products'))
        result['daily_sales_products']['sales'].append(v.get('sales'))

    for k, v in monthly_sales_products.items():
        result['monthly_sales_products']['products'].append(v.get('products'))
        result['monthly_sales_products']['sales'].append(v.get('sales'))

    # sort from sup to inf
    total_days = ceil((orders_docs[0].get('order_date') - orders_docs[-1].get('order_date')).days)
    result['sale_per_day'] = result.get('total_sales') / total_days
    result['days_since_first_order'] = total_days
    # result['top_stores'] = {k: v for k, v in sorted(top_stores.items(), key=lambda item: item[1])}
    if store_id is None:
        result['top_stores'] = top_stores

    return result
