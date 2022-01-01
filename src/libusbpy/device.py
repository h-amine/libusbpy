from __future__ import annotations
from deprecated import deprecated

from .defines import *
from .exceptions import LibusbException
from .descriptors import *


class LibusbDevice:
    """
    A class representing a USB device detected on the system.
    Certain operations can be performed on a device, but in order to do any I/O you will have to first open a device
    using LibusbDevice.open().
    """
    def __init__(self, device: ct.POINTER(libusb.device)) -> None:
        """
        LibusbDevice object initializer.
        :param device: The underlying usb device reference.
        """
        self._device = device

    def __del__(self) -> None:
        """
        Frees the underlying usb device.
        :return: None
        """
        self.unref_device()

    # ******************************************************************************************************************
    # USB handling and enumeration methods *****************************************************************************
    # ******************************************************************************************************************
    def get_bus_number(self) -> int:
        """
        Get the number of the bus that a device is connected to.
        :return: The bus number.
        """
        return int(libusb.get_bus_number(self._device))

    def get_port_number(self) -> int:
        """
        Get the number of the port that a device is connected to.
        :return: The port number (0 if not available).
        """
        return int(libusb.get_port_number(self._device))

    if libusb.LIBUSB_API_VERSION >= 0x01000102:
        def get_port_numbers(self) -> tuple:
            """
            Get the list of all port numbers from root for the specified device.
            if the underlying libusb function call fails, a LibusbException will be thrown.
            :return: The port numbers.
            """
            numbers = ct.c_buffer(b"", 7)
            ret = libusb.get_port_numbers(self._device, ct.cast(numbers, ct.POINTER(ct.c_uint8)), 7)
            if ret >= libusb.LIBUSB_SUCCESS:
                return tuple([numbers[x][0] for x in range(0, ret)])

            raise LibusbException(ret)

        @deprecated(version="1.0.16", reason="LibusbDevice.get_port_path is deprecated: "
                                             "Please use LibusbDevice.get_port_numbers() instead.")
        def get_port_path(self) -> tuple:
            """
            LibusbDevice.get_port_path is deprecated: Please use LibusbDevice.get_port_numbers() instead.
            :return: The port numbers.
            """
            return tuple()
    else:
        def get_port_path(self) -> tuple:
            """
            Get the list of all port numbers from root for the specified device.
            :return: The port numbers.
            """
            #@TODO: Add the implementation
            return tuple()

    def get_parent(self) -> LibusbDevice | None:
        """
        Get the parent from the specified device.
        :return: The device parent or None if not available.
        """
        parent = libusb.get_parent(self._device)
        if parent:
            return LibusbDevice(parent)

        return None

    def get_device_address(self) -> int:
        """
        Get the address of the device on the bus it is connected to.
        :return: The device address
        """
        return int(libusb.get_device_address(self._device))

    def get_device_speed(self) -> LibusbDeviceSpeed:
        """
        Get the negotiated connection speed for a device.
        :return: A LibusbDeviceSpeed, where LibusbDeviceSpeed.UNKNOWN means that the OS doesn't know or doesn't support
        returning the negotiated speed.
        """
        return LibusbDeviceSpeed(libusb.get_device_speed(self._device))

    def get_max_packet_size(self, endpoint: int) -> int:
        """
        Convenience function to retrieve the wMaxPacketSize value for a particular endpoint in the active device
        configuration. If you're dealing with isochronous transfers, you probably want Device.get_max_iso_packet_size()
        instead.
        if the underlying libusb function call fails, a LibusbException will be thrown.
        :param endpoint: Address of the endpoint in question.
        :return: The wMaxPacketSize value.
        """
        ret = libusb.get_max_packet_size(self._device, endpoint)
        if ret == libusb.LIBUSB_SUCCESS:
            return int(ret)
        raise LibusbException(ret)

    def get_max_iso_packet_size(self, endpoint: int) -> int:
        """
        Calculate the maximum packet size which a specific endpoint is capable is sending or receiving in the duration
        of 1 microframe.
        if the underlying libusb function call fails, a LibusbException will be thrown.
        :param endpoint: Address of the endpoint in question.
        :return: The maximum packet size which can be sent/received on this endpoint.
        """
        ret = libusb.get_max_iso_packet_size(self._device, endpoint)
        if ret == libusb.LIBUSB_SUCCESS:
            return int(ret)
        raise LibusbException(ret)

    def ref_device(self) -> None:
        """
        Increment the reference count of the underlying libusb device.
        :return: None
        """
        libusb.ref_device(self._device)

    def unref_device(self) -> None:
        """
        Decrement the reference count of the underlying libusb device. If the decrement operation causes the reference
        count to reach zero, the underlying libusb device shall be destroyed.
        :return: None
        """
        libusb.unref_device(self._device)

    # ******************************************************************************************************************
    # USB descriptors methods ******************************************************************************************
    # ******************************************************************************************************************
    def get_device_descriptor(self) -> LibusbDeviceDescriptor:
        """
        Get the USB device descriptor for a given device.
        if the underlying libusb function call fails, a LibusbException will be thrown.
        :return: The usb device descriptor.
        """
        desc = libusb.device_descriptor()
        ret = libusb.get_device_descriptor(self._device, ct.byref(desc))
        if ret != libusb.LIBUSB_SUCCESS:
            raise LibusbException(ret)
        return LibusbDeviceDescriptor(ct.pointer(desc))

    def get_active_config_descriptor(self) -> LibusbConfigurationDescriptor:
        """
        Get the USB configuration descriptor for the currently active configuration.
        This is a non-blocking function which does not involve any requests being sent to the device.
        if the underlying libusb function call fails, a LibusbException will be thrown.
        :return: The usb configuration descriptor.
        """
        c_config = ct.POINTER(libusb.config_descriptor)()
        ret = libusb.get_active_config_descriptor(self._device, ct.byref(c_config))
        if ret != libusb.LIBUSB_SUCCESS:
            raise LibusbException(ret)
        return LibusbConfigurationDescriptor(c_config)

    def get_config_descriptor(self, index: int) -> LibusbConfigurationDescriptor:
        """
        Get a USB configuration descriptor based on its index.
        This is a non-blocking function which does not involve any requests being sent to the device.
        if the underlying libusb function call fails, a LibusbException will be thrown.
        :param index: The index of the configuration.
        :return: The usb configuration descriptor.
        """
        c_config = ct.POINTER(libusb.config_descriptor)()
        ret = libusb.get_config_descriptor(self._device, index, ct.byref(c_config))
        if ret != libusb.LIBUSB_SUCCESS:
            raise LibusbException(ret)
        return LibusbConfigurationDescriptor(c_config[0])


