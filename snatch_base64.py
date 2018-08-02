status = 0
cmd = ""
is_gzipped = None

def capture_line(line):
    global status
    global cmd, is_gzipped
    if status == 0:
        index_centos = line.find("base64 -w0")
        index_mac = line.find("base64 -i -")
        if (index_centos != -1) or (index_mac != -1):
            status = 1
            cmd = line
            print "start capture!!"
            if line.find("gzip") != -1:
                is_gzipped = True
                print "gzip support"

    elif status == 1:
        from base64 import b64decode
        filename = "dumped_{}".format(get_filename(cmd))
        with open(filename, "wb") as fout:
            if is_gzipped:
                import gzip, StringIO
                in_ = StringIO.StringIO(b64decode(line))
                with gzip.GzipFile(fileobj=in_, mode='rb') as fo:
                    gunzipped_bytes_obj = fo.read()

                fout.write(gunzipped_bytes_obj)
            else:
                fout.write(b64decode(line))
        print "dumped!!"
        status = 0
    else:
        status = 0

def get_filename(line):
    start = line.find("cat")
    end = line.find("|", start)
    name = line[start+4:end].strip()
    print "filename", name
    return name

buffer = []
lines = []
with open("fifo.pipe") as fp:
    while True:
        r = fp.read(1)
        if len(r) == 0:
            break

        buffer.append(r)
        # print r, ord(r)
        if r == "\n":
            line = "".join(buffer).strip()
            lines.append(line)
            # print "> {}".format(line)
            buffer = []
            capture_line(line)
