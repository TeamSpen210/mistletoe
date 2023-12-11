import re
import sys
from unicodedata import category


whitespace = {' ', '\t', '\n', '\x0b', '\x0c', '\r'}
unicode_whitespace = {'\t', '\n', '\x0b', '\x0c', '\r', '\x1c', '\x1d', '\x1e',
        '\x1f', ' ', '\x85', '\xa0', '\u1680', '\u2000', '\u2001', '\u2002',
        '\u2003', '\u2004', '\u2005', '\u2006', '\u2007', '\u2008', '\u2009',
        '\u200a', '\u2028', '\u2029', '\u202f', '\u205f', '\u3000'}

# BEGIN GENERATED PUNCTUATION
# See gen_punctuation.py.
punctuation = set(
    '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~!"#%&\'()*,-./:;?'
    '@[\\]_{}¡§«¶·»¿;·՚՛՜՝՞՟։֊־׀׃׆׳״؉؊،؍؛؝؞؟٪٫٬٭۔܀܁܂܃܄'
    '܅܆܇܈܉܊܋܌܍߷߸߹࠰࠱࠲࠳࠴࠵࠶࠷࠸࠹࠺࠻࠼࠽࠾࡞।॥॰৽੶૰౷಄෴๏๚๛༄༅༆༇༈༉༊་'
    '༌།༎༏༐༑༒༔༺༻༼༽྅࿐࿑࿒࿓࿔࿙࿚၊။၌၍၎၏჻፠፡።፣፤፥፦፧፨᐀᙮᚛᚜᛫᛬᛭᜵᜶។៕៖'
    '៘៙៚᠀᠁᠂᠃᠄᠅᠆᠇᠈᠉᠊᥄᥅᨞᨟᪠᪡᪢᪣᪤᪥᪦᪨᪩᪪᪫᪬᪭᭚᭛᭜᭝᭞᭟᭠᭽᭾᯼᯽᯾᯿᰻᰼᰽᰾'
    '᰿᱾᱿᳀᳁᳂᳃᳄᳅᳆᳇᳓‐‑‒–—―‖‗‘’‚‛“”„‟†‡•‣․‥…‧‰‱′″‴‵‶‷‸‹›※'
    '‼‽‾‿⁀⁁⁂⁃⁅⁆⁇⁈⁉⁊⁋⁌⁍⁎⁏⁐⁑⁓⁔⁕⁖⁗⁘⁙⁚⁛⁜⁝⁞⁽⁾₍₎⌈⌉⌊⌋〈〉❨❩❪❫❬'
    '❭❮❯❰❱❲❳❴❵⟅⟆⟦⟧⟨⟩⟪⟫⟬⟭⟮⟯⦃⦄⦅⦆⦇⦈⦉⦊⦋⦌⦍⦎⦏⦐⦑⦒⦓⦔⦕⦖⦗⦘⧘⧙⧚⧛⧼'
    '⧽⳹⳺⳻⳼⳾⳿⵰⸀⸁⸂⸃⸄⸅⸆⸇⸈⸉⸊⸋⸌⸍⸎⸏⸐⸑⸒⸓⸔⸕⸖⸗⸘⸙⸚⸛⸜⸝⸞⸟⸠⸡⸢⸣⸤⸥⸦⸧'
    '⸨⸩⸪⸫⸬⸭⸮⸰⸱⸲⸳⸴⸵⸶⸷⸸⸹⸺⸻⸼⸽⸾⸿⹀⹁⹂⹃⹄⹅⹆⹇⹈⹉⹊⹋⹌⹍⹎⹏⹒⹓⹔⹕⹖⹗⹘⹙⹚'
    '⹛⹜⹝、。〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〽゠・꓾꓿꘍꘎꘏꙳꙾꛲꛳꛴꛵꛶꛷꡴꡵꡶'
    '꡷꣎꣏꣸꣹꣺꣼꤮꤯꥟꧁꧂꧃꧄꧅꧆꧇꧈꧉꧊꧋꧌꧍꧞꧟꩜꩝꩞꩟꫞꫟꫰꫱꯫﴾﴿︐︑︒︓︔︕︖︗︘︙︰︱'
    '︲︳︴︵︶︷︸︹︺︻︼︽︾︿﹀﹁﹂﹃﹄﹅﹆﹇﹈﹉﹊﹋﹌﹍﹎﹏﹐﹑﹒﹔﹕﹖﹗﹘﹙﹚﹛﹜﹝﹞﹟﹠﹡﹣'
    '﹨﹪﹫！＂＃％＆＇（）＊，－．／：；？＠［＼］＿｛｝｟｠｡｢｣､･𐄀𐄁𐄂𐎟𐏐𐕯𐡗𐤟𐤿𐩐𐩑𐩒𐩓𐩔𐩕'
    '𐩖𐩗𐩘𐩿𐫰𐫱𐫲𐫳𐫴𐫵𐫶𐬹𐬺𐬻𐬼𐬽𐬾𐬿𐮙𐮚𐮛𐮜𐺭𐽕𐽖𐽗𐽘𐽙𐾆𐾇𐾈𐾉𑁇𑁈𑁉𑁊𑁋𑁌𑁍𑂻𑂼𑂾𑂿𑃀𑃁𑅀𑅁𑅂'
    '𑅃𑅴𑅵𑇅𑇆𑇇𑇈𑇍𑇛𑇝𑇞𑇟𑈸𑈹𑈺𑈻𑈼𑈽𑊩𑑋𑑌𑑍𑑎𑑏𑑚𑑛𑑝𑓆𑗁𑗂𑗃𑗄𑗅𑗆𑗇𑗈𑗉𑗊𑗋𑗌𑗍𑗎𑗏𑗐𑗑𑗒𑗓𑗔'
    '𑗕𑗖𑗗𑙁𑙂𑙃𑙠𑙡𑙢𑙣𑙤𑙥𑙦𑙧𑙨𑙩𑙪𑙫𑙬𑚹𑜼𑜽𑜾𑠻𑥄𑥅𑥆𑧢𑨿𑩀𑩁𑩂𑩃𑩄𑩅𑩆𑪚𑪛𑪜𑪞𑪟𑪠𑪡𑪢𑱁𑱂𑱃𑱄'
    '𑱅𑱰𑱱𑻷𑻸𑿿𒑰𒑱𒑲𒑳𒑴𒿱𒿲𖩮𖩯𖫵𖬷𖬸𖬹𖬺𖬻𖭄𖺗𖺘𖺙𖺚𖿢𛲟𝪇𝪈𝪉𝪊𝪋𞥞𞥟'
)
# END GENERATED PUNCTUATION

