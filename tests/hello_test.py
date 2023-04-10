import pytest
from src.hello import Hello

def test_say():
    hello = Hello()
    assert hello.say(3) == "HelloHelloHello"
    assert hello.say(1) == "Hello"
    assert hello.say(0) == ""