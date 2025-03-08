import functools

from .. import excel
from .base import View


class ExtraEffectConfig(View[excel.ExtraEffectConfig]):
    """精英组别，属性加成"""

    type ExcelOutput = excel.ExtraEffectConfig

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.extra_effect_name)
