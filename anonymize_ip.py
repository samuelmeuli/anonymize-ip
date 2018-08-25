from ipaddress import ip_address


def anonymize_ip(
    address,
    ipv4_mask="255.255.255.0",
    ipv6_mask="ffff:ffff:ffff:ffff:0000:0000:0000:0000"
):
    """
    Anonymize the provided IPv4 or IPv6 address by setting parts of the
    address to 0

    :param str|int address: IP address to be anonymized
    :param str ipv4_mask: Mask that defines which parts of an IPv4 address are
    set to 0 (default: "255.255.255.0")
    :param str ipv6_mask: Mask that defines which parts of an IPv6 address are
    set to 0 (default: "ffff:ffff:ffff:ffff:0000:0000:0000:0000")
    :return: Anonymized IP address
    :rtype: str
    """

    # IP address to be anonymized
    address_packed = ip_address(address).packed
    address_len = len(address_packed)

    if address_len == 4:
        # IPv4
        ipv4_mask_packed = ip_address(ipv4_mask).packed
        __validate_ipv4_mask(ipv4_mask_packed)
        return __apply_mask(address_packed, ipv4_mask_packed, 4)
    elif address_len == 16:
        # IPv6
        ipv6_mask_packed = ip_address(ipv6_mask).packed
        __validate_ipv6_mask(ipv6_mask_packed)
        return __apply_mask(address_packed, ipv6_mask_packed, 16)
    else:
        # Invalid address
        raise ValueError("Address does not consist of 4 (IPv4) or 16 (IPv6) "
                         "octets")


def __apply_mask(address_packed, mask_packed, nr_bytes):
    """
    Perform a bitwise AND operation on all corresponding bytes between the
    mask and the provided address. Mask parts set to 0 will become 0 in the
    anonymized IP address as well

    :param bytes address_packed: Binary representation of the IP address to
    be anonymized
    :param bytes mask_packed: Binary representation of the corresponding IP
    address mask
    :param int nr_bytes: Number of bytes in the address (4 for IPv4, 16 for
    IPv6)
    :return: Anonymized IP address
    :rtype: str
    """

    anon_packed = bytearray()
    for i in range(0, nr_bytes):
        anon_packed.append(mask_packed[i] & address_packed[i])
    return str(ip_address(bytes(anon_packed)))


def __validate_ipv4_mask(mask_packed):
    # Test that mask only contains valid numbers
    for byte in mask_packed:
        if byte != 0 and byte != 255:
            raise ValueError("ipv4_mask must only contain numbers 0 or 255")

    # Test that IP address does not get anonymized completely
    if mask_packed == b'\x00\x00\x00\x00':
        raise ValueError("ipv4_mask cannot be set to \"0.0.0.0\" (all "
                         "anonymized addresses will be 0.0.0.0)")

    # Test that IP address is changed by anonymization
    if mask_packed == b'\xff\xff\xff\xff':
        raise ValueError("ipv4_mask cannot be set to \"255.255.255.255\" "
                         "(addresses will not be anonymized)")


def __validate_ipv6_mask(mask_packed):
    # Test that mask only contains valid numbers
    for byte in mask_packed:
        if byte != 0 and byte != 255:
            raise ValueError("ipv6_mask must only contain numbers 0 or ffff")

    # Test that IP address does not get anonymized completely
    if (
        mask_packed ==
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    ):
        raise ValueError("ipv6_mask cannot be set to "
                         "\"0000:0000:0000:0000:0000:0000:0000:0000\" (all "
                         "anonymized addresses will be 0.0.0.0)")

    # Test that IP address is changed by anonymization
    if (
        mask_packed ==
        b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
    ):
        raise ValueError("ipv6_mask cannot be set to "
                         "\"ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff\" "
                         "(addresses will not be anonymized)")
