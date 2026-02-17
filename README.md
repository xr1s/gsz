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

## Achievement Tool usage

This script prints achievements from game data.

```bash
python3 achievement.py --base ../TurnBasedGameData --e-hkrpg-token @secret-file.txt
```

### Print achievements in a specific series

For example, to list achievements under the series “众秘探奇”:

```bash
python3 achievement.py --base ../TurnBasedGameData --e-hkrpg-token @secret-file.txt --series 众秘探奇
```

### Obtaining the token

The `e_hkrpg_token` is required for authentication. You can retrieve it from the [Mihoyo Cultivation Tool](https://act.mihoyo.com/sr/event/cultivation-tool/index.html) by inspecting the cookies in your browser.

### Passing the token

You can provide the token in two ways:

Directly as a command-line argument:

```bash
python3 achievement.py --base ../TurnBasedGameData --e-hkrpg-token YOUR_TOKEN
```

Via a file (recommended for security): save the token in a file and reference it with @:

```bash
python3 achievement.py --base ../TurnBasedGameData --e-hkrpg-token @path/to/token-file
```

Using a file prevents the token from being exposed in your shell history.
