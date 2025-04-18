# tests/test_firewall.py
def test_malicious_command_blocking():
    firewall = AIFirewall()
    assert firewall.validate_input("rm -rf /") == False
    assert firewall.validate_input("Hello world") == True
