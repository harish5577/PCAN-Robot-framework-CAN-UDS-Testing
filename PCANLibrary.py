import ctypes
from ctypes import c_uint, c_ubyte, c_ushort
 
class PCANLibrary:
    def __init__(self):
        self.pcan = ctypes.WinDLL("PCANBasic.dll")
 
        self.PCAN_USBBUS1 = 0x51
        self.PCAN_BAUD_500K = 0x001C
        self.PCAN_ERROR_QRCVEMPTY = 0x02
 
        self.initialized = False
 
        class TPCANMsg(ctypes.Structure):
            _fields_ = [
                ("ID", c_uint),
                ("MSGTYPE", c_ubyte),
                ("LEN", c_ubyte),
                ("DATA", c_ubyte * 8)
            ]
 
        class TPCANTimestamp(ctypes.Structure):
            _fields_ = [
                ("millis", c_uint),
                ("micros", c_ushort),
                ("overflow", c_ushort)
            ]
 
        self.TPCANMsg = TPCANMsg
        self.TPCANTimestamp = TPCANTimestamp
 
    def initialize_pcan(self):
        result = self.pcan.CAN_Initialize(self.PCAN_USBBUS1, self.PCAN_BAUD_500K)
        if result != 0:
            raise Exception(f"PCAN init failed: {hex(result)}")
        self.initialized = True
 
    def uninitialize_pcan(self):
        self.pcan.CAN_Uninitialize(self.PCAN_USBBUS1)
        self.initialized = False
 
    def send_uds_request(self, service_id, sub_function):
        msg = self.TPCANMsg()
        msg.ID = 0x7E7
        msg.MSGTYPE = 0x00
        msg.LEN = 8
        
        # Convert hex strings to integers
        msg.DATA[0] = 0x02                   
        msg.DATA[1] = int(str(service_id), 0)    
        msg.DATA[2] = int(str(sub_function), 0)  
 
        for i in range(3, 8):
            msg.DATA[i] = 0x00
 
        result = self.pcan.CAN_Write(self.PCAN_USBBUS1, ctypes.byref(msg))
        if result != 0:
            raise Exception(f"Failed to send CAN message: {hex(result)}")
 
    def read_uds_response(self, expected_id=0x7EC, timeout_ms=2000):
        msg = self.TPCANMsg()
        ts = self.TPCANTimestamp()
        expected_id_int = int(str(expected_id), 0)
        waited = 0
        poll = 50
 
        while waited < timeout_ms:
            result = self.pcan.CAN_Read(self.PCAN_USBBUS1, ctypes.byref(msg), ctypes.byref(ts))
            if result == 0:
                if msg.ID == expected_id_int:
                    # Format each byte as 0xXX hex string for display 
                    hex_data = [f"0x{msg.DATA[i]:02X}" for i in range(msg.LEN)]
                    return hex(msg.ID), hex_data
 
            ctypes.windll.kernel32.Sleep(poll)
            waited += poll
 
        raise Exception("UDS response timeout")

    def send_can_single_frame(self, can_id, data_bytes):
        if not self.initialized:
            raise Exception("PCAN not initialized")
 
        msg = self.TPCANMsg()
        msg.ID = int(str(can_id), 0)
        msg.MSGTYPE = 0x00  
        msg.LEN = len(data_bytes)
 
        for i in range(msg.LEN):
            # Convert input list items to integers 
            msg.DATA[i] = int(str(data_bytes[i]), 0)
 
        self.pcan.CAN_Write(self.PCAN_USBBUS1, ctypes.byref(msg))