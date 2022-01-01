from __future__ import annotations
import ctypes as ct
import libusb


class LibusbDescriptor:
    """
    This is the parent class of all the usb descriptors.
    Attributes of a descriptor can be read by indexing the attribute's name(exp: descriptor['bDescriptorType']).
    """
    def __init__(self, descriptor: ct.POINTER(ct.Structure)) -> None:
        """
        LibusbDescriptor object initializer.
        :param descriptor: Usb descriptor.
        """
        self._descriptor = descriptor
        self._bLength = descriptor[0].bLength
        self._bDescriptorType = descriptor[0].bDescriptorType

    def __getitem__(self, field: str) -> int | tuple | bytes:
        """
        Returns the field value from the given descriptor.
        :param field: Field name.
        :return: value.
        """
        return getattr(self, "_" + field)


class LibusbDeviceDescriptor(LibusbDescriptor):
    """
    A class representing the standard USB device descriptor.
    Attributes of a descriptor can be read by indexing the attribute's name(exp: descriptor['bDescriptorType']).
    """
    def __init__(self, descriptor: ct.POINTER(libusb.device_descriptor)) -> None:
        """
        LibusbDeviceDescriptor object initializer.
        :param descriptor: Usb descriptor.
        """
        super().__init__(descriptor)
        self._bcdUSB = descriptor[0].bcdUSB
        self._bDeviceClass = descriptor[0].bDeviceClass
        self._bDeviceSubClass = descriptor[0].bDeviceSubClass
        self._bDeviceProtocol = descriptor[0].bDeviceProtocol
        self._bMaxPacketSize0 = descriptor[0].bMaxPacketSize0
        self._idVendor = descriptor[0].idVendor
        self._idProduct = descriptor[0].idProduct
        self._bcdDevice = descriptor[0].bcdDevice
        self._iManufacturer = descriptor[0].iManufacturer
        self._iProduct = descriptor[0].iProduct
        self._iSerialNumber = descriptor[0].iSerialNumber
        self._bNumConfigurations = descriptor[0].bNumConfigurations

    def __str__(self) -> str:
        """
        Returns the descriptor as a string.
        :return: The descriptor as a string.
        """
        return                                                           \
            F"Device Descriptor\n"                                       \
            F"  bLength           : 0x{self._bLength           :0>2x}\n" \
            F"  bDescriptorType   : 0x{self._bDescriptorType   :0>2x}\n" \
            F"  bcdUSB            : 0x{self._bcdUSB            :0>4x}\n" \
            F"  bDeviceClass      : 0x{self._bDeviceClass      :0>2x}\n" \
            F"  bDeviceSubClass   : 0x{self._bDeviceSubClass   :0>2x}\n" \
            F"  bDeviceProtocol   : 0x{self._bDeviceProtocol   :0>2x}\n" \
            F"  bMaxPacketSize0   : 0x{self._bMaxPacketSize0   :0>2x}\n" \
            F"  idVendor          : 0x{self._idVendor          :0>4x}\n" \
            F"  idProduct         : 0x{self._idProduct         :0>4x}\n" \
            F"  bcdDevice         : 0x{self._bcdDevice         :0>4x}\n" \
            F"  iManufacturer     : 0x{self._iManufacturer     :0>2x}\n" \
            F"  iProduct          : 0x{self._iProduct          :0>2x}\n" \
            F"  iSerialNumber     : 0x{self._iSerialNumber     :0>2x}\n" \
            F"  bNumConfigurations: 0x{self._bNumConfigurations:0>2x}"


class LibusbSsEndpointCompanionDescriptor(LibusbDescriptor):
    """
    A class representing the superspeed endpoint companion descriptor.
    Attributes of a descriptor can be read by indexing the attribute's name(exp: descriptor['bDescriptorType']).
    """
    def __init__(self, descriptor: ct.POINTER(libusb.ss_endpoint_companion_descriptor)) -> None:
        """
        LibusbSsEndpointCompanionDescriptor object initializer.
        :param descriptor: Usb descriptor.
        """
        super().__init__(descriptor)
        self._bMaxBurst = descriptor[0].bMaxBurst
        self._bmAttributes = descriptor[0].bmAttributes
        self._wBytesPerInterval = descriptor[0].wBytesPerInterval

    def __str__(self) -> str:
        """
        Returns the descriptor as a string.
        :return: The descriptor as a string.
        """
        return F"SS Endpoint Companion Descriptor\n"                       \
               F"   bLength          : 0x{self._bLength          :0>2x}\n" \
               F"   bDescriptorType  : 0x{self._bDescriptorType  :0>2x}\n" \
               F"   bMaxBurst        : 0x{self._bMaxBurst        :0>2x}\n" \
               F"   bmAttributes     : 0x{self._bmAttributes     :0>2x}\n" \
               F"   wBytesPerInterval: 0x{self._wBytesPerInterval:0>4x}"


