import io


def word_group(start_word: str, state: str, followup_word: str) -> str:
    colour = {
        'B': 'black',
        'Y': 'yellow',
        'G': 'green'
    }

    out = ''
    out += '<div class="word-group">'
    out += '<div class="word">'
    for i in range(len(start_word)):
        out += f'<div class="letter letter-{colour[state[i]]}">{start_word[i]}</div>'
    out += '</div>'

    out += '<div class="word">'
    for i in range(len(followup_word)):
        out += f'<div class="letter letter-none">{followup_word[i]}</div>'
    out += '</div>'
    out += '</div>\n'

    return out


with open('test.html', 'r') as file:
    template = file.read()


def sort_func(content) -> int:
    _, state, _ = content
    state: str
    assert len(state) == 5

    out = 0
    # out |= state.count('G') << 13
    out |= (state.count('Y') + state.count('G')) << 10
    out |= int(state.replace('G', '10').replace('Y', '01').replace('B', '00'), base=2)
    return out


contents = []
body = io.StringIO()
with open('tarse.tree', 'r', encoding='ascii', newline='\n') as tree:
    word = tree.read(6)[:-1]
    # ⚠️ ⚠️ WARNING bad code alert! ⚠️ ⚠️
    while len(line := tree.readline()) == 16:
        index = tree.tell()
        state = line[:5]
        tree.seek(int(line[5:-1]))
        # body.write(word_group(word, state, tree.read(5)))
        contents.append((word, state, tree.read(5)))
        tree.seek(index)

contents.sort(key=sort_func)
# print([c[1] for c in contents])
l = None
# body.write('<div>')
for content in contents:
    n = sort_func(content) >> 10
    if n != l:
        if l is not None:
            body.write('</div>')
        body.write('<div class=columns>')
        body.write(f'<h1>Case: LC{n}</h1>\n')
    l = n

    body.write(word_group(*content))

with open('out.html', 'w') as file:
    file.write(template.replace('{{BODY}}', body.getvalue()))
