from typing import Union

from appbase import AppBase


class SwitchBase(AppBase):
    def initialize(self) -> None:
        super().initialize()
        self.switch = self.entities['switch']

    @property
    def state(self) -> bool:
        return self.get_state(self.switch)

    def toggle(self, state: str) -> None:
        switch_type, switch_name = self.split_entity(self.switch)
        if self.state == 'off' and state == 'on':
            self.turn_on(self.switch)
        elif self.state == 'on' and state == 'off':
            self.turn_off(self.switch)
        elif switch_type == 'scene' and state == 'on':
            self.turn_on(self.switch)

    def toggle_on_schedule(self, kwargs: dict) -> None:
        self.toggle(kwargs['state'])

        
class ToggleOnStateChange(SwitchBase):
    def initialize(self) -> None:
        super().initialize()
        self.listen_state(self.state_change,
                          self.entities['target'],
                          constrain_app_enabled=1)

    def state_change(self, entity: Union[str, dict], attribute: str,
                     old: str, new: str, kwargs: dict) -> None:
        if new == self.properties['target_state']:
            self.toggle(self.properties['state'])


class ToggleAtTime(SwitchBase):
    def initialize(self) -> None:
        super().initialize()
        self.run_daily(self.toggle_on_schedule,
                       self.parse_time(self.properties['schedule_time']),
                       state=self.properties['state'],
                       constrain_app_enabled=1)
