from ipaddress import ip_address


def anonymize(
    address,
    ipv4_mask="255.255.255.0",
    ipv6_mask="ffff:ffff:ffff:ffff:0000:0000:0000:0000"
):
    """
    Anonymize the provided IPv4 or IPv6 address by setting parts of the
    address to 0

    :param str address: IP address to be anonymized
    :param str ipv4_mask: Mask that defines which parts of an IPv4 address are
    set to 0 (default: "255.255.255.0")
    :param str ipv6_mask: Mask that defines which parts of an IPv6 address are
    set to 0 (default: "ffff:ffff:ffff:ffff:0000:0000:0000:0000")
    :return: Anonymized IP address
    :rtype: str
    """

    # IP address masks
    ipv4_mask_packed = ip_address(ipv4_mask).packed
    ipv6_mask_packed = ip_address(ipv6_mask).packed

    # IP address to be anonymized
    address_packed = ip_address(address).packed
    address_len = len(address_packed)

    if address_len == 4:
        # IPv4
        return __apply_mask(address_packed, ipv4_mask_packed, 4)
    elif address_len == 16:
        # IPv6
        return __apply_mask(address_packed, ipv6_mask_packed, 16)
    else:
        # Invalid address
        raise Exception("Address does not consist of 4 (IPv4) or 16 "
                        "(IPv6) octets")


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
