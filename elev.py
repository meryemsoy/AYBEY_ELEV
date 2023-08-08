AYBEY_ELEV_REQ_PACK_HEADER_1_VAL = 0xF2
AYBEY_ELEV_REQ_PACK_HEADER_2_VAL = 0xF4
AYBEY_ELEV_REQ_PACK_HEADER_3_VAL = 0xF1
AYBEY_ELEV_REQ_PACK_ID           = 0X14
from enum import Enum

class aybey_elev_robot_req_indexes(Enum):
     AYBEY_ELEV_ROBOT_REQ_INDEX_HEADER_1          = 0
     AYBEY_ELEV_ROBOT_REQ_INDEX_HEADER_2          = 1
     AYBEY_ELEV_ROBOT_REQ_INDEX_HEADER_3          = 2
     AYBEY_ELEV_ROBOT_REQ_INDEX_NODE_ID           = 3
     AYBEY_ELEV_ROBOT_REQ_INDEX_PACKAGE_ID        = 4
     AYBEY_ELEV_ROBOT_REQ_INDEX_PACKAGE_LAST_BYTE = 5
     AYBEY_ELEV_ROBOT_REQ_INDEX_LIFT_PASS_HB      = 6
     AYBEY_ELEV_ROBOT_REQ_INDEX_LIFT_PASS_LB      = 7
     AYBEY_ELEV_ROBOT_REQ_INDEX_VX                = 8
     AYBEY_ELEV_ROBOT_REQ_INDEX_VY                = 9
     AYBEY_ELEV_ROBOT_REQ_INDEX_VZ                = 10
     AYBEY_ELEV_ROBOT_REQ_INDEX_CMD               = 11
     AYBEY_ELEV_ROBOT_REQ_INDEX_SUB_CMD           = 12
     AYBEY_ELEV_ROBOT_REQ_INDEX_SUB_FREE          = 13
     AYBEY_ELEV_ROBOT_REQ_INDEX_SUB_CL            = 14
     AYBEY_ELEV_ROBOT_REQ_INDEX_SUB_CH            = 15
     AYBEY_ELEV_ROBOT_REQ_INDEX_TOTAL             = 16
class aybey_elev_command_t(Enum):
    AYBEY_ELEV_CMD_GET_STATUS     = 10
    AYBEY_ELEV_CMD_CAR_CALL       = 21
    AYBEY_ELEV_CMD_DOOR_A_OPEN    = 24
    AYBEY_ELEV_CMD_DOOR_A_CLOSE   = 25
    AYBEY_ELEV_CMD_DOOR_B_OPEN    = 26
    AYBEY_ELEV_CMD_DOOR_B_CLOSE   = 27
  
class aybey_elev_robot_req_version_t:
        def __init__(self,x=0,y=0,z=0,):
           self.x  =  x
           self.y  =  y
           self.z  =  z
           

class aybey_elev_robot_req_t:
     def __init__(self, node_id, password, cmd, sub_cmd, x, y, z):
        self.node_id      =  node_id
        self.password     =  password
        self.version      =  aybey_elev_robot_req_version_t(x, y, z)
        self.sub_cmd      =  sub_cmd
        self.cmd          =  cmd

class aybey_elev_robot_req_response_t:
    def __init__(self, node_id, password, cmd, sub_cmd, x, y, z, is_responsed=True):
       self.node_id = node_id
       self.password = password
       self.data = aybey_elev_robot_req_t(node_id, password, cmd, sub_cmd, x, y, z)
       self.is_responsed = is_responsed
   
class received_message_t():
    def __init__(self, data=[], length=0, is_responsed=False):
        self.len           =     length
        self.data          =     data
        self.is_responsed  =     is_responsed
def check_sum(arr, length ):
    sum = 0
    for c in range(length):
        sum += arr[c]
    return sum % 0x1000
