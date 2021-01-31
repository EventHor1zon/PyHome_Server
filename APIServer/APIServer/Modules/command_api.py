

ERR_CODE_INVALID_RESPONSE_LEN = 0x1e
ERR_CODE_INVALID_JSON = 0x1f

ERR_CODE_MISSING_FIELD = 0x0d
ERR_CODE_INVALID_CMD_PARAMS = 0x0f

ERR_CODE_INVALID_DEV_ID = 0x2a
ERR_CODE_INVALID_PERIPH_ID = 0x2b
ERR_CODE_INVALID_PARAM_ID = 0x2c
ERR_CODE_FUNC_ERR = 0x3d

CMD_TYPE_INFO = 0x00
CMD_TYPE_GET = 0x01
CMD_TYPE_SET = 0x02
CMD_TYPE_ACTION = 0x04
CMD_TYPE_STREAM = 0x05


RSP_TYPE_INFO = 0x00
RSP_TYPE_OK = 0x01
RSP_TYPE_DATA = 0x02
RSP_TYPE_ERR = 0x03
RSP_TYPE_STREAM = 0x04

API_GET_MASK = 1
API_SET_MASK = 2
API_ACT_MASK = 4

API_METHOD_MAX = 16


PARAMTYPE_NONE = 0
PARAMTYPE_INT8 = 1
PARAMTYPE_UINT8 = 1
PARAMTYPE_INT16 = 2
PARAMTYPE_UINT16 = 2
PARAMTYPE_INT32 = 4
PARAMTYPE_UINT32 = 4
PARAMTYPE_FLOAT = 5
PARAMTYPE_DOUBLE = 8
PARAMTYPE_STRING = 0x0A
PARAMTYPE_BOOL = 0x0B
PARAMTYPE_INVALID = 0xFF

base_keys = ["cmd_type", "periph_id", "param_id"]
set_keys = ["cmd_type", "periph_id", "param_id", "data", "data_type"]



PTYPE_ADDR_LEDS = 0x01 # /** < leds, addressable */
PTYPE_STD_LED = 0x02 #         /** < leds regular */
PTYPE_ACCEL_SENSOR = 0x03 #    /** < accelerometer/gyroscope/g-sensors */
PTYPE_ENVIRO_SENSOR = 0x04 #   /** < environment, temp, humid, pressure sensors */
PTYPE_DISTANCE_SENSOR = 0x05 # /** < distance/movement/etc sensors */
PTYPE_POWER_SENSOR = 0x06 #    /** < voltage/current sensor */
PTYPE_ADC = 0x07 #             /** < adc periperal (on board) */
PTYPE_IO = 0x08 #              /** < basic io function */
PTYPE_DISPLAY = 0x09 #         /** < display oled/led/epaper */
PTYPE_COMMS = 0x0A #           /** < a comms/bluetooth/radio */
PTYPE_NONE = 0xFF #      /** < blank **/


def CommandTypeToInteger(cmd):
    retval = 0xFF
    
    if cmd.upper() == "INFO":
        retval = 0
    elif cmd.upper() == "GET":
        retval = 1
    elif cmd.upper() == "SET":
        retval = 2
    elif cmd.upper() == "ACT":
        retval = 4
    elif cmd.upper() == "STREAM":
        retval = 5

    return retval


def check_set_keys(request):
    for key in set_keys:
        if key not in request.keys():
            return False
    return True



def check_basic_keys(request):
    for key in base_keys:
        if key not in request.keys():
            return False
    return True
