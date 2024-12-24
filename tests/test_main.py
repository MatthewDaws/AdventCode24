import pytest

import advent.__main__ as main

def test_parse_args():
    assert main.parse_args(["", "all"])[0] == "all"
    assert main.parse_args(["", "3"]) == ("run", 3, False)
    assert main.parse_args(["", "5", "2nd"]) == ("run", 5, True)
    with pytest.raises(SyntaxError):
        main.parse_args([""])
    with pytest.raises(SyntaxError):
        main.parse_args(["", "bob"])
    with pytest.raises(SyntaxError):
        main.parse_args(["", 5, "2nd", "thing"])
    with pytest.raises(SyntaxError):
        main.parse_args(["", 5, "thing"])


