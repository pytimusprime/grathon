"""
Core functions for common operations

Provides helper functions for:
- Sending messages
- Editing messages
- Deleting messages
- Forwarding messages
"""

from grathon.core.functions.send_message import send_message_base, create_input_text
from grathon.core.functions.edit_message import edit_message_text
from grathon.core.functions.delete_message import delete_messages
from grathon.core.functions.forward_message import forward_messages

__all__ = [
    "send_message_base",
    "create_input_text",
    "edit_message_text",
    "delete_messages",
    "forward_messages",
]