code_pattern = re.compile(r"(?<!\\|`)(?:\\\\)*(`+)(?!`)(.+?)(?<!`)\1(?!`)", re.DOTALL)


_code_matches = []


def find_core_tokens(string, root):
    delimiters = []
    matches = []
    escaped = False
    in_delimiter_run = None
    in_image = False
    start = 0
    i = 0
    code_match = code_pattern.search(string)
    while i < len(string):
        if code_match is not None and i == code_match.start():
            if in_delimiter_run is not None:
                delimiters.append(Delimiter(start, i if not escaped else i - 1, string))
                in_delimiter_run = None
                escaped = False
            _code_matches.append(code_match)
            i = code_match.end()
            code_match = code_pattern.search(string, i)
            continue
        c = string[i]
        if c == '\\' and not escaped:
            escaped = True
            i += 1
            continue
        if in_delimiter_run is not None and (c != in_delimiter_run or escaped):
            delimiters.append(Delimiter(start, i if not escaped else i - 1, string))
            in_delimiter_run = None
        if in_delimiter_run is None and (c == '*' or c == '_') and not escaped:
            in_delimiter_run = c
            start = i
        if not escaped:
            if c == '[':
                if not in_image:
                    delimiters.append(Delimiter(i, i + 1, string))
                else:
                    delimiters.append(Delimiter(i - 1, i + 1, string))
                    in_image = False
            elif c == '!':
                in_image = True
            elif c == ']':
                i = find_link_image(string, i, delimiters, matches, root)
                code_match = code_pattern.search(string, i)
            elif in_image:
                in_image = False
        else:
            escaped = False
        i += 1
    if in_delimiter_run:
        delimiters.append(Delimiter(start, i, string))
    process_emphasis(string, None, delimiters, matches)
    return matches


