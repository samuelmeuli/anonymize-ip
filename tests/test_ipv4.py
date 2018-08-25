import unittest

from anonymize_ip import anonymize_ip


class TestIpv4(unittest.TestCase):
    def test_default(self):
        address = "95.239.169.11"
        anonymized = anonymize_ip(address)
        self.assertEqual(anonymized, "95.239.169.0")

    def test_last_two_octets(self):
        address = "224.6.226.252"
        mask = "255.255.0.0"
        anonymized = anonymize_ip(address, ipv4_mask=mask)
        self.assertEqual(anonymized, "224.6.0.0")

    def test_last_three_octets(self):
        address = "76.173.77.243"
        mask = "255.0.0.0"
        anonymized = anonymize_ip(address, ipv4_mask=mask)
        self.assertEqual(anonymized, "76.0.0.0")

    def test_full_address(self):
        address = "146.255.125.163"
        mask = "0.0.0.0"
        self.assertRaises(ValueError, anonymize_ip, address, ipv4_mask=mask)

    def test_no_anonymization(self):
        address = "107.154.113.161"
        mask = "255.255.255.255"
        self.assertRaises(ValueError, anonymize_ip, address, ipv4_mask=mask)

    def test_integer(self):
        # Integer representation of 176.126.30.183
        address = 2961055415
        anonymized = anonymize_ip(address)
        self.assertEqual(anonymized, "176.126.30.0")

    def test_invalid_address(self):
        address = "4"
        self.assertRaises(ValueError, anonymize_ip, address)

    def test_invalid_mask(self):
        address = "7.187.60.47"
        mask = "3.255.0.4"
        self.assertRaises(ValueError, anonymize_ip, address, ipv4_mask=mask)
