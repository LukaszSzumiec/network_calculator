# import fcntl
import struct
import sys
import socket

import platform  # For getting the operating system name
import subprocess  # For executing a shell command


def ping(host):
    s = input("This is a host ip, do you want to ping it? Y/N")

    if s != "Y":
        return

    param = '-n' if platform.system().lower() == 'windows' else '-c'

    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
        # print(IP)
    return IP


def checkIfPrivate(tab):
    if (tab[0] == 10) and (0 <= tab[1] <= 255) and (0 <= tab[2] <= 255) and (1 <= tab[3] <= 254):
        return "Private, class A"
    elif (tab[0] == 172) and (16 <= tab[1] <= 31) and (0 <= tab[2] <= 255) and (1 <= tab[3] <= 254):
        return "Private, class B"
    elif (tab[0] == 192) and (tab[1] == 168) and (0 <= tab[2] <= 255) and (1 <= tab[3] <= 254):
        return "Private, class C"
    else:
        return "Public"


def get_mask(mask):
    _mask = "0b"
    # print("MASKAAAAAAAA" + mask)
    try:
        mask = int(mask)
    except ValueError:
        print("Invalid mask")
        sys.exit(0)
    print(mask)
    if mask <= 0 or mask >= 30:
        print("Invalid mask")
        sys.exit(0)
    z = 0
    x = 32
    check = 0
    while x > 0:
        if z < mask:
            if (check == 8):
                _mask += ".0b"
                check = 0
            _mask += "1"
            check += 1
            z += 1
        else:
            if (check == 8):
                _mask += ".0b"
                check = 0
            _mask += "0"
            check += 1
        x -= 1

    pmask = _mask.split(".")

    # print (pmask)
    _mask = ""
    temp = 0
    for x in pmask:
        # print (x)
        temp = int(x, 2)
        _mask += str(temp)
        _mask += "."
    # print (_mask)
    return _mask


def check_ip(tab):
    check_signs(tab)


def check_signs(tab):
    for x in tab:
        if x < 0 or x > 255:
            print("Wrong IP address")
            sys.exit(0)


def tab_to_string(tab):
    string = ""
    for x in tab:
        if len(string) == 0:
            string += str(x)
        else:
            string += "." + str(x)
    return string


def tab_to_string_bin(tab):
    string = ""
    for x in tab:
        if len(string) == 0:
            x = bin(x)
            string += x
        else:
            x = bin(x)
            string += "." + x
    return string


def remove0b(string):
    ret_string = ""
    _string = string.split("0b")

    p = 0
    for x in _string:
        if x != '':

            if len(x) < 9:
                zeros = ""
                m = x
                c = len(x)
                if p == 3:
                    c += 1
                while c < 9:
                    zeros += "0"
                    c += 1
                x = zeros + m
            p += 1
            ret_string += x

    return ret_string


def fullfil_signs(string, type):
    _string = string.split(".")
    # print(_string)
    ret_string = ""
    p = 0
    for x in _string:
        if x is not None:
            # print(x)
            # print(len(x))
            if len(x) < 10:
                signs = ""
                m = x
                c = len(x)
                # if p == 3:
                # c += 1
                while c < 10:
                    if type == 0:
                        signs += "0"
                        c += 1
                    else:
                        signs += "1"
                        c += 1
                x = m + signs

            if p != 0:
                ret_string = ret_string + "."
            ret_string += x
            p += 1
    return ret_string


if len(sys.argv) == 2:
    arg = sys.argv[1]
    ip, mask = arg.split("/")
    # print(len(mask))
    mask = get_mask(mask)
    # print("MASKA" + mask)
    # mask = int(mask,2)
else:
    ip = get_ip()
    mask = "255.255.255.0"
tab_string_ip = ip.split(".")
string_ip = ""
if len(tab_string_ip) != 4:
    print("Wrong ip address")
    sys.exit(0)
tab_ip = []
ip_as_bin = ""
fullfil_signs(ip, 1)
for x in tab_string_ip:
    try:
        x = int(x)
    except ValueError:
        print("Ip address is incorrect")
        sys.exit(0)

    tab_ip.append(x)
    string_ip += str(x)
    if len(ip_as_bin) != 0:
        ip_as_bin += "." + bin(x)
    else:
        ip_as_bin += bin(x)
check_signs(tab_ip)
ip_as_int = int(string_ip)

