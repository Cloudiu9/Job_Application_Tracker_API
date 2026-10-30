from security import hash_password, verify_password

def test_verify_password_success():
    dummy_pass = "DUMMY_PASSWORD"
    hashed_pass = hash_password(dummy_pass)

    verified_pass = verify_password(hashed_pass, dummy_pass)

    assert verified_pass is True

def test_incorrect_password():
    dummy_pass = "DUMMY_PASSWORD"
    wrong_password = "WRONG_PASSWORD"
    hashed_pass = hash_password(dummy_pass)

    verified_pass = verify_password(hashed_pass, wrong_password)

    assert verified_pass is False

def test_two_password_hashes():
    dummy_pass = "DUMMY_PASSWORD"
    hashed_pass = hash_password(dummy_pass)
    hashed_pass_2 = hash_password(dummy_pass)

    verified_pass = verify_password(hashed_pass, dummy_pass)
    verified_pass_2 = verify_password(hashed_pass_2, dummy_pass)

    assert verified_pass is True
    assert verified_pass_2 is True
    assert hashed_pass != hashed_pass_2