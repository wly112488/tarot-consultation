#!/usr/bin/env python3
"""Versioned, timestamp-seeded tarot deck: shuffle first, select positions later.

Standard-library only. Intended to be called by tarot-consultation's DRAW Skill.
A timestamp alone is reproducible and publicly guessable; not a secure entropy source.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import time

VERSION = "tarot-sha256-fy-v1"
CARDS = (
    "愚者", "魔术师", "女祭司", "皇后", "皇帝", "教皇", "恋人", "战车", "力量",
    "隐者", "命运之轮", "正义", "倒吊人", "死神", "节制", "恶魔", "高塔",
    "星星", "月亮", "太阳", "审判", "世界",
    "权杖王牌", "权杖二", "权杖三", "权杖四", "权杖五", "权杖六", "权杖七",
    "权杖八", "权杖九", "权杖十", "权杖侍从", "权杖骑士", "权杖皇后", "权杖国王",
    "圣杯王牌", "圣杯二", "圣杯三", "圣杯四", "圣杯五", "圣杯六", "圣杯七",
    "圣杯八", "圣杯九", "圣杯十", "圣杯侍从", "圣杯骑士", "圣杯皇后", "圣杯国王",
    "宝剑王牌", "宝剑二", "宝剑三", "宝剑四", "宝剑五", "宝剑六", "宝剑七",
    "宝剑八", "宝剑九", "宝剑十", "宝剑侍从", "宝剑骑士", "宝剑皇后", "宝剑国王",
    "星币王牌", "星币二", "星币三", "星币四", "星币五", "星币六", "星币七",
    "星币八", "星币九", "星币十", "星币侍从", "星币骑士", "星币皇后", "星币国王",
)
assert len(CARDS) == len(set(CARDS)) == 78


class Sha256Stream:
    """Domain-separated SHA256 counter stream with rejection sampling."""

    def __init__(self, timestamp_ms, domain):
        self.prefix = f"{VERSION}|{timestamp_ms}|{domain}|".encode("ascii")
        self.counter = 0

    def below(self, upper):
        if not isinstance(upper, int) or upper < 1:
            raise ValueError("upper must be a positive integer")
        limit = (1 << 256) - ((1 << 256) % upper)
        while True:
            digest = hashlib.sha256(self.prefix + self.counter.to_bytes(8, "big")).digest()
            self.counter += 1
            value = int.from_bytes(digest, "big")
            if value < limit:
                return value % upper


def _payload(state):
    fields = ("version", "timestamp_ms", "deck_ids", "orientation_by_position")
    return json.dumps({k: state[k] for k in fields}, sort_keys=True,
                      ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def init_state(timestamp_ms=None):
    if timestamp_ms is None:
        timestamp_ms = time.time_ns() // 1_000_000
    if type(timestamp_ms) is not int or timestamp_ms < 0:
        raise ValueError("timestamp_ms must be a nonnegative integer")
    deck = list(range(1, 79))
    shuffle_stream = Sha256Stream(timestamp_ms, "shuffle")
    for i in range(77, 0, -1):
        j = shuffle_stream.below(i + 1)
        deck[i], deck[j] = deck[j], deck[i]
    orientation_stream = Sha256Stream(timestamp_ms, "orientation")
    orientations = ["正位" if orientation_stream.below(2) == 0 else "逆位"
                    for _ in range(78)]
    state = {"version": VERSION, "timestamp_ms": timestamp_ms,
             "deck_ids": deck, "orientation_by_position": orientations,
             "used_positions": []}
    state["commitment"] = hashlib.sha256(_payload(state)).hexdigest()
    return state


def validate_state(state):
    if not isinstance(state, dict) or state.get("version") != VERSION:
        raise ValueError("unsupported or invalid state version")
    expected = init_state(state.get("timestamp_ms"))
    for key in ("deck_ids", "orientation_by_position", "commitment"):
        if state.get(key) != expected[key]:
            raise ValueError(f"state verification failed: {key}")
    used = state.get("used_positions")
    if (not isinstance(used, list) or
        any(type(x) is not int or x < 1 or x > 78 for x in used) or
        len(set(used)) != len(used)):
        raise ValueError("invalid used_positions")


def reveal(state, numbers):
    validate_state(state)
    if not isinstance(numbers, (list, tuple)) or not numbers:
        raise ValueError("at least one chosen position is required")
    if any(type(n) is not int or not 1 <= n <= 78 for n in numbers):
        raise ValueError("positions must be integers from 1 to 78")
    if len(set(numbers)) != len(numbers):
        raise ValueError("chosen positions cannot repeat")
    if set(numbers) & set(state["used_positions"]):
        raise ValueError("chosen position was already drawn in this round")
    cards = [{"position": n, "card_id": state["deck_ids"][n - 1],
              "card": CARDS[state["deck_ids"][n - 1] - 1],
              "orientation": state["orientation_by_position"][n - 1]}
             for n in numbers]
    next_state = {**state, "used_positions": state["used_positions"] + list(numbers)}
    return next_state, cards


def _read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path, state, replace=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(state, ensure_ascii=False, indent=2) + "\n"
    if not replace:
        with path.open("x", encoding="utf-8") as out:
            out.write(payload)
        return
    fd, temp = tempfile.mkstemp(prefix=".tarot-", suffix=".json", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as out:
            out.write(payload)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Deterministic tarot shuffling")
    commands = parser.add_subparsers(dest="command", required=True)
    setup = commands.add_parser("prepare", help="Shuffle and lock before asking numbers")
    setup.add_argument("--state", required=True, type=Path)
    setup.add_argument("--timestamp-ms", type=int, help="Replay/testing only; omit in normal readings")
    draw = commands.add_parser("reveal", help="Select positions from locked deck")
    draw.add_argument("--state", required=True, type=Path)
    draw.add_argument("--numbers", type=int, nargs="+", required=True)
    draw.add_argument("--count", type=int, help="Expected number of positions")
    verify = commands.add_parser("verify", help="Verify state matches its timestamp")
    verify.add_argument("--state", required=True, type=Path)
    args = parser.parse_args(argv)
    if args.command == "prepare":
        state = init_state(args.timestamp_ms)
        _write(args.state, state)
        result = {"status": "ready", "version": state["version"],
                  "timestamp_ms": state["timestamp_ms"], "commitment": state["commitment"]}
    elif args.command == "reveal":
        state = _read(args.state)
        if args.count is not None and (args.count < 1 or len(args.numbers) != args.count):
            raise ValueError("number count does not match locked spread")
        state, cards = reveal(state, args.numbers)
        _write(args.state, state, replace=True)
        result = {"status": "revealed", "cards": cards,
                  "commitment": state["commitment"],
                  "remaining": 78 - len(state["used_positions"])}
    else:
        state = _read(args.state)
        validate_state(state)
        result = {"status": "valid", "commitment": state["commitment"],
                  "used_positions": state["used_positions"]}
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, ensure_ascii=False),
              file=sys.stderr)
        raise SystemExit(2)
