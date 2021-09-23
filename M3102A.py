from .SD_common.SD_DIG import SD_DIG


class M3102A(SD_DIG):
    """Driver for the digitizer of the Keysight M3102A card.

    Args:
        name (str)    : name for this instrument, passed to the base instrument
        chassis (int) : chassis number where the device is located
        slot (int)    : slot number where the device is plugged in

    Example:
        digitizier  = M3102A('digitizer')
    """
    def __init__(self, name, chassis=1, slot=8, **kwargs):
        super().__init__(
            name, chassis, slot, channels=4, triggers=8,
            min_sampling_interval=2,
            half_ranges_hz=[0.1, 0.2, 0.4, 1, 2, 4, 8],
            half_ranges_50=[0.0625, 0.125, 0.25, 0.5, 1, 2, 4],
            **kwargs
        )
