"""Generate the _punctuation set.

This requires iterating over the whole Unicode character set, which doesn't change often.
It's more efficient to do this earlier.
"""
import sys

import unicodedata


# punctuation: _ASCII and Unicode punctuation characters_ as defined at
# <https://spec.commonmark.org/0.30/#ascii-punctuation-character> and
# <https://spec.commonmark.org/0.30/#unicode-punctuation-character>
COLUMNS = 48


def build() -> list[str]:
    """Build the characters list."""
    characters = [
        '!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',',
        '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\',
        ']', '^', '_', '`', '{', '|', '}', '~'
    ]
    for i in range(sys.maxunicode + 1):
        c = chr(i)
        if unicodedata.category(c).startswith("P"):
            characters.append(c)
    return characters


def write_module() -> None:
    chars = ''.join(build())

    prefix = []
    postfix = []
    with open('mistletoe/core_tokens.py', 'r', encoding='utf8') as f:
        for line in f:
            prefix.append(line)
            if line.startswith('# BEGIN GENERATED PUNCTUATION'):
                break
        else:
            raise ValueError('No start comment!')
        for line in f:
            if line.startswith('# END GENERATED PUNCTUATION'):
                postfix.append(line)
                break
        else:
            raise ValueError('No end comment!')
        postfix.extend(f.readlines())

    with open('mistletoe/core_tokens.py', 'w', encoding='utf8') as f:
        f.writelines(prefix)
        f.write('# See gen_punctuation.py.\n')
        f.write('punctuation = set(\n')
        for i in range(0, len(chars), COLUMNS):
            f.write(f'    {chars[i:i+COLUMNS]!r}\n')
        f.write(')\n')
        f.writelines(postfix)


if __name__ == '__main__':
    write_module()
