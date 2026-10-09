"""Tests for the executable DRAW Skill's timestamp-first scheme B."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "skills/draw/scripts/tarot_shuffle.py"
sys.path.insert(0, str(SCRIPT.parent))
from tarot_shuffle import CARDS, init_state, reveal, validate_state


class TarotShuffleTests(unittest.TestCase):
    TS = 1791512400000

    def test_78_unique_pre_shuffled(self):
        state = init_state(self.TS)
        self.assertEqual(sorted(state["deck_ids"]), list(range(1, 79)))
        self.assertEqual(len(CARDS), len(set(CARDS)))
        self.assertEqual(len(state["orientation_by_position"]), 78)
        self.assertNotEqual(state["deck_ids"], list(range(1, 79)))

    def test_stable_results_same_timestamp(self):
        self.assertEqual(init_state(self.TS), init_state(self.TS))
        self.assertNotEqual(init_state(self.TS)["deck_ids"], init_state(self.TS+1)["deck_ids"])

    def test_five_numbers_are_positions_not_seed(self):
        state = init_state(self.TS)
        updated, cards = reveal(state, [48, 31, 44, 35, 34])
        self.assertEqual([card["card_id"] for card in cards], [20, 35, 9, 3, 14])
        self.assertEqual(len(set(card["card_id"] for card in cards)), 5)
        self.assertEqual(updated["commitment"], state["commitment"])
        self.assertEqual(state["used_positions"], [])
        _, alternate = reveal(state, [48, 31, 44, 35, 36])
        self.assertEqual(alternate[:4], cards[:4])

    def test_no_replacement_even_after_follow_up(self):
        state = init_state(self.TS)
        first, cards1 = reveal(state, list(range(1, 41)))
        second, cards2 = reveal(first, list(range(41, 79)))
        self.assertEqual(len(set(x["card_id"] for x in cards1+cards2)), 78)
        self.assertEqual(len(second["used_positions"]), 78)
        with self.assertRaises(ValueError):
            reveal(second, [48])

    def test_bad_input_and_tampering_rejected(self):
        state = init_state(self.TS)
        for nums in ([48, 48], [0], [79], [True], [], [48.0]):
            with self.assertRaises(ValueError):
                reveal(state, nums)
        for edit in (lambda x: x["deck_ids"].reverse(),
                     lambda x: x.__setitem__("commitment", "x"),
                     lambda x: x.__setitem__("used_positions", [4, 4])):
            other = copy.deepcopy(state)
            edit(other)
            with self.assertRaises(ValueError):
                validate_state(other)

    def test_cli_lock_before_reveal_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as p:
            state_path = Path(p)/"round.json"

            def cmd(*args):
                return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                                      capture_output=True, text=True)

            prep = cmd("prepare", "--state", state_path, "--timestamp-ms", self.TS)
            self.assertEqual(prep.returncode, 0, prep.stderr)
            self.assertNotIn("deck_ids", prep.stdout)
            self.assertNotEqual(cmd("prepare", "--state", state_path).returncode, 0)
            before = state_path.read_bytes()
            bad = cmd("reveal", "--state", state_path, "--numbers", 48, 31, "--count", 5)
            self.assertNotEqual(bad.returncode, 0)
            self.assertEqual(before, state_path.read_bytes())
            good = cmd("reveal", "--state", state_path, "--numbers",
                       48, 31, 44, 35, 34, "--count", 5)
            self.assertEqual(good.returncode, 0, good.stderr)
            self.assertEqual(json.loads(good.stdout)["cards"][0]["card"], "太阳")
            self.assertEqual(json.loads(cmd("verify", "--state", state_path).stdout)["status"], "valid")
            before = state_path.read_bytes()
            self.assertNotEqual(cmd("reveal", "--state", state_path,
                                    "--numbers", 48, "--count", 1).returncode, 0)
            self.assertEqual(before, state_path.read_bytes())


if __name__ == "__main__":
    unittest.main()