class LibusbEndpointDescriptor(LibusbDescriptor):
    """
    A class representing the standard USB endpoint descriptor.
    Attributes of a descriptor can be read by indexing the attribute's name(exp: descriptor['bDescriptorType']).
    """
    def __init__(self, descriptor: ct.POINTER(libusb.endpoint_descriptor)) -> None:
        """
        LibusbEndpointDescriptor object initializer.
        :param descriptor: Usb descriptor.
        """
        super().__init__(descriptor)
        self._bEndpointAddress = descriptor[0].bEndpointAddress
        self._bmAttributes = descriptor[0].bmAttributes
        self._wMaxPacketSize = descriptor[0].wMaxPacketSize
        self._bInterval = descriptor[0].bInterval
        self._bRefresh = descriptor[0].bRefresh
        self._bSynchAddress = descriptor[0].bSynchAddress
        self._extra = bytes(descriptor[0].extra[0:descriptor[0].extra_length])

    def __str__(self) -> str:
        """
        Returns the descriptor as a string.
        :return: The descriptor as a string.
        """
        ep_str = F"      Endpoint Descriptor\n"                                   \
                 F"          bLength         : 0x{self._bLength         :0>2x}\n" \
                 F"          bDescriptorType : 0x{self._bDescriptorType :0>2x}\n" \
                 F"          bEndpointAddress: 0x{self._bEndpointAddress:0>2x}\n" \
                 F"          bmAttributes    : 0x{self._bmAttributes    :0>2x}\n" \
                 F"          wMaxPacketSize  : 0x{self._wMaxPacketSize  :0>4x}\n" \
                 F"          bInterval       : 0x{self._bInterval       :0>2x}\n" \
                 F"          bRefresh        : 0x{self._bRefresh        :0>2x}\n" \
                 F"          bSynchAddress   : 0x{self._bSynchAddress   :0>2x}"

        if len(self._extra) > 0:
            ep_str = ep_str + F"\n          extra           : {self._extra.hex()}"
        return ep_str


class LibusbInterfaceDescriptor(LibusbDescriptor):
    """
    A class representing the standard USB interface descriptor.
    Attributes of a descriptor can be read by indexing the attribute's name(exp: descriptor['bDescriptorType']).
    """
    def __init__(self, descriptor: ct.POINTER(libusb.interface_descriptor)) -> None:
        """
        LibusbInterfaceDescriptor object initializer.
        :param descriptor: Usb descriptor.
        """
        super().__init__(descriptor)
        self._bInterfaceNumber = descriptor[0].bInterfaceNumber
        self._bAlternateSetting = descriptor[0].bAlternateSetting
        self._bNumEndpoints = descriptor[0].bNumEndpoints
        self._bInterfaceClass = descriptor[0].bInterfaceClass
        self._bInterfaceSubClass = descriptor[0].bInterfaceSubClass
        self._bInterfaceProtocol = descriptor[0].bInterfaceProtocol
        self._iInterface = descriptor[0].iInterface
        self._endpoint = tuple([LibusbEndpointDescriptor(ct.pointer(descriptor[0].endpoint[index]))
                                for index in range(0, descriptor[0].bNumEndpoints)])
        self._extra = bytes(descriptor[0].extra[0:descriptor[0].extra_length])

    def __str__(self) -> str:
        """
        Returns the descriptor as a string.
        :return: The descriptor as a string.
        """
        inter_str = F"  Interface Descriptor\n"                                      \
                    F"      bLength           : 0x{self._bLength           :0>2x}\n" \
                    F"      bDescriptorType   : 0x{self._bDescriptorType   :0>2x}\n" \
                    F"      bInterfaceNumber  : 0x{self._bInterfaceNumber  :0>2x}\n" \
                    F"      bAlternateSetting : 0x{self._bAlternateSetting :0>2x}\n" \
                    F"      bNumEndpoints     : 0x{self._bNumEndpoints     :0>2x}\n" \
                    F"      bInterfaceClass   : 0x{self._bInterfaceClass   :0>2x}\n" \
                    F"      bInterfaceSubClass: 0x{self._bInterfaceSubClass:0>2x}\n" \
                    F"      bInterfaceProtocol: 0x{self._bInterfaceProtocol:0>2x}\n" \
                    F"      iInterface        : 0x{self._iInterface        :0>2x}"

        for index in range(0, len(self._endpoint)):
            inter_str = inter_str + "\n" + str(self._endpoint[index])

        if len(self._extra) > 0:
            inter_str = inter_str + F"\n      extra             : {self._extra.hex()}"
        return inter_str


