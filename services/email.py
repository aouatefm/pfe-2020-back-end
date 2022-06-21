from models.order import Order
from models.user import User
from settings import mailjet, APP_EMAIL


def send_order_confirmation_email(user: User, order: Order):
    product_rows = ""
    product_row = f"""
    <tr>
    <td style="width: 151.484px; height: 40px; text-align: center;"><img style="margin: 1px 15px;" src="#IMG_URL" width="140" height="120" /></td>
    <td style="width: 237.75px; height: 40px; text-align: center;">#PRODUCT_NAME</td>
    <td style="width: 123.391px; height: 40px; text-align: center;">#QUANTITY</td>
    <td style="width: 106.375px; height: 40px; text-align: center;">#PRICE</td>
    </tr>"""

    for p in order.products:
        price = p.get('discounted_price') if p.get('discounted_price', None) else p.get('price')
        product_rows += product_row.replace('#IMG_URL', p.get('images')).replace('#PRODUCT_NAME', p.get('name')) \
            .replace('#QUANTITY', str(p.get('quantity'))).replace('#PRICE', str(price))

    data = {
        'Messages': [{
            "From": {"Email": f"{APP_EMAIL}", "Name": "ShoBig"},
            "To": [{"Email": f"{user.email}", "Name": f"{user.display_name}"}],
            "Subject": f"Your Order ShoBig {order.order_id} - Thank you for rating the products you have just purchased",
            "TextPart": "Greetings from ShoBig!",
            "HTMLPart": f"""
                            <h2 style="color: #2e6c80;">&nbsp;</h2>
    <p>Dear {user.display_name},&nbsp;</p>
    <p><br />Thank you for purchasing from <strong>ShoBig</strong>.</p>
    <p>Your opinion is precious to us. Help us improve our services and give all <strong>ShoBig</strong> customers a better understanding of the product (s) you have ordered!</p>
    <p>Please note that :</p>
    <ul>
    <li>You can rate products from ★ (very bad) to ★★★★★ (very good).</li>
    </ul>
    <ul>
    <li>If you are not happy with your purchase, you can always return it to us. At <strong>ShoBig</strong> we have an easy return and fast refund option.</li>
    </ul>
    <p>&nbsp;</p>
    <p>Your order for:</p>
    <table class="editorDemoTable" style="height: 166px; width: 647px; margin-left: auto; margin-right: auto; border-style: solid; border-color: black;" border="1">
    <thead>
    <tr style="height: 18px;">
    <td style="width: 151.484px; height: 18px; text-align: center;">IMAGE</td>
    <td style="width: 237.75px; height: 18px; text-align: center;">PRODUCT</td>
    <td style="width: 123.391px; height: 18px; text-align: center;">QUANTITY</td>
    <td style="width: 106.375px; height: 18px; text-align: center;">PRICE</td>
    </tr>
    </thead>
    <tbody>
    {product_rows}
    </tbody>
    </table>
    <p><strong>&nbsp;</strong></p>
    <p>Good day,&nbsp;</p>
    <p><strong><em>SHOBIG Team</em></strong></p>
    <p><strong>&nbsp;</strong></p>
"""
        }]
    }
    result = mailjet.send.create(data=data)
    print("mailjet log")
    print(result.status_code)
    print(result.json())
