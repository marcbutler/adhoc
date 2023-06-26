#!/usr/bin/env python3

# Generate current standup entry in standup.md or if one
# exists for today copy it to the clipboard.

import datetime, re, shutil, sys, tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import List, TextIO


DATE_FMT = '%Y-%m-%d %A'
standup_log_backup = Path(Path.home(), 'My Drive/Notes/Standup/standup.md')
standup_log = Path(Path.home(), 'Documents/standup.md')
worklog = Path(Path.home(), 'Documents/worklog.md')


@dataclass
class StandupEntry:
    date: datetime
    text: List[str]

    def that_day(self):
        '''Return anticipated activity from the entry.'''
        i = self.text.index('Today')
        return '\n'.join(self.text[i+1:])

    def as_markdown(self):
        ticket_types = "WT WTBUILD BACKPORT HELP SERVER PM SEAI".split()

        def link(match):
            ticket = match.group(0).upper()
            prefix, _ = ticket.split('-')
            if prefix not in ticket_types:
                return match.group(0)
            return f'[{ticket}](https://jira.mongodb.org/browse/{ticket})'

        msg = ''
        for line in self.text:
            # I found re.IGNORECASE would not match case variations of
            # the following: '(wt|backup|help)'. So use a function for
            # the substitution.
            msg += re.sub(r'\b((?:\w+)-\d+)\b', link, line) + '\n'
        return msg

def parse_date(datestr:str) -> datetime:
    return datetime.datetime.strptime(datestr, DATE_FMT).date()

@dataclass
class WorklogEntry:
    date: datetime
    issues: List[str]

    @staticmethod
    def extract_list(file: TextIO) -> 'WorklogEntry':
        in_entry = False
        text = []
        for line in file.readlines():
            if m := re.match(r'^##\s+(.*)\s*$', line):
                if in_entry:
                    break
                in_entry = True
                text.append(m.group(0))
            if m := re.match(r'^###\s+(.*)\s*$') and in_entry:
                text.append(m.group(1))
        if text == [] or in_entry == True:
            raise RuntimeError("Unterminated entry.")

        return WorklogEntry(parse_date(text[0], text[1:]))


def previous_standup(path: Path) -> StandupEntry:
    last_entry = []
    date_of_last_entry = None
    with open(standup_log, 'r') as f:
        for l in f.readlines():
            if m := re.match('^##\s+(.*)\s*$', l):
                if date_of_last_entry:
                    break
                date_of_last_entry = parse_date(m.group(1))
            elif date_of_last_entry:
                last_entry.append(l.rstrip())
    return StandupEntry(date_of_last_entry, last_entry)


if __name__ == '__main__':

    assert standup_log.exists()
    assert standup_log_backup.exists()

    last_entry = previous_standup(standup_log)

    today = datetime.datetime.now().date()
    if last_entry.date == today:
        import clipboard
        clipboard.copy(last_entry.as_markdown())
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

        writeln(f'{last_entry.date.strftime("%A")}')
        f.write(bytes(last_entry.that_day(), 'utf-8'))
        writeln('\nToday')
        writeln('-')

        # Append standup history.
        with open(standup_log, 'rb') as history:
            # Throw away first line containing standup title.
            history.readline()

            shutil.copyfileobj(history, f)

    shutil.move(temp_file, standup_log)
    shutil.copy2(standup_log, standup_log_backup)
    print(f'Added entry template for today {standup_log}')
