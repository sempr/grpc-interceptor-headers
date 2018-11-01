import grpc
import pytest
import random
from samples.greeter_client import do_call
from samples.greeter_server import get_serve


def test_pass():
    bind = "0.0.0.0:{}".format(random.randint(60000, 61000))
    serv = get_serve(bind=bind)
    serv.start()
    try:
        resp = do_call(bind=bind, name="abc")
        assert resp == 'Hello, abc!', "Normal Call Failed"
        try:
            resp = do_call(bind=bind, header_name="error")
            assert False, "Should Be Failed"
        except grpc._channel._Rendezvous as e:
            assert e.code(
            ) == grpc.StatusCode.UNAUTHENTICATED, "Should be UNAUTHENTICATED code"
    finally:
        serv.stop(0)
