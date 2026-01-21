# Copyright 2025 Altaira Labs
# SPDX-License-Identifier: Apache-2.0

"""Multimodal content conversion for LangChain."""

from __future__ import annotations

from typing import Any

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from promptpack import ContentPart


def convert_content_parts(parts: list[ContentPart]) -> list[dict[str, Any]]:
    """Convert PromptPack content parts to LangChain message content format.

    LangChain uses a list of dicts for multimodal content, with each dict
    having a "type" key and type-specific content keys.

    Args:
        parts: List of PromptPack ContentPart objects.

    Returns:
        List of content dicts in LangChain format.
    """
    result = []

    for part in parts:
        if part.type == "text":
            result.append({
                "type": "text",
                "text": part.text or "",
            })
        elif part.type == "image" and part.media:
            result.append(_convert_image_part(part))
        elif part.type == "audio" and part.media:
            result.append(_convert_audio_part(part))
        elif part.type == "video" and part.media:
            result.append(_convert_video_part(part))
        else:
            # Unknown or unsupported type - include as text if available
            if part.text:
                result.append({
                    "type": "text",
                    "text": part.text,
                })

    return result


def _convert_image_part(part: ContentPart) -> dict[str, Any]:
    """Convert an image content part to LangChain format.

    Args:
        part: The ContentPart with image media.

    Returns:
        LangChain image content dict.
    """
    media = part.media
    if media is None:
        return {"type": "text", "text": "[missing image]"}

    # LangChain expects image_url format
    image_content: dict[str, Any] = {"type": "image_url"}

    if media.url:
        image_content["image_url"] = {"url": media.url}
    elif media.base64:
        # Format: data:mime_type;base64,data
        data_url = f"data:{media.mime_type};base64,{media.base64}"
        image_content["image_url"] = {"url": data_url}
    elif media.file_path:
        # File path needs to be resolved by the caller before conversion
        image_content["image_url"] = {"url": f"file://{media.file_path}"}

    # Add detail level if specified
    if media.detail and "image_url" in image_content:
        image_content["image_url"]["detail"] = media.detail

    return image_content


def _convert_audio_part(part: ContentPart) -> dict[str, Any]:
    """Convert an audio content part to LangChain format.

    Args:
        part: The ContentPart with audio media.

    Returns:
        LangChain audio content dict.
    """
    media = part.media
    if media is None:
        return {"type": "text", "text": "[missing audio]"}

    audio_content: dict[str, Any] = {"type": "audio"}

    if media.url:
        audio_content["audio_url"] = {"url": media.url}
    elif media.base64:
        audio_content["audio_data"] = {
            "data": media.base64,
            "mime_type": media.mime_type,
        }
    elif media.file_path:
        audio_content["audio_url"] = {"url": f"file://{media.file_path}"}

    return audio_content


def _convert_video_part(part: ContentPart) -> dict[str, Any]:
    """Convert a video content part to LangChain format.

    Args:
        part: The ContentPart with video media.

    Returns:
        LangChain video content dict.
    """
    media = part.media
    if media is None:
        return {"type": "text", "text": "[missing video]"}

    video_content: dict[str, Any] = {"type": "video"}

    if media.url:
        video_content["video_url"] = {"url": media.url}
    elif media.base64:
        video_content["video_data"] = {
            "data": media.base64,
            "mime_type": media.mime_type,
        }
    elif media.file_path:
        video_content["video_url"] = {"url": f"file://{media.file_path}"}

    return video_content


def create_multimodal_message(
    role: str,
    parts: list[ContentPart],
) -> HumanMessage | AIMessage | SystemMessage:
    """Create a LangChain message from multimodal content parts.

    Args:
        role: Message role ("user", "assistant", "system").
        parts: List of content parts.

    Returns:
        A LangChain message with multimodal content.
    """
    content = convert_content_parts(parts)

    # If single text content, use simple string
    if len(content) == 1 and content[0].get("type") == "text":
        content = content[0]["text"]  # type: ignore[assignment]

    if role == "assistant":
        return AIMessage(content=content)
    if role == "system":
        return SystemMessage(content=content)
    # Default to human message
    return HumanMessage(content=content)
