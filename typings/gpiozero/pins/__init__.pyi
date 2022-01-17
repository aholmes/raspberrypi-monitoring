"""
This type stub file was generated by pyright.
"""

from __future__ import absolute_import, division, print_function, unicode_literals
from weakref import ref
from collections import defaultdict
from threading import Lock
from ..exc import GPIOPinInUse, PinEdgeDetectUnsupported, PinFixedPull, PinInvalidFunction, PinPWMUnsupported, PinSPIUnsupported, PinSetInput, PinUnsupported, SPIFixedBitOrder, SPIFixedClockMode, SPIFixedSelect, SPIFixedWordSize

str = ...
class Factory:
    """
    Generates pins and SPI interfaces for devices. This is an abstract
    base class for pin factories. Descendents *must* override the following
    methods:

    * :meth:`ticks`
    * :meth:`ticks_diff`

    Descendents *may* override the following methods, if applicable:

    * :meth:`close`
    * :meth:`reserve_pins`
    * :meth:`release_pins`
    * :meth:`release_all`
    * :meth:`pin`
    * :meth:`spi`
    * :meth:`_get_pi_info`
    """
    def __init__(self) -> None:
        ...
    
    def reserve_pins(self, requester, *pins):
        """
        Called to indicate that the device reserves the right to use the
        specified *pins*. This should be done during device construction.  If
        pins are reserved, you must ensure that the reservation is released by
        eventually called :meth:`release_pins`.
        """
        ...
    
    def release_pins(self, reserver, *pins): # -> None:
        """
        Releases the reservation of *reserver* against *pins*.  This is
        typically called during :meth:`~gpiozero.Device.close` to clean up
        reservations taken during construction. Releasing a reservation that is
        not currently held will be silently ignored (to permit clean-up after
        failed / partial construction).
        """
        ...
    
    def release_all(self, reserver): # -> None:
        """
        Releases all pin reservations taken out by *reserver*. See
        :meth:`release_pins` for further information).
        """
        ...
    
    def close(self): # -> None:
        """
        Closes the pin factory. This is expected to clean up all resources
        manipulated by the factory. It it typically called at script
        termination.
        """
        ...
    
    def pin(self, spec): # -> NoReturn:
        """
        Creates an instance of a :class:`Pin` descendent representing the
        specified pin.

        .. warning::

            Descendents must ensure that pin instances representing the same
            hardware are identical; i.e. two separate invocations of
            :meth:`pin` for the same pin specification must return the same
            object.
        """
        ...
    
    def spi(self, **spi_args): # -> NoReturn:
        """
        Returns an instance of an :class:`SPI` interface, for the specified SPI
        *port* and *device*, or for the specified pins (*clock_pin*,
        *mosi_pin*, *miso_pin*, and *select_pin*).  Only one of the schemes can
        be used; attempting to mix *port* and *device* with pin numbers will
        raise :exc:`SPIBadArgs`.
        """
        ...
    
    def ticks(self):
        """
        Return the current ticks, according to the factory. The reference point
        is undefined and thus the result of this method is only meaningful when
        compared to another value returned by this method.

        The format of the time is also arbitrary, as is whether the time wraps
        after a certain duration. Ticks should only be compared using the
        :meth:`ticks_diff` method.
        """
        ...
    
    def ticks_diff(self, later, earlier):
        """
        Return the time in seconds between two :meth:`ticks` results. The
        arguments are specified in the same order as they would be in the
        formula *later* - *earlier* but the result is guaranteed to be in
        seconds, and to be positive even if the ticks "wrapped" between calls
        to :meth:`ticks`.
        """
        ...
    
    pi_info = ...


