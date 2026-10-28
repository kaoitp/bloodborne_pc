"""Check the guest's BBSC mod logs from an R03 native gate run (B15 R4-N0..N4, B17 N1..N3).

Pass the guest's bbsc-mod-*.log files in process order (one file per guest process) and the case.
The checker only reads logs and, with --user-dir, the record/journal files; it starts nothing.
Verdict: PASS (exit 0), FAIL (1), INCOMPLETE (2: an expected line is missing, the run may have
stopped early) or MANUAL (3: the remaining judgement is a person's, as for R4-N4).
"""
import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import sys

LINE = re.compile(r'^\[(\d\d):(\d\d):(\d\d)\.(\d\d\d)\] \w (\w+): (.*)$')
CASES = ('b15-n0', 'b15-n1', 'b15-n2', 'b15-n3', 'b15-n4', 'b17-n1', 'b17-n2', 'b17-n3')


@dataclass
class Entry:
    process: int  # index of the log file, 1-based in the report
    line: int     # index within the process: the order, since consecutive lines can share a millisecond
    seconds: float
    text: str

    def show(self):
        h, rest = divmod(self.seconds, 3600)
        m, s = divmod(rest, 60)
        return f'p{self.process + 1} [{int(h):02}:{int(m):02}:{s:06.3f}] {self.text}'


def parse(text, process):
    entries = []
    for raw in text.splitlines():
        match = LINE.match(raw)
        if match:
            h, m, s, ms, _, message = match.groups()
            entries.append(Entry(process, len(entries), int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000,
                                 message))
    return entries


class Report:
    def __init__(self):
        self.rows = []

    def add(self, status, name, detail=''):
        self.rows.append((status, name, detail))

    def need(self, entry, name, missing=''):
        """ok with the line when found, missing (INCOMPLETE) otherwise."""
        if entry:
            self.add('ok', name, entry.show())
        else:
            self.add('missing', name, missing)
        return entry

    def expect(self, good, name, detail=''):
        self.add('ok' if good else 'fail', name, detail)
        return good

    def verdict(self):
        statuses = {row[0] for row in self.rows}
        for status, word in (('fail', 'FAIL'), ('missing', 'INCOMPLETE'), ('manual', 'MANUAL')):
            if status in statuses:
                return word
        return 'PASS'


def first(entries, pattern, after=None, before=None):
    for entry in entries:
        if after is not None and _order(entry) <= _order(after):
            continue
        if before is not None and _order(entry) >= _order(before):
            continue
        if re.search(pattern, entry.text):
            return entry
    return None


def every(entries, pattern):
    return [entry for entry in entries if re.search(pattern, entry.text)]


def _order(entry):
    return entry.process, entry.line


def elapsed(earlier, later):
    """Seconds from earlier to later in one process; the log has only the time of day, so past midnight wraps."""
    return (later.seconds - earlier.seconds) % 86400


class B15:
    def __init__(self, args):
        e, u, s = args.event, re.escape(args.user), args.slot
        drop = 'BBSC boss drop: '
        self.queued = rf'{drop}event {e} queued for user {u} slot {s}$'
        self.add = rf'{drop}goods {args.goods} x\d+ put into the carried items .*there now: true'
        self.finished = rf'{drop}event {e} lot -?\d+ finished for user {u} slot {s}$'
        self.final = rf'{drop}event {e} is in the save of user {u} slot {s} - final$'
        self.not_again = rf'{drop}event {e} was already given to user {u} slot {s} in an earlier run - not again$'
        self.never_saved = rf'{drop}event {e} of user {u} slot {s} from an earlier run - never saved, can be earned again$'
        self.unwritable = rf'{drop}event {e} - record not writable, waiting$'
        # Lines only the opt-in record writes; none of them may appear with the variable off.
        self.record = (rf'{drop}event {e} (- record not writable|is in the save|given, its granted line'
                       rf'|of user .* from an earlier run|of user .* an earlier run\'s add'
                       rf'|of user .* save not readable|was already given|- an earlier run\'s add)')
        self.held = rf'{drop}event {e} of user {u} slot {s} - an earlier run\'s add has no recorded outcome'
        self.file = Path(args.user_dir) / 'boss-rewards' / f'given-{args.user}-{s}.txt' if args.user_dir else None
        self.event = e

    def file_lines(self):
        if self.file is None or not self.file.is_file():
            return None
        return self.file.read_text(encoding='utf-8').splitlines()


