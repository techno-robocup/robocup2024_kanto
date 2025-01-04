from techno_client.techno_client import TechnoClient

HOST = "roboberry.local"
# HOST = "192.168.11.123"
# HOST = "127.0.0.1"
PORT = 8085

client = TechnoClient(host=HOST, port=PORT)

while True:
    t = input("[input l/ld/li/r/rd/ci or q]% ")
    if t == 'q':
        print("close request")
        break
    elif t == 'l':
        r = client.line()
        print(r)
        # print(r.image_height)
        # print(str(r.colors[0].h)+","+str(r.colors[0].s)+","+str(r.colors[0].v))
    elif t == 'ld':
        print(client.line(debug=True))
    elif t.startswith("li"):
        ar = t.split(" ")
        if (len(ar) == 9):
            print(client.line_info(ar[1], ar[2], ar[3], ar[4],
                                   ar[5], ar[6], ar[7], ar[8]))
        else:
            print(client.line_info(1008, 0, 3608, 2592,
                                   3, 3, 50, 50))
    elif t == 'r':
        r = client.rescue()
        print(r)
        print(r.image_height)
    elif t == 'rd':
        print(client.rescue(debug=True))
    elif t == 'ci':
        print(client.clear_debug_image())
    else:
        print('unknown request')
