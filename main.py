from flask import Flask
from members.authentication import members
from members.profile import profile
from members.orders import orders
from members.organization import organization
from members.pelbox import pelbox

app = Flask(__name__)
app.register_blueprint(members)
app.register_blueprint(profile)
app.register_blueprint(orders)
app.register_blueprint(organization)
app.register_blueprint(pelbox)

def main():
    app.run(host='0.0.0.0', port=9000)

if __name__ == "__main__":
    main()