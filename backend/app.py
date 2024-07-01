from flask import Flask, request, jsonify
from flask_cors import CORS
from kazoo.client import KazooClient
from kazoo.exceptions import NodeExistsError, KazooException, SessionExpiredError

app = Flask(__name__)
CORS(app)

zk_hosts = 'localhost:2181'
tuple_path = '/tuple_space/'
login_path = '/users/'
zk = KazooClient(hosts=zk_hosts)
zk.start()
zk.ensure_path(tuple_path)
zk.ensure_path(login_path)
# username = input("Digite seu usuário: ")
# password = input("Senha: ")

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if authenticate_user(username, password):
        return jsonify({"authenticated": True})
    else:
        return jsonify({"authenticated": False})

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if create_user(username, password):
        return jsonify({"created": True})
    else:
        return jsonify({"created": False})


def authenticate_user(username, password):
    user_path = f"{login_path}{username}"
    if zk.exists(user_path):
        data, _ = zk.get(user_path)
        user_data = data.decode('utf-8').split(':')
        if user_data[1] == password:
            return True
    return False

def create_user(username, password):
    user_path = f"{login_path}{username}"
    try:
        if not zk.exists(user_path):
            zk.create(user_path, f"{username}:{password}:0".encode('utf-8'))
            return True
    except KazooException as e:
        print(f"Error creating user: {e}")
    return False

def get_user_credit_at_backend(username):
    user_path = f"{login_path}{username}"
    if zk.exists(user_path):
        data, _ = zk.get(user_path)
        user_data = data.decode('utf-8').split(':')
        return int(user_data[2])
    return None  

def update_user_credit(username, credit):
    user_path = f"{login_path}{username}"
    if zk.exists(user_path):
        data, _ = zk.get(user_path)
        user_data = data.decode('utf-8').split(':')
        user_data[2] = str(credit)
        zk.set(user_path, ':'.join(user_data).encode('utf-8'))
        
@app.route('/get_user_credits', methods=['POST'])
def get_user_credits():
    data = request.json
    username = data.get('username')
    credits = get_user_credit_at_backend(username)
    if credits is not None:
        return jsonify({"credits": credits})
    else:
        return jsonify({"error": "User not found"})

@app.route('/write_tuple', methods=['POST'])
def write_tuple():
    data = request.json
    tuple_data = data.get('tuple_data')
    username = data.get('username')
    print(tuple_data)
    print(tuple_data.encode('utf-8'))
    try:
        if not check_tuple_exists(tuple_data):
            created_path = zk.create(tuple_path, value = tuple_data.encode('utf-8'), sequence=True, ephemeral=False)
            credit = get_user_credit_at_backend(username)
            print(credit)
            update_user_credit(username, credit+1)
            print(f"novo credito: {get_user_credit_at_backend(username)}")
            
            return jsonify({"message": f"Written tuple at {created_path}: {tuple_data}"})
        else:
            return jsonify({"message": f"Tuple already exists: {tuple_data}"})
    except NodeExistsError:
        return jsonify({"error": f"Error: Tuple already exists at path {tuple_path}"})
    except KazooException as e:
        return jsonify({"error": f"Error writing tuple: {e}"})

@app.route('/get_tuple', methods=['POST'])
def get_tuple():
    searched_tuple = request.json.get('searched_tuple')
    username = request.json.get('username')
    if get_user_credit_at_backend(username) <= 0:
        return jsonify({"message": "Insuficient Credits. Donate more books!"})
    found_tuple = get(searched_tuple)
    if found_tuple:
        credit = get_user_credit_at_backend(username)
        update_user_credit(username,credit-1)
        return jsonify({"tuple": found_tuple})
    else:
        return jsonify({"message": "Tuple not found"})

@app.route('/list_tuples', methods=['GET'])
def list_tuples():
    try:
        if zk.exists(tuple_path):
            children = zk.get_children(tuple_path)
            tuples = []
            for child in children:
                tuple_full_path = f"{tuple_path}/{child}"
                data, _ = zk.get(tuple_full_path)
                tuple_data = data.decode('utf-8')
                tuples.append(tuple_data)
            return jsonify({"tuples": tuples})
        else:
            return jsonify({"message": f"Path {tuple_path} does not exist"})
    except SessionExpiredError:
        return jsonify({"error": "Session with ZooKeeper expired. Reconnecting..."})
    except KazooException as e:
        return jsonify({"error": f"Error listing tuples: {e}"})

def check_tuple_exists(tuple_data):
    try:
        children = zk.get_children(tuple_path)
        for child in children:
            tuple_full_path = f"{tuple_path}/{child}"
            data, _ = zk.get(tuple_full_path)
            if data.decode('utf-8') == tuple_data:
                return True
        return False
    except KazooException as e:
        print(f"Error checking tuple existence: {e}")
        return False

def get(searched_tuple):
    found_tuple = None
    parse_search = searched_tuple.split(',')
    parse_search_size = len(parse_search)
    if zk.exists(tuple_path):
        children = zk.get_children(tuple_path)
        if children:
            for child in children:
                match_found = True
                tuple_full_path = f"{tuple_path}/{child}"
                data, _ = zk.get(tuple_full_path)
                tuple_data = data.decode('utf-8')
                parse_tuple = tuple_data.split(',')
                parse_tuple_size = len(parse_tuple)
                if parse_search_size == parse_tuple_size:
                    for i in range(len(parse_search)):
                        # if parse_search[i] != '*':
                            if parse_search[i] != parse_tuple[i]:
                                match_found = False
                                break
                    if match_found:
                        found_tuple = tuple_data
                        zk.delete(tuple_full_path)
                        return found_tuple
    return found_tuple

if __name__ == '__main__':
    app.run(debug=True)
