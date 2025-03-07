# GSZ

Example Usage

```python
import argparse
import pathlib

import pydantic

from gsz.sr import GameData


@pydantic.dataclasses.dataclass
class Arguments:
    base: pathlib.Path


def parse_arguments():
    parser = argparse.ArgumentParser()
    _ = parser.add_argument("--base", type=pathlib.Path, required=True)
    namespace = parser.parse_args()
    return Arguments(base=namespace.base)


def main():
    arguments = parse_arguments()
    game = GameData(arguments.base)
    for monster in game.monster_config():
        print(monster.wiki_name)


if __name__ == "__main__":
    main()
```
