from .base import Model


class OptionDynamic(Model):
    display_id: int


class Option(Model):
    option_id: int
    display_id: int
    special_option_id: int | None = None
    """带图标的选项，比如阮梅特殊选项、寰宇蝗灾中的命途选项凡此种种"""
    dynamic_map: dict[int, OptionDynamic] | None = None
    desc_value: int | None = None
    desc_value2: int | None = None
    desc_value3: int | None = None
    desc_value4: int | None = None


class Opt(Model):
    option_list: list[Option]
