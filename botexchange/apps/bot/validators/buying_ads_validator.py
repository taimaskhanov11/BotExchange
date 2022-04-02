from loguru import logger

from botexchange.apps.bot.validators.common_validators import thematic_validator, platform_type_validator


class BuyingAdsValidator:
    @classmethod
    def platform_type(self, text: str) -> bool:
        return platform_type_validator(text)

    @classmethod
    def thematic(cls, text: str) -> bool:
        return thematic_validator(text)

    @classmethod
    def audience_size(cls, text: str) -> bool | tuple[int, int] | int:
        try:
            if text == "any":
                return 0
            pr = map(lambda x: x.strip(), text.split("-"))
            pr = tuple(map(int, pr))
            logger.trace(pr)
            if len(pr) == 2:
                _min, _max = pr
                if _min > _max:
                    logger.trace(f"min {_min, _max} ")
                    return False
                logger.trace(f"return {_min, _max}")
                return _min, _max
            _max = pr[0]
            logger.trace(f"return {_max}")
            return _max
        except Exception as e:
            logger.warning(e)
            return False
        finally:
            logger.info(text)
