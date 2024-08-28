from pynostr.relay import Relay
from pynostr.filters import FiltersList, Filters
from pynostr.base_relay import RelayPolicy
from pynostr.message_pool import MessagePool
import tornado.ioloop
from tornado import gen
import uuid
import json

def getevent(ids=None, kinds=None, authors=None, since=None, until=None, event_refs=None, pubkey_refs=None, limit=None, relaywss = "wss://relay.primal.net"):
    message_pool = MessagePool(first_response_only=False)
    policy = RelayPolicy()
    io_loop = tornado.ioloop.IOLoop.current()
    r = Relay(
        relaywss,
        message_pool,
        io_loop,
        policy,
        timeout=2
    )

    event_list = []
    filter = FiltersList([Filters(ids=ids, kinds=kinds, authors=authors, since=since, until=until, event_refs=event_refs, pubkey_refs=pubkey_refs, limit=limit)])
    subscription_id = uuid.uuid1().hex
    r.add_subscription(subscription_id, filter)

    try:
        io_loop.run_sync(r.connect)
    except gen.Return:
        pass

    while message_pool.has_notices():
        notice_msg = message_pool.get_notice()
        print(notice_msg.content)
    while message_pool.has_events():
        event_msg = message_pool.get_event()
        event = json.loads(str(event_msg.event))
        event_list.append(event)

    return event_list