class LibusbInterface:
    """
    A collection of alternate settings for a particular USB interface.
    """
    def __init__(self, interface: libusb.interface):
        """
        LibusbInterface object initializer.
        :param interface: Usb interface.
        """
        self._altsetting = tuple([LibusbInterfaceDescriptor(ct.pointer(interface.altsetting[index]))
                                  for index in range(0, interface.num_altsetting)])

    def __getitem__(self, index: int) -> LibusbInterfaceDescriptor:
        """
        Returns the alternate setting number: index.
        :param index: The alternate setting index
        :return: value.
        """
        return self._altsetting[index]

    def __str__(self) -> str:
        """
        Returns the descriptor as a string.
        :return: The descriptor as a string.
        """
        inter_str = str()
        nbr_alt = len(self._altsetting)
        for index in range(0, nbr_alt):
            inter_str = inter_str + str(self._altsetting[index])
            if index != nbr_alt - 1:
                inter_str = inter_str + "\n"

        return inter_str


class LibusbConfigurationDescriptor(LibusbDescriptor):
    """
    A class representing the standard USB configuration descriptor.
    """
    def __init__(self, descriptor: ct.POINTER(libusb.config_descriptor)) -> None:
        """
        LibusbConfigurationDescriptor object initializer.
        :param descriptor: Usb descriptor.
        """
        super().__init__(descriptor)
        self._wTotalLength = descriptor[0].wTotalLength
        self._bNumInterfaces = descriptor[0].bNumInterfaces
        self._bConfigurationValue = descriptor[0].bConfigurationValue
        self._iConfiguration = descriptor[0].iConfiguration
        self._bmAttributes = descriptor[0].bmAttributes
        self._MaxPower = descriptor[0].MaxPower
        self._interface = tuple([LibusbInterface(descriptor[0].interface[index])
                                 for index in range(0, self._bNumInterfaces)])
        self._extra = bytes(descriptor[0].extra[0:descriptor[0].extra_length])

    def __del__(self) -> None:
        """
        Frees the underlying usb configuration descriptor.
        :return: None
        """
        libusb.free_config_descriptor(self._descriptor)

    def __str__(self) -> str:
        """
        Returns the descriptor as a string.
        :return: The descriptor as a string.
        """
        conf_str = F"Configuration Descriptor\n"                                  \
                   F"  bLength            : 0x{self._bLength            :0>2x}\n" \
                   F"  bDescriptorType    : 0x{self._bDescriptorType    :0>2x}\n" \
                   F"  wTotalLength       : 0x{self._wTotalLength       :0>4x}\n" \
                   F"  bNumInterfaces     : 0x{self._bNumInterfaces     :0>2x}\n" \
                   F"  bConfigurationValue: 0x{self._bConfigurationValue:0>2x}\n" \
                   F"  iConfiguration     : 0x{self._iConfiguration     :0>2x}\n" \
                   F"  bmAttributes       : 0x{self._bmAttributes       :0>2x}\n" \
                   F"  MaxPower           : 0x{self._MaxPower           :0>2x}"

        for index in range(0, len(self._interface)):
            conf_str = conf_str + "\n" + str(self._interface[index])

        if len(self._extra) > 0:
            conf_str = conf_str + F"\n  extra              : {self._extra.hex()}"
        return conf_str

