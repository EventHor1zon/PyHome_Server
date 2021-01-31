



class AbstractPeripheral(object):

    def __init__(self, periph_name: str, periph_id: int, periph_type: int):
        self.periph_id = periph_id
        self.periph_type = periph_type
        self.sleep_state = 0
        self.is_powered = True
        self.num_params = 0
        self.parameters = []
        self.name = periph_name

    def Startup(self, **kwargs):
        pass

    def Shutdown(self, **kwargs):
        pass





class AbstractParameter(object):

    def __init__(self, param_name: str, param_id: int, param_type: int, methods: int, data_type: int, p_max: int):
        self.param_name = param_name
        self.param_id = param_id
        self.p_type = param_type
        if methods < API_METHOD_MAX:
            self.methods = methods
        else:
            self.methods = 0
        self.data_type = data_type
        self.is_gettable = (self.methods & API_GET_MASK)
        self.is_settable = (self.methods & API_SET_MASK)
        self.is_action = (self.methods & API_ACT_MASK) 
        self.p_max = p_max


    def get_self(self):
        pass

    def set_self(self, data):
        pass




    