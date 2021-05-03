from flask import Blueprint, jsonify, request
from environs import Env
import logging
import psycopg2
import json
import jwt

from members import common
from members.keycloak import Keycloak
from members.member import Member

logging.basicConfig()
log = logging.getLogger()
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(level=logging.NOTSET)

profile = Blueprint("profile", __name__)

env = Env()
env.read_env()

keycloak = Keycloak(env.str("ADMIN_CLIENT_SECRET"), env.str("MEMBER_CLIENT_SECRET"))

try:
    log.info(f"Connecting to {env.str('DB_NAME')} database from members.profile module")
    conn = psycopg2.connect(host=env.str("DB_HOST"),
                            port=env.str("DB_PORT"),
                            database=env.str("DB_NAME"),
                            user=env.str("DB_USER"),
                            password=env.str("DB_PASSWORD"))
    log.info(f"Connected to {env.str('DB_NAME')} database")
except Exception as e:
    log.critical(e)

@profile.route("/members/profile/<id>/", methods=["PUT"])
def member_details_update(id):
    try:
        data_json = json.loads(request.data.decode("utf-8"))

        data_json = {key: None if data_json[key] == "" else data_json[key] for key in data_json}
        data_json["postal_code"] = int(data_json["postal_code"]) if data_json["postal_code"] else None
        
        logged_in, status_code = keycloak.is_member_logged(data_json["access_token"])
        if status_code == 200 and logged_in:
            username = jwt.decode(data_json["access_token"], verify=False)["preferred_username"]
            member_details = common.get_member_details(username)
            member = Member.new(*member_details)
            if member_details_changed(member, data_json):
                update_member_details(member, data_json)
                return jsonify({"success": True, "message": f"Member profile successfully updated"}), 200, {"ContentType":"application/json"}
            else:
                return jsonify({"success": False, "message": f"Member profile is not updated. Data is same"}), 200, {"ContentType":"application/json"}
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

def member_details_changed(member, new_member_details):
    return  member.username != new_member_details["username"] or \
            member.email != new_member_details["email"] or \
            member.first_name != new_member_details["first_name"] or \
            member.last_name != new_member_details["last_name"] or \
            member.gender != new_member_details["gender"] or \
            member.country != new_member_details["country"] or \
            member.city != new_member_details["city"] or \
            member.city_address != new_member_details["city_address"] or \
            member.postal_code != new_member_details["postal_code"] or \
            member.phone_number != new_member_details["phone_number"]

def update_member_details(member, new_member_details):
    try:
        member_details_query = """
            WITH member_information (id)
            AS 
            (
                SELECT id FROM members WHERE username = %s
            )
            UPDATE member_details md
                SET first_name = %s, last_name = %s, gender = %s, country = %s, city = %s, city_address = %s, postal_code = %s, phone_number = %s
            FROM member_information
            WHERE md.member_id = member_information.id
        """
        cur = conn.cursor()
        cur.execute(member_details_query, (new_member_details["username"], new_member_details["first_name"], new_member_details["last_name"], new_member_details["gender"], \
                                            new_member_details["country"], new_member_details["city"], new_member_details["city_address"], \
                                            new_member_details["postal_code"], new_member_details["phone_number"]))
        conn.commit()
        cur.close()
    except Exception as e:
        log.critical(e)

@profile.route("/members/profile/", methods=["GET"])
def get_member_details():
    try:
        data_json = dict(request.headers)
        data_json = {key: None if data_json[key] == "" else data_json[key] for key in data_json}

        logged_in, status_code = keycloak.is_member_logged(data_json["Access-Token"])
        if status_code == 200 and logged_in:
            username = jwt.decode(data_json["Access-Token"], verify=False)["preferred_username"]
            member_details = common.get_member_details(username)
            print(member_details)
            member = Member.new(*member_details)
            return jsonify({"success": True, "message": member.json_data()}), 200, {"ContentType":"application/json"}
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

@profile.route("/members/profile/first_name", methods=["PUT"])
def update_member_first_name():
    try:
        data_json = json.loads(request.data.decode("utf-8"))
        data_json = {key: None if data_json[key] == "" else data_json[key] for key in data_json}
        
        logged_in, status_code = keycloak.is_member_logged(data_json["access_token"])
        if status_code == 200 and logged_in:
            username = jwt.decode(data_json["access_token"], verify=False)["preferred_username"]
            common.update_first_name(data_json["first_name"], username)
            return jsonify({"success": True, "message": "First name is updated"}), 200, {"ContentType":"application/json"}
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

