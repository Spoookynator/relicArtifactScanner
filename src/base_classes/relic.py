import json
from enum import Enum


class Relic:
    def __init__(
            self,
            set_name: str,
            main_stat_name: str,
            slot: Enum, sub_stats: list,
            level: int,
            state: Enum,
            scan_datetime,
            inventory_position: int
    ):
        self.set_name = set_name
        self.main_stat_name = main_stat_name
        self.slot = slot
        self.sub_stats = sub_stats
        self.level = level
        self.state = state

        self.scan_datetime = scan_datetime
        self.position = inventory_position

    def to_dict(self):
        return {
            "set_name": self.set_name,
            "main_stat_name": self.main_stat_name,
            "slot": self.slot.name,  # Convert Enum to string
            "sub_stats": self.sub_stats,
            "level": self.level,
            "state": self.state.name,  # Convert Enum to string
            "scan_datetime": self.scan_datetime,
            "inventory_position": self.position
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)

    @classmethod
    def from_dict(cls, data):
        slot_enum = Relic.Slot[data["slot"]]
        state_enum = Relic.State[data["state"]]
        return cls(
            data["set_name"],
            data["main_stat_name"],
            slot_enum,
            data["sub_stats"],
            data["level"],
            state_enum,
            data["scan_datetime"],
            data["inventory_position"]
        )

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls.from_dict(data)

    class State(Enum):
        none = 0
        locked = 1
        trashed = 2

    class Slot(Enum):
        head = 0
        hands = 1
        body = 2
        feet = 3
        sphere = 4
        rope = 5