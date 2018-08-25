import unittest

import ip_anonymizer


class TestIpv6(unittest.TestCase):
    def test_default(self):
        address = "5219:3a94:fdc5:19e1:70a3:b2c4:40ef:ae03"
        anonymized = ip_anonymizer.anonymize(address)
        self.assertEqual(anonymized, "5219:3a94:fdc5:19e1::")

    def test_last_block(self):
        address = "c03d:13b:4757:674a:7563:cd57:6ac0:57c5"
        mask = "ffff:ffff:ffff:ffff:ffff:ffff:ffff:0000"
        anonymized = ip_anonymizer.anonymize(address, ipv6_mask=mask)
        self.assertEqual(anonymized, "c03d:13b:4757:674a:7563:cd57:6ac0:0")

    def test_last_two_blocks(self):
        address = "4942:70b7:1441:7814:4f1b:ab59:1501:ddec"
        mask = "ffff:ffff:ffff:ffff:ffff:ffff::"
        anonymized = ip_anonymizer.anonymize(address, ipv6_mask=mask)
        self.assertEqual(anonymized, "4942:70b7:1441:7814:4f1b:ab59::")

    def test_full_address(self):
        address = "895f:5f37:69a8:d069:8744:2854:61ca:4eff"
        mask = "0000:0000:0000:0000:0000:0000:0000:0000"
        self.assertRaises(ValueError, ip_anonymizer.anonymize, address,
                          ipv6_mask=mask)

    def test_no_anonymization(self):
        address = "3c84:eba0:d242:370:e79d:2e39:e5cb:254b"
        mask = "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"
        self.assertRaises(ValueError, ip_anonymizer.anonymize, address,
                          ipv6_mask=mask)

    def test_integer(self):
        # Integer representation of 2d09:1b4b:9fd0:9edf:a856:5086:69ec:9282
        address = 59862544098679838285986760092514292354
        anonymized = ip_anonymizer.anonymize(address)
        self.assertEqual(anonymized, "2d09:1b4b:9fd0:9edf::")

    def test_invalid_address(self):
        address = "4"
        self.assertRaises(ValueError, ip_anonymizer.anonymize, address)

    def test_invalid_mask(self):
        address = "cc32:cf4d:7e7a:89cf:5d2:895c:2a93:a67a"
        mask = "ffff:ffff:ffff:abcd:1234:ffff:0000:0000"
        self.assertRaises(ValueError, ip_anonymizer.anonymize, address,
                          ipv6_mask=mask)
