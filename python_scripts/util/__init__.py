def read_file(filename):
    f = open(filename, "rb")
    data = f.read()
    f.close()
    return data

def write_file(filename,data):
    f = open(filename, "wb")
    f.write(data)
    f.close()