class Pin:
    """
    Abstract base class representing a pin attached to some form of controller,
    be it GPIO, SPI, ADC, etc.

    Descendents should override property getters and setters to accurately
    represent the capabilities of pins. Descendents *must* override the
    following methods:

    * :meth:`_get_function`
    * :meth:`_set_function`
    * :meth:`_get_state`

    Descendents *may* additionally override the following methods, if
    applicable:

    * :meth:`close`
    * :meth:`output_with_state`
    * :meth:`input_with_pull`
    * :meth:`_set_state`
    * :meth:`_get_frequency`
    * :meth:`_set_frequency`
    * :meth:`_get_pull`
    * :meth:`_set_pull`
    * :meth:`_get_bounce`
    * :meth:`_set_bounce`
    * :meth:`_get_edges`
    * :meth:`_set_edges`
    * :meth:`_get_when_changed`
    * :meth:`_set_when_changed`
    """
    def __repr__(self): # -> Literal['<Pin>']:
        ...
    
    def close(self): # -> None:
        """
        Cleans up the resources allocated to the pin. After this method is
        called, this :class:`Pin` instance may no longer be used to query or
        control the pin's state.
        """
        ...
    
    def output_with_state(self, state): # -> None:
        """
        Sets the pin's function to "output" and specifies an initial state
        for the pin. By default this is equivalent to performing::

            pin.function = 'output'
            pin.state = state

        However, descendents may override this in order to provide the smallest
        possible delay between configuring the pin for output and specifying an
        initial value (which can be important for avoiding "blips" in
        active-low configurations).
        """
        ...
    
    def input_with_pull(self, pull): # -> None:
        """
        Sets the pin's function to "input" and specifies an initial pull-up
        for the pin. By default this is equivalent to performing::

            pin.function = 'input'
            pin.pull = pull

        However, descendents may override this order to provide the smallest
        possible delay between configuring the pin for input and pulling the
        pin up/down (which can be important for avoiding "blips" in some
        configurations).
        """
        ...
    
    function = ...
    state = ...
    pull = ...
    frequency = ...
    bounce = ...
    edges = ...
    when_changed = ...


