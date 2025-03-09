from gsz.format import Formatter, GenderOrder, Syntax


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


def test_simple_tag():
    formatter = Formatter(syntax=Syntax.MediaWiki)
    assert formatter.format("<i>斜体</i>") == "''斜体''"
    assert formatter.format("<b>粗体</b>") == "'''粗体'''"
    assert formatter.format("<u>下划线</u>") == "<u>下划线</u>"
    assert formatter.format("<unbreak>不折行</unbreak>") == "不折行"
    assert formatter.format("<color=#abcdef>文本颜色</color>") == "{{颜色|abcdef|文本颜色}}"
    assert formatter.format("<size=+4px>字号</size>") == '<span style="font-size: 1.2em">字号</size>'
    assert formatter.format('<align="right">右对齐</align>') == '<p style="text-align: right">右对齐</p>'

    assert formatter.format("<color=#f29e3800>特殊颜色</color>") == "{{颜色|描述2|特殊颜色}}"


def test_plain_syntax():
    formatter = Formatter()
    assert formatter.format("<b>粗体<i>加粗斜体</i>粗体</b>") == "粗体加粗斜体粗体"


def test_nested_tags():
    formatter = Formatter(syntax=Syntax.MediaWiki)
    assert formatter.format("<b>粗体<i>加粗斜体</i>粗体</b>") == "'''粗体''加粗斜体''粗体'''"
    assert formatter.format("<b>粗体<i>加粗斜体</i>粗体</b>#") == "'''粗体''加粗斜体''粗体'''#"
    assert formatter.format("<color=#abcdef>彩色<i>斜体</i></color>") == "{{颜色|abcdef|彩色''斜体''}}"
    assert (  # 测试连续 tag 第二个 tag 是否缺第一个字符
        formatter.format("天依<b><color=#66ccff>蓝</color></b>\\n阿绫<b><color=#ee0000>红</color></b>")
        == """天依'''{{颜色|66ccff|蓝}}'''<br />阿绫'''{{颜色|ee0000|红}}'''"""
    )


def test_invalid_tag():
    formatter = Formatter(syntax=Syntax.MediaWiki)
    assert formatter.format("<>") == "&lt;&gt;"
    assert formatter.format("<=>") == "&lt;=&gt;"
    assert formatter.format("<(￣︶￣)>") == "&lt;(￣︶￣)&gt;"
    assert formatter.format("<Grand\u00a0Melodie\u00a0黄金的时刻>") == "&lt;Grand&nbsp;Melodie&nbsp;黄金的时刻&gt;"
    assert formatter.format("</b>") == "&lt;/b&gt;"
    assert formatter.format("<i>斜体</b>这是什么</i>") == "''斜体&lt;/b&gt;这是什么''"


def test_unclosed_tag():
    formatter = Formatter(syntax=Syntax.MediaWiki)
    assert formatter.format("<i>斜体") == "''斜体''"
    assert formatter.format('<align="center">居中') == '<p style="text-align: center">居中</p>'


def test_pretty_print_mediawiki():
    formatter = Formatter(syntax=Syntax.MediaWikiPretty)
    assert (
        formatter.format('<i><align="center">这是内容</align></i>')
        == """''<p style="text-align: center">这是内容</p>''"""
    )
    assert (
        formatter.format('<i><align="center">这是内容</align></i>#')
        == """''<p style="text-align: center">这是内容</p>''\n#"""
    )
    assert (
        formatter.format('<align="center">第一段</align><align="center">第二段</align>')
        == """<p style="text-align: center">第一段</p>\n<p style="text-align: center">第二段</p>"""
    )


def test_simple_var():
    formatter = Formatter()
    assert formatter.format("{NICKNAME}") == "开拓者"
    formatter = Formatter(syntax=Syntax.MediaWiki)
    assert formatter.format("{RUBY_B#丰饶星神}「药师」{RUBY_E}") == "{{注音|「药师」|丰饶星神}}"


def test_var_male_female_order():
    formatter = Formatter()
    assert formatter.format("{F#她}{M#他}") == "她/他"
    assert formatter.format("{M#他}{F#她}") == "他/她"
    formatter = Formatter(gender_order=GenderOrder.Male)
    assert formatter.format("{F#她}{M#他}") == "他/她"
    assert formatter.format("{M#他}{F#她}") == "他/她"
    formatter = Formatter(gender_order=GenderOrder.Female)
    assert formatter.format("{F#她}{M#他}") == "她/他"
    assert formatter.format("{M#他}{F#她}") == "她/他"
