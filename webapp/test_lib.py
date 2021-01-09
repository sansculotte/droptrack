from .lib.helpers import validate_url


def test_validate_url_success():
    assert validate_url('http://test.at')
    assert validate_url('https://sansculotte.net')

def test_validate_url_fail():
    assert not validate_url('gibberish')
    assert not validate_url('ftp://kernel.org')
