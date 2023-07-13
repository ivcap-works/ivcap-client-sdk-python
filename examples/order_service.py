import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../src'))
from ivcap_client import IVCAP

# from ivcap_client import AuthenticatedClient
# from ivcap_client.api.order import order_create, order_read
# from ivcap_client.models import OrderRequestT, ParameterT, OrderRequestT, OrderStatusRT
import pprint
pp = pprint.PrettyPrinter(indent=2)

img_url = 'https://wallpaperaccess.com/full/4482737.png'
service_id = 'urn:ivcap:service:266cf1ad-0949-5c40-b6a7-a0ebcdb5b8b5'

ivcap = IVCAP()
service = ivcap.get_service(service_id)
order = service.place_order(msg='Hello World', background_img=img_url)
pp.pprint(order)

