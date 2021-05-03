from environs import Env
import logging
from flask import Blueprint, request, jsonify
import json
import psycopg2
import requests

from members import common
from members.member import Member
from members.keycloak import Keycloak

logging.basicConfig()
log = logging.getLogger()
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(level=logging.NOTSET)

env = Env()
env.read_env()

keycloak = Keycloak(env.str("ADMIN_CLIENT_SECRET"), env.str("MEMBER_CLIENT_SECRET"))

try:
    log.info(f"Connecting to {env.str('DB_NAME')} database from members.authentication module")
    conn = psycopg2.connect(host=env.str("DB_HOST"),
                            port=env.str("DB_PORT"),
                            database=env.str("DB_NAME"),
                            user=env.str("DB_USER"),
                            password=env.str("DB_PASSWORD"))
    log.info(f"Connected to {env.str('DB_NAME')} database")
except Exception as e:
    log.critical(e)

members = Blueprint("members", __name__)

@members.route("/members/register/", methods=["POST"])
def members_register():
    try:
        member = Member(request.data)
        if not common.member_exists(member.username, member.email):
            try:                
                # Send request to Keycloak to insert/register member
                if insert_member_keycloak(member):
                    # Insert member into members table in postgres
                    insert_member(member)
                    return jsonify({"success": True, "message": f"Member {member.username} successfully registered"}), 200, {"ContentType":"application/json"}
                else:
                    return jsonify({"success": False, "message": f"There is a problem with registering member within keycloak"}), 500, {"ContentType":"application/json"}
            except Exception as e:
                log.critical(e)
                return jsonify({"success": True, "message": f"Can't register member. There is an issue on the server side"}), 500, {"ContentType":"application/json"}
        return jsonify({"success": False, "message": "Username or Email already taken"}), 409, {"ContentType":"application/json"}
    except KeyError as e:
        log.critical(e)
        return jsonify({"success": False, "error": "Missing arguments"}), 400, {"ContentType":"application/json"}
    except json.decoder.JSONDecodeError as e:
        log.critical(e)
        return jsonify({"success": False, "error": "JSON is badly formatted"}), 400, {"ContentType":"application/json"}

def insert_member(member):
    """
        Inserts member into pelbox database.

        Args:
            member - of type Member
        Returns:
            None
    """

    insert_member_query = """
        INSERT INTO members (username, email, phone_token)
        VALUES (%s, %s, %s)
        RETURNING id
    """
    cur = conn.cursor()
    cur.execute(insert_member_query, (member.username, member.email, member.phone_token))
    result = cur.fetchone()
    conn.commit()
    cur.close()

    insert_member_details_query = "INSERT INTO member_details (member_id) VALUES (%s)"
    cur = conn.cursor()
    cur.execute(insert_member_details_query, (result[0],))
    conn.commit()
    cur.close()

def insert_member_keycloak(member):
    """
        Inserts/register member into keycloak of pelbox realm.

        Args:
            member - of type Member
        Returns:
            None
    """
    return keycloak.register(member)

@members.route("/members/login/", methods=["POST"])
def member_login():
    try:
        member = Member(request.data)
        response = keycloak.member_login(member)
        
        if response["success"]:
            response["is_in_organization"] = common.is_member_in_organization(member.username)[0] == True
            return jsonify(response), 200, {"ContentType":"application/json"}
        else:
            return jsonify(response), 401, {"ContentType":"application/json"}
    except KeyError as e:
        log.critical(e)
        return jsonify({"success": False, "error": "Missing arguments"}), 400, {"ContentType":"application/json"}
    except json.decoder.JSONDecodeError as e:
        log.critical(e)
        return jsonify({"success": False, "error": "JSON is badly formatted"}), 400, {"ContentType":"application/json"}

@members.route("/members/logout/", methods=["POST"])
def member_logout():
    url = "http://localhost:8080/auth/realms/pelbox/protocol/openid-connect/logout"

    try:
        data_json = json.loads(request.data.decode("utf-8"))
        payload = f"Authorization=Bearer%20{data_json['access_token']}&client_id=pelbox-users&refresh_token={data_json['refresh_token']}&client_secret={env.str('MEMBER_CLIENT_SECRET')}"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 204:
            return jsonify({"success": True, "message": f"Member successfully logged out"}), 200, {"ContentType":"application/json"}
        else:
            return jsonify({"success": False, "message": f"There is a problem with logging member out within keycloak"}), 500, {"ContentType":"application/json"}
    except KeyError as e:
        log.critical(e)
        return jsonify({"success": False, "error": "Missing arguments"}), 400, {"ContentType":"application/json"}
    except json.decoder.JSONDecodeError as e:
        log.critical(e)
        return jsonify({"success": False, "error": "JSON is badly formatted"}), 400, {"ContentType":"application/json"}
