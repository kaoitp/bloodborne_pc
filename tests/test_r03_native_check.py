"""The R03 native-gate log checker (tools/check_r03_native.py) against logs made from the actual BBSC
log format strings, so a changed message in the source breaks this test instead of the friend's run.
Synthetic logs only: no game, no native run."""
from paths import ROOT
import importlib.util
import os
from pathlib import Path
import re
import tempfile
import unittest

SOURCE = Path(os.environ.get('BBSC_FIXTURE_SOURCE') or
              ROOT / '.superpowers/reference/BBSC/emulator/src/core/bloodborne_re.cpp')
spec = importlib.util.spec_from_file_location('check_r03_native', ROOT / 'tools/check_r03_native.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

FORMATS = {''.join(re.findall(r'"((?:[^"\\]|\\.)*)"', match.group(1)))
           for match in re.finditer(r'LOG_(?:INFO|WARNING)\(Debug,\s*((?:"(?:[^"\\]|\\.)*"\s*)+)',
                                    SOURCE.read_text(encoding='utf-8'))}


def say(fragment, *values):
    """The source's one message containing fragment, with its {} fields filled in order (fmt style)."""
    found = [f for f in FORMATS if fragment in f]
    assert len(found) == 1, (fragment, found)
    values = iter(values)

    def field(match):
        value = next(values)
        if isinstance(value, bool):
            return 'true' if value else 'false'
        return format(value, match.group(0)[2:-1])
    return re.sub(r'\{[^}]*\}', field, found[0])


class Log:
    def __init__(self, start=20 * 3600):
        self.lines, self.t = [], start

    def __call__(self, fragment, *values, after=1):
        self.t += after
        h, rest = divmod(self.t % 86400, 3600)
        self.lines.append(f'[{h:02}:{rest // 60:02}:{rest % 60:02}.000] I Debug: ' + say(fragment, *values))
        return self


E, U, S, GOODS, MAP, LAMP = 12401800, 'sd1', 3, 4001, 0x18010000, 2401000
QUEUED, ADDED, FINISHED = 'queued for user', 'put into the carried items', 'finished for user'
FINAL, EARLIER, AGAIN = 'is in the save of user', 'from an earlier run - {}', 'was already given to user'
WAITING, NEVER = 'record not writable, waiting', 'never saved, can be earned again'
LEFT, BACK, REQUESTED = 'was left with another player', 'user {} slot {} goes back to', 'requested {} into'
SETTLED, GAVE_UP = 'own world and return point settled', 'no way back to the spot'
TITLE, CANCELED = 'a character is loading from the title', 'another load canceled pending return'
FAILED = 'BBSC home recovery: {} ({} {} of {})'


def finished(log):
    return log(QUEUED, E, U, S)(ADDED, GOODS, 1, True, 0, True, 0)(FINISHED, E, 50000001, U, S)


def recovered(log):
    return log(LEFT, U, S)(BACK, U, S, MAP, 'where it joined')


def point(log, attempt=1):
    return log(REQUESTED, 'original point', MAP, LAMP, True, attempt)


class R03NativeCheckTests(unittest.TestCase):
    def verdict(self, case, *logs, user_dir=None):
        with tempfile.TemporaryDirectory() as directory:
            paths = []
            for index, log in enumerate(logs):
                path = Path(directory) / f'bbsc-mod-{index}.log'
                path.write_text('\n'.join(log.lines) + '\n', encoding='utf-8')
                paths.append(str(path))
            report = checker.run([case, *paths] + (['--user-dir', str(user_dir)] if user_dir else []))
        return report.verdict(), report.rows

    def assertVerdict(self, expected, case, *logs, user_dir=None):
        verdict, rows = self.verdict(case, *logs, user_dir=user_dir)
        self.assertEqual(verdict, expected, rows)

    def test_b15_n0_default_off(self):
        self.assertVerdict('PASS', 'b15-n0', finished(Log()), finished(Log()))
        self.assertVerdict('FAIL', 'b15-n0', finished(Log()), finished(Log())(FINAL, E, U, S))  # record on
        self.assertVerdict('FAIL', 'b15-n0', finished(Log()), Log()(AGAIN, E, U, S))

    def test_b15_n1_normal_grant(self):
        good = finished(Log())(FINAL, E, U, S, after=26)
        self.assertVerdict('PASS', 'b15-n1', good)
        self.assertVerdict('INCOMPLETE', 'b15-n1', finished(Log()))  # exit before the save
        self.assertVerdict('FAIL', 'b15-n1', finished(finished(Log()))(FINAL, E, U, S))
        self.assertVerdict('FAIL', 'b15-n1', finished(Log())(FINAL, E, U, S, after=90))
        late = finished(Log(start=24 * 3600 - 10))(FINAL, E, U, S, after=26)   # the save past midnight
        self.assertVerdict('PASS', 'b15-n1', late)
        self.assertVerdict('INCOMPLETE', 'b15-n1', good, Log())   # one process only, a second is not ignored
        with tempfile.TemporaryDirectory() as user_dir:
            (Path(user_dir) / 'boss-rewards').mkdir()
            record = Path(user_dir) / 'boss-rewards' / f'given-{U}-{S}.txt'
            record.write_text(f'granted {E} 1\n')
            self.assertVerdict('FAIL', 'b15-n1', good, user_dir=user_dir)
            record.write_text(f'{E}\n')
            self.assertVerdict('PASS', 'b15-n1', good, user_dir=user_dir)

    def test_b15_n2_exit_before_save(self):
        self.assertVerdict('PASS', 'b15-n2', finished(Log()), finished(Log()(EARLIER, E, U, S, NEVER)))
        self.assertVerdict('FAIL', 'b15-n2', finished(Log()), Log()(AGAIN, E, U, S))
        self.assertVerdict('FAIL', 'b15-n2', finished(Log())(FINAL, E, U, S),
                           finished(Log()(EARLIER, E, U, S, NEVER)))   # saved: not this case
        self.assertVerdict('INCOMPLETE', 'b15-n2', finished(Log()), Log()(EARLIER, E, U, S, NEVER))

    def test_b15_n3_unwritable_record(self):
        first = finished(Log()(WAITING, E)(WAITING, E))(FINAL, E, U, S)
        again = Log()(AGAIN, E, U, S)
        self.assertVerdict('PASS', 'b15-n3', first, again)
        early = finished(Log()(WAITING, E))(WAITING, E)(FINAL, E, U, S)
        self.assertVerdict('FAIL', 'b15-n3', early, again)             # a Pendant while unwritable
        twice = finished(finished(Log()(WAITING, E)))(FINAL, E, U, S)
        self.assertVerdict('FAIL', 'b15-n3', twice, again)             # two Pendants
        self.assertVerdict('FAIL', 'b15-n3', first, finished(Log()))   # a second lot after the restart
        self.assertVerdict('PASS', 'b15-n3', first, again, Log()(AGAIN, E, U, S))
        self.assertVerdict('FAIL', 'b15-n3', first, finished(Log()), again)   # a duplicate in a middle process
        self.assertVerdict('FAIL', 'b15-n3', first, Log()(ADDED, GOODS, 1, True, 0, True, 0), again)

    def test_b15_n4_is_left_to_a_person(self):
        self.assertVerdict('MANUAL', 'b15-n4', finished(Log())(FINAL, E, U, S, after=26))

    def test_b17_n1_locked_map_return(self):
        good = point(recovered(Log()))(SETTLED, after=3)
        self.assertVerdict('MANUAL', 'b17-n1', Log(), good)  # the position is a person's check
        same_ms = point(Log()(LEFT, U, S)(BACK, U, S, MAP, 'where it joined', after=0))(SETTLED, after=3)
        self.assertVerdict('MANUAL', 'b17-n1', same_ms)    # consecutive lines in one millisecond keep their order
        self.assertVerdict('MANUAL', 'b17-n1', point(recovered(Log(start=24 * 3600 - 1)))(SETTLED, after=3))
        self.assertVerdict('INCOMPLETE', 'b17-n1', point(recovered(Log())))
        self.assertVerdict('FAIL', 'b17-n1', point(recovered(Log()))(GAVE_UP))
        with tempfile.TemporaryDirectory() as user_dir:
            (Path(user_dir) / 'own-world').mkdir()
            journal = Path(user_dir) / 'own-world' / f'own-{U}-{S}.bin'
            journal.touch()
            self.assertVerdict('FAIL', 'b17-n1', good, user_dir=user_dir)
            journal.rename(journal.with_name(journal.name + '.restored'))
            self.assertVerdict('MANUAL', 'b17-n1', good, user_dir=user_dir)

    def test_b17_n2_title_and_other_character(self):
        def start():
            return point(recovered(Log()))(TITLE)(CANCELED, U, S)
        self.assertVerdict('MANUAL', 'b17-n2', point(recovered(start()))(SETTLED))
        self.assertVerdict('INCOMPLETE', 'b17-n2', start())  # the owner not loaded again yet
        self.assertVerdict('FAIL', 'b17-n2', point(start(), 2))  # the other character was warped
        self.assertVerdict('FAIL', 'b17-n2', start()(SETTLED))   # or settled

    def test_b17_n3_lamp_fallback(self):
        good = point(recovered(Log()))(FAILED, 'arrived elsewhere', 'point', 1, 3)
        good(REQUESTED, 'recorded lamp', 0x18000000, LAMP, True, 1)(SETTLED)
        self.assertVerdict('MANUAL', 'b17-n3', good)
        self.assertVerdict('INCOMPLETE', 'b17-n3', point(recovered(Log()))(SETTLED))  # the point did not fail

    def test_every_message_is_in_the_source(self):
        for fragment in (QUEUED, ADDED, FINISHED, FINAL, EARLIER, AGAIN, WAITING, LEFT, BACK, REQUESTED,
                         SETTLED, GAVE_UP, TITLE, CANCELED, FAILED):
            say(fragment, *range(9))


if __name__ == '__main__':
    unittest.main()