def check_b15(case, logs, args, report):
    b = B15(args)
    flat = [entry for log in logs for entry in log]
    # (fewest, most) guest processes each case is written for; evidence in other processes is never ignored.
    fewest, most = {'b15-n0': (2, 2), 'b15-n1': (1, 1), 'b15-n4': (1, 1)}.get(case, (2, None))
    if len(logs) < fewest or (most is not None and len(logs) > most):
        wanted = f'{fewest}' if fewest == most else f'at least {fewest}'
        report.add('missing', 'processes', f'{wanted} guest log(s) (one per process) for this case, got {len(logs)}')
        return
    held = first(flat, b.held)
    if case != 'b15-n0' and held:
        report.add('fail', 'no held attempt', held.show())

    if case == 'b15-n0':
        for index in (0, 1):
            given = every(logs[index], b.finished)
            report.expect(len(given) == 1, f'p{index + 1}: one lot given (the existing behaviour)',
                          f'{len(given)} "finished" line(s)')
        record = first(flat, b.record)
        report.expect(record is None, 'no record line with the variable off',
                      record.show() if record else '')
        if b.file is not None:
            report.expect(not b.file.exists(), 'no record file with the variable off', str(b.file))
        return

    if case in ('b15-n1', 'b15-n4'):
        p = logs[0]
        report.need(first(p, b.queued), 'queued')
        add = report.need(first(p, b.add), 'goods put into the carried items')
        given = every(p, b.finished)
        report.expect(len(given) == 1, 'one lot given', f'{len(given)} "finished" line(s)')
        final = report.need(first(p, b.final, after=given[0] if given else None),
                            'final after the save', 'no "- final": did the game save before the exit?')
        report.expect(first(flat, b.unwritable) is None, 'record was writable')
        if add and final:
            delta = elapsed(add, final)
            note = f'save seen {delta:.1f} s after the add (checked once a second)'
            if case == 'b15-n4':
                report.add('manual', 'in-flight save boundary',
                           note + '; compare the add time with the first userdata save write after it '
                                  '(file times) and say whether that save could have begun before the add')
            else:
                report.expect(delta <= 60, 'final within 60 s', note)
        lines = b.file_lines()
        if b.file is not None:
            report.expect(lines is not None and str(b.event) in lines, 'record file holds the final line',
                          f'{b.file}: {lines}')
        return

    if case == 'b15-n2':
        given = every(logs[0], b.finished)
        report.expect(len(given) == 1, 'p1: one lot given', f'{len(given)} "finished" line(s)')
        final = first(logs[0], b.final)
        report.expect(final is None, 'p1: killed before the save', final.show() if final else '')
        later = logs[1:]
        flat_later = [entry for log in later for entry in log]
        never = report.need(first(flat_later, b.never_saved), 'restart: never saved, can be earned again')
        again = first(flat_later, b.not_again)
        report.expect(again is None, 'restart: not refused', again.show() if again else '')
        regiven = every(flat_later, b.finished)
        if not regiven:
            report.add('missing', 'next joint kill gives it', 'no "finished" after the restart')
        else:
            report.expect(len(regiven) == 1 and (never is None or _order(regiven[0]) > _order(never)),
                          'next joint kill gives it exactly once', f'{len(regiven)} "finished" line(s)')
        return

    if case == 'b15-n3':
        p = logs[0]
        waits = every(p, b.unwritable)
        report.need(waits[0] if waits else None, 'p1: record not writable, waiting')
        given = every(p, b.finished)
        adds = every(p, b.add)
        if waits:
            # The tick logs "waiting" every second until the folder is writable again; the add comes after.
            early = [entry for entry in adds if _order(entry) < _order(waits[-1])]
            report.expect(not early, 'p1: no Pendant while unwritable',
                          early[0].show() if early else '')
        if not given:
            report.add('missing', 'p1: given once write access is back', 'no "finished" line')
        else:
            report.expect(len(given) == 1 and len(adds) == 1, 'p1: given exactly once',
                          f'{len(given)} "finished", {len(adds)} add line(s)')
            report.need(first(p, b.final, after=given[0]), 'p1: final after the save')
        report.need(first(logs[-1], b.not_again), f'p{len(logs)}: not again after the restart')
        for index in range(1, len(logs)):
            again = every(logs[index], rf'{b.finished}|{b.add}')
            report.expect(not again, f'p{index + 1}: no second lot after the restart',
                          again[0].show() if again else '')
        return


class B17:
    def __init__(self, args):
        u, s = re.escape(args.user), args.slot
        home = 'BBSC home recovery: '
        self.left = rf'BBSC own world: user {u} slot {s} was left with another player\'s world in it'
        self.goes_back = rf'{home}user {u} slot {s} goes back to {args.map:#x} '
        self.goes_back_any = rf'{home}user {u} slot {s} goes back to '
        self.point = rf'{home}requested original point into {args.map:#x}, lamp -?\d+, accepted true \(try 1\)'
        self.requested = rf'{home}requested '
        self.lamp = rf'{home}requested recorded lamp into 0x[0-9a-f]+, lamp -?\d+, accepted true'
        self.point_failed = (rf'{home}(request refused|arrived elsewhere|the requested load did not come) '
                             rf'\(point \d+ of \d+\)')
        self.settled = rf'{home}own world and return point settled'
        self.gave_up = rf'{home}no way back'
        self.canceled = (rf'{home}(another load canceled pending return; journal retained for user {u} '
                         rf'slot {s}$|user .* is loaded, not the journal\'s user {u} slot {s} )')
        self.title = r'BBSC own world: a character is loading from the title'
        folder = Path(args.user_dir) / 'own-world' if args.user_dir else None
        self.journal = folder / f'own-{args.user}-{s}.bin' if folder else None


