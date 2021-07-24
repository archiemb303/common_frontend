# channels_tut/routing.py
from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import common.chatengine.routing
import pdb
# pdb.set_trace()
application = ProtocolTypeRouter({
    # (http->django views is added by default)
    # 'websocket': AuthMiddlewareStack(
    'websocket': SessionMiddlewareStack(
        URLRouter(
            common.chatengine.routing.websocket_urlpatterns
        )
    ),
})
