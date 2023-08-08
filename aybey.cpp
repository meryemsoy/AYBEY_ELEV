#include "stdbool.h"
#include "stdint.h"
#include "stdio.h"
#include "stdlib.h"
#include "string.h"

#define AYBEY_ELEV_REQ_PACK_HEADER_1_VAL 0xF2
#define AYBEY_ELEV_REQ_PACK_HEADER_2_VAL 0xF4
#define AYBEY_ELEV_REQ_PACK_HEADER_3_VAL 0xF1

#define AYBEY_ELEV_REQ_PACK_ID           0x14

typedef enum
{
    AYBEY_ELEV_CMD_GET_STATUS   = 0,
    AYBEY_ELEV_CMD_CAR_CALL     = 21,
    AYBEY_ELEV_CMD_DOOR_A_OPEN  = 24,
    AYBEY_ELEV_CMD_DOOR_A_CLOSE = 25,
    AYBEY_ELEV_CMD_DOOR_B_OPEN  = 26,
    AYBEY_ELEV_CMD_DOOR_B_CLOSE = 27
}aybey_elev_command_t;

typedef enum
{
    AYBEY_ELEV_ROBOT_REQ_INDEX_HEADER_1          = 0,
    AYBEY_ELEV_ROBOT_REQ_INDEX_HEADER_2             ,
    AYBEY_ELEV_ROBOT_REQ_INDEX_HEADER_3             ,
    AYBEY_ELEV_ROBOT_REQ_INDEX_NODE_ID              ,
    AYBEY_ELEV_ROBOT_REQ_INDEX_PACKAGE_ID           ,
    AYBEY_ELEV_ROBOT_REQ_INDEX_PACKAGE_LAST_BYTE    ,
    AYBEY_ELEV_ROBOT_REQ_INDEX_LIFT_PASS_HB         , // HB: High byte
    AYBEY_ELEV_ROBOT_REQ_INDEX_LIFT_PASS_LB         , // LB: Low byte
    AYBEY_ELEV_ROBOT_REQ_INDEX_VX                   ,
    AYBEY_ELEV_ROBOT_REQ_INDEX_VY                   ,
    AYBEY_ELEV_ROBOT_REQ_INDEX_VZ                   ,
    AYBEY_ELEV_ROBOT_REQ_INDEX_CMD                  ,
    AYBEY_ELEV_ROBOT_REQ_INDEX_SUB_CMD              ,
    AYBEY_ELEV_ROBOT_REQ_INDEX_SUB_FREE             ,
    AYBEY_ELEV_ROBOT_REQ_INDEX_SUB_CL               , // crc: Low byte
    AYBEY_ELEV_ROBOT_REQ_INDEX_SUB_CH               , // crc: High byte
    AYBEY_ELEV_ROBOT_REQ_INDEX_TOTAL                  // crc: High byte
}aybey_elev_robot_req_indexes_t;

typedef struct
{
    uint8_t x;
    uint8_t y;
    uint8_t z;
}aybey_elev_robot_req_version_t;

typedef struct
{
    uint8_t node_id;
    uint16_t password;
    aybey_elev_robot_req_version_t version;
    uint8_t cmd;
    uint8_t sub_cmd;
}aybey_elev_robot_req_t;


typedef struct
{
    aybey_elev_robot_req_t data;
    bool is_responsed;
}aybey_elev_robot_req_response_t;

typedef struct
{
    uint8_t data[AYBEY_ELEV_ROBOT_REQ_INDEX_TOTAL];
    uint8_t len;
    bool is_responsed;
}received_message_t;


uint16_t checkSum(uint8_t * arr, uint8_t len)
{
    uint32_t sum = 0;
    for (uint8_t c = 0; c < len; c++)
        sum += arr[c];
    return (uint16_t)(sum %=0x1000);
}

received_message_t sendRequestFromRobotToElev(const aybey_elev_robot_req_t req)
{
    received_message_t frame;
    memset(&frame, 0, sizeof(frame));
    uint8_t arr[AYBEY_ELEV_ROBOT_REQ_INDEX_TOTAL];
    memset(arr, 0, sizeof(arr));
    arr[AYBEY_ELEV_ROBOT_REQ_INDEX_HEADER_1] = AYBEY_ELEV_REQ_PACK_HEADER_1_VAL;
    arr[AYBEY_ELEV_ROBOT_REQ_INDEX_HEADER_2] = AYBEY_ELEV_REQ_PACK_HEADER_2_VAL;
    arr[AYBEY_ELEV_ROBOT_REQ_INDEX_HEADER_3] = AYBEY_ELEV_REQ_PACK_HEADER_3_VAL;
    arr[AYBEY_ELEV_ROBOT_REQ_INDEX_NODE_ID] = req.node_id;
    arr[AYBEY_ELEV_ROBOT_REQ_INDEX_PACKAGE_ID] = AYBEY_ELEV_REQ_PACK_ID;
    arr[AYBEY_ELEV_ROBOT_REQ_INDEX_PACKAGE_LAST_BYTE] = sizeof(arr) - 1;
    arr[AYBEY_ELEV_ROBOT_REQ_INDEX_LIFT_PASS_HB] = (uint8_t)(req.password >> 8);
    arr[AYBEY_ELEV_ROBOT_REQ_INDEX_LIFT_PASS_LB] = (uint8_t)(req.password & 0xFF);
    arr[AYBEY_ELEV_ROBOT_REQ_INDEX_VX] = req.version.x;
    arr[AYBEY_ELEV_ROBOT_REQ_INDEX_VY] = req.version.y;
    arr[AYBEY_ELEV_ROBOT_REQ_INDEX_VZ] = req.version.z;
    arr[AYBEY_ELEV_ROBOT_REQ_INDEX_CMD] = req.cmd;
    if (AYBEY_ELEV_CMD_GET_STATUS == arr[AYBEY_ELEV_ROBOT_REQ_INDEX_CMD])
        if (0 != req.sub_cmd)
            return frame;
    arr[AYBEY_ELEV_ROBOT_REQ_INDEX_SUB_CMD] = req.sub_cmd;
    arr[AYBEY_ELEV_ROBOT_REQ_INDEX_SUB_FREE] = 0x00;
    arr[AYBEY_ELEV_ROBOT_REQ_INDEX_SUB_CL] = (uint8_t)(checkSum(arr, sizeof(arr) - sizeof(uint16_t)) & 0xFF);
    arr[AYBEY_ELEV_ROBOT_REQ_INDEX_SUB_CH] = (uint8_t)(checkSum(arr, sizeof(arr) - sizeof(uint16_t)) >> 8);
    printf("Sending Array\n");
    for (uint8_t c = 0; c < sizeof(arr); c++)
        printf("0x%x | ", arr[c]);
    printf("\nArray sent...\n");
    memcpy(frame.data, arr, sizeof(arr));
    frame.len = sizeof(arr);
    frame.is_responsed = true;
    return frame;
}
#define ELEV_ASLI   0x01
#define ELEV_MERYEM 0x02