def check_b17(case, logs, args, report):
    b = B17(args)
    flat = [entry for log in logs for entry in log]
    gave_up = first(flat, b.gave_up)
    report.expect(gave_up is None, 'no give-up', gave_up.show() if gave_up else '')
    left = report.need(first(flat, b.left), 'journal found after the crash',
                       'kill the guest within 10 s of "placed", then restart it and load the character')
    back = report.need(first(flat, b.goes_back, after=left) if left else None,
                       f'goes back to {args.map:#x}')
    if back is None:
        return

    if case == 'b17-n1':
        point = report.need(first(flat, b.point, after=back), 'original point requested (try 1)')
        settled = report.need(first(flat, b.settled, after=point or back), 'settled')
        if point and settled:
            tries = every([e for e in flat if _order(back) < _order(e) < _order(settled)], b.requested)
            report.expect(len(tries) == 1, 'arrived on the first request', f'{len(tries)} request(s)')
        report.add('manual', 'position', 'within 5 m of the journaled spot; still in the Clinic after '
                                         'quitting and reloading')
    elif case == 'b17-n2':
        request = report.need(first(flat, b.requested, after=back), 'return requested')
        cancel = report.need(first(flat, b.canceled, after=request) if request else None,
                             'pending return dropped by the other load',
                             'Quit Game to the title before the arrival and load another character')
        if cancel is None:
            return
        title = first(flat, b.title, after=request)
        report.add('ok' if title else 'note', 'load from the title seen', title.show() if title else '')
        again = first(flat, b.goes_back_any, after=cancel)
        window = [e for e in flat if _order(cancel) < _order(e) and (again is None or _order(e) < _order(again))]
        stray = first(window, rf'{b.requested}|{b.settled}')
        report.expect(stray is None, 'the other character neither warps nor settles',
                      stray.show() if stray else '')
        report.add('manual', 'other character', 'no flag difference against its own baseline')
        if again is None:
            report.add('missing', 'owner loaded again and returned', 'load the owner again')
            if b.journal is not None:
                report.expect(b.journal.is_file(), 'journal still on disk', str(b.journal))
        else:
            report.need(first(flat, b.settled, after=again), 'owner loaded again and returned')
    else:  # b17-n3
        failed = report.need(first(flat, b.point_failed, after=back), 'the point failed',
                             'make the point fail, for example an unreachable position in a copy of the journal')
        lamp = report.need(first(flat, b.lamp, after=failed) if failed else None, 'recorded lamp requested')
        report.need(first(flat, b.settled, after=lamp) if lamp else None, 'settled at the lamp')
        report.add('manual', 'reload', 'after quitting and reloading, still at the lamp with its own flags')

    if b.journal is not None and case != 'b17-n2':
        restored = b.journal.with_name(b.journal.name + '.restored')
        report.expect(restored.is_file() and not b.journal.exists(), 'journal kept as .restored',
                      f'{restored.name}: {restored.is_file()}, {b.journal.name}: {b.journal.exists()}')


def run(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('case', choices=CASES)
    parser.add_argument('logs', nargs='+', type=Path, help="guest bbsc-mod-*.log files, in process order")
    parser.add_argument('--user', default='sd1', help='save user of the guest character (default sd1)')
    parser.add_argument('--slot', type=int, default=3, help='save slot of the guest character (default 3)')
    parser.add_argument('--event', type=int, default=12401800, help='B15 boss event (default Amelia)')
    parser.add_argument('--goods', type=int, default=4001, help='B15 reward goods (default Gold Pendant)')
    parser.add_argument('--map', type=lambda v: int(v, 0), default=0x18010000, help='B17 journaled map')
    parser.add_argument('--user-dir', help="the mod's user folder holding boss-rewards/ and own-world/")
    args = parser.parse_args(argv)
    logs = [parse(path.read_text(encoding='utf-8', errors='replace'), index)
            for index, path in enumerate(args.logs)]
    report = Report()
    (check_b15 if args.case.startswith('b15') else check_b17)(args.case, logs, args, report)
    return report


def main():
    report = run()
    for status, name, detail in report.rows:
        print(f'{status:8} {name}' + (f'\n         {detail}' if detail else ''))
    verdict = report.verdict()
    print(verdict)
    return {'PASS': 0, 'FAIL': 1, 'INCOMPLETE': 2, 'MANUAL': 3}[verdict]


if __name__ == '__main__':
    sys.exit(main())
