"""Fluent keyboard builder for inline buttons"""

from __future__ import annotations
import json
from typing import Optional

from grathon.core.TLSchema_Manager.tltypes import (
    inlineKeyboardButton,
    inlineKeyboardButtonTypeCallback,
    inlineKeyboardButtonTypeUrl,
    inlineKeyboardButtonTypeSwitchInline,
    inlineKeyboardButtonTypeCopyText,
    targetChatChosen,
    targetChatTypes,
    replyMarkupInlineKeyboard,
    ButtonStyle,
    buttonStyleDefault,
    buttonStylePrimary,
    buttonStyleDanger,
    buttonStyleSuccess,
)
from grathon.high_level.callback_db import register_callback

# Telegram's actual limit for callback_data
MAX_CALLBACK_BYTES = 64


class KeyboardBuilder:
    """Fluent builder for inline keyboards (replyMarkupInlineKeyboard)

    Usage:
        >>> kb = (
        ...     KeyboardBuilder()
        ...     .primary_button("تایید", "confirm")
        ...     .danger_button("حذف", "delete")
        ...     .row()
        ...     .success_button("بله", "yes")
        ...     .button("خیر", "no")
        ...     .build()
        ... )
    """

    def __init__(self):
        self._rows: list[list[inlineKeyboardButton]] = []
        self._current_row: list[inlineKeyboardButton] = []

    def button(self, text: str, callback_data: str | bytes | dict, style: Optional[ButtonStyle] = None) -> KeyboardBuilder:
        """Add callback button to current row

        Args:
            text: Button label
            callback_data: Data sent to bot when clicked
                - If > 64 bytes: auto-compressed via zlib + base64
                - String: encoded as UTF-8
                - Bytes: used as-is
                - Dict: JSON-encoded
            style: Button style (default, primary, danger, success)

        Returns:
            self (for chaining)
        """
        data_bytes = _encode(callback_data)

        # Telegram caps callback_data at 64 bytes. Compression (zlib+base64)
        # could never guarantee the bound for payloads in the ~33-200 byte
        # range (they always *grow*). Instead we use DB-backed indirection: a
        # short key (cb_<12hex> = 15 bytes) is stored alongside the payload.
        # The key is always well under the limit, for any payload size.
        if len(data_bytes) > MAX_CALLBACK_BYTES:
            short_key = register_callback(_encode_to_str(callback_data))
            data_bytes = short_key.encode('ascii')

        btn = inlineKeyboardButton(
            text=text,
            type=inlineKeyboardButtonTypeCallback(data=data_bytes),
            style=style or buttonStyleDefault()
        )

        self._current_row.append(btn)
        return self

    def url_button(self, text: str, url: str, style: Optional[ButtonStyle] = None) -> KeyboardBuilder:
        """Add URL button to current row

        Args:
            text: Button label
            url: URL to open
            style: Button style (default, primary, danger, success)

        Returns:
            self (for chaining)
        """
        btn = inlineKeyboardButton(
            text=text,
            type=inlineKeyboardButtonTypeUrl(url=url),
            style=style or buttonStyleDefault()
        )
        self._current_row.append(btn)
        return self

    def switch_inline_button(self, text: str, query: str, allow_user_chats: bool = True, allow_bot_chats: bool = False, allow_group_chats: bool = True, allow_channel_chats: bool = True, style: Optional[ButtonStyle] = None) -> KeyboardBuilder:
        """Add switch inline button to current row

        Args:
            text: Button label
            query: Inline query text to pre-fill
            allow_user_chats: Allow private chats with users
            allow_bot_chats: Allow private chats with bots
            allow_group_chats: Allow group and supergroup chats
            allow_channel_chats: Allow channel chats
            style: Button style (default, primary, danger, success)

        Returns:
            self (for chaining)
        """
        btn = inlineKeyboardButton(
            text=text,
            type=inlineKeyboardButtonTypeSwitchInline(
                query=query,
                target_chat=targetChatChosen(
                    types=targetChatTypes(
                        allow_user_chats=allow_user_chats,
                        allow_bot_chats=allow_bot_chats,
                        allow_group_chats=allow_group_chats,
                        allow_channel_chats=allow_channel_chats,
                    )
                )
            ),
            style=style or buttonStyleDefault()
        )
        self._current_row.append(btn)
        return self

    def primary_button(self, text: str, callback_data: str | bytes | dict) -> KeyboardBuilder:
        """Add primary (blue) callback button to current row

        Args:
            text: Button label
            callback_data: Data sent to bot when clicked

        Returns:
            self (for chaining)
        """
        return self.button(text, callback_data, buttonStylePrimary())

    def danger_button(self, text: str, callback_data: str | bytes | dict) -> KeyboardBuilder:
        """Add danger (red) callback button to current row

        Args:
            text: Button label
            callback_data: Data sent to bot when clicked

        Returns:
            self (for chaining)
        """
        return self.button(text, callback_data, buttonStyleDanger())

    def success_button(self, text: str, callback_data: str | bytes | dict) -> KeyboardBuilder:
        """Add success (green) callback button to current row

        Args:
            text: Button label
            callback_data: Data sent to bot when clicked

        Returns:
            self (for chaining)
        """
        return self.button(text, callback_data, buttonStyleSuccess())

    def secondary_button(self, text: str, callback_data: str | bytes | dict) -> KeyboardBuilder:
        """Add secondary (gray) callback button to current row

        Uses the default button style — visually less prominent than primary.

        Args:
            text: Button label
            callback_data: Data sent to bot when clicked

        Returns:
            self (for chaining)

        Example:
            >>> kb = KeyboardBuilder()
            >>> kb.primary_button("تأیید", "confirm")
            ...    .secondary_button("انصراف", "cancel")
            ...    .build()
        """
        return self.button(text, callback_data, buttonStyleDefault())

    def copy_button(self, text: str, copy_text: str) -> KeyboardBuilder:
        """Add copy-to-clipboard button to current row

        When clicked, copies the specified text to user's clipboard
        (Telegram native feature, no bot callback needed).

        Args:
            text: Button label
            copy_text: Text to copy to clipboard when clicked

        Returns:
            self (for chaining)

        Example:
            >>> kb = KeyboardBuilder()
            >>> kb.copy_button("کپی لینک", "https://t.me/example")
            ...    .build()
        """
        btn = inlineKeyboardButton(
            text=text,
            type=inlineKeyboardButtonTypeCopyText(text=copy_text),
            style=buttonStyleDefault()
        )
        self._current_row.append(btn)
        return self

    def close_button(self, text: str = "❌ بستن", closing_message: Optional[str] = None) -> KeyboardBuilder:
        """Add close/cancel button that Grathon auto-handles

        When clicked:
        - If closing_message is None: Removes keyboard from message
        - If closing_message is provided: Replaces message with that text (keyboard removed)

        Args:
            text: Button label (default: "❌ بستن")
            closing_message: Optional message to show when menu closes
                            If None, just removes the keyboard silently

        Returns:
            self (for chaining)

        Example:
            >>> kb = KeyboardBuilder()
            >>> kb.button("تایید", "confirm")
            >>> kb.close_button("❌ بستن", closing_message="✅ منو بسته شد")
        """
        # Store closing message in special format for grathon to handle
        callback = {
            "__grathon_close__": True,
            "message": closing_message or ""
        }
        return self.button(text, callback)

    def row(self) -> KeyboardBuilder:
        """Start new row

        Returns:
            self (for chaining)
        """
        if self._current_row:
            self._rows.append(self._current_row)
            self._current_row = []
        return self

    def build(self) -> replyMarkupInlineKeyboard:
        """Build final keyboard markup

        Returns:
            replyMarkupInlineKeyboard ready for send_message(..., reply_markup=kb)
        """
        rows = list(self._rows)
        if self._current_row:
            rows.append(list(self._current_row))
        return replyMarkupInlineKeyboard(rows=rows or None)


def _encode(data: str | bytes | dict) -> bytes:
    """Encode callback data to bytes"""
    if isinstance(data, bytes):
        return data
    if isinstance(data, str):
        return data.encode('utf-8')
    # dict: JSON encode
    return json.dumps(data, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def _encode_to_str(data: str | bytes | dict) -> str:
    """Convert callback data to string (for compression)"""
    if isinstance(data, bytes):
        return data.decode('utf-8', errors='replace')
    if isinstance(data, str):
        return data
    # dict: JSON encode
    return json.dumps(data, separators=(',', ':'), ensure_ascii=False)
