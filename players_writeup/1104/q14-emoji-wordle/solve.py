from __future__ import annotations

import re
import sys
import random
from dataclasses import dataclass, field
from typing import Sequence, Collection

import httpx


def guess_and_get_results(client, my_guess):
    response = client.get(f"https://prob14.geekgame.pku.edu.cn/{level}?guess={my_guess}")
    results_match = re.search(r'results\.push\("([^"]+)"\)', response.text)
    remaining_match = re.search(r"Number of guesses remaining: (\d+)", response.text)
    if results_match is None or remaining_match is None:
        print(response)
        print(response.text)
        print(f"{results_match = }, {remaining_match = }")
        sys.exit(1)
    return results_match.group(1), int(remaining_match.group(1))


def choose_undup(chosen, sequence):
    while True:
        choice = random.choice(sequence)
        if choice not in chosen or len(sequence) == 1:
            return choice
        sequence.remove(choice)


@dataclass
class WordleStatus:
    letter: str | None = None
    exclude: set[str] = field(default_factory=set)

    @property
    def solved(self) -> bool:
        return self.letter is not None

    def gen_a_guess(
        self,
        guess_list: list[str],
        candidates: Collection[str],
        all_emojis: Sequence[str],
    ) -> None:
        local_candidates = set(candidates) - self.exclude
        non_candidates = set(all_emojis) - set(candidates) - self.exclude
        if self.solved:
            if non_candidates:
                choice = choose_undup(guess_list, list(non_candidates))
            else:
                choice = self.letter
        else:
            if len(non_candidates) >= len(local_candidates):
                choice = choose_undup(guess_list, list(non_candidates))
            else:
                choice = choose_undup(guess_list, list(local_candidates))
        guess_list.append(choice)


def main() -> None:
    client = httpx.Client()
    client.get(f"https://prob14.geekgame.pku.edu.cn/?token={input('token: ')}")

    if level == "level2":
        client.get("https://prob14.geekgame.pku.edu.cn/level2")
        print(client.cookies["PLAY_SESSION"])

    all_emojis = list("🐐🐑🐒🐓🐔🐕🐖🐗🐘🐙🐚🐛🐜🐝🐞🐟🐠🐡🐢🐣🐤🐥🐦🐧🐨🐩🐪🐫🐬🐭🐮🐯🐰🐱🐲🐳🐴🐵🐶🐷🐸🐹🐺🐻🐼🐽🐾🐿👀👁👂👃👄👅👆👇👈👉👊👋👌👍👎👏👐👑👒👓👔👕👖👗👘👙👚👛👜👝👞👟👠👡👢👣👤👥👦👧👨👩👪👫👬👭👮👯👰👱👲👳👴👵👶👷👸👹👺👻👼👽👾👿💀💁💂💃💄💅💆💇💈💉💊💋💌💍💎💏")
    candidates: set[str] = set()
    wordle_status_list = [WordleStatus() for _ in range(64)]

    while True:
        print(f"{len(candidates) = }, {len(all_emojis) = }")

        guess_list: list[str] = []
        for status in wordle_status_list:
            status.gen_a_guess(guess_list, candidates, all_emojis)
        guess = "".join(guess_list)
        # print(f"next guess: \"{guess}\"")

        try:
            my_guess = input("my_guess: ")
        except EOFError:
            break
        if not my_guess:
            my_guess = guess

        print(f'guess:  "{my_guess}"')
        try:
            results, remaining = guess_and_get_results(client, my_guess)
        except BaseException:
            for status in wordle_status_list:
                print(status)
            print(my_guess)
            raise
        print(f"results: {results}")
        print(f"Number of guesses remaining: {remaining}")

        assert len(results) == len(wordle_status_list) == len(guess_list) == 64
        for result, status, guess_char in zip(results, wordle_status_list, my_guess):
            if result == "🟩":
                status.letter = guess_char
            elif result == "🟨":
                status.exclude.add(guess_char)
                candidates.add(guess_char)
            elif result == "🟥":
                try:
                    all_emojis.remove(guess_char)
                except ValueError:
                    pass
            else:
                raise ValueError(f"result can't be {result!r}")

if __name__ == "__main__":
    level = sys.argv[1]
    assert level in ("level1", "level2")
    main()
