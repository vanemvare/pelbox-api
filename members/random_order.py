import psycopg2
from environs import Env
import logging
import random
import json
import datetime
from pyfcm import FCMNotification

logging.basicConfig()
log = logging.getLogger()
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(level=logging.NOTSET)

env = Env()
env.read_env()

push_service = FCMNotification(api_key="AAAA9AKlqFM:APA91bE8HOlYptJAI_P1_tQD1fVGpZe0ZrwjZjKL8O_ORfQIfrX6YFccP7AfVQNctp8TPoHGPZ960WgsxgbqqHGqTjOUg77lmc66FuQjFQxjghSNoIIMlDT1eAr9I5EF9YiLIjWxM0j8")

def get_connection():
    try:
        conn = psycopg2.connect(host=env.str("DB_HOST"),
                                port=env.str("DB_PORT"),
                                database=env.str("DB_NAME"),
                                user=env.str("DB_USER"),
                                password=env.str("DB_PASSWORD"))
        log.info(f"Connected to {env.str('DB_NAME')} database")
        return conn
    except Exception as e:
        log.critical(e)

def menu():
    print("1. Place a random order")
    print("3. Exit")

def menu_option_valid(option):
    return option >= 1 and option <= 1

def get_categories(conn):
    try:
        query = "SELECT id, category_name FROM order_category"

        cur = conn.cursor()
        cur.execute(query)

        rows = cur.fetchall()
        orders = []
        cur.close()

        for row in rows:
            orders.append((row[0], row[1]))

        return orders
    except Exception as e:
        log.critical(e)

def get_random_member_id(conn):
    try:
        query = """
            SELECT id FROM members
            ORDER BY RANDOM()
            LIMIT 1
        """

        cur = conn.cursor()
        cur.execute(query)
        
        row = cur.fetchone()
        cur.close()

        return row[0]
    except Exception as e:
        log.critical(e)

def get_random_organization_id(conn):
    try:
        query = """
            SELECT id FROM organizations
            ORDER BY RANDOM()
            LIMIT 1
        """

        cur = conn.cursor()
        cur.execute(query)
        
        row = cur.fetchone()
        cur.close()

        return row[0]
    except Exception as e:
        log.critical(e)

def get_phone_token_from_member_id(conn, id):
    try:
        query = """
            SELECT phone_token FROM members
            WHERE id = %s
        """

        cur = conn.cursor()
        cur.execute(query, (id,))
        
        row = cur.fetchone()
        cur.close()

        return row[0]
    except Exception as e:
        log.critical(e)

def get_random_product_by_category(products, random_category):
    random_products = list(filter(lambda product: product["order_category"] == random_category, products))
    return random_products[random.randint(0, len(random_products) - 1)]

def get_products():
    with open("random_orders.json", encoding="utf8") as file:
        return json.load(file)

def place_random_order(random_category, random_product, random_member_id, conn):
    log.info(f"Placing random order for member with id {random_member_id} with category {random_category} with the product details below") 
    log.info(random_product)

    try:
        query = """
            INSERT INTO orders (member_id, asin, order_category, price, product_title, product_short_description, product_url, product_image, product_order_status, ordered_on) VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """

        status = ["In a box", "Canceled", "Shipping", "Delivered"]

        cur = conn.cursor()
        cur.execute(query, (random_member_id, random_product["asin"], random_category[0], random_product["price"], random_product["product_title"], random_product["product_short_description"], random_product["product_url"], random_product["product_image"], random.randint(0, len(status) - 1) + 1, datetime.date.today()))
        order_id = cur.fetchone()[0]
        conn.commit()
        cur.close()

        query = """
            INSERT INTO notifications (member_id, notification_title, notification_text, notification_image_url)
            VALUES (%s, %s, %s, %s)
        """
        cur = conn.cursor()
        cur.execute(query, (random_member_id, 'You have a new order', random_product["product_title"], random_product["product_image"]))
        conn.commit()

        query = """
            INSERT INTO organization_deliveries (organization_id, order_id)
            VALUES(%s, %s)
        """
        cur = conn.cursor()
        cur.execute(query, (get_random_organization_id(conn), order_id))
        conn.commit()

        result = push_service.notify_single_device(registration_id=get_phone_token_from_member_id(conn, random_member_id), message_title='You have a new order', message_body=random_product["product_title"])
        print(result)

        cur.close()
    except Exception as e:
        log.critical(e)

def main():
    conn = get_connection()
    
    categories = get_categories(conn)
    products = get_products()

    while True:
        menu()

        try:
            user_option = int(input((" : ")))
            if user_option == 3:
                break
            if menu_option_valid(user_option):
                random_category = categories[random.randint(0, len(categories) - 1)]
                random_member_id = get_random_member_id(conn)
                random_product = get_random_product_by_category(products, random_category[1])
                
                place_random_order(random_category, random_product, random_member_id, conn)
            else:
                print("\nERROR: Enter a valid menu option number (1-2)\n")
        except ValueError:
            print("\nERROR: Please enter a number\n")

    conn.close()

if __name__ == "__main__":
    main()