SIZE_HEADER_FORMAT = "000000|"
size_header_size = len(SIZE_HEADER_FORMAT)
def recv_by_size (sock):
    str_size = ""
    data_len = 0
    while len(str_size) < size_header_size:
        str_size += sock.recv(size_header_size - len(str_size))
        if str_size == "":
            break
    data  = ""
    if str_size != "":
        data_len = int(str_size[:size_header_size - 1])
        while len(data) < data_len:
            data += sock.recv(data_len - len(data))
            if data == "":
                break
    DEBUG = False
    if DEBUG and str_size !="" and len(data) < 100 :
        print "\nRecv(%s)>>>%s"%(str_size, data)
    if data_len != len(data):
        data=""
    return data

def send_with_size (sock,data):
    data = str(len(data)).zfill(size_header_size - 1) + "|" + data

    sock.send(data)
    DEBUG = False

    if DEBUG and len(data) < 100:
          print "\nSent>>>"+data
