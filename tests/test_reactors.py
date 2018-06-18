from sourcing.reactors import Reactor, register, get_registered, reset_registered


class ReactorA1(Reactor):
    def execute(self):
        return 'A1'


class ReactorA2(Reactor):
    def execute(self):
        return 'A2'


class ReactorB1(ReactorA1):
    def execute(self):
        return 'B1'


class ReactorC1(ReactorB1):
    def execute(self):
        return 'C1'


def test_register_and_get_registered():
    reset_registered()
    register(ReactorA1)
    register(ReactorA2)
    register(ReactorB1)
    register(ReactorC1)
    reactors = get_registered()
    assert reactors == {ReactorA1, ReactorA2, ReactorB1, ReactorC1}


def test_register_and_get_registered_with_type():
    reset_registered()
    register(ReactorA1)
    register(ReactorA2, 'foo')
    register(ReactorB1, 'bar')
    register(ReactorC1, 'bar')
    register(ReactorC1, 'foo')
    assert get_registered() == {ReactorA1}
    assert get_registered('foo') == {ReactorA1, ReactorA2, ReactorC1}
    assert get_registered('bar') == {ReactorA1, ReactorB1, ReactorC1}
