from projector.handler.base_handler import BaseEventHandler
from projector.handler.create_profile_handler import CreateProfileHandler
from projector.handler.send_code_handler import SendCodeHandler


class HandlerProxy(BaseEventHandler):
    def __init__(self, message):
        super().__init__(message=message)

        self.actual_event = None

    def do_something(self):
        event = self.message.get('event', '')

        if event == 'create_profile':
            self.actual_event = CreateProfileHandler(self.message)
        elif event == 'send_code':
            self.actual_event = SendCodeHandler(self.message)

        if self.actual_event:
            self.actual_event.do_something()
