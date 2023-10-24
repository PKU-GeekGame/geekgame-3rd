from __future__ import annotations

import re
import sys
import random
from dataclasses import dataclass, field
from typing import Sequence, Collection

import emoji
import httpx


def get_emojis(client: httpx.Client) -> str:
    response = client.get("https://prob14.geekgame.pku.edu.cn/level2")
    match = re.search(r'placeholder="([^"]+)"', response.text)
    if match is None:
        print(response)
        print(response.text)
        sys.exit(1)
    return match.group(1)


def main() -> None:
    client = httpx.Client()
    client.get(f"https://prob14.geekgame.pku.edu.cn/?token={input('token: ')}")

    emojis: set[str] = set()
    same_count = 0
    while True:
        try:
            input(">>> ")
        except EOFError:
            break
        length_before = len(emojis)
        emojis.update(get_emojis(client))
        length_after = len(emojis)

        print(f"{len(emojis):3}", "".join(sorted(emojis)))

        if length_before == length_after:
            same_count += 1
        else:
            same_count = 0
        if same_count >= 10:
            break

main()
# 128 🐐🐑🐒🐓🐔🐕🐖🐗🐘🐙🐚🐛🐜🐝🐞🐟🐠🐡🐢🐣🐤🐥🐦🐧🐨🐩🐪🐫🐬🐭🐮🐯🐰🐱🐲🐳🐴🐵🐶🐷🐸🐹🐺🐻🐼🐽🐾🐿👀👁👂👃👄👅👆👇👈👉👊👋👌👍👎👏👐👑👒👓👔👕👖👗👘👙👚👛👜👝👞👟👠👡👢👣👤👥👦👧👨👩👪👫👬👭👮👯👰👱👲👳👴👵👶👷👸👹👺👻👼👽👾👿💀💁💂💃💄💅💆💇💈💉💊💋💌💍💎💏