aybey_elev_robot_req_response_t parseRequestFromRobotToElev(uint8_t * data, uint8_t len, uint8_t node_id)
{
    aybey_elev_robot_req_response_t req;
    memset(&req, 0, sizeof(req));
    if (data != NULL)
    {
        if ((data[AYBEY_ELEV_ROBOT_REQ_INDEX_PACKAGE_LAST_BYTE] + 1) != len)
            return req;
        if (!((AYBEY_ELEV_REQ_PACK_HEADER_1_VAL == data[AYBEY_ELEV_ROBOT_REQ_INDEX_HEADER_1]) ||
              (AYBEY_ELEV_REQ_PACK_HEADER_2_VAL == data[AYBEY_ELEV_ROBOT_REQ_INDEX_HEADER_2]) ||
              (AYBEY_ELEV_REQ_PACK_HEADER_3_VAL == data[AYBEY_ELEV_ROBOT_REQ_INDEX_HEADER_3])))
            return req;
        if (node_id != data[AYBEY_ELEV_ROBOT_REQ_INDEX_NODE_ID])
            return req;
        uint16_t calculated_checksum = checkSum(data, len - sizeof(uint16_t));
        uint16_t received_checksum = (data[AYBEY_ELEV_ROBOT_REQ_INDEX_SUB_CH] << 8) |
            data[AYBEY_ELEV_ROBOT_REQ_INDEX_SUB_CL];
        if (received_checksum != calculated_checksum)
            return req;
            printf("Parsing Starting...\n");
            req.data.node_id = data[AYBEY_ELEV_ROBOT_REQ_INDEX_NODE_ID];
            req.data.password = (data[AYBEY_ELEV_ROBOT_REQ_INDEX_LIFT_PASS_HB] << 8) |
                                 data[AYBEY_ELEV_ROBOT_REQ_INDEX_LIFT_PASS_LB];
            req.data.cmd = data[AYBEY_ELEV_ROBOT_REQ_INDEX_CMD];
            req.data.sub_cmd = data[AYBEY_ELEV_ROBOT_REQ_INDEX_SUB_CMD];
            req.data.version.x = data[AYBEY_ELEV_ROBOT_REQ_INDEX_VX];
            req.data.version.y = data[AYBEY_ELEV_ROBOT_REQ_INDEX_VY];
            req.data.version.z = data[AYBEY_ELEV_ROBOT_REQ_INDEX_VZ];
            req.is_responsed = true;
            printf("Parsing Ended...\n");
    }
    return req;
}

int main(int argc, char const *argv[])
{
    uint16_t val = 0x1234;
   
    aybey_elev_robot_req_t request;
    request.node_id = ELEV_ASLI; 
    request.password = 0x1453; 
    request.cmd = AYBEY_ELEV_CMD_GET_STATUS;
    request.sub_cmd = 0x14;
 
    printf("False -> %d\n", sendRequestFromRobotToElev((const aybey_elev_robot_req_t)request).is_responsed);
    request.sub_cmd = 0x00;
    received_message_t received = sendRequestFromRobotToElev((const aybey_elev_robot_req_t)request);
    printf("True -> %d\n", received.is_responsed);
    aybey_elev_robot_req_response_t response =
    parseRequestFromRobotToElev(received.data, received.len, ELEV_ASLI);
    printf("\nResponse:\n");
    printf("is_responsed: 0x%x |", response.is_responsed);
    printf("cmd: 0x%x |", response.data.cmd);
    printf("node_id: 0x%x |", response.data.node_id);
    printf("password: 0x%x |", response.data.password);
    printf("sub_cmd: 0x%x |", response.data.sub_cmd);
    printf("version.x: 0x%x |", response.data.version.x);
    printf("version.y: 0x%x |", response.data.version.y);
    printf("version.z: 0x%x\n", response.data.version.z);
    return 0;
}