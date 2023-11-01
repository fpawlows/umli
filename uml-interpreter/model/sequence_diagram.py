from enum import Enum
from typing import Optional

from class_diagram import Method
from base_classes import BehavioralDiagram


class SequenceDiagram(BehavioralDiagram):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.actors: list[Actor] = []


class Actor():
    def __init__(self, name: str) -> None:
        self.messages_from: list[Message] = []
        self.messages_to: list[Message] = []
        self.events: list[LifespanEvent] = []
        self.name = name


class LifespanEvent():
    def __init__(self) -> None:
        self.predecessor: Optional[LifespanEvent] = None
        self.successor: Optional[LifespanEvent] = None
        self.time: int = 0


class MessageStatus(Enum):
    FAILED = 0
    SUCCEEDED = 1


class Message(LifespanEvent):
    def __init__(self, sender: Actor, receiver: Actor) -> None:
        super().__init__()
        self.sender = sender
        sender.messages_from.append(self)
        self.receiver = receiver
        receiver.messages_to.append(self)
        self.related_method: Optional[Method] = None
        self.status: MessageStatus = MessageStatus.SUCCEEDED
        self.display_text: Optional[str] = None


class SyncMessage(Message):
    def __init__(self, sender: Actor, receiver: Actor) -> None:
        super().__init__(sender, receiver)
        self.response: Optional[AsyncMessage] = None


class AsyncMessage(Message):
    def __init__(self, sender: Actor, receiver: Actor) -> None:
        super().__init__(sender, receiver)
        self.response: Optional[SyncMessage] = None


class Fragment(SequenceDiagram, LifespanEvent):
    def __init__(self, parent: SequenceDiagram) -> None:
        super().__init__()
        self.actors = parent.actors


class LoopFragment(Fragment):
    def __init__(self, parent: SequenceDiagram) -> None:
        super().__init__(parent)


class ConditionFragment(Fragment):
    def __init__(self, parent: SequenceDiagram) -> None:
        super().__init__(parent)
