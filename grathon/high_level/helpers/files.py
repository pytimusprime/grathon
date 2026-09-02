"""
File handling helpers for sending and receiving files via TDLib
"""

from __future__ import annotations
import asyncio
import os
import shutil
import logging
from typing import TYPE_CHECKING, Optional
from pathlib import Path

from grathon.core.TLSchema_Manager.tltypes import (
    formattedText, inputFileLocal, inputFileId, inputFileRemote,
    inputMessagePhoto, inputMessageVideo, inputMessageAudio,
    inputMessageDocument, inputMessageSticker,
    inputMessageVoiceNote, inputMessageAnimation,
    inputPhoto, inputVideo, inputAudio, inputAnimation,
    fileTypePhoto, fileTypeVideo, fileTypeAudio, fileTypeSticker,
    fileTypeVoiceNote, fileTypeAnimation, fileTypeDocument,
    messageSendOptions, InputMessageContent, message,
    messageSendingStateFailed
)
from grathon.core.functions.send_message import send_message_base

if TYPE_CHECKING:
    from grathon.core.contexts.NewMessageCtx import NewMessageCtx

logger = logging.getLogger(__name__)


class FileHelper:
    """Helpers for file operations"""

    @staticmethod
    async def send_file(
        ctx: NewMessageCtx,
        file_path: str,
        caption: str | formattedText = "",
        file_type: str = "auto",
        reply_markup: Optional[ReplyMarkup] = None,
    ) -> Optional[message]:
        try:
            abs_path = os.path.abspath(file_path)
            if not os.path.exists(abs_path):
                logger.warning(f"File not found: {abs_path}")
                return None

            file_size = os.path.getsize(abs_path)
            max_size = 2 * 1024 * 1024 * 1024
            if file_size > max_size:
                logger.error(f"File too large: {file_size} > {max_size}")
                return None

            if file_type == "auto":
                if FileHelper.is_image(abs_path):
                    file_type = "photo"
                elif FileHelper.is_video(abs_path):
                    file_type = "video"
                elif FileHelper.is_audio(abs_path):
                    file_type = "audio"
                else:
                    file_type = "document"

            if isinstance(caption, formattedText):
                caption_text = caption
            else:
                caption_text = formattedText(text=caption or "", entities=[])

            content = FileHelper._build_content(abs_path, file_type, caption_text)

            send_options = messageSendOptions(
                disable_notification=False,
                from_background=False
            )
            result = await send_message_base(
                ctx=ctx,
                chat_id=ctx.chat_id,
                topic_id=None,
                reply_to=None,
                options=send_options,
                reply_markup=reply_markup,
                input_message_content=content,
                wait_for_confirmation=True,
            )

            if isinstance(result, message) and getattr(result, 'sending_state', None) is not None:
                if isinstance(result.sending_state, messageSendingStateFailed):
                    err = getattr(getattr(result.sending_state, 'error', None), 'message', 'Unknown')
                    print(f"[FILEHELPER] SEND FAILED: {err}")
                    return None

            logger.info(f"Sent file: {abs_path} ({file_type})")
            print(f"[FILEHELPER] Returning message id={getattr(result, 'id', '?')}, type={type(result).__name__}")
            return result

        except (OSError, asyncio.TimeoutError, RuntimeError) as e:
            print(f"[FILEHELPER ERROR] {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            logger.error(f"Failed to send file: {e}")
            return None

    @staticmethod
    async def send_by_file_id(
        ctx: NewMessageCtx,
        file_id: str | int,
        caption: str | formattedText = "",
        file_type: str = "document",
        reply_markup: Optional[ReplyMarkup] = None,
    ) -> Optional[message]:
        """Send a file by its Telegram file_id (from Telegram's servers, not local disk)

        Use this when you have stored a file_id in your database and want to re-send it.

        Args:
            ctx: Context object
            file_id: Telegram file_id (string for remote, int for local TDLib ID)
            caption: Caption text or formattedText
            file_type: "photo", "video", "audio", "document", "voice", "animation"
            reply_markup: Optional inline keyboard

        Returns:
            Sent message object or None on failure

        Examples:
            # Send by remote file_id string (from database)
            await FileHelper.send_by_file_id(ctx, "AgACAgIAAxk...", file_type="photo")

            # Send by internal TDLib file ID (int)
            await FileHelper.send_by_file_id(ctx, 123456789, file_type="video")
        """
        try:
            # Build inputFile based on type
            if isinstance(file_id, str):
                input_file = inputFileRemote(id=file_id)
            elif isinstance(file_id, int):
                input_file = inputFileId(id=file_id)
            else:
                logger.error(f"Invalid file_id type: {type(file_id)}")
                return None

            # Build caption
            if isinstance(caption, formattedText):
                caption_text = caption
            else:
                caption_text = formattedText(text=caption or "", entities=[])

            # Build inputMessageContent based on file_type
            content = FileHelper._build_content_from_input_file(input_file, file_type, caption_text)

            send_options = messageSendOptions(
                disable_notification=False,
                from_background=False
            )
            result = await send_message_base(
                ctx=ctx,
                chat_id=ctx.chat_id,
                topic_id=None,
                reply_to=None,
                options=send_options,
                reply_markup=reply_markup,
                input_message_content=content,
                wait_for_confirmation=True,
            )

            if isinstance(result, message) and getattr(result, 'sending_state', None) is not None:
                if isinstance(result.sending_state, messageSendingStateFailed):
                    err = getattr(getattr(result.sending_state, 'error', None), 'message', 'Unknown')
                    print(f"[FILEHELPER] SEND_BY_ID FAILED: {err}")
                    return None

            logger.info(f"Sent file by ID: {file_id} ({file_type})")
            return result

        except (asyncio.TimeoutError, RuntimeError) as e:
            print(f"[FILEHELPER SEND_BY_ID ERROR] {type(e).__name__}: {e}")
            logger.error(f"Failed to send file by ID: {e}")
            return None

    @staticmethod
    def _build_content_from_input_file(input_file, file_type: str, caption: formattedText) -> InputMessageContent:
        """Build inputMessageContent from an inputFile (remote or local ID)."""
        if file_type == "photo":
            return inputMessagePhoto(
                photo=inputPhoto(photo=input_file, width=1, height=1),
                caption=caption,
                has_spoiler=False
            )
        elif file_type == "video":
            return inputMessageVideo(
                video=inputVideo(video=input_file, width=1, height=1, duration=1),
                caption=caption,
                has_spoiler=False
            )
        elif file_type == "audio":
            return inputMessageAudio(
                audio=inputAudio(audio=input_file, duration=1),
                caption=caption
            )
        elif file_type == "voice":
            return inputMessageVoiceNote(
                voice_note=input_file,
                duration=1,
                waveform=b""
            )
        elif file_type == "animation":
            return inputMessageAnimation(
                animation=inputAnimation(animation=input_file, width=1, height=1, duration=1),
                caption=caption,
                has_spoiler=False
            )
        else:
            return inputMessageDocument(
                document=input_file,
                caption=caption
            )

    @staticmethod
    def _build_content(file_path: str, file_type: str, caption: formattedText) -> InputMessageContent:
        """Build inputMessageContent from local file path."""
        from grathon.core.TLSchema_Manager.tltypes import (
            inputMessagePhoto, inputMessageVideo, inputMessageAudio,
            inputMessageDocument, inputMessageSticker,
            inputMessageVoiceNote, inputMessageAnimation,
            inputFileLocal
        )

        if file_type == "photo":
            return inputMessagePhoto(
                photo=inputPhoto(
                    photo=inputFileLocal(path=file_path),
                    width=1,
                    height=1
                ),
                caption=caption,
                has_spoiler=False
            )
        elif file_type == "video":
            return inputMessageVideo(
                video=inputVideo(
                    video=inputFileLocal(path=file_path),
                    width=1,
                    height=1,
                    duration=1
                ),
                caption=caption,
                has_spoiler=False
            )
        elif file_type == "audio":
            return inputMessageAudio(
                audio=inputAudio(
                    audio=inputFileLocal(path=file_path),
                    duration=1
                ),
                caption=caption
            )
        elif file_type == "sticker":
            return inputMessageSticker(
                sticker=inputFileLocal(path=file_path),
                width=1,
                height=1,
                emoji=""
            )
        elif file_type == "voice":
            return inputMessageVoiceNote(
                voice_note=inputFileLocal(path=file_path),
                duration=1,
                waveform=b""
            )
        elif file_type == "animation":
            return inputMessageAnimation(
                animation=inputAnimation(
                    animation=inputFileLocal(path=file_path),
                    width=1,
                    height=1,
                    duration=1
                ),
                caption=caption,
                has_spoiler=False
            )
        else:
            return inputMessageDocument(
                document=inputFileLocal(path=file_path),
                caption=caption
            )

    @staticmethod
    async def download_file(
        ctx: NewMessageCtx,
        file_id: int,
        output_path: str = "",
        priority: int = 32
    ) -> Optional[str]:
        """
        Download file from Telegram via TDLib
        """
        try:
            file_result = await ctx.api.download_file(
                file_id=file_id,
                priority=priority,
                offset=0,
                limit=0,
                synchronous=True
            )

            local_path = file_result.local.path

            if output_path:
                output_abs = os.path.abspath(output_path)
                os.makedirs(os.path.dirname(output_abs), exist_ok=True)
                shutil.copy(local_path, output_abs)
                logger.info(f"Downloaded file to: {output_abs}")
                return output_abs
            else:
                logger.info(f"Downloaded file to TDLib cache: {local_path}")
                return local_path

        except (asyncio.TimeoutError, OSError, RuntimeError) as e:
            logger.error(f"Failed to download file: {e}")
            return None

    @staticmethod
    def get_file_extension(file_path: str) -> str:
        _, ext = os.path.splitext(file_path)
        return ext.lower().lstrip(".")

    @staticmethod
    def get_file_size(file_path: str) -> int | None:
        try:
            return os.path.getsize(file_path)
        except OSError:
            return None

    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024

        return f"{size_bytes:.1f} PB"

    @staticmethod
    def is_image(file_path: str) -> bool:
        ext = FileHelper.get_file_extension(file_path)
        return ext in ["jpg", "jpeg", "png", "gif", "webp", "bmp"]

    @staticmethod
    def is_video(file_path: str) -> bool:
        ext = FileHelper.get_file_extension(file_path)
        return ext in ["mp4", "mov", "avi", "mkv", "flv", "wmv", "webm"]

    @staticmethod
    def is_audio(file_path: str) -> bool:
        ext = FileHelper.get_file_extension(file_path)
        return ext in ["mp3", "wav", "flac", "aac", "ogg", "m4a"]

    @staticmethod
    def is_document(file_path: str) -> bool:
        ext = FileHelper.get_file_extension(file_path)
        return ext in ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt"]
