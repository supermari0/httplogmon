def poll_log_file(filename):
    with open(filename, 'r') as f:
        while True:
            line = f.readline()
            if line:
                yield line

if __name__ == '__main__':
    for l in poll_log_file('test.txt'):
        print(l)
