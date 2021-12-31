import libusb


class LibusbException(Exception):
    def __init__(self, error: libusb.error):
        # Input/output error
        if error == libusb.LIBUSB_ERROR_IO:
            self.message = f"({error}) IO Error"
        # Invalid parameter
        elif error == libusb.LIBUSB_ERROR_INVALID_PARAM:
            self.message = f"({error}) Invalid parameter"
        # Access denied (insufficient permissions)
        elif error == libusb.LIBUSB_ERROR_ACCESS:
            self.message = f"({error}) Access denied (insufficient permissions)"
        # No such device (it may have been disconnected)
        elif error == libusb.LIBUSB_ERROR_NO_DEVICE:
            self.message = f"({error}) No such device (it may have been disconnected)"
        # Entity not found
        elif error == libusb.LIBUSB_ERROR_NOT_FOUND:
            self.message = f"({error}) Entity not found"
        # Resource busy
        elif error == libusb.LIBUSB_ERROR_BUSY:
            self.message = f"({error}) Resource busy"
        # Operation timed out
        elif error == libusb.LIBUSB_ERROR_TIMEOUT:
            self.message = f"({error}) Operation timed out"
        # Overflow
        elif error == libusb.LIBUSB_ERROR_OVERFLOW:
            self.message = f"({error}) Overflow"
        # Pipe error
        elif error == libusb.LIBUSB_ERROR_PIPE:
            self.message = f"({error}) Pipe error"
        # System call interrupted (perhaps due to signal)
        elif error == libusb.LIBUSB_ERROR_INTERRUPTED:
            self.message = f"({error}) System call interrupted (perhaps due to signal)"
        # Insufficient memory
        elif error == libusb.LIBUSB_ERROR_NO_MEM:
            self.message = f"({error}) Insufficient memory"
        # Operation not supported or unimplemented on this platform
        elif error == libusb.LIBUSB_ERROR_NOT_SUPPORTED:
            self.message = f"({error}) Operation not supported or unimplemented on this platform"
        # Other error
        else:
            self.message = f"({error}) Other error"
        super().__init__(self.message)