def send_request_from_robot_to_elev(req):
    frame      =  received_message_t(data=[], length=0,is_responsed=True)
    frame.data =  bytearray() 
    arr = bytearray([0] *aybey_elev_robot_req_indexes. AYBEY_ELEV_ROBOT_REQ_INDEX_TOTAL.value)
    arr[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_HEADER_1.value]          = AYBEY_ELEV_REQ_PACK_HEADER_1_VAL
    arr[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_HEADER_2.value]          = AYBEY_ELEV_REQ_PACK_HEADER_2_VAL
    arr[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_HEADER_3.value]          = AYBEY_ELEV_REQ_PACK_HEADER_3_VAL
    arr[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_NODE_ID.value]           = req.node_id
    arr[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_PACKAGE_ID.value]        = AYBEY_ELEV_REQ_PACK_ID
    arr[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_PACKAGE_LAST_BYTE.value] = len(arr)-1
    arr[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_LIFT_PASS_HB.value]      = req.password >>8 
    arr[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_LIFT_PASS_LB.value]      = req.password & 0xFF
    arr[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_VX.value]                = req.version.x
    arr[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_VY.value]                = req.version.y
    arr[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_VZ.value]                = req.version.z
    arr[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_CMD.value]               = req.cmd
    AYBEY_ELEV_CMD_GET_STATUS  = aybey_elev_command_t.AYBEY_ELEV_CMD_GET_STATUS
    if AYBEY_ELEV_CMD_GET_STATUS  ==   arr[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_CMD.value]:
        if 0 != req.sub_cmd:
            return frame
    arr[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_SUB_CMD.value] = req.sub_cmd
    arr[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_SUB_FREE.value] = 0x00
    checksum = check_sum(arr, len(arr) - 2)
    arr[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_SUB_CL.value] = checksum & 0xFF
    arr[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_SUB_CH.value] = checksum >> 8
    print("Sending Array\n")
    for c in arr:
        print(f"0x{c:02x} | ", end="")
    print("\n Array sent... \n")
    frame.data = arr
    frame.data = arr.copy()
    frame.len = len(arr)
    frame.is_responsed = True
    return frame
Elev_Asli=0x01
Elev_Meryem=0x02
def parseRequestFromRobotToElev(data, length, node_id):
    req = aybey_elev_robot_req_response_t(node_id=Elev_Meryem,x=5,y=10,z=2, password=0x1453, is_responsed=False, cmd=aybey_elev_command_t.AYBEY_ELEV_CMD_GET_STATUS.value, sub_cmd=0x14)
    if data is not None:
        if (data[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_PACKAGE_LAST_BYTE.value] + 1) != length:
            return req
        if not (AYBEY_ELEV_REQ_PACK_HEADER_1_VAL == data[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_HEADER_1.value]or
                AYBEY_ELEV_REQ_PACK_HEADER_2_VAL == data[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_HEADER_2.value]or
                AYBEY_ELEV_REQ_PACK_HEADER_3_VAL == data[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_HEADER_3.value]
                ):
            return req
        if node_id != data[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_NODE_ID.value]:
            return req
        
        calcuted_checksum = check_sum(data, len(data)-2)
        received_checksum = (data[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_SUB_CH.value] << 8) | data[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_SUB_CL.value]
        if received_checksum != calcuted_checksum:
          print("Parsing starting \n")
          req.data.node_id    =   data[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_NODE_ID.value]
          req.data.password   =   (data[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_LIFT_PASS_HB.value] << 8) | data[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_LIFT_PASS_LB.value]
          req.data.cmd        =   data[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_CMD.value]
          req.data.sub_cmd    =   data[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_SUB_CMD.value]
          req.data.version    =   aybey_elev_robot_req_version_t()
          req.data.version.x  =   data[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_VX.value]
          req.data.version.y  =   data[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_VY.value]
          req.data.version.z  =   data[aybey_elev_robot_req_indexes.AYBEY_ELEV_ROBOT_REQ_INDEX_VZ.value]
          req.is_responsed    =  True
          print("Parsing Ended \n")
        return req  
        
request             = aybey_elev_robot_req_t(Elev_Meryem, 0x1453, aybey_elev_command_t.AYBEY_ELEV_CMD_GET_STATUS.value,0x14,15,21,5)
#request.node_id     = Elev_Meryem
#request.password    = 0x1453
#request.cmd         = aybey_elev_command_t.AYBEY_ELEV_CMD_GET_STATUS.value
#request.sub_cmd     = 0x14

received = send_request_from_robot_to_elev(request)
print("False req -> ", int(received.is_responsed))
received = send_request_from_robot_to_elev(request)
print("True req -> ", int(received.is_responsed))
response = aybey_elev_robot_req_response_t
response = parseRequestFromRobotToElev(received.data, received.len, Elev_Meryem)
print("\nResponse:")
print("is_responsed: 0x%x |"  % response.is_responsed)
print("cmd: 0x%x |"           % response.data.cmd)
print("node_id: 0x%x |"       % response.data.node_id)
print("password: 0x%x |"      % response.data.password)
print("sub_cmd: 0x%x |"       % response.data.sub_cmd)
print("version.x: 0x%x |"     % response.data.version.x)
print("version.y: 0x%x |"     % response.data.version.y)
print("version.z: 0x%x\n"     % response.data.version.z)
arr = [0x10, 0x11, 0x12]
print(check_sum(arr,len(arr)))