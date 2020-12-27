import pywinusb.hid as hid
from pprint import pprint
from time import sleep



class Dream_Cheeky_Button:

    callbacks = {
        'DISCONNECTED': [],
        'LID_CLOSED':   [],
        'BUTTON_PRESS': [],
        'LID_OPEN':     [],
        'BUTTON_DOWN':  [],
        'BUTTON_HELD':  [],
        'BUTTON_UP':    []
    }

    codes = {
        0:  'DISCONNECTED',
        21: 'LID_CLOSED',
        22: 'BUTTON_PRESS',
        23: 'LID_OPEN',
        24: 'BUTTON_DOWN',
        25: 'BUTTON_HELD',
        26: 'BUTTON_UP'
    };

    events = {
        'DISCONNECTED': 0,
        'LID_CLOSED':   21,
        'BUTTON_PRESS': 22,
        'LID_OPEN':     23,
        'BUTTON_DOWN':  24,
        'BUTTON_HELD':  25,
        'BUTTON_UP':    26
    };

    previous_code = 0;
    previous_event = 0;
    button_press = False;

    def handle_event(self, data):
        event_code = data[1];
        if(self.previous_event == self.events['BUTTON_UP'] and event_code == self.events['LID_OPEN']):
            return; # Don't relaunch Open Lid after button press.
        if(self.previous_code == self.events['BUTTON_PRESS'] and event_code == self.events['LID_OPEN']):
            return self.trigger_event(self.events['BUTTON_UP'], event_code);
        if(self.previous_code == self.events['BUTTON_PRESS'] and event_code == self.events['BUTTON_PRESS']):
            return self.trigger_event(self.events['BUTTON_HELD'], event_code);
        if(self.previous_code != self.events['BUTTON_PRESS'] and event_code == self.events['BUTTON_PRESS']):
            return self.trigger_event(self.events['BUTTON_DOWN'], event_code);
        return self.trigger_event(event_code, event_code);

    def trigger_event(self, event_code, original_code):
        if(self.previous_event != event_code):
            pprint(self.codes[event_code]);
            self.trigger_callback(event_code);
        self.previous_event = event_code;
        self.previous_code = original_code;

    def trigger_callback(self, event_code):
        for callback in self.callbacks[self.codes[event_code]]:
            if(callable(callback)):
                callback();

    def run(self):
        vendor_id = 0x1d34
        product_id = 0x000d

        devices = hid.HidDeviceFilter(vendor_id=vendor_id, product_id=product_id).get_devices();

        if devices:
            device = devices[0]

        device.open()
        device.set_raw_data_handler(self.handle_event)
        while device.is_plugged():
            # just keep the device opened to receive events
            buffer = [0x0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02]
            if device.is_plugged():
                device.send_output_report(buffer)
            sleep(0.10)