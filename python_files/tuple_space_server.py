import Pyro4

import redis
import threading

@Pyro4.expose
class TupleSpace:
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.tuples = []
        self.lock = threading.Lock()
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

    def write(self, tuple_data):
        with self.lock:
            tuple_id = len(self.tuples) + 1
            self.tuples.append(tuple_data)
            return tuple_id

    def read(self, tuple_pattern):
        self.acquire_lock()
        try:
            for tuple_data in self.tuples:
                if self.match_tuple(tuple_data, tuple_pattern):
                    return tuple_data
            return None
        finally:
            self.release_lock()

    def get(self, tuple_pattern):
        self.acquire_lock()
        try:
            for tuple_data in self.tuples:
                if self.match_tuple(tuple_data, tuple_pattern):
                    self.tuples.remove(tuple_data)
                    return tuple_data
            return None
        finally:
            self.release_lock()

    def acquire_lock(self):
        while True:
            if self.redis_client.set("lock", "locked", nx=True, ex=5):
                break

    def release_lock(self):
        self.redis_client.delete("lock")

    @staticmethod
    def match_tuple(stored_tuple, tuple_pattern):
        if len(stored_tuple) != len(tuple_pattern):
            return False
        for st, tp in zip(stored_tuple, tuple_pattern):
            if tp != '*' and st != tp:
                return False
        return True

# Start Pyro4 server ????
if __name__ == "__main__":
    Pyro4.Daemon.serveSimple(
        {
            TupleSpace: "example.tuple_space"
        },
        ns=True
    )