def find_link_image(string, offset, delimiters, matches, root=None):
    i = len(delimiters) - 1
    for delimiter in delimiters[::-1]:
        # found a link/image delimiter
        if delimiter.type in ('[', '!['):
            # not active, remove delimiter
            if not delimiter.active:
                delimiters.remove(delimiter)
                return offset
            match = match_link_image(string, offset, delimiter, root)
            # found match
            if match:
                # parse for emphasis
                process_emphasis(string, i, delimiters, matches)
                # append current match
                matches.append(match)
                # if match is a link, set all previous links to be inactive
                if delimiter.type == '[':
                    deactivate_delimiters(delimiters, i, '[')
                # shift index till end of match
                return match.end() - 1
            # no match, remove delimiter
            delimiters.remove(delimiter)
            return offset
        i -= 1
    # no link/image delimiter
    return offset


def process_emphasis(string, stack_bottom, delimiters, matches):
    star_bottom = stack_bottom
    underscore_bottom = stack_bottom
    curr_pos = next_closer(stack_bottom, delimiters)
    while curr_pos is not None:
        closer = delimiters[curr_pos]
        bottom = star_bottom if closer.type[0] == '*' else underscore_bottom
        open_pos = matching_opener(curr_pos, delimiters, bottom)
        if open_pos is not None:
            opener = delimiters[open_pos]
            n = 2 if closer.number >= 2 and opener.number >= 2 else 1
            start = opener.end - n
            end = closer.start + n
            match = MatchObj(start, end, (start + n, end - n, string[start + n:end - n]))
            match.type = 'Strong' if n == 2 else 'Emphasis'
            match.delimiter = string[start]
            matches.append(match)
            # remove all delimiters in between
            del delimiters[open_pos + 1:curr_pos]
            curr_pos -= curr_pos - open_pos - 1
            # remove appropriate number of chars from delimiters
            if not opener.remove(n, left=False):
                delimiters.remove(opener)
                curr_pos -= 1
            if not closer.remove(n, left=True):
                delimiters.remove(closer)
                curr_pos -= 1
            if curr_pos < 0:
                curr_pos = 0
        else:
            bottom = curr_pos - 1 if curr_pos > 1 else None
            if closer.type[0] == '*':
                star_bottom = bottom
            else:
                underscore_bottom = bottom
            if not closer.open:
                delimiters.remove(closer)
            else:
                curr_pos += 1
        curr_pos = next_closer(curr_pos, delimiters)
    del delimiters[stack_bottom:]


def match_link_image(string, offset, delimiter, root=None):
    image = delimiter.type == '!['
    start = delimiter.start
    text_start = start + delimiter.number
    text_end = offset
    text = string[text_start:text_end]
    # inline link
    if follows(string, offset, '('):
        # link destination
        match_info = match_link_dest(string, offset + 1)
        if match_info is not None:
            dest_start, dest_end, dest = match_info
            # link title
            match_info = match_link_title(string, dest_end)
            if match_info is not None:
                title_start, title_end, title = match_info
                # assert closing paren
                paren_index = shift_whitespace(string, title_end)
                if paren_index < len(string) and string[paren_index] == ')':
                    end = paren_index + 1
                    match = MatchObj(start, end,
                                      (text_start, text_end, text),
                                      (dest_start, dest_end, dest),
                                      (title_start, title_end, title))
                    match.type = 'Link' if not image else 'Image'
                    match.dest_type = "angle_uri" if dest_start < dest_end and string[dest_start] == "<" else "uri"
                    match.title_delimiter = string[title_start] if title_start < title_end else None
                    return match
    # footnote link
    if follows(string, offset, '['):
        # full footnote link: [label][dest]
        result = match_link_label(string, offset + 1, root)
        if result:
            match_info, (dest, title) = result
            end = match_info[1]
            match = MatchObj(start, end,
                              (text_start, text_end, text),
                              (-1, -1, dest),
                              (-1, -1, title))
            match.type = 'Link' if not image else 'Image'
            match.label = match_info[2]
            match.dest_type = "full"
            return match
        ref = get_link_label(text, root)
        if ref:
            # compact (collapsed) footnote link: [dest][]
            if follows(string, offset + 1, ']'):
                dest, title = ref
                end = offset + 3
                match = MatchObj(start, end,
                                  (text_start, text_end, text),
                                  (-1, -1, dest),
                                  (-1, -1, title))
                match.type = 'Link' if not image else 'Image'
                match.dest_type = "collapsed"
                return match
        return None
    # shortcut footnote link: [dest]
    ref = get_link_label(text, root)
    if ref:
        dest, title = ref
        end = offset + 1
        match = MatchObj(start, end,
                          (text_start, text_end, text),
                          (-1, -1, dest),
                          (-1, -1, title))
        match.type = 'Link' if not image else 'Image'
        match.dest_type = "shortcut"
        return match
    return None


