from _common import ivcap, pp

img_url = 'https://wallpaperaccess.com/full/4482737.png'
service_id = 'urn:ivcap:service:266cf1ad-0949-5c40-b6a7-a0ebcdb5b8b5'

service = ivcap.get_service_by_name("hello-world-python")
order = service.place_order(msg='Hello World', background_img=img_url)
pp.pprint(order)
