
from aiohttp import web
from Modules.command_api import *
from PeripheralManager import *
from Modules import ws2812 as ws
import board

import json


running_tasks = []

DEBUG_MODE = True

def DEBUG_LOG(msg):
    if DEBUG_MODE:
        print(msg)


def valid_peripheral(p_id):

    for p in PERIPHERALS:
        if p.periph_id == p_id:
            return True
    return False

def valid_parameter(p_id, prm_id):
    for p in PERIPHERALS:
        if p.periph_id == p_id:
            for prm in p.parameters:
                if prm['param_id'] == prm_id:
                    return True
    return False

def valid_method(p_id, prm_id, cmd_type):
    param = None
    for p in PERIPHERALS:
        if p.periph_id == p_id:
            for prm in p.parameters:
                if prm['param_id'] == prm_id: 
                    param = prm
    if param == None:
        return False
    else:
        if cmd_type == CMD_TYPE_GET and param['get_func'] is not None:
            return True
        elif cmd_type == CMD_TYPE_SET and param['set_func'] is not None:
            return True
        elif cmd_type == CMD_TYPE_ACT and param['act_func'] is not None:
            return True
        else:
            return False





async def hello(request):
    return web.Response(text="hiya!")


async def command_handler(request):

    error_rsp = {
        "rsp_type": RSP_TYPE_ERR,
        "message": "",
        "code": 0,
    }

    rsp = None

    fail = False

    try:
        data = await request.json()

        for key in base_keys:
            if key not in data.keys():
                DEBUG_LOG(f"Error: missing key {key}")
                error_rsp["message"] = f"Error: missing key {key}"
                error_rsp["code"] = 506
                fail = True
        
        if not fail:
            # process request & build response
            if data['cmd_type'] == CMD_TYPE_INFO:
                DEBUG_LOG("got info cmd")
                if data['periph_id'] == 0:
                    rsp = build_device_info()
                elif data['param_id'] == 0:
                    rsp = build_periph_info(data['periph_id'])
                else:
                    rsp = build_param_info(data['periph_id'], data['param_id'])

            # all following commands need a validated periph, param and method
            elif data['periph_id'] == 0 or data['param_id'] == 0:
                DEBUG_LOG(f"Error: Invalid id")
                error_rsp["message"] = "Error: Invalid ID"
                error_rsp["code"] = 505
                fail = True
            elif not valid_peripheral(data['periph_id']) or not valid_parameter(data['periph_id'], data['param_id']):
                DEBUG_LOG("Error: invalid id")
                error_rsp["message"] = "Error:  invalid id"
                error_rsp["code"] = 506
                fail = True                
            elif not valid_method(data['periph_id'], data['param_id'], data['cmd_type']):
                DEBUG_LOG("Error: invalid method")
                error_rsp["message"] = "Error:  invalid method"
                error_rsp["code"] = 506
                fail = True                
            elif data['cmd_type'] == CMD_TYPE_GET:
                DEBUG_LOG("Got GET request")
                rsp = await process_get_request(data)
            elif data['cmd_type'] == CMD_TYPE_SET:
                DEBUG_LOG("Got SET request")
                rsp = await process_set_request(data)
            elif data['cmd_type'] == CMD_TYPE_ACT:
                DEBUG_LOG("Got ACT request")                
                rsp = await process_action_request(data)
            elif data['cmd_type'] == CMD_TYPE_STREAM:
                DEBUG_LOG("Error: Not implemented")
                error_rsp["message"] = "Error:  Not implemented!"
                error_rsp["code"] = 401
                fail = True              
            else:
                DEBUG_LOG(f"Error: invalid command type {data['cmd_type']}")
                error_rsp["message"] = "Error:  invalid cmd_type"
                error_rsp["code"] = 507
                fail = True

    except Exception as e:
        DEBUG_LOG(f"Error: { e }")
        return 


    if not fail:
        if rsp == None:
            DEBUG_LOG("rsp is none")
        else:
            DEBUG_LOG(rsp)
            return web.json_response(rsp)
    else:
        DEBUG_LOG(error_rsp)
        return web.json_response(error_rsp)


async def start_background_tasks(app):
    for p in PERIPHERALS:
        try:
            task = p.task
            taskname = p.name + "_task"
            running = asyncio.create_task(task())
            running_tasks.append(running)
        except:
            pass

async def fin_background_tasks(app):
    for task in running_tasks:
        task.cancel()
    await asyncio.gather(running_tasks)

async def main():

    leds = await ws.WS2812Strip.Create(board.D18, 21, "leds", 0x0A, PTYPE_ADDR_LEDS)
    leds.set_all_colour()
    pm_add_peripheral(leds)
    print(leds)

    print("added led peripheral")
    return


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    app = web.Application()
    app.add_routes([web.get("/", hello),
                    web.post("/cmd", command_handler)])
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(fin_background_tasks)
    web.run_app(app, host="0.0.0.0", port=8000)