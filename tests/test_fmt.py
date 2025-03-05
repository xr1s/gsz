from gsz.format import Formatter


def test_format_simple():
    formatter = Formatter()
    assert formatter.format("世界第#1美少女", 1) == "世界第1美少女"
    assert formatter.format("造成#1[i]%基础伤害", 18) == "造成1800%基础伤害"
    assert formatter.format("所有角色失去#2[f1]%生命值", 0, 0.3) == "所有角色失去30.0%生命值"


def test_format_incomplete():
    formatter = Formatter()
    assert formatter.format("#", 0, 42) == "#"
    assert formatter.format("#$", 0, 42) == "#$"
    assert formatter.format("#2", 0, 42) == "42"
    assert formatter.format("#2$", 0, 42) == "42$"
    assert formatter.format("#2[", 0, 42) == "42["
    assert formatter.format("#2[$", 0, 42) == "42[$"
    assert formatter.format("#2[f", 0, 42) == "42[f"
    assert formatter.format("#2[f1", 0, 42) == "42[f1"
    assert formatter.format("#2[f1$", 0, 42) == "42[f1$"
    assert formatter.format("#2[f1]", 0, 42) == "42.0"
    assert formatter.format("#2[f1]$", 0, 42) == "42.0$"
    assert formatter.format("#2[f1]%", 0, 42) == "4200.0%"
    assert formatter.format("#2[f1]%$", 0, 42) == "4200.0%$"


def test_format_param_num():
    formatter = Formatter()
    assert formatter.format("尊贵的#100号客人", 0, 1, 2) == "尊贵的#100号客人"
    assert formatter.format("启动#0号预案") == "启动#0号预案"
    assert formatter.format("#100[i") == "#100[i"


def test_format_invalid_specifier():
    formatter = Formatter()
    assert formatter.format("#1[f]%", 0.3) == "0.3[f]%"
    assert formatter.format("#1[g]", 0.3) == "0.3[g]"
