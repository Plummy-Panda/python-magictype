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
        if '=====Magic Type Menu=====' in data and playing:
            print "[*] Play a game!"
            sock.sendall('1\r\n')
        if 'Choose the speed level' in data and playing:
            print "[*] Choose speed level at " + str(config.LEVEL) + '!'
            sock.sendall(str(config.LEVEL) + '\r\n')
        if 'Game over' in data:
            print '[*] Game over!'
            is_game_over = True
        if '|' in data and playing:
            score = get_score(data)
            word = get_word(data)
            if score is not None:
                if score >= config.STOP_THRESHOLD_SCORE:
                    playing = False
                else:
                    if lastScore != score:
                        print 'Score:', score
                    lastScore = score

            if word is not None:
                print 'Found word: ', word
                sock.sendall(word + '\r\n')
        if is_game_over:
            data = sock.recv(1024)
            print data
            break

    print 'Close the socket!'
    sock.close()

if __name__ == '__main__':
    main()
