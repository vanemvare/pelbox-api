from flask import Blueprint, jsonify, request
from environs import Env
import logging
import psycopg2
import json
import jwt
from decimal import Decimal
import simplejson as sjson

from members import common
from members.keycloak import Keycloak
from members.member import Member

logging.basicConfig()
log = logging.getLogger()
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(level=logging.NOTSET)

orders = Blueprint("orders", __name__)

env = Env()
env.read_env()

keycloak = Keycloak(env.str("ADMIN_CLIENT_SECRET"), env.str("MEMBER_CLIENT_SECRET"))

try:
    log.info(f"Connecting to {env.str('DB_NAME')} database from members.orders module")
    conn = psycopg2.connect(host=env.str("DB_HOST"),
                            port=env.str("DB_PORT"),
                            database=env.str("DB_NAME"),
                            user=env.str("DB_USER"),
                            password=env.str("DB_PASSWORD"))
    log.info(f"Connected to {env.str('DB_NAME')} database")
except Exception as e:
    log.critical(e)

@orders.route("/members/orders/details/", methods=["GET"])
def get_member_all_order_details():
    try:
        data_json = dict(request.headers)
        data_json = {key: None if data_json[key] == "" else data_json[key] for key in data_json}

        logged_in, status_code = keycloak.is_member_logged(data_json["Access-Token"])
        if status_code == 200 and logged_in:
            username = jwt.decode(data_json["Access-Token"], verify=False)["preferred_username"]
            total_count, total_price = common.get_member_orders_details_all(username)

            if total_price == None:
                total_price = 0

            return jsonify({"success": True, "message": {"total_count": total_count, "total_price": sjson.dumps(Decimal(total_price), use_decimal=True)}}), 200, {"ContentType":"application/json"}
        elif status_code == 200 and not logged_in:
            return jsonify({"success": False, "message": f"Member is not logged in"}), 401, {"ContentType":"application/json"}
        else:
            return jsonify({"success": False, "message": f"Something went wrong"}), 500, {"ContentType":"application/json"}
    except KeyError as e:
        log.critical(e)
        return jsonify({"success": False, "error": "Missing arguments"}), 400, {"ContentType":"application/json"}
    except json.decoder.JSONDecodeError as e:
        log.critical(e)
        return jsonify({"success": False, "error": "JSON is badly formatted"}), 400, {"ContentType":"application/json"}

@orders.route("/members/orders/all/", methods=["GET"])
def get_all_member_orders():
    try:
        data_json = dict(request.headers)
        data_json = {key: None if data_json[key] == "" else data_json[key] for key in data_json}

        logged_in, status_code = keycloak.is_member_logged(data_json["Access-Token"])
        if status_code == 200 and logged_in:
            username = jwt.decode(data_json["Access-Token"], verify=False)["preferred_username"]
            orders = common.get_all_member_orders(username)
            return jsonify({"success": True, "message": orders}), 200, {"ContentType":"application/json"}
        elif status_code == 200 and not logged_in:
            return jsonify({"success": False, "message": f"Member is not logged in"}), 401, {"ContentType":"application/json"}
        else:
            return jsonify({"success": False, "message": f"Something went wrong"}), 500, {"ContentType":"application/json"}
    except KeyError as e:
        log.critical(e)
        return jsonify({"success": False, "error": "Missing arguments"}), 400, {"ContentType":"application/json"}
    except json.decoder.JSONDecodeError as e:
        log.critical(e)
        return jsonify({"success": False, "error": "JSON is badly formatted"}), 400, {"ContentType":"application/json"}

@orders.route("/members/orders/notifications/", methods=["GET"])
def get_member_notifications():
    try:
        data_json = dict(request.headers)
        data_json = {key: None if data_json[key] == "" else data_json[key] for key in data_json}

        logged_in, status_code = keycloak.is_member_logged(data_json["Access-Token"])
        if status_code == 200 and logged_in:
            username = jwt.decode(data_json["Access-Token"], verify=False)["preferred_username"]
            notifications = common.get_unread_notifications(username)
            return jsonify({"success": True, "message": notifications}), 200, {"ContentType":"application/json"}
        elif status_code == 200 and not logged_in:
            return jsonify({"success": False, "message": f"Member is not logged in"}), 401, {"ContentType":"application/json"}
        else:
            return jsonify({"success": False, "message": f"Something went wrong"}), 500, {"ContentType":"application/json"}
    except KeyError as e:
        log.critical(e)
        return jsonify({"success": False, "error": "Missing arguments"}), 400, {"ContentType":"application/json"}
    except json.decoder.JSONDecodeError as e:
        log.critical(e)
        return jsonify({"success": False, "error": "JSON is badly formatted"}), 400, {"ContentType":"application/json"}

@orders.route("/members/orders/notifications/", methods=["PUT"])
def read_member_notifications():
    try:
        data_json = json.loads(request.data.decode("utf-8"))
        data_json = {key: None if data_json[key] == "" else data_json[key] for key in data_json}
        
        logged_in, status_code = keycloak.is_member_logged(data_json["access_token"])
        if status_code == 200 and logged_in:
            common.update_read_notification(data_json["id"])
            return jsonify({"success": True, "message": "Notification is updated"}), 200, {"ContentType":"application/json"}
        elif status_code == 200 and not logged_in:
            return jsonify({"success": False, "message": f"Member is not logged in"}), 401, {"ContentType":"application/json"}
        else:
            return jsonify({"success": False, "message": f"Something went wrong"}), 500, {"ContentType":"application/json"}
    except KeyError as e:
        log.critical(e)
        return jsonify({"success": False, "error": "Missing arguments"}), 400, {"ContentType":"application/json"}
    except json.decoder.JSONDecodeError as e:
        log.critical(e)
        return jsonify({"success": False, "error": "JSON is badly formatted"}), 400, {"ContentType":"application/json"}