def match_link_dest(string, offset):
    offset = shift_whitespace(string, offset + 1)
    if offset == len(string):
        return None
    if string[offset] == '<':
        escaped = False
        for i, c in enumerate(string[offset + 1:], start=offset + 1):
            if c == '\\' and not escaped:
                escaped = True
            elif c == '\n' or (c == '<' and not escaped):
                return None
            elif c == '>' and not escaped:
                return offset, i + 1, string[offset + 1:i]
            elif escaped:
                escaped = False
        return None
    else:
        escaped = False
        count = 1
        for i, c in enumerate(string[offset:], start=offset):
            if c == '\\' and not escaped:
                escaped = True
            elif c in whitespace:
                return offset, i, string[offset:i]
            elif not escaped:
                if c == '(':
                    count += 1
                elif c == ')':
                    count -= 1
            elif is_control_char(c):
                return None
            elif escaped:
                escaped = False
            if count == 0:
                return offset, i, string[offset:i]
        return None


def match_link_title(string, offset):
    offset = shift_whitespace(string, offset)
    if offset == len(string):
        return None
    if string[offset] == ')':
        return offset, offset, ''
    if string[offset] == '"':
        closing = '"'
    elif string[offset] == "'":
        closing = "'"
    elif string[offset] == '(':
        closing = ')'
    else:
        return None
    escaped = False
    for i, c in enumerate(string[offset + 1:], start=offset + 1):
        if c == '\\' and not escaped:
            escaped = True
        elif c == closing and not escaped:
            return offset, i + 1, string[offset + 1:i]
        elif escaped:
            escaped = False
    return None


def match_link_label(string, offset, root=None):
    start = -1
    end = -1
    escaped = False
    for i, c in enumerate(string[offset:], start=offset):
        if c == '\\' and not escaped:
            escaped = True
        elif c == '[' and not escaped:
            if start == -1:
                start = i
            else:
                return None
        elif c == ']' and not escaped:
            end = i
            label = string[start + 1:end]
            match_info = start, end + 1, label
            if label.strip() != '':
                ref = root.footnotes.get(normalize_label(label), None)
                if ref is not None:
                    return match_info, ref
                return None
            return None
        elif escaped:
            escaped = False
    return None


def get_link_label(text, root):
    """
    Normalize and look up `text` among the footnotes.
    Returns (destination, title) if successful, otherwise None.
    """
    if not root:
        return None
    escaped = False
    for c in text:
        if c == '\\' and not escaped:
            escaped = True
        elif (c == '[' or c == ']') and not escaped:
            return None
        elif escaped:
            escaped = False
    if text.strip() != '':
        return root.footnotes.get(normalize_label(text), None)
    return None


def normalize_label(text):
    return ' '.join(text.split()).casefold()


def next_closer(curr_pos, delimiters):
    for i, delimiter in enumerate(delimiters[curr_pos:], start=curr_pos or 0):
        if hasattr(delimiter, 'close') and delimiter.close:
            return i
    return None


