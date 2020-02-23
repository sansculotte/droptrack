from .lib import validate


def test_validate_url_success():
    assert validate('http://test.at')
    assert validate('https://sansculotte.net')

def test_validate_url_fail():
    assert not validate('gibberish')
    assert not validate('ftp://kernel.org')