tab_string_mask = mask.split(".")
if len(tab_string_mask) == 5:
    tab_string_mask.remove('')

# print(tab_string_mask)
string_mask_bin = ""
tab_mask = []
for x in tab_string_mask:  # mask
    x = int(x)
    tab_mask.append(x)
    x = bin(x)
    if len(string_mask_bin) != 0:
        string_mask_bin += "." + x
    else:
        string_mask_bin += x

tab_address = [tab_ip[0] & tab_mask[0], tab_ip[1] & tab_mask[1], tab_ip[2] & tab_mask[2], tab_ip[3] & tab_mask[3]]
address = ""

subaddr = tab_address[3]

for x in tab_address:
    if len(address) != 0:
        address = address + "." + str(x)
    else:
        address = str(x)

reversed_mask = "0b"  # REVERSED MASK
broadcast_address_tab = []
temp = 0
check = 0
digit_counter = 0
for x in tab_mask:
    # print(x)
    x = bin(x)
    if check != 0:
        reversed_mask += ".0b"
    check += 1
    counter = 0
    for p in x:
        if counter > 1:
            if p == "0":
                p = "1"
            else:
                digit_counter += 1
                p = "0"
            reversed_mask += p
        counter += 1
broadcast_address = ""
counter = 0
broadcast_address_bin = ""

reversed_mask = fullfil_signs(reversed_mask, 1)
# print(reversed_mask + "reversed mask")
# reversed_mask = fullfil_signs(reversed_mask, 0)
# print(reversed_mask)
# tab_broadcast_address = []
tab_broadcast_address = reversed_mask.split(".")
tab_broadcast_address_dec = []

for x in tab_broadcast_address:
    x = int(x, 2)
    x = x + tab_address[counter]
    counter += 1
    if len(broadcast_address) != 0:
        broadcast_address = broadcast_address + "." + str(x)
        tab_broadcast_address_dec.append(int(x))
    else:
        broadcast_address += str(x)
        tab_broadcast_address_dec.append(int(x))

max_hosts = 2 ** (32 - digit_counter) - 2

tab_address[3] += 1

broadcast_address_bin = tab_to_string_bin(tab_broadcast_address_dec)
tab_broadcast_address_dec[3] -= 1

first_host = tab_to_string(tab_address)
last_host = tab_to_string(tab_broadcast_address_dec)

first_host_bin = tab_to_string_bin(tab_address)
last_host_bin = tab_to_string_bin(tab_broadcast_address_dec)
first_host_bin = remove0b(first_host_bin)
last_host_bin = remove0b(last_host_bin)

ip_as_bin = remove0b(ip_as_bin)
string_mask_bin = remove0b(string_mask_bin)
broadcast_address_bin = remove0b(broadcast_address_bin)

subIP = tab_ip[3]
subBroadcast = tab_broadcast_address_dec[3]
subBroadcast += 1
# print(subaddr)
# print(subIP)
# print(subBroadcast)
# print(intIP)


wyjscie = open("wyjscie.txt", "w")


def Save():
    print()
    print("Address number:" + address, file=wyjscie)
    print("Address is" + checkIfPrivate(tab_ip), file=wyjscie)
    print("IP: ", ip, "\t\t", ip_as_bin, file=wyjscie)
    print("Mask: " + mask, "\t\t" + string_mask_bin, file=wyjscie)
    print("Broadcast address:" + broadcast_address + "\t\t" + broadcast_address_bin, file=wyjscie)
    print("First hosts:" + first_host, "\t\t" + first_host_bin, file=wyjscie)
    print("Last host:" + last_host, "\t\t" + last_host_bin, file=wyjscie)
    print("Max hosts:" + str(max_hosts), file=wyjscie)


def Print():
    print()
    print("Address number:", address)
    print("Address is", checkIfPrivate(tab_ip))
    print("IP: ", ip, "\t\t", ip_as_bin)
    print("Mask: ", mask, "\t\t", string_mask_bin)
    print("Broadcast address:", broadcast_address, "\t\t", broadcast_address_bin)
    print("First hosts:", first_host, "\t\t", first_host_bin)
    print("Last host:", last_host, "\t\t", last_host_bin)
    print("Max hosts:", max_hosts)


Print()
Save()
if subaddr < subIP < subBroadcast:
    ping(ip)
