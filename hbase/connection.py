# coding: UTF-8

"""
HappyBase connection module.
"""

import logging

from hbase.THBaseService import Client
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport, TFramedTransport
from thrift.protocol import TBinaryProtocol


logger = logging.getLogger(__name__)

THRIFT_TRANSPORTS = dict(
    buffered=TBufferedTransport,
    framed=TFramedTransport,
)

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 9090


class Connection(Client):

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT, timeout=None,
                 autoconnect=True, transport='buffered'):

        if transport not in THRIFT_TRANSPORTS:
            raise ValueError("'transport' must be one of %s"
                             % ", ".join(THRIFT_TRANSPORTS.keys()))

        # Allow host and port to be None, which may be easier for
        # applications wrapping a Connection instance.
        self.host = host or DEFAULT_HOST
        self.port = port or DEFAULT_PORT
        self.timeout = timeout

        self._transport_class = THRIFT_TRANSPORTS[transport]
        self.transport = None
        self._refresh_thrift_client()

        if autoconnect:
            self.open()

        self._initialized = True

    def refresh(self):
        """Refresh the Thrift socket, transport, and client."""
        socket = TSocket(self.host, self.port)
        if self.timeout is not None:
            socket.setTimeout(self.timeout)

        self.transport = self._transport_class(socket)
        protocol = TBinaryProtocol.TBinaryProtocolAccelerated(self.transport)
        Client.__init__(self, protocol)

    def open(self):
        """Open the underlying transport to the HBase instance.

This method opens the underlying Thrift transport (TCP connection).
"""
        if self.transport.isOpen():
            return

        logger.debug("Opening Thrift transport to %s:%d", self.host, self.port)
        self.transport.open()

    def close(self):
        """Close the underyling transport to the HBase instance.

This method closes the underlying Thrift transport (TCP connection).
"""
        if not self.transport.isOpen():
            return

        if logger is not None:
            # If called from __del__(), module variables may no longer
            # exist.
            logger.debug(
                "Closing Thrift transport to %s:%d",
                self.host, self.port)

        self.transport.close()

    def __del__(self):
        try:
            self._initialized
        except AttributeError:
            # Failure from constructor
            return
        else:
            self.close()
