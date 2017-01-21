import random
from calendar import monthrange
from datetime import datetime
from optparse import OptionParser
from loremipsum import get_sentence
from psycopg2 import IntegrityError
from sqlalchemy import create_engine, insert, select, exc
from settings import settings
from data_access.auth import users, ad_placers, ad_providers
from data_access.advert_orders import advert_orders
from data_access.placements import placements
from data_access.analytics import clicks, views


random.seed()
engine = create_engine('postgresql+psycopg2://{user}:{password}@{host}/{database}'.format(
    user=settings.DB_USER, password=settings.DB_PASS, host=settings.DB_HOST, database=settings.DB_NAME
))


def get_provider_id(email):
    tables = ad_providers.join(users, ad_providers.c.user_id == users.c.id)
    return select([ad_providers.c.id]).select_from(tables).where(users.c.email == email)


def get_random_date():
    year = random.randint(2013, 2016)
    month = random.randint(1, 12)
    day = random.randint(1, monthrange(year, month)[1])
    hour = random.randint(0, 23)
    return datetime(year=year, month=month, day=day, hour=hour)


def get_placer_id(email):
    tables = ad_placers.join(users, ad_placers.c.user_id == users.c.id)
    return select([ad_placers.c.id]).select_from(tables).where(users.c.email == email)


def generate_advert_orders(provider_id):
    num_of_orders = random.randint(10, 20)
    orders = []
    for i in range(num_of_orders):
        heading_pic_host, url_link_host = str(get_sentence()).split(' ')[:2]
        rank = random.randint(1, 3)
        description = str(get_sentence(random.randint(3, 6)))
        orders.append({
            'heading_picture': 'https://{}.com/image'.format(heading_pic_host),
            'follow_url_link': 'https://{}.com/about'.format(url_link_host),
            'rank': rank,
            'description': description,
            'owner_id': provider_id
        })
    return orders


def generate_placements(placer_id, order_ids):
    return [{
        'order_id': order_id,
        'placer_id': placer_id
    } for order_id in order_ids]


def generate_analytics(placement_ids):
    data = []
    for p_id in placement_ids:
        for i in range(1, random.randint(50, 500)):
            data.append({
                'placement_id': p_id,
                'registered_at': get_random_date()
            })
    return data


def populate_db(provider_email, placer_email):
    get_provider_query = get_provider_id(provider_email)
    get_placer_query = get_placer_id(placer_email)

    with engine.connect() as conn:
        rp = conn.execute(get_provider_query)
        result = rp.first()
        if result is None:
            raise Exception('Ad provider with email {} does not exist'.format(provider_email))
        provider_id = result.id

        rp = conn.execute(get_placer_query)
        result = rp.first()
        if result is None:
            raise Exception('Ad placer with email {} does not exist'.format(placer_email))
        placer_id = result.id

        ad_orders_data = generate_advert_orders(provider_id)
        for order_data in ad_orders_data:
            try:
                conn.execute(insert(advert_orders).values(**order_data))
            except (IntegrityError, exc.IntegrityError):
                pass
        rp = conn.execute(select([advert_orders.c.id]))
        ad_order_ids = [item.id for item in rp]

        placements_data = generate_placements(placer_id, ad_order_ids)
        for placement_data in placements_data:
            try:
                conn.execute(insert(placements).values(**placement_data))
            except (IntegrityError, exc.IntegrityError):
                pass
        rp = conn.execute(select([placements.c.id]))
        placement_ids = [item.id for item in rp]

        analytics_data = generate_analytics(placement_ids)
        for data in analytics_data:
            try:
                conn.execute(insert(clicks).values(**data))
            except (IntegrityError, exc.IntegrityError):
                pass

        analytics_data = generate_analytics(placement_ids)
        for data in analytics_data:
            try:
                conn.execute(insert(views).values(**data))
            except (IntegrityError, exc.IntegrityError):
                pass

        conn.execute(insert(views), analytics_data)


def main():
    parser = OptionParser()
    parser.add_option('-r', '--provider', dest='provider_email', help='Advert provider email')
    parser.add_option('-l', '--placer', dest='placer_email', help='Ad placer email')
    (options, args) = parser.parse_args()
    populate_db(provider_email=options.provider_email, placer_email=options.placer_email)


if __name__ == '__main__':
    main()