class LibusbDeviceList:
    """
    This class is a list of USB devices currently attached to the system, which can be retrieved using
    LibusbContext.get_device_list.
    """
    class DeviceListIterator:
        """
        This class is a DeviceList Iterator.
        """
        def __init__(self, device_list: list) -> None:
            """
            DeviceListIterator object initializer.
            :param device_list: A list of usb devices.
            """
            self._device_list = device_list
            self._len = len(device_list)
            self._index = 0

        def __next__(self) -> LibusbDevice:
            """
            Returns the next usb device in the list.
            :return: A usb device.
            """
            if self._index < self._len:
                result = self._device_list[self._index]
                self._index += 1
                return result
            # End of Iteration
            raise StopIteration

    def __init__(self, devices: ct.POINTER(ct.POINTER(libusb.device)), device_nbr: int) -> None:
        """
        DeviceList object initializer.
        :param devices: A c list of usb devices currently attached to the system.
        :param device_nbr: The number of usb devices currently attached to the system.
        """
        self._devices = devices
        self._device_nbr = device_nbr
        self._list = [LibusbDevice(self._devices[index]) for index in range(0, self._device_nbr)]
        # self._list = [self._devices[index] for index in range(0, self._device_nbr)]

    def __del__(self) -> None:
        """
        Frees the underlying list of usb devices.
        :return: None
        """
        libusb.free_device_list(self._devices, 0)

    def __iter__(self) -> LibusbDeviceList.DeviceListIterator:
        """
        Returns a DeviceList iterator.
        :return:
        """
        return LibusbDeviceList.DeviceListIterator(self._list)

    def __getitem__(self, index: int) -> LibusbDevice:
        """
        Returns the usb device at index from the DeviceList.
        :param index: index of the device.
        :return: A usb device.
        """
        return self._list[index]

    def __len__(self) -> int:
        """
        Returns the length of the DeviceList.
        :return:
        """
        return self._device_nbr