def matching_opener(curr_pos, delimiters, bottom):
    if curr_pos > 0:
        curr_delimiter = delimiters[curr_pos]
        index = curr_pos - 1
        for delimiter in delimiters[curr_pos - 1:bottom:-1]:
            if (hasattr(delimiter, 'open')
                    and delimiter.open
                    and delimiter.closed_by(curr_delimiter)):
                return index
            index -= 1
    return None


def is_opener(start, end, string):
    if string[start] == '*':
        return is_left_delimiter(start, end, string)
    is_right = is_right_delimiter(start, end, string)
    return (is_left_delimiter(start, end, string)
            and (not is_right
                 or (is_right and preceded_by(start, string, punctuation))))


def is_closer(start, end, string):
    if string[start] == '*':
        return is_right_delimiter(start, end, string)
    is_left = is_left_delimiter(start, end, string)
    return (is_right_delimiter(start, end, string)
            and (not is_left
                 or (is_left and succeeded_by(end, string, punctuation))))


def is_left_delimiter(start, end, string):
    return (not succeeded_by(end, string, unicode_whitespace)
            and (not succeeded_by(end, string, punctuation)
                 or preceded_by(start, string, punctuation)
                 or preceded_by(start, string, unicode_whitespace)))


def is_right_delimiter(start, end, string):
    return (not preceded_by(start, string, unicode_whitespace)
            and (not preceded_by(start, string, punctuation)
                 or succeeded_by(end, string, unicode_whitespace)
                 or succeeded_by(end, string, punctuation)))


def preceded_by(start, string, charset):
    preceding_char = string[start - 1] if start > 0 else ' '
    return preceding_char in charset


def succeeded_by(end, string, charset):
    succeeding_char = string[end] if end < len(string) else ' '
    return succeeding_char in charset


def is_control_char(char):
    return ord(char) < 32 or ord(char) == 127


def follows(string, index, char):
    return index + 1 < len(string) and string[index + 1] == char


def shift_whitespace(string, index):
    for i, c in enumerate(string[index:], start=index):
        if c not in whitespace:
            return i
    return len(string)


def deactivate_delimiters(delimiters, index, delimiter_type):
    for delimiter in delimiters[:index]:
        if delimiter.type == delimiter_type:
            delimiter.active = False


class Delimiter:
    def __init__(self, start, end, string):
        self.type = string[start:end]
        self.number = end - start
        self.active = True
        self.start = start
        self.end = end
        if self.type.startswith(('*', '_')):
            self.open = is_opener(start, end, string)
            self.close = is_closer(start, end, string)

    def remove(self, n, left=True):
        if self.number - n == 0:
            return False
        if left:
            self.start = self.start + n
            self.number = self.end - self.start
            self.type = self.type[n:]
            return True
        self.end = self.end - n
        self.number = self.end - self.start
        self.type = self.type[:n]
        return True

    def closed_by(self, other):
        if self.type[0] != other.type[0]:
            return False
        if self.open and self.close or other.open and other.close:
            # if either of the delimiters can both open and close emphasis, then additional
            # restrictions apply: the sum of the lengths of the delimiter runs
            # containing the opening and closing delimiters must not be a multiple of 3
            # unless both lengths are multiples of 3.
            return ((self.number + other.number) % 3 != 0
                    or (self.number % 3 == 0 and other.number % 3 == 0))
        return True

    def __repr__(self):
        if not self.type.startswith(('*', '_')):
            return '<Delimiter type={} active={}>'.format(repr(self.type), self.active)
        return '<Delimiter type={} active={} open={} close={}>'.format(repr(self.type), self.active, self.open, self.close)


class MatchObj:
    def __init__(self, start, end, *fields):
        self._start = start
        self._end = end
        self.fields = fields

    def start(self, n=0):
        if n == 0:
            return self._start
        return self.fields[n - 1][0]

    def end(self, n=0):
        if n == 0:
            return self._end
        return self.fields[n - 1][1]

    def group(self, n=0):
        if n == 0:
            return ''.join([field[2] for field in self.fields])
        return self.fields[n - 1][2]

    def __repr__(self):
        return '<MatchObj fields={} start={} end={}>'.format(self.fields, self._start, self._end)
