# GSZ

Choose one listed below as your package manager:

```bash
pip install 'git+https://github.com/xr1s/gsz'
```

```bash
uv add 'git+https://github.com/xr1s/gsz'
```

```bash
pdm add 'git+https://github.com/xr1s/gsz'
```

```bash
poetry add 'git+https://github.com/xr1s/gsz'
```

Example Usage


```python
import argparse
import dataclasses
import pathlib

from gsz import SRGameData


@dataclasses.dataclass
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
        print(monster.wiki())


if __name__ == "__main__":
    main()
```
