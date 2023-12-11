"""Generate the _punctuation set.

This requires iterating over the whole Unicode character set, which doesn't change often.
It's more efficient to do this earlier.
"""
import sys
import pprint
import unicodedata


def build() -> set[str]:
    """Build the characters list."""
    characters = {
        '!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',',
        '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\',
        ']', '^', '_', '`', '{', '|', '}', '~'
    }
    for i in range(sys.maxunicode + 1):
        c = chr(i)
        if unicodedata.category(c).startswith("P"):
            characters.add(c)
    return characters


def write_module() -> None:
    chars = build()

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

    formatted = pprint.pformat(chars, width=72, compact=True).splitlines()

    with open('mistletoe/core_tokens.py', 'w', encoding='utf8') as f:
        f.writelines(prefix)
        f.write('# Precomuted, iterating all Unicode is quite slow. See gen_punctuation.py.\n')
        # First line here, all others indented by 8.
        f.write(f'punctuation = {formatted[0]}\n')
        for line in formatted[1:]:
            f.write(f'        {line}\n')
        f.writelines(postfix)


if __name__ == '__main__':
    write_module()
