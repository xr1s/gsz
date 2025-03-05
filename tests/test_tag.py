from gsz.format import Formatter, Syntax


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


def test_invalid_tag():
    formatter = Formatter(syntax=Syntax.MediaWiki)
    assert formatter.format("<>") == "&lt;&gt;"
    assert formatter.format("<=>") == "&lt;=&gt;"
    assert formatter.format("<(￣︶￣)>") == "&lt;(￣︶￣)&gt;"
    assert formatter.format("<Grand\u00a0Melodie\u00a0黄金的时刻>") == "&lt;Grand&nbsp;Melodie&nbsp;黄金的时刻&gt;"
    assert formatter.format("</b>") == "&lt;/b&gt;"
    assert formatter.format("<i>斜体</b>这是什么</i>") == "''斜体&lt;/b&gt;这是什么''"
