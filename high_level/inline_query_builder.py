"""Fluent builder for inline query results"""

from typing import Optional, List
from grathon.core.TLSchema_Manager.tltypes import (
    InputInlineQueryResult,
    inputInlineQueryResultArticle,
    inputInlineQueryResultPhoto,
    inputInlineQueryResultVideo,
    inputInlineQueryResultAudio,
    inputInlineQueryResultDocument,
    inputInlineQueryResultVoiceNote,
    inputInlineQueryResultAnimation,
    inputInlineQueryResultContact,
    inputInlineQueryResultLocation,
    inputInlineQueryResultVenue,
    inputInlineQueryResultSticker,
    inputInlineQueryResultGame,
    contact,
    location,
    venue,
    inputMessageText,
    inputMessageLocation,
    inputMessageVenue,
    inputMessageContact,
    formattedText,
)


class InlineQueryResultBuilder:
    """Fluent builder for creating inline query results

    Usage:
        builder = (InlineQueryResultBuilder()
            .article("1", "Title", "https://example.com", "Description")
            .photo("2", "https://example.com/image.jpg")
            .row()
            .video("3", "https://example.com/video.mp4", "video/mp4")
            .build())
    """

    def __init__(self):
        self._results: List[InputInlineQueryResult] = []
        self._current_row: List[InputInlineQueryResult] = []

    def article(
        self,
        id: str,
        title: str,
        url: str,
        description: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        thumbnail_width: Optional[int] = None,
        thumbnail_height: Optional[int] = None,
        message_text: Optional[str] = None,
    ) -> "InlineQueryResultBuilder":
        """Add an article result (web page)

        Args:
            id: Unique identifier for this result
            title: Title of the article
            url: URL of the article
            description: Optional description
            thumbnail_url: URL of thumbnail image
            thumbnail_width: Width of thumbnail
            thumbnail_height: Height of thumbnail
            message_text: Text to send when result is selected (if None, title + description will be used)
        """
        if message_text is None:
            if description:
                message_text = f"{title}\n{description}"
            else:
                message_text = title

        input_message_content = inputMessageText(
            text=formattedText(text=message_text, entities=None)
        )

        result = inputInlineQueryResultArticle(
            id=id,
            url=url,
            title=title,
            description=description,
            thumbnail_url=thumbnail_url,
            thumbnail_width=thumbnail_width,
            thumbnail_height=thumbnail_height,
            input_message_content=input_message_content,
        )
        self._current_row.append(result)
        return self

    def photo(
        self,
        id: str,
        photo_url: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        photo_width: Optional[int] = None,
        photo_height: Optional[int] = None,
        message_text: Optional[str] = None,
    ) -> "InlineQueryResultBuilder":
        """Add a photo result

        Args:
            id: Unique identifier for this result
            photo_url: URL of the photo
            title: Optional title
            description: Optional description
            thumbnail_url: URL of thumbnail
            photo_width: Width of photo
            photo_height: Height of photo
            message_text: Text to send when result is selected (if None, title + description will be used)
        """
        if message_text is None:
            if description:
                message_text = f"{title or 'Photo'}\n{description}"
            else:
                message_text = title or "Photo"

        if thumbnail_url is None:
            thumbnail_url = photo_url

        input_message_content = inputMessageText(
            text=formattedText(text=message_text, entities=None)
        )

        result = inputInlineQueryResultPhoto(
            id=id,
            photo_url=photo_url,
            title=title,
            description=description,
            thumbnail_url=thumbnail_url,
            photo_width=photo_width,
            photo_height=photo_height,
            input_message_content=input_message_content,
        )
        self._current_row.append(result)
        return self

    def video(
        self,
        id: str,
        video_url: str,
        mime_type: str = "video/mp4",
        title: Optional[str] = None,
        description: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        video_width: Optional[int] = None,
        video_height: Optional[int] = None,
        video_duration: Optional[int] = None,
        message_text: Optional[str] = None,
    ) -> "InlineQueryResultBuilder":
        """Add a video result

        Args:
            id: Unique identifier for this result
            video_url: URL of the video
            mime_type: MIME type (default: "video/mp4")
            title: Optional title
            description: Optional description
            thumbnail_url: URL of thumbnail
            video_width: Width of video
            video_height: Height of video
            video_duration: Duration in seconds
            message_text: Text to send when result is selected (if None, title + description will be used)
        """
        if message_text is None:
            if description:
                message_text = f"{title or 'Video'}\n{description}"
            else:
                message_text = title or "Video"

        if thumbnail_url is None:
            thumbnail_url = video_url

        input_message_content = inputMessageText(
            text=formattedText(text=message_text, entities=None)
        )

        result = inputInlineQueryResultVideo(
            id=id,
            video_url=video_url,
            mime_type=mime_type,
            title=title,
            description=description,
            thumbnail_url=thumbnail_url,
            video_width=video_width,
            video_height=video_height,
            video_duration=video_duration,
            input_message_content=input_message_content,
        )
        self._current_row.append(result)
        return self

    def audio(
        self,
        id: str,
        audio_url: str,
        title: Optional[str] = None,
        performer: Optional[str] = None,
        audio_duration: Optional[int] = None,
        message_text: Optional[str] = None,
    ) -> "InlineQueryResultBuilder":
        """Add an audio result

        Args:
            id: Unique identifier for this result
            audio_url: URL of the audio file
            title: Optional title
            performer: Optional performer name
            audio_duration: Duration in seconds
            message_text: Text to send when result is selected (if None, title + performer will be used)
        """
        if message_text is None:
            parts = []
            if title:
                parts.append(title)
            if performer:
                parts.append(performer)
            message_text = "\n".join(parts) if parts else "Audio"

        input_message_content = inputMessageText(
            text=formattedText(text=message_text, entities=None)
        )

        result = inputInlineQueryResultAudio(
            id=id,
            audio_url=audio_url,
            title=title,
            performer=performer,
            audio_duration=audio_duration,
            input_message_content=input_message_content,
        )
        self._current_row.append(result)
        return self

    def document(
        self,
        id: str,
        document_url: str,
        mime_type: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        thumbnail_width: Optional[int] = None,
        thumbnail_height: Optional[int] = None,
        message_text: Optional[str] = None,
    ) -> "InlineQueryResultBuilder":
        """Add a document result

        Args:
            id: Unique identifier for this result
            document_url: URL of the document
            mime_type: MIME type of the document
            title: Optional title
            description: Optional description
            thumbnail_url: URL of thumbnail
            thumbnail_width: Width of thumbnail
            thumbnail_height: Height of thumbnail
            message_text: Text to send when result is selected (if None, title + description will be used)
        """
        if message_text is None:
            if description:
                message_text = f"{title or 'Document'}\n{description}"
            else:
                message_text = title or "Document"

        input_message_content = inputMessageText(
            text=formattedText(text=message_text, entities=None)
        )

        result = inputInlineQueryResultDocument(
            id=id,
            document_url=document_url,
            mime_type=mime_type,
            title=title,
            description=description,
            thumbnail_url=thumbnail_url,
            thumbnail_width=thumbnail_width,
            thumbnail_height=thumbnail_height,
            input_message_content=input_message_content,
        )
        self._current_row.append(result)
        return self

    def voice_note(
        self,
        id: str,
        voice_note_url: str,
        title: Optional[str] = None,
        voice_note_duration: Optional[int] = None,
        message_text: Optional[str] = None,
    ) -> "InlineQueryResultBuilder":
        """Add a voice note result

        Args:
            id: Unique identifier for this result
            voice_note_url: URL of the voice note (OGG/opus)
            title: Optional title
            voice_note_duration: Duration in seconds
            message_text: Text to send when result is selected
        """
        if message_text is None:
            message_text = title or "Voice Note"

        input_message_content = inputMessageText(
            text=formattedText(text=message_text, entities=None)
        )

        result = inputInlineQueryResultVoiceNote(
            id=id,
            voice_note_url=voice_note_url,
            title=title,
            voice_note_duration=voice_note_duration,
            input_message_content=input_message_content,
        )
        self._current_row.append(result)
        return self

    def animation(
        self,
        id: str,
        video_url: str,
        thumbnail_url: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        video_width: Optional[int] = None,
        video_height: Optional[int] = None,
        video_duration: Optional[int] = None,
        message_text: Optional[str] = None,
    ) -> "InlineQueryResultBuilder":
        """Add an animation (GIF) result

        Args:
            id: Unique identifier for this result
            video_url: URL of the animation
            thumbnail_url: URL of thumbnail
            title: Optional title
            description: Optional description
            video_width: Width of animation
            video_height: Height of animation
            video_duration: Duration in seconds
            message_text: Text to send when result is selected
        """
        if message_text is None:
            if description:
                message_text = f"{title or 'Animation'}\n{description}"
            else:
                message_text = title or "Animation"

        if thumbnail_url is None:
            thumbnail_url = video_url

        input_message_content = inputMessageText(
            text=formattedText(text=message_text, entities=None)
        )

        result = inputInlineQueryResultAnimation(
            id=id,
            video_url=video_url,
            thumbnail_url=thumbnail_url,
            title=title,
            video_mime_type="video/mp4",
            video_width=video_width,
            video_height=video_height,
            video_duration=video_duration,
            thumbnail_mime_type="image/jpeg",
            input_message_content=input_message_content,
        )
        self._current_row.append(result)
        return self

    def contact(
        self,
        id: str,
        phone_number: str,
        first_name: str,
        last_name: Optional[str] = None,
        vcard: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        thumbnail_width: Optional[int] = None,
        thumbnail_height: Optional[int] = None,
    ) -> "InlineQueryResultBuilder":
        """Add a contact result

        Args:
            id: Unique identifier for this result
            phone_number: Contact phone number
            first_name: Contact first name
            last_name: Optional last name
            vcard: Optional vCard data
            thumbnail_url: URL of thumbnail
            thumbnail_width: Width of thumbnail
            thumbnail_height: Height of thumbnail
        """
        contact_obj = contact(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            vcard=vcard,
        )

        input_message_content = inputMessageContact(
            contact=contact_obj
        )

        result = inputInlineQueryResultContact(
            id=id,
            contact=contact_obj,
            thumbnail_url=thumbnail_url,
            thumbnail_width=thumbnail_width,
            thumbnail_height=thumbnail_height,
            input_message_content=input_message_content,
        )
        self._current_row.append(result)
        return self

    def location(
        self,
        id: str,
        latitude: float,
        longitude: float,
        title: Optional[str] = None,
        live_period: Optional[int] = None,
        thumbnail_url: Optional[str] = None,
        thumbnail_width: Optional[int] = None,
        thumbnail_height: Optional[int] = None,
    ) -> "InlineQueryResultBuilder":
        """Add a location result

        Args:
            id: Unique identifier for this result
            latitude: Location latitude
            longitude: Location longitude
            title: Optional title
            live_period: Optional live period in seconds
            thumbnail_url: URL of thumbnail
            thumbnail_width: Width of thumbnail
            thumbnail_height: Height of thumbnail
        """
        location_obj = location(latitude=latitude, longitude=longitude)

        input_message_content = inputMessageLocation(
            location=location_obj,
            live_period=live_period,
        )

        result = inputInlineQueryResultLocation(
            id=id,
            location=location_obj,
            title=title,
            live_period=live_period,
            thumbnail_url=thumbnail_url,
            thumbnail_width=thumbnail_width,
            thumbnail_height=thumbnail_height,
            input_message_content=input_message_content,
        )
        self._current_row.append(result)
        return self

    def venue(
        self,
        id: str,
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        provider: Optional[str] = None,
        venue_id: Optional[str] = None,
        venue_type: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        thumbnail_width: Optional[int] = None,
        thumbnail_height: Optional[int] = None,
    ) -> "InlineQueryResultBuilder":
        """Add a venue result

        Args:
            id: Unique identifier for this result
            latitude: Venue latitude
            longitude: Venue longitude
            title: Venue title
            address: Venue address
            provider: Optional map provider (e.g. "foursquare", "gplaces")
            venue_id: Optional provider venue ID
            venue_type: Optional venue type in provider database
            thumbnail_url: URL of thumbnail
            thumbnail_width: Width of thumbnail
            thumbnail_height: Height of thumbnail
        """
        location_obj = location(latitude=latitude, longitude=longitude)
        venue_obj = venue(
            location=location_obj,
            title=title,
            address=address,
            provider=provider,
            id=venue_id,
            type=venue_type,
        )

        input_message_content = inputMessageVenue(
            venue=venue_obj
        )

        result = inputInlineQueryResultVenue(
            id=id,
            venue=venue_obj,
            thumbnail_url=thumbnail_url,
            thumbnail_width=thumbnail_width,
            thumbnail_height=thumbnail_height,
            input_message_content=input_message_content,
        )
        self._current_row.append(result)
        return self

    def sticker(
        self,
        id: str,
        sticker_url: str,
        thumbnail_url: Optional[str] = None,
        sticker_width: Optional[int] = None,
        sticker_height: Optional[int] = None,
    ) -> "InlineQueryResultBuilder":
        """Add a sticker result

        Args:
            id: Unique identifier for this result
            sticker_url: URL of the sticker (WebP, TGS, or WebM)
            thumbnail_url: URL of thumbnail
            sticker_width: Width of sticker
            sticker_height: Height of sticker
        """
        if thumbnail_url is None:
            thumbnail_url = sticker_url

        input_message_content = inputMessageText(
            text=formattedText(text="Sticker", entities=None)
        )

        result = inputInlineQueryResultSticker(
            id=id,
            sticker_url=sticker_url,
            thumbnail_url=thumbnail_url,
            sticker_width=sticker_width,
            sticker_height=sticker_height,
            input_message_content=input_message_content,
        )
        self._current_row.append(result)
        return self

    def game(
        self,
        id: str,
        game_short_name: str,
    ) -> "InlineQueryResultBuilder":
        """Add a game result

        Args:
            id: Unique identifier for this result
            game_short_name: Short name of the game
        """
        result = inputInlineQueryResultGame(
            id=id,
            game_short_name=game_short_name,
        )
        self._current_row.append(result)
        return self

    def row(self) -> "InlineQueryResultBuilder":
        """Finish the current row and start a new one

        In inline queries, all results are typically shown in a single column,
        but this method allows logical grouping of results.
        """
        if self._current_row:
            self._results.extend(self._current_row)
            self._current_row = []
        return self

    def build(self) -> List[InputInlineQueryResult]:
        """Build and return the list of results

        Examples:
            results = builder.article(...).photo(...).build()
            await ctx.answer_results(results)
        """
        self.row()  # Flush remaining results
        return self._results
