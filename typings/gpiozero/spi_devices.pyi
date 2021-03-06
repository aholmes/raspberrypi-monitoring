"""
This type stub file was generated by pyright.
"""

from .devices import Device

str = ...
class SPIDevice(Device):
    """
    Extends :class:`Device`. Represents a device that communicates via the SPI
    protocol.

    See :ref:`spi_args` for information on the keyword arguments that can be
    specified with the constructor.
    """
    def __init__(self, **spi_args) -> None:
        ...
    
    def close(self): # -> None:
        ...
    
    @property
    def closed(self): # -> bool:
        ...
    
    def __repr__(self): # -> str:
        ...
    


class AnalogInputDevice(SPIDevice):
    """
    Represents an analog input device connected to SPI (serial interface).

    Typical analog input devices are `analog to digital converters`_ (ADCs).
    Several classes are provided for specific ADC chips, including
    :class:`MCP3004`, :class:`MCP3008`, :class:`MCP3204`, and :class:`MCP3208`.

    The following code demonstrates reading the first channel of an MCP3008
    chip attached to the Pi's SPI pins::

        from gpiozero import MCP3008

        pot = MCP3008(0)
        print(pot.value)

    The :attr:`value` attribute is normalized such that its value is always
    between 0.0 and 1.0 (or in special cases, such as differential sampling,
    -1 to +1). Hence, you can use an analog input to control the brightness of
    a :class:`PWMLED` like so::

        from gpiozero import MCP3008, PWMLED

        pot = MCP3008(0)
        led = PWMLED(17)
        led.source = pot

    The :attr:`voltage` attribute reports values between 0.0 and *max_voltage*
    (which defaults to 3.3, the logic level of the GPIO pins).

    .. _analog to digital converters: https://en.wikipedia.org/wiki/Analog-to-digital_converter
    """
    def __init__(self, bits, max_voltage=..., **spi_args) -> None:
        ...
    
    @property
    def bits(self):
        """
        The bit-resolution of the device/channel.
        """
        ...
    
    @property
    def value(self):
        """
        The current value read from the device, scaled to a value between 0 and
        1 (or -1 to +1 for certain devices operating in differential mode).
        """
        ...
    
    @property
    def raw_value(self):
        """
        The raw value as read from the device.
        """
        ...
    
    @property
    def max_voltage(self): # -> float:
        """
        The voltage required to set the device's value to 1.
        """
        ...
    
    @property
    def voltage(self):
        """
        The current voltage read from the device. This will be a value between
        0 and the *max_voltage* parameter specified in the constructor.
        """
        ...
    


class MCP3xxx(AnalogInputDevice):
    """
    Extends :class:`AnalogInputDevice` to implement an interface for all ADC
    chips with a protocol similar to the Microchip MCP3xxx series of devices.
    """
    def __init__(self, channel=..., bits=..., differential=..., max_voltage=..., **spi_args) -> None:
        ...
    
    @property
    def channel(self): # -> Unknown:
        """
        The channel to read data from. The MCP3008/3208/3304 have 8 channels
        (0-7), while the MCP3004/3204/3302 have 4 channels (0-3), the
        MCP3002/3202 have 2 channels (0-1), and the MCP3001/3201/3301 only
        have 1 channel.
        """
        ...
    
    @property
    def differential(self): # -> bool:
        """
        If ``True``, the device is operated in differential mode. In this mode
        one channel (specified by the channel attribute) is read relative to
        the value of a second channel (implied by the chip's design).

        Please refer to the device data-sheet to determine which channel is
        used as the relative base value (for example, when using an
        :class:`MCP3008` in differential mode, channel 0 is read relative to
        channel 1).
        """
        ...
    


class MCP3xx2(MCP3xxx):
    ...


class MCP30xx(MCP3xxx):
    """
    Extends :class:`MCP3xxx` to implement an interface for all ADC
    chips with a protocol similar to the Microchip MCP30xx series of devices.
    """
    def __init__(self, channel=..., differential=..., max_voltage=..., **spi_args) -> None:
        ...
    


class MCP32xx(MCP3xxx):
    """
    Extends :class:`MCP3xxx` to implement an interface for all ADC
    chips with a protocol similar to the Microchip MCP32xx series of devices.
    """
    def __init__(self, channel=..., differential=..., max_voltage=..., **spi_args) -> None:
        ...
    


class MCP33xx(MCP3xxx):
    """
    Extends :class:`MCP3xxx` with functionality specific to the MCP33xx family
    of ADCs; specifically this handles the full differential capability of
    these chips supporting the full 13-bit signed range of output values.
    """
    def __init__(self, channel=..., differential=..., max_voltage=..., **spi_args) -> None:
        ...
    
    @property
    def differential(self): # -> bool:
        """
        If ``True``, the device is operated in differential mode. In this mode
        one channel (specified by the channel attribute) is read relative to
        the value of a second channel (implied by the chip's design).

        Please refer to the device data-sheet to determine which channel is
        used as the relative base value (for example, when using an
        :class:`MCP3304` in differential mode, channel 0 is read relative to
        channel 1).
        """
        ...
    
    @property
    def value(self):
        """
        The current value read from the device, scaled to a value between 0 and
        1 (or -1 to +1 for devices operating in differential mode).
        """
        ...
    


