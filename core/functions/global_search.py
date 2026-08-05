"""
Global search across chats, channels, and messages

Provides comprehensive search functionality for:
- Public channels and chats
- User's existing chats
- Messages across all chats
- Combined results with proper formatting
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Dict, List, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from grathon.core.contexts.context import Context


@dataclass
class SearchResult:
    """Container for search results"""
    chats: List[Dict[str, Any]] = None
    channels: List[Dict[str, Any]] = None
    messages: List[Dict[str, Any]] = None
    users: List[Dict[str, Any]] = None
    total_count: int = 0

    def __post_init__(self):
        if self.chats is None:
            self.chats = []
        if self.channels is None:
            self.channels = []
        if self.messages is None:
            self.messages = []
        if self.users is None:
            self.users = []


async def search_public_chats(
    ctx: 'Context',
    query: str,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """
    Search public chats and channels by name or username

    Args:
        ctx: Context object
        query: Search query string
        limit: Maximum results to return (default: 10)

    Returns:
        List of public chat objects with basic info including username and link
    """
    try:
        result = await ctx.api.search_public_chats(query=query)

        chats = []
        if result:
            # Try to get chat_ids from result
            if hasattr(result, 'chat_ids'):
                chat_ids = result.chat_ids[:limit]
            else:
                chat_ids = []

            for chat_id in chat_ids:
                try:
                    chat = await ctx.api.get_chat(chat_id=chat_id)
                    if chat:
                        chat_id_val = getattr(chat, 'id', '?')
                        chat_title = getattr(chat, 'title', '?')
                        chat_type = type(chat.type).__name__ if hasattr(chat, 'type') else '?'

                        logger.debug(f"[SEARCH DEBUG] Chat: {chat_title} (ID: {chat_id_val}, Type: {chat_type})")

                        # Extract username if available
                        username = ""

                        # Check if this is a supergroup or channel by type name
                        is_supergroup = 'supergroup' in chat_type.lower() or 'channel' in chat_type.lower()
                        logger.debug(f"  - Is supergroup/channel: {is_supergroup}")

                        # For Supergroup/Channel, try to get the actual supergroup/channel object
                        if is_supergroup and hasattr(chat, 'type'):
                            logger.debug(f"  - Trying supergroup/channel API...")
                            chat_type_obj = chat.type  # type: ignore

                            # Try to get supergroup_id or channel_id
                            sg_id = None
                            if hasattr(chat_type_obj, 'supergroup_id'):
                                sg_id = chat_type_obj.supergroup_id  # type: ignore
                                logger.debug(f"    - supergroup_id: {sg_id}")
                            elif hasattr(chat_type_obj, 'channel_id'):
                                sg_id = chat_type_obj.channel_id  # type: ignore
                                logger.debug(f"    - channel_id: {sg_id}")

                            if sg_id:
                                try:
                                    # Try regular supergroup info first
                                    sg = await ctx.api.get_supergroup(supergroup_id=sg_id)  # type: ignore
                                    logger.debug(f"    - Got supergroup object")
                                    if sg:
                                        logger.debug(f"    - Supergroup object attributes: {[attr for attr in dir(sg) if not attr.startswith('_')]}")
                                        if hasattr(sg, 'username') and sg.username:
                                            username = sg.username
                                            logger.debug(f"    - ✓ Got username from sg.username: {username}")
                                        # Try usernames object (has active_usernames, editable_username, etc)
                                        elif hasattr(sg, 'usernames') and sg.usernames:  # type: ignore
                                            usernames_obj = sg.usernames  # type: ignore
                                            logger.debug(f"    - Has usernames object: {usernames_obj}")

                                            # Try active_usernames first
                                            if hasattr(usernames_obj, 'active_usernames') and usernames_obj.active_usernames:
                                                active_list = usernames_obj.active_usernames  # type: ignore
                                                if isinstance(active_list, list) and len(active_list) > 0:
                                                    username = active_list[0]
                                                    logger.debug(f"    - ✓ Got username from active_usernames: {username}")

                                            # Try editable_username as fallback
                                            elif hasattr(usernames_obj, 'editable_username') and usernames_obj.editable_username:
                                                username = usernames_obj.editable_username  # type: ignore
                                                logger.debug(f"    - ✓ Got username from editable_username: {username}")

                                    # Try full info as fallback
                                    if not username:
                                        logger.debug(f"    - Trying full info...")
                                        sg_full = await ctx.api.get_supergroup_full_info(supergroup_id=sg_id)  # type: ignore
                                        logger.debug(f"    - Got full info object")
                                        if sg_full:
                                            logger.debug(f"    - Full info attributes: {[attr for attr in dir(sg_full) if not attr.startswith('_')]}")
                                            if hasattr(sg_full, 'username'):
                                                username = getattr(sg_full, 'username', '') or ''
                                                logger.debug(f"    - ✓ Got username from full info: {username}")
                                except Exception as e:
                                    logger.debug(f"    - ✗ Error getting supergroup: {e}")
                        else:
                            # Try to get username from chat object directly
                            if hasattr(chat, 'username'):
                                logger.debug(f"  - Has 'username' attr: {chat.username}")
                                if chat.username:
                                    username = chat.username
                            else:
                                logger.debug(f"  - No 'username' attr")

                            # If no username, try usernames property (list)
                            if not username and hasattr(chat, 'usernames'):
                                logger.debug(f"  - Has 'usernames' attr (list)")
                                usernames = chat.usernames  # type: ignore
                                if usernames and isinstance(usernames, list) and len(usernames) > 0:
                                    first = usernames[0]
                                    logger.debug(f"    - First item type: {type(first)}")
                                    if hasattr(first, 'username'):
                                        username = first.username  # type: ignore
                                        logger.debug(f"    - Got username from list item: {username}")
                                    elif isinstance(first, str):
                                        username = first
                                        logger.debug(f"    - Got username as string: {username}")

                        logger.debug(f"  - Final username: '{username}'")

                        # Build access link
                        link = ""
                        is_channel = hasattr(chat.type, '__class__') and 'Channel' in str(chat.type.__class__.__name__)

                        if username:
                            # Public chat with username - use direct link
                            link = f"https://t.me/{username}"
                        else:
                            # Try to get invite link if available
                            if hasattr(chat, 'invite_link') and chat.invite_link:  # type: ignore
                                link = chat.invite_link  # type: ignore
                            else:
                                # Mark as private/no public access link
                                link = "[Private - no username]"

                        chats.append({
                            'id': chat.id,
                            'title': chat.title,
                            'type': type(chat.type).__name__,
                            'is_channel': is_channel,
                            'username': username,
                            'link': link,
                            'members_count': chat.member_count if hasattr(chat, 'member_count') else 0,
                        })
                except Exception as e:
                    pass

        return chats
    except Exception as e:
        print(f"Error searching public chats: {e}")
        return []


async def search_user_chats(
    ctx: 'Context',
    query: str,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """
    Search through user's existing chats

    Args:
        ctx: Context object
        query: Search query string
        limit: Maximum results to return (default: 10)

    Returns:
        List of chat objects that match the query
    """
    try:
        result = await ctx.api.search_chats(query=query, limit=limit)

        chats = []
        if result and hasattr(result, 'chat_ids'):
            for chat_id in result.chat_ids:
                try:
                    chat = await ctx.api.get_chat(chat_id=chat_id)
                    if chat:
                        chats.append({
                            'id': chat.id,
                            'title': chat.title,
                            'type': type(chat.type).__name__,
                            'unread_count': chat.unread_count if hasattr(chat, 'unread_count') else 0,
                        })
                except Exception:
                    pass

        return chats
    except Exception as e:
        print(f"Error searching user chats: {e}")
        return []


async def search_messages(
    ctx: 'Context',
    query: str,
    chat_id: Optional[int] = None,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """
    Search messages across chats

    Args:
        ctx: Context object
        query: Search query string
        chat_id: Optional - search only in specific chat (None = all chats)
        limit: Maximum results to return (default: 10)

    Returns:
        List of message objects with content info
    """
    try:
        if chat_id:
            # Search in specific chat
            result = await ctx.api.search_chat_messages(
                chat_id=chat_id,
                query=query,
                limit=limit
            )
        else:
            # Search globally (all chats)
            result = await ctx.api.search_messages(query=query, limit=limit)

        messages = []
        if result and hasattr(result, 'messages'):
            for msg in result.messages:
                if msg:
                    msg_info = {
                        'id': msg.id,
                        'chat_id': msg.chat_id if hasattr(msg, 'chat_id') else None,
                        'content_type': type(msg.content).__name__ if hasattr(msg, 'content') else 'unknown',
                    }

                    # Extract text content
                    if hasattr(msg, 'content'):
                        content = msg.content
                        if hasattr(content, 'text'):
                            msg_info['text'] = content.text.text if hasattr(content.text, 'text') else str(content.text)[:100]
                        elif hasattr(content, 'caption'):
                            msg_info['text'] = content.caption.text if hasattr(content.caption, 'text') else str(content.caption)[:100]

                    messages.append(msg_info)

        return messages
    except Exception as e:
        print(f"Error searching messages: {e}")
        return []


async def search_contacts(
    ctx: 'Context',
    query: str,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """
    Search through contacts by name or username

    Args:
        ctx: Context object
        query: Search query string
        limit: Maximum results to return (default: 10)

    Returns:
        List of user/contact objects
    """
    try:
        result = await ctx.api.search_contacts(query=query, limit=limit)

        users = []
        if result and hasattr(result, 'user_ids'):
            for user_id in result.user_ids:
                try:
                    user = await ctx.api.get_user(user_id=user_id)
                    if user:
                        users.append({
                            'id': user.id,
                            'first_name': user.first_name if hasattr(user, 'first_name') else '',
                            'last_name': user.last_name if hasattr(user, 'last_name') else '',
                            'username': user.username if hasattr(user, 'username') else '',
                        })
                except Exception:
                    pass

        return users
    except Exception as e:
        print(f"Error searching contacts: {e}")
        return []


async def global_search(
    ctx: 'Context',
    query: str,
    limit: int = 10,
    search_types: Optional[List[str]] = None,
) -> SearchResult:
    """
    Perform a comprehensive global search

    Searches across:
    - Public channels and chats
    - User's existing chats
    - Messages
    - Contacts

    Args:
        ctx: Context object
        query: Search query string
        limit: Maximum results per type (default: 10)
        search_types: List of types to search ('public', 'chats', 'messages', 'contacts')
                     None = search all types

    Returns:
        SearchResult object with organized results

    Examples:
        # Search everything
        results = await global_search(ctx, "python")

        # Search specific types
        results = await global_search(
            ctx, "bot",
            search_types=['public', 'chats']
        )
    """
    if search_types is None:
        search_types = ['public', 'chats', 'messages', 'contacts']

    result = SearchResult()

    # Search public channels
    if 'public' in search_types:
        result.channels = await search_public_chats(ctx, query, limit)

    # Search user's chats
    if 'chats' in search_types:
        result.chats = await search_user_chats(ctx, query, limit)

    # Search messages
    if 'messages' in search_types:
        result.messages = await search_messages(ctx, query, limit=limit)

    # Search contacts
    if 'contacts' in search_types:
        result.users = await search_contacts(ctx, query, limit)

    # Calculate total count
    result.total_count = (
        len(result.chats) +
        len(result.channels) +
        len(result.messages) +
        len(result.users)
    )

    return result
