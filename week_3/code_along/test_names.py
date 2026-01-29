import pytest
from names import make_full_name, extract_family_name, extract_given_name

def test_make_full_name():
    full_name = make_full_name('Odogwu', 'Malay')
    assert isinstance(full_name, str)

    assert make_full_name('Nnaji', 'Chimamkpam') == "Nnaji; Chimamkpam"
    assert make_full_name('Xavier', 'Rodriquez') == "Xavier; Rodriquez"
    assert make_full_name('Loius', 'De-Angelou') == 'Loius; De-Angelou'

def test_extract_family_name():
    family_name = extract_family_name('Odogwu Malay')
    assert isinstance(family_name, str)

    assert extract_family_name('Nnaji Chimamkpam') == 'Nnaji'
    assert extract_family_name('Xavier Rodriquez') == 'Xavier'
    assert extract_family_name('Loius De-Angelou') == 'Loius'

def test_extract_given_name():
    given_name = extract_given_name('Odogwu Malay')
    assert isinstance(given_name, str)

    assert extract_given_name('Nnaji Chimamkpam') == 'Chimamkpam'
    assert extract_given_name('Xavier Rodriquez') == 'Rodriquez'
    assert extract_given_name('Loius De-Angelou') == 'De-Angelou'
    

pytest.main(["-v", "--tb=line", "-rN", __file__])