class SPI:
    """
    Abstract interface for `Serial Peripheral Interface`_ (SPI)
    implementations. Descendents *must* override the following methods:

    * :meth:`transfer`
    * :meth:`_get_clock_mode`

    Descendents *may* override the following methods, if applicable:

    * :meth:`read`
    * :meth:`write`
    * :meth:`_set_clock_mode`
    * :meth:`_get_lsb_first`
    * :meth:`_set_lsb_first`
    * :meth:`_get_select_high`
    * :meth:`_set_select_high`
    * :meth:`_get_bits_per_word`
    * :meth:`_set_bits_per_word`

    .. _Serial Peripheral Interface: https://en.wikipedia.org/wiki/Serial_Peripheral_Interface_Bus
    """
    def read(self, n):
        """
        Read *n* words of data from the SPI interface, returning them as a
        sequence of unsigned ints, each no larger than the configured
        :attr:`bits_per_word` of the interface.

        This method is typically used with read-only devices that feature
        half-duplex communication. See :meth:`transfer` for full duplex
        communication.
        """
        ...
    
    def write(self, data): # -> int:
        """
        Write *data* to the SPI interface. *data* must be a sequence of
        unsigned integer words each of which will fit within the configured
        :attr:`bits_per_word` of the interface. The method returns the number
        of words written to the interface (which may be less than or equal to
        the length of *data*).

        This method is typically used with write-only devices that feature
        half-duplex communication. See :meth:`transfer` for full duplex
        communication.
        """
        ...
    
    def transfer(self, data):
        """
        Write *data* to the SPI interface. *data* must be a sequence of
        unsigned integer words each of which will fit within the configured
        :attr:`bits_per_word` of the interface. The method returns the sequence
        of words read from the interface while writing occurred (full duplex
        communication).

        The length of the sequence returned dictates the number of words of
        *data* written to the interface. Each word in the returned sequence
        will be an unsigned integer no larger than the configured
        :attr:`bits_per_word` of the interface.
        """
        ...
    
    @property
    def clock_polarity(self): # -> bool:
        """
        The polarity of the SPI clock pin. If this is :data:`False` (the
        default), the clock pin will idle low, and pulse high. Setting this to
        :data:`True` will cause the clock pin to idle high, and pulse low. On
        many data sheets this is documented as the CPOL value.

        The following diagram illustrates the waveform when
        :attr:`clock_polarity` is :data:`False` (the default), equivalent to
        CPOL 0:

        .. code-block:: text

                   on      on      on      on      on      on      on
                  ,---.   ,---.   ,---.   ,---.   ,---.   ,---.   ,---.
            CLK   |   |   |   |   |   |   |   |   |   |   |   |   |   |
                  |   |   |   |   |   |   |   |   |   |   |   |   |   |
            ------'   `---'   `---'   `---'   `---'   `---'   `---'   `------
            idle       off     off     off     off     off     off       idle

        The following diagram illustrates the waveform when
        :attr:`clock_polarity` is :data:`True`, equivalent to CPOL 1:

        .. code-block:: text

            idle       off     off     off     off     off     off       idle
            ------.   ,---.   ,---.   ,---.   ,---.   ,---.   ,---.   ,------
                  |   |   |   |   |   |   |   |   |   |   |   |   |   |
            CLK   |   |   |   |   |   |   |   |   |   |   |   |   |   |
                  `---'   `---'   `---'   `---'   `---'   `---'   `---'
                   on      on      on      on      on      on      on
        """
        ...
    
    @clock_polarity.setter
    def clock_polarity(self, value): # -> None:
        ...
    
    @property
    def clock_phase(self): # -> bool:
        """
        The phase of the SPI clock pin. If this is :data:`False` (the default),
        data will be read from the MISO pin when the clock pin activates.
        Setting this to :data:`True` will cause data to be read from the MISO
        pin when the clock pin deactivates. On many data sheets this is
        documented as the CPHA value. Whether the clock edge is rising or
        falling when the clock is considered activated is controlled by the
        :attr:`clock_polarity` attribute (corresponding to CPOL).

        The following diagram indicates when data is read when
        :attr:`clock_polarity` is :data:`False`, and :attr:`clock_phase` is
        :data:`False` (the default), equivalent to CPHA 0:

        .. code-block:: text

                ,---.   ,---.   ,---.   ,---.   ,---.   ,---.   ,---.
            CLK |   |   |   |   |   |   |   |   |   |   |   |   |   |
                |   |   |   |   |   |   |   |   |   |   |   |   |   |
            ----'   `---'   `---'   `---'   `---'   `---'   `---'   `-------
                :       :       :       :       :       :       :
            MISO---.   ,---.   ,---.   ,---.   ,---.   ,---.   ,---.
              /     \\ /     \\ /     \\ /     \\ /     \\ /     \\ /     \\
            -{  Bit  X  Bit  X  Bit  X  Bit  X  Bit  X  Bit  X  Bit  }------
              \\     / \\     / \\     / \\     / \\     / \\     / \\     /
               `---'   `---'   `---'   `---'   `---'   `---'   `---'

        The following diagram indicates when data is read when
        :attr:`clock_polarity` is :data:`False`, but :attr:`clock_phase` is
        :data:`True`, equivalent to CPHA 1:

        .. code-block:: text

                ,---.   ,---.   ,---.   ,---.   ,---.   ,---.   ,---.
            CLK |   |   |   |   |   |   |   |   |   |   |   |   |   |
                |   |   |   |   |   |   |   |   |   |   |   |   |   |
            ----'   `---'   `---'   `---'   `---'   `---'   `---'   `-------
                    :       :       :       :       :       :       :
            MISO   ,---.   ,---.   ,---.   ,---.   ,---.   ,---.   ,---.
                  /     \\ /     \\ /     \\ /     \\ /     \\ /     \\ /     \\
            -----{  Bit  X  Bit  X  Bit  X  Bit  X  Bit  X  Bit  X  Bit  }--
                  \\     / \\     / \\     / \\     / \\     / \\     / \\     /
                   `---'   `---'   `---'   `---'   `---'   `---'   `---'
        """
        ...
    
    @clock_phase.setter
    def clock_phase(self, value): # -> None:
        ...
    
    clock_mode = ...
    lsb_first = ...
    select_high = ...
    bits_per_word = ...


