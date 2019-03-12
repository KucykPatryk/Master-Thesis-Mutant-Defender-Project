import os
import signal
import socket
import subprocess
from tempfile import TemporaryDirectory


class VWWrapper:
    def __init__(self, arguments, executable):
        self.arguments = arguments
        self.executable = executable
        self.pid = None
        self.port = None
        self.start()

    def start(self):
        with TemporaryDirectory() as tmpdir:
            pid_file = os.path.join(tmpdir, 'pid.txt')
            port_file = os.path.join(tmpdir, 'port.txt')
            cmd = [self.executable, '--daemon', '--port', '0', '--pid_file', pid_file, '--port_file', port_file]
            cmd += self.arguments.split(' ')
            result = subprocess.run(cmd)
            print(result)
            self.pid = int(open(pid_file, 'r').readline())
            self.port = int(open(port_file, 'r').readline())

    def stop(self):
        os.kill(self.pid, signal.SIGINT)

    def predict(self, query):
        if not query.endswith('\r\n\r\n'):
            query += '\r\n\r\n'
        answer = netcat('localhost', self.port, query)
        return [float(x[1]) for x in sorted([ans.split(':') for ans in answer.split(',')])]

    def learn(self, query):
        if not query.endswith('\r\n\r\n'):
            query += '\r\n\r\n'

        netcat('localhost', self.port, query)


def netcat(hostname, port, content):
    data = ""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((hostname, port))
        s.sendall(content.encode())
        s.shutdown(socket.SHUT_WR)
        while True:
            chunk = s.recv(1024)

            if not chunk:
                break
            else:
                data += chunk.decode()
            #print("Received:", repr(data))
        #print("Connection closed.")

    return data.strip()


if __name__ == '__main__':
    vw = VWWrapper('--cb_explore_adf --cb_type dr --epsilon 0.2', '/home/kucyk-p/UiO/Master_Thesis/vowpal_wabbit/build/vowpalwabbit/vw')
    print("Port", vw.port)
    print("Predict")
    pred = vw.predict("| q:1.2 w:1.5 e:1.3\r\n| a:1.3 s:1.4 d:1.1\r\n\r\n")

    print(pred)
    print("Learn")
    vw.learn("0:0.5:0.1 | q:1.2 w:1.5 e:1.3")
    vw.learn("0:0.4:0.5 | a:1.3 s:1.4 d:1.1")

    print("Predict")
    pred = vw.predict("| q:1.2 w:1.5 e:1.3\r\n| a:1.3 s:1.4 d:1.1\r\n\r\n")

    print(pred)
    # print("Learn")
    # vw.learn("0:0.1:0.1 | q w e")
    # vw.learn("0:0.6:0.5 | a s d")
    #
    # print("Predict")
    # pred = vw.predict("0:0.01:0.1 | q w e\r\n0:0.6:0.5 | a s d\r\n\r\n")
    # print(pred)

    vw.stop()
