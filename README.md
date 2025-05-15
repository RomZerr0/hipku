# Hipku

Port of a tiny javascript library to encode IPv6 and IPv4 addresses as haiku. Original library: https://github.com/gabemart/hipku


## Usage

To encode `127.0.0.1` or `::1` call `Hipku.encode('127.0.0.1')` or `Hipku.encode('::1')`. IPv4 addresses must have octets separated by a `.` period character and IPv6 addresses must have hextets separated by a `:` colon character.

When decoding a hipku, such as:

    The weary red dove
    fights in the empty tundra.
    Jasmine petals dance.

the lines can be separated either by the newline character `\n` or by a space. Both will produce the same result.

    Hipku.decode('The weary red dove\nfights in the empty tundra.\nJasmine petals dance.');

    > "254.53.93.114"

    Hipku.decode('The weary red dove fights in the empty tundra. Jasmine petals dance.');

    > "254.53.93.114"

