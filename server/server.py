import sys
from twisted.web.static import File
from twisted.python import log
from twisted.web.server import Site
from twisted.internet import reactor
import json

from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol

from autobahn.twisted.resource import WebSocketResource

class SomeServerProtocol(WebSocketServerProtocol):
    def onOpen(self):
        self.factory.register(self)
        # self.factory.findPartner(self)

    def connectionLost(self, reason):
        self.factory.unregister(self)

    def onMessage(self, payload):
        self.factory.communicate(self, payload)

class ChatRouletteFactory(WebSocketServerFactory):
    def __init__(self, *args, **kwargs):
        super(ChatRouletteFactory, self).__init__(*args, **kwargs)
        self.clients = {}

    def register(self, client):
        self.clients[client.peer] = {"object": client, "partner": None}

    def unregister(self, client):
        self.clients.pop(client.peer)

    # def findPartner(self, client):
    #     available_partners = [c for c in self.clients if c != client.peer 
    #                           and not self.clients[c]["partner"]]
    #     if not available_partners:
    #         print("no partners for {} check in a moment".format(client.peer))
    #     else:
    #         partner_key = random.choice(available_partners)
    #         self.clients[partner_key]["partner"] = client
    #         self.clients[client.peer]["partner"] = self.clients[partner_key]["object"]

    def communicate(self, client, payload):
        c = self.clients[client.peer]
        if not c["partner"]:
            c["object"].sendMessage("Sorry you dont have partner yet, check back in a minute")
        else:
            c["partner"].sendMessage(payload)

#{type: "message", msg:"this is a sample message", to:3, type="private"}
#{type:"update_user_id", instance_id: "1223", user_id:2}
# async def receivemessage(websocket):
#     data = await websocket.recv()
#     data = json.load(data)
#     if data.type == "update_user_id":
#         clients[data.user_id] = clients[data.instance_id]
#         del clients[data.instance_id]
#     elif data.type == "message":
#         await clients[data.to].websocket.send(json.dumps(data))


if __name__ == "__main__":
    log.startLogging(sys.stdout)

    # static file server seving index.html as root
    root = File(".")

    factory = ChatRouletteFactory(u"ws://127.0.0.1:8080", debug=True)
    factory.protocol = SomeServerProtocol
    resource = WebSocketResource(factory)
    # websockets resource on "/ws" path
    root.putChild(u"ws", resource)

    site = Site(root)
    reactor.listenTCP(8080, site)
    reactor.run()
