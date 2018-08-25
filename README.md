# anonymize_ip

This is a simple Python library for anonymizing IP addresses. Both IPv4 and IPv6 addresses are supported.

Examples:

* IPv4: `95.239.169.11` → `95.239.169.0`
* IPv6: `5219:3a94:fdc5:19e1:70a3:b2c4:40ef:ae03` → `5219:3a94:fdc5:19e1::`


## Usage

```
pip install anonymizeip
```

```py
from anonymizeip import anonymize_ip

address = "fe80::0202:b3ff:fe1e:8329"
anonymized = anonymize_ip(address)
print(anonymized)

# Prints "fe80::"
```


## Settings

The number of address blocks that are set to 0 can be customized.

Besides the IP address, the function `anonymize_ip` takes two optional parameters:

```py
anonymize_ip(
  address,
  ipv4_mask="...",
  ipv6_mask="..."
)
```

* `ipv4_mask`: Defaults to `255.255.255.0`, i.e. the last octet will be anonymized (set to 0)
* `ipv6_mask`: Defaults to `ffff:ffff:ffff:ffff::` (same as `ffff:ffff:ffff:ffff:0:0:0:0`), i.e. the last four blocks will be anonymized (set to 0)


## Development

1. `git clone`
2. `pipenv install --dev`
3. Make your code modifications
4. `pipenv run test`
5. `pipenv run lint`

Contributions are always welcome. Please first discuss changes via issue before submitting a pull request.


## Credits

The implementation of this library was strongly inspired by [php-ip-anonymizer](https://github.com/geertw/php-ip-anonymizer) by Geert Wirken.