class MCP3001(MCP30xx):
    """
    The `MCP3001`_ is a 10-bit analog to digital converter with 1 channel.
    Please note that the MCP3001 always operates in differential mode,
    measuring the value of IN+ relative to IN-.

    .. _MCP3001: http://www.farnell.com/datasheets/630400.pdf
    """
    def __init__(self, max_voltage=..., **spi_args) -> None:
        ...
    


class MCP3002(MCP30xx, MCP3xx2):
    """
    The `MCP3002`_ is a 10-bit analog to digital converter with 2 channels
    (0-1).

    .. _MCP3002: http://www.farnell.com/datasheets/1599363.pdf
    """
    def __init__(self, channel=..., differential=..., max_voltage=..., **spi_args) -> None:
        ...
    


class MCP3004(MCP30xx):
    """
    The `MCP3004`_ is a 10-bit analog to digital converter with 4 channels
    (0-3).

    .. _MCP3004: http://www.farnell.com/datasheets/808965.pdf
    """
    def __init__(self, channel=..., differential=..., max_voltage=..., **spi_args) -> None:
        ...
    


class MCP3008(MCP30xx):
    """
    The `MCP3008`_ is a 10-bit analog to digital converter with 8 channels
    (0-7).

    .. _MCP3008: http://www.farnell.com/datasheets/808965.pdf
    """
    def __init__(self, channel=..., differential=..., max_voltage=..., **spi_args) -> None:
        ...
    


class MCP3201(MCP32xx):
    """
    The `MCP3201`_ is a 12-bit analog to digital converter with 1 channel.
    Please note that the MCP3201 always operates in differential mode,
    measuring the value of IN+ relative to IN-.

    .. _MCP3201: http://www.farnell.com/datasheets/1669366.pdf
    """
    def __init__(self, max_voltage=..., **spi_args) -> None:
        ...
    


class MCP3202(MCP32xx, MCP3xx2):
    """
    The `MCP3202`_ is a 12-bit analog to digital converter with 2 channels
    (0-1).

    .. _MCP3202: http://www.farnell.com/datasheets/1669376.pdf
    """
    def __init__(self, channel=..., differential=..., max_voltage=..., **spi_args) -> None:
        ...
    


class MCP3204(MCP32xx):
    """
    The `MCP3204`_ is a 12-bit analog to digital converter with 4 channels
    (0-3).

    .. _MCP3204: http://www.farnell.com/datasheets/808967.pdf
    """
    def __init__(self, channel=..., differential=..., max_voltage=..., **spi_args) -> None:
        ...
    


class MCP3208(MCP32xx):
    """
    The `MCP3208`_ is a 12-bit analog to digital converter with 8 channels
    (0-7).

    .. _MCP3208: http://www.farnell.com/datasheets/808967.pdf
    """
    def __init__(self, channel=..., differential=..., max_voltage=..., **spi_args) -> None:
        ...
    


class MCP3301(MCP33xx):
    """
    The `MCP3301`_ is a signed 13-bit analog to digital converter.  Please note
    that the MCP3301 always operates in differential mode measuring the
    difference between IN+ and IN-. Its output value is scaled from -1 to +1.

    .. _MCP3301: http://www.farnell.com/datasheets/1669397.pdf
    """
    def __init__(self, max_voltage=..., **spi_args) -> None:
        ...
    


class MCP3302(MCP33xx):
    """
    The `MCP3302`_ is a 12/13-bit analog to digital converter with 4 channels
    (0-3). When operated in differential mode, the device outputs a signed
    13-bit value which is scaled from -1 to +1. When operated in single-ended
    mode (the default), the device outputs an unsigned 12-bit value scaled from
    0 to 1.

    .. _MCP3302: http://www.farnell.com/datasheets/1486116.pdf
    """
    def __init__(self, channel=..., differential=..., max_voltage=..., **spi_args) -> None:
        ...
    


class MCP3304(MCP33xx):
    """
    The `MCP3304`_ is a 12/13-bit analog to digital converter with 8 channels
    (0-7). When operated in differential mode, the device outputs a signed
    13-bit value which is scaled from -1 to +1. When operated in single-ended
    mode (the default), the device outputs an unsigned 12-bit value scaled from
    0 to 1.

    .. _MCP3304: http://www.farnell.com/datasheets/1486116.pdf
    """
    def __init__(self, channel=..., differential=..., max_voltage=..., **spi_args) -> None:
        ...
    


