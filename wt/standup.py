#!/usr/bin/env python3

# Generate current standup entry in standup.md or if one
# exists for today copy it to the clipboard.

import datetime, os, re, shutil, sys, tempfile

DATE_FMT = '%Y-%m-%d %A'

log = '/Users/marcbutler/My Drive/Notes/Standup/standup.md'
assert os.path.exists(log)

def parse_date(datestr):
    return datetime.datetime.strptime(datestr, '%Y-%m-%d %A').date()

last_entry = []
date_of_last_entry = None
with open(log, 'r') as f:
    for l in f.readlines():
        if m := re.match('^##\s+(.*)\s*$', l):
            if date_of_last_entry:
                break
            date_of_last_entry = parse_date(m.group(1))
        elif date_of_last_entry:
            last_entry.append(l.rstrip())

today = datetime.datetime.now().date()
if date_of_last_entry == today:
    import clipboard
    clipboard.copy('\n'.join(last_entry))
    print(f'Today\'s standup entry copied to clipboard.')
    sys.exit(0)

with tempfile.NamedTemporaryFile(delete=False) as f:
    temp_file = f.name
    print(temp_file)

    def writeln(s, depth=0):
        indent = '' if depth == 0 else ' ' * (depth * 4)
        f.write(bytes(indent + s + '\n', 'utf-8'))
    
    writeln('# Standup')
    writeln(f'## {today.strftime(DATE_FMT)}')

    writeln(f'{date_of_last_entry.strftime("%A")}')
    i = last_entry.index('Today')
    f.write(bytes('\n'.join(last_entry[i+1:]), 'utf-8'))
    writeln('\nToday')
    writeln('-')

    with open(log, 'r') as history:
        history.readline()
        f.write(bytes(history.read(), 'utf-8'))

shutil.copy2(log, log + '.bak')
shutil.move(temp_file, log)
print(f'Added entry template for today {log}')
