
import asyncio
from Modules.command_api import *
import Device as D

## Master list of peripherals
PERIPHERALS = []

# base templates
device_info_base = {
    "name": "",
    "periph_num": 0,
    "periph_ids":[],
    "dev_id":0,
    "periph_id":0,
}

periph_info_base= {
    'periph_id': 0,
    'name': "",
    "param_num":0,
    "param_ids":[],
    "periph_type": 0,
}

periph_ext = {
    "parameters":[],
}

param_info_base = {
    "name": "",
    "periph_id": 0,
    "param_id": 0,
    "p_type": 0,
    "p_max": 0,
    "methods": 0,
    "data_type": 0,
}

param_ext = {
    "is_gettable": False,
    "is_settable": False,
    "is_action": False,
    "get_func": None,
    "set_func": None,
    "act_func": None,
}


## processing function


def get_peripheral(p_id):
    for p in PERIPHERALS:
        if p.periph_id == p_id:
            return p
    
def get_parameter(p_id, prm_id):
    p = get_peripheral(p_id)
    for param in p.parameters:
        if param["param_id"] == prm_id:
            return param


def build_device_info():
    data = device_info_base
    data['name'] = D.DEVICE_NAME
    data["periph_num"] = len(PERIPHERALS)
    data["periph_ids"] =[x.periph_id for x in PERIPHERALS]
    data["dev_id"] = D.DEVICE_ID
    data["periph_id"] = 0
    data["rsp_type"] = RSP_TYPE_INFO
    return data

def build_periph_info(p_id):
    p = get_peripheral(p_id)
    data = periph_info_base

    data['periph_id'] = p.periph_id
    data['name'] = p.name
    data["param_num"] = p.num_params
    data["param_ids"] = [x["param_id"] for x in p.parameters]
    data["periph_type"] = p.periph_type
    data["rsp_type"] = RSP_TYPE_INFO

    return data

def build_param_info(p_id, prm_id):
    prm = get_parameter(p_id, prm_id)
    data = param_info_base

    data["param_name"] = prm["name"]
    data["periph_id"] = p_id
    data["param_id"] = prm["param_id"]
    data["param_max"] = prm["p_max"]
    data["methods"] = prm["methods"]
    data["data_type"] = prm["data_type"]
    data["rsp_type"] = RSP_TYPE_INFO

    return data

async def process_get_request(data):

    prh = get_peripheral(data['periph_id'])
    prm = get_parameter(data['periph_id'], data['param_id'])

    if prm['get_func'] != None:
        result, get_data = prm['get_func']()
        if result:
            data = {
                "periph_id": data['periph_id'],
                "param_id": prm['param_id'],
                "rsp_type": RSP_TYPE_DATA,
                "data": get_data,
                "data_type": prm['data_type']
            }
            return data
        else:
            data = {
                    "rsp_type": RSP_TYPE_ERR,
                    "message": "Error in get function",
                    "code": ERR_CODE_FUNC_ERR,
                    }
            return data
    else:
        data = {
                "rsp_type": RSP_TYPE_ERR,
                "message": "Error in calling get function",
                "code": ERR_CODE_FUNC_ERR,
                }
        return data

async def process_set_request(data):
    
    prh = get_peripheral(data['periph_id'])
    prm = get_parameter(data['periph_id'], data['param_id'])

    if prm['set_func'] != None and data['data'] <= prm['p_max']:
        result = prm['set_func'](data['data'])
        if result:
            data = {
                "periph_id": data['periph_id'],
                "param_id": prm['param_id'],
                "rsp_type": RSP_TYPE_OK,
            }
            return data
        else:
            data = {
                    "rsp_type": RSP_TYPE_ERR,
                    "message": "Error in set function",
                    "code": ERR_CODE_FUNC_ERR,
                    }
            return data
    else:
        data = {
                "rsp_type": RSP_TYPE_ERR,
                "message": "Error in calling set function",
                "code": ERR_CODE_FUNC_ERR,
                }
        return data


async def process_action_request(data):
    prh = get_peripheral(data['periph_id'])
    prm = get_parameter(data['periph_id'], data['param_id'])

    if prm['act_func'] != None:
        result = prm['set_func']()
        if result:
            data = {
                "periph_id": prh['periph_id'],
                "param_id": prm['param_id'],
                "rsp_type": RSP_TYPE_OK,
            }
            return data
        else:
            data = {
                    "rsp_type": RSP_TYPE_ERR,
                    "message": "Error in action function",
                    "code": ERR_CODE_FUNC_ERR,
                    }
            return data
    else:
        data = {
                "rsp_type": RSP_TYPE_ERR,
                "message": "Error in calling action function",
                "code": ERR_CODE_FUNC_ERR,
                }
        return data


def pm_add_peripheral(Obj):

    PERIPHERALS.append(Obj)




