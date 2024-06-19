from kazoo.client import KazooClient
from kazoo.exceptions import NodeExistsError, KazooException, SessionExpiredError

class TupleSpace:
    def __init__(self, zk_hosts, tuple_path):
        self.zk_hosts = zk_hosts
        self.tuple_path = tuple_path
        self.zk = KazooClient(hosts=zk_hosts)
        self.connected = False

    def connect(self):
        try:
            self.zk.start()
            self.connected = True
            print(f"Connected to ZooKeeper at {self.zk_hosts}")

        except KazooException as e:
            print(f"Failed to connect to ZooKeeper at {self.zk_hosts}: {e}")
            self.connected = False

    def disconnect(self):
        try:
            if self.connected:
                self.zk.stop()
                self.connected = False
                print("Disconnected from ZooKeeper")

        except KazooException as e:
            print(f"Error disconnecting from ZooKeeper: {e}")

    def ensure_path(self):
        try:
            if not self.zk.exists(self.tuple_path):
                self.zk.ensure_path(self.tuple_path)
                print(f"Created path {self.tuple_path}")
            else:
                print(f"Path {self.tuple_path} already exists")

        except KazooException as e:
            print(f"Error creating path {self.tuple_path}: {e}")

    def list_tuples(self):
        try:
            self.connect()  # Ensure connection before listing tuples

            if self.connected and self.zk.exists(self.tuple_path):
                children = self.zk.get_children(self.tuple_path)

                if children:
                    print(f"Tuples under path {self.tuple_path}:")
                    for child in children:
                        tuple_full_path = f"{self.tuple_path}/{child}"
                        data, _ = self.zk.get(tuple_full_path)
                        tuple_data = data.decode('utf-8')
                        print(f"- {tuple_data}")
                else:
                    print(f"No tuples found under path {self.tuple_path}")

            elif not self.connected:
                print("Cannot list tuples: Not connected to ZooKeeper")

            else:
                print(f"Path {self.tuple_path} does not exist")

        except SessionExpiredError:
            print("Session with ZooKeeper expired. Reconnecting...")
            self.connect()

        except KazooException as e:
            print(f"Error listing tuples: {e}")

        finally:
            self.disconnect()  # Always disconnect after operations

    def check_tuple_exists(self, tuple_data):
        try:
            children = self.zk.get_children(self.tuple_path)
            if children:
                for child in children:
                    tuple_full_path = f"{self.tuple_path}/{child}"
                    data, _ = self.zk.get(tuple_full_path)
                    if data.decode('utf-8') == tuple_data:
                        return True
            return False

        except KazooException as e:
            print(f"Error checking tuple existence: {e}")
            return False

    def write_tuple(self, tuple_data):
        try:
            self.connect()
            self.ensure_path()

            if not self.check_tuple_exists(tuple_data): 
                created_path = self.zk.create(self.tuple_path, tuple_data.encode('utf-8'), sequence=True, ephemeral=False)
                print(f"Written tuple at {created_path}: {tuple_data}")
            else:
                print(f"Tuple already exists: {tuple_data}")

        except NodeExistsError:
            print(f"Error: Tuple already exists at path {self.tuple_path}")

        except KazooException as e:
            print(f"Error writing tuple: {e}")

        finally:
            self.disconnect()

# Example usage:
if __name__ == "__main__":
    zk_hosts = 'localhost:2181'  # Replace with your ZooKeeper server(s) hosts
    tuple_path = '/tuple_space/'  # Replace with the path where your tuples are stored in ZooKeeper

    tuple_space = TupleSpace(zk_hosts, tuple_path)

    # Write a new tuple
    tuple_data = "INE5418,Fodano,9,60"
    tuple_space.write_tuple(tuple_data)

    # List existing tuples
    tuple_space.list_tuples()
