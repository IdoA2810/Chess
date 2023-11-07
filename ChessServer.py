from __future__ import division
import ChessEngine
import ChessMain
import ChessBot
import socket
import time
import threading
import SizeOfSize
import pickle
Game_list= []
Connected_Users = []
locker = threading.Lock()
BLACK_BOT = True
WHITE_BOT = True
WIDTH = 512
HEIGHT = 512
DIMENSION = 8 #dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 60 # for animation later on
IMAGES = {}

class ClientThread(threading.Thread):

    def __init__(self, ip, port, conn, tid):
        threading.Thread.__init__(self)
        print "New thread started for "+ip+":"+str(port)
        self.ip = ip
        self.port = port
        self.conn = conn
        self.stid = str(tid)  # threading.current_thread().ident
        self.client_name = "unknown"
        self.Pnum = 0
        self.color = None
        self.game = None

    def run(self):
        global running
        running = True
        moveMade = False
        self.conn.setblocking(1)
        data = SizeOfSize.recv_by_size(self.conn)
        print "Received: " + data
        if data == "":
            running = False
        if running:
            data = SizeOfSize.recv_by_size(self.conn)
            if data == "JOIN":
                found = False
                for game in Game_list:
                    if not game.started:
                        if not game.whiteTaken:
                            self.color = "w" #white color
                        else:
                            self.color = "b"
                        game.add_player(self.conn, self.color)
                        self.game = game
                        found = True
                        break
                if not found:
                    self.color = "w"
                    self.game = ChessEngine.GameState()
                    Game_list.append(self.game)
                    self.game.add_player(self.conn, self.color)

            else:
                running = False

        while running and not self.game.started:
            pass

        SizeOfSize.send_with_size(self.conn, "COLOR|" + self.color)
        while running:
            SizeOfSize.send_with_size(self.conn, "BOARD|" + pickle.dumps(self.game.board))
            if self.game.whiteToMove:
                SizeOfSize.send_with_size(self.conn, "TURN|w")
            else:
                SizeOfSize.send_with_size(self.conn, "TURN|b")
            my_turn = False
            if self.game.started and ((self.color == "b" and not self.game.whiteToMove) or (self.color == "w" and self.game.whiteToMove)):
                validMoves = self.game.getValidMoves()
                SizeOfSize.send_with_size(self.conn, "MOVES|" + pickle.dumps(validMoves))
                my_turn = True

            self.conn.settimeout(0.05)
            try:
                data = SizeOfSize.recv_by_size(self.conn)
                if data == "" or data == "QUIT":
                    self.game.remove_player(self.color)
                    running = False
                    break

                if not self.game.checkMate and not self.game.staleMate and self.game.started and my_turn and data.split("|")[0] == "MOVE":
                    move = pickle.loads(data.split("|")[1])

                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            if move.isPawnPromotion:
                                SizeOfSize.send_with_size(self.conn, "PROMOTION")
                                self.conn.setblocking(1)
                                data = SizeOfSize.recv_by_size(self.conn)
                                self.game.make_move(validMoves[i])
                                if data == "Q" or data == "B" or data == "N" or data == "R":
                                    self.game.board[move.endRow][move.endCol] = move.pieceMoved[0] + data
                                else:
                                    running = False
                                    break
                            else:
                                self.game.make_move(validMoves[i])
                            moveMade = True
                    if moveMade:
                        for sock in self.game.sockets.values():
                            SizeOfSize.send_with_size(sock, "MOVE|" + pickle.dumps(move))
                        moveMade = False

            except socket.timeout:
                pass




            if self.game.checkMate:
                running = False
                if self.game.whiteToMove:
                    SizeOfSize.send_with_size(self.conn, "CHECKMATE|BLACK")
                else:
                    SizeOfSize.send_with_size(self.conn, "CHECKMATE|WHITE")
            elif self.game.staleMate:
                running = False
                SizeOfSize.send_with_size(self.conn, "STALEMATE")
        self.game.remove_player(self.color)
        if self.game.NumPlayers == 0:
            Game_list.remove(self.game)
        self.conn.close()









def main():
    global client_socket
    srv_sock = socket.socket()
    ip = "0.0.0.0"
    port = 12345
    srv_sock.bind((ip, port))
    srv_sock.listen(10)
    threads = []
    tid = 0
    srv_sock.settimeout(600)
    while True:
        try:
            (conn, (ip, port)) = srv_sock.accept()
            print "new client\n"
            tid += 1

            new_thread = ClientThread(ip, port, conn, tid)
            new_thread.start()
            threads.append(new_thread)

        except socket.timeout:
            break

    srv_sock.close()
    for new_thread in threads:  # iterates over the threads
        new_thread.join()       # waits until the thread has finished wor
if __name__ == '__main__':
    main()