@profile.route("/members/profile/last_name", methods=["PUT"])
def update_member_last_name():
    try:
        data_json = json.loads(request.data.decode("utf-8"))
        data_json = {key: None if data_json[key] == "" else data_json[key] for key in data_json}
        
        logged_in, status_code = keycloak.is_member_logged(data_json["access_token"])
        if status_code == 200 and logged_in:
            username = jwt.decode(data_json["access_token"], verify=False)["preferred_username"]
            common.update_last_name(data_json["last_name"], username)
            return jsonify({"success": True, "message": "Last name is updated"}), 200, {"ContentType":"application/json"}
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

@profile.route("/members/profile/city", methods=["PUT"])
def update_member_city():
    try:
        data_json = json.loads(request.data.decode("utf-8"))
        data_json = {key: None if data_json[key] == "" else data_json[key] for key in data_json}
        
        logged_in, status_code = keycloak.is_member_logged(data_json["access_token"])
        if status_code == 200 and logged_in:
            username = jwt.decode(data_json["access_token"], verify=False)["preferred_username"]
            common.update_city(data_json["city"], username)
            return jsonify({"success": True, "message": "City is updated"}), 200, {"ContentType":"application/json"}
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

@profile.route("/members/profile/city_address", methods=["PUT"])
def update_member_city_address():
    try:
        data_json = json.loads(request.data.decode("utf-8"))
        data_json = {key: None if data_json[key] == "" else data_json[key] for key in data_json}
        
        logged_in, status_code = keycloak.is_member_logged(data_json["access_token"])
        if status_code == 200 and logged_in:
            username = jwt.decode(data_json["access_token"], verify=False)["preferred_username"]
            common.update_city_address(data_json["city_address"], username)
            return jsonify({"success": True, "message": "Address is updated"}), 200, {"ContentType":"application/json"}
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

@profile.route("/members/profile/postal_code", methods=["PUT"])
def update_member_postal_code():
    try:
        data_json = json.loads(request.data.decode("utf-8"))
        data_json = {key: None if data_json[key] == "" else data_json[key] for key in data_json}
        
        logged_in, status_code = keycloak.is_member_logged(data_json["access_token"])
        if status_code == 200 and logged_in:
            username = jwt.decode(data_json["access_token"], verify=False)["preferred_username"]
            common.update_postal_code(data_json["postal_code"], username)
            return jsonify({"success": True, "message": "Postal code is updated"}), 200, {"ContentType":"application/json"}
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

@profile.route("/members/profile/get_countries", methods=["GET"])
def get_countries():
    try:
        data_json = dict(request.headers)
        data_json = {key: None if data_json[key] == "" else data_json[key] for key in data_json}

        logged_in, status_code = keycloak.is_member_logged(data_json["Access-Token"])
        if status_code == 200 and logged_in:
            countries = common.get_countries()
            return jsonify({"success": True, "message": countries}), 200, {"ContentType":"application/json"}
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

@profile.route("/members/profile/country_name", methods=["PUT"])
def update_member_country_name():
    try:
        data_json = json.loads(request.data.decode("utf-8"))
        data_json = {key: None if data_json[key] == "" else data_json[key] for key in data_json}
        
        logged_in, status_code = keycloak.is_member_logged(data_json["access_token"])
        if status_code == 200 and logged_in:
            username = jwt.decode(data_json["access_token"], verify=False)["preferred_username"]
            common.update_member_country_name(data_json["country_name"], username)
            return jsonify({"success": True, "message": "Country is updated"}), 200, {"ContentType":"application/json"}
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

@profile.route("/members/profile/country_code", methods=["GET"])
def get_country_code():
    try:
        data_json = dict(request.headers)
        data_json = {key: None if data_json[key] == "" else data_json[key] for key in data_json}

        logged_in, status_code = keycloak.is_member_logged(data_json["Access-Token"])
        if status_code == 200 and logged_in:
            country_code = common.get_country_code_by_country_name(data_json["Country-Name"])
            return jsonify({"success": True, "message": country_code[0]}), 200, {"ContentType":"application/json"}
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

@profile.route("/members/profile/gender", methods=["PUT"])
def update_member_gender():
    try:
        data_json = json.loads(request.data.decode("utf-8"))
        data_json = {key: None if data_json[key] == "" else data_json[key] for key in data_json}
        
        logged_in, status_code = keycloak.is_member_logged(data_json["access_token"])
        if status_code == 200 and logged_in:
            username = jwt.decode(data_json["access_token"], verify=False)["preferred_username"]
            common.update_member_gender("M" if data_json["gender"] == "Male" else "F", username)
            return jsonify({"success": True, "message": "Gender is updated"}), 200, {"ContentType":"application/json"}
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