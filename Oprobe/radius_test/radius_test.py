import argparse
import pyrad.packet
from pyrad.client import Client
from pyrad.dictionary import Dictionary

def test_radius(server, secret, username, password):
    client = Client(server=server, secret=bytes(secret, 'utf-8'), dict=Dictionary("/usr/share/freeradius/dictionary"))
    
    request = client.CreateAuthPacket(code=pyrad.packet.AccessRequest, User_Name=username)
    request["User-Password"] = request.PwCrypt(password)
    
    try:
        reply = client.SendPacket(request)
        if reply.code == pyrad.packet.AccessAccept:
            print("Authentication successful!")
        else:
            print("Authentication failed!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RADIUS Server Tester")
    parser.add_argument("-s", "--server", required=True, help="RADIUS Server IP")
    parser.add_argument("-p", "--password", required=True, help="User Password")
    parser.add_argument("-u", "--username", required=True, help="Username")
    parser.add_argument("-k", "--secret", required=True, help="RADIUS Secret Key")
    
    args = parser.parse_args()
    test_radius(args.server, args.secret, args.username, args.password)
