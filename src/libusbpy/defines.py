from enum import Enum, unique

import libusb


@unique
class LibusbOption(Enum):
    LOG_LEVEL = libusb.LIBUSB_OPTION_LOG_LEVEL
    USE_USBDK = libusb.LIBUSB_OPTION_USE_USBDK
    WEAK_AUTHORITY = libusb.LIBUSB_OPTION_WEAK_AUTHORITY


@unique
class LibusbLogLevel(Enum):
    NONE = libusb.LIBUSB_LOG_LEVEL_NONE
    # Error messages are emitted
    ERROR = libusb.LIBUSB_LOG_LEVEL_ERROR
    # Warning and error messages are emitted
    WARNING = libusb.LIBUSB_LOG_LEVEL_WARNING
    # Informational, warning and error messages are emitted
    INFO = libusb.LIBUSB_LOG_LEVEL_INFO
    # All messages are emitted
    DEBUG = libusb.LIBUSB_LOG_LEVEL_DEBUG


@unique
class LibusbDeviceSpeed(Enum):
    # The OS doesn't report or know the device speed.
    UNKNOWN = libusb.LIBUSB_SPEED_UNKNOWN
    # The device is operating at low speed (1.5MBit/s).
    LOW = libusb.LIBUSB_SPEED_LOW
    # The device is operating at full speed (12MBit/s).
    FULL = libusb.LIBUSB_SPEED_FULL
    # The device is operating at high speed (480MBit/s).
    HIGH = libusb.LIBUSB_SPEED_HIGH
    # The device is operating at super speed (5000MBit/s).
    SUPER = libusb.LIBUSB_SPEED_SUPER
    # The device is operating at super speed plus (10000MBit/s).
    SUPER_PLUS = libusb.LIBUSB_SPEED_SUPER_PLUS
