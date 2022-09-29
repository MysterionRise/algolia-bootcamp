from command_processing import process_message


def test_simple():
    user = process_message("biletik @klydd")
    assert user == "@klydd"
