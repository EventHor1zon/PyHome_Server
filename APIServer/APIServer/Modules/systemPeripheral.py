
from command_api import *
from APIClasses import AbstractPeripheral
from datetime import datetime

class SystemPeripheral(AbstractPeripheral):


    def __init__(self, *args, **kwargs):
        self.peripherals = [
            {
                "name": "hostname",
                "param_id": 0x01,
                "param_type": 5,
                "p_max": 0,
                "methods": (API_GET_MASK),
                "get_func": self.get_hostname,
                "set_func": None,
                "act_func": None,
            },
            {
                "name": "mac_address",
                "param_id": 0x02,
                "param_type": 5,
                "p_max": 0,
                "methods": (API_GET_MASK),
                "get_func": self.get_mac_address,
                "set_func": None,
                "act_func": None,
            },
        ]
        super().__init__()

    


    async def get_hostname(self):
        proc = await asyncio.create_subprocess_shell(
            "uname -n",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    
        stdout, stderr = await proc.communicate()
        if proc.returncode == 0:
            return 1, stdout
        else:
            return -1, ""
        
    async def get_mac_address(self):
        proc = await asyncio.create_subprocess_shell(
            "ifconfig eth0 | grep ether | cut -d' ' -f10",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    
        stdout, stderr = await proc.communicate()
        if proc.returncode == 0:
            return 1, stdout
        else:
            return -1, ""

    async def get_uptime(self):
        proc = await asyncio.create_subprocess_shell(
            "ifconfig eth0 | grep ether | cut -d' ' -f10",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    
        stdout, stderr = await proc.communicate()
        if proc.returncode == 0:

            since = stdout
            dto = datetime.strptime(since, "%Y-%m-%d %H:%M:%S")


            return 1, stdout
        else:
            return -1, ""