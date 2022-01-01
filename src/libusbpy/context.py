from __future__ import annotations
from deprecated import deprecated
import ctypes as ct

from .defines import *
from .exceptions import LibusbException
from .device import LibusbDeviceList


class LibusbContext:
    """
    A class representing a libusb session.
    The concept of individual libusb sessions allows for your program to use two libraries (or dynamically load two
    modules) which both independently use libusb.
    This will prevent interference between the individual libusb users - for example LibusbContext.set_option() will not
    affect the other user of the library, and LibusbContext.exit() will not destroy resources that the other user is
    still using.
    Sessions are created by LibusbContext.init() and destroyed through LibusbContext.exit(). If your application is
    guaranteed to only ever include a single libusb user (i.e. you), you do not have to worry about contexts: pass
    None(default) in the class constructor, the default context will be used.
    """
    def __init__(self, name: str | None = None) -> None:
        """
        LibusbContext object initializer.
        :param name: The context name
        """
        if name:
            self._name = name
            self._context = ct.POINTER(libusb.context)()
        else:
            self._name = "Default"
            self._context = None

    def __enter__(self) -> LibusbContext:
        """
        Enter the runtime context related to this object.
        :return: None
        """
        self.init()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit the runtime context related to this object.
        :param exc_type: Exception type.
        :param exc_val: Exception value.
        :param exc_tb: Exception traceback.
        :return: None
        """
        self.exit()

    @property
    def context(self) -> ct.POINTER(libusb.context) | None:
        """
        Returns the underlying libusb context.
        :return: The underlying libusb context.
        """
        return self._context

    def init(self) -> None:
        """
        Initialize libusb. This method must be called before calling any other libusb function.
        If the underlying libusb function fails, an exception will be thrown.
        :return: None
        """
        if self._context:
            ret = libusb.init(ct.byref(self._context))
        else:
            ret = libusb.init(None)

        if ret != libusb.LIBUSB_SUCCESS:
            raise LibusbException(ret)

    def exit(self) -> None:
        """
        Deinitialize libusb. Should be called after closing all open devices and before your application terminates.
        :return: None
        """
        libusb.exit(self._context)

    if libusb.LIBUSB_API_VERSION >= 0x01000106:
        @deprecated(version="1.0.22", reason="LibusbContext.set_debug' is deprecated: Use LibusbContext.set_option "
                                             "instead using the LibusbOption.LOG_LEVEL option")
        def set_debug(self, level: LibusbLogLevel = LibusbLogLevel.NONE) -> None:
            """
            Use LibusbContext.set_option() instead using the LibusbOption.LOG_LEVEL option.
            :param level: log level
            :return: None
            """
            libusb.set_debug(self._context, level.value)

        def set_option(self, option: LibusbOption, value: LibusbLogLevel | None = None) -> None:
            """
            Set an option in the library.
            Only the Option.LOG_LEVEL option is supported at the moment. If you use any other option, an exception will
            be thrown.
            :param option: LibusbOption to be configured.
            :param value: Value of the option.
            :return:
            """
            if option.value == LibusbOption.LOG_LEVEL.value:
                if value:
                    ret = libusb.set_option(self._context, option.value, value.value)
                else:
                    raise LibusbException(libusb.LIBUSB_ERROR_INVALID_PARAM)
            else:
                ret = libusb.set_option(self._context, option.value)

            if ret != libusb.LIBUSB_SUCCESS:
                raise LibusbException(ret)
    else:
        def set_debug(self, level: LibusbLogLevel = LibusbLogLevel.LOG_LEVEL_NONE) -> None:
            """
            Sets the debug level of this context.
            :param level: log level
            :return: None
            """
            libusb.set_debug(self._context, level.value)

    def get_device_list(self) -> LibusbDeviceList:
        """
        Returns a list of USB devices currently attached to the system. This is your entry point into finding a USB
        device to operate.
        :return: A list of USB devices.
        """
        devices = ct.POINTER(ct.POINTER(libusb.device))()
        devices_nbr = libusb.get_device_list(self._context, ct.byref(devices))
        return LibusbDeviceList(devices, devices_nbr)
