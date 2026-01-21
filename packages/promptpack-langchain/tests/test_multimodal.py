# Copyright 2025 Altaira Labs
# SPDX-License-Identifier: Apache-2.0

"""Tests for multimodal content conversion."""

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from promptpack import ContentPart, MediaReference
from promptpack_langchain import convert_content_parts, create_multimodal_message


class TestConvertContentParts:
    """Tests for convert_content_parts function."""

    def test_text_content(self) -> None:
        """Test converting text content."""
        parts = [ContentPart(type="text", text="Hello world")]
        result = convert_content_parts(parts)

        assert len(result) == 1
        assert result[0]["type"] == "text"
        assert result[0]["text"] == "Hello world"

    def test_empty_text_content(self) -> None:
        """Test converting text content with None text."""
        parts = [ContentPart(type="text")]
        result = convert_content_parts(parts)

        assert len(result) == 1
        assert result[0]["type"] == "text"
        assert result[0]["text"] == ""

    def test_image_with_url(self) -> None:
        """Test converting image with URL."""
        parts = [
            ContentPart(
                type="image",
                media=MediaReference(
                    url="https://example.com/image.jpg",
                    mime_type="image/jpeg",
                ),
            )
        ]
        result = convert_content_parts(parts)

        assert len(result) == 1
        assert result[0]["type"] == "image_url"
        assert result[0]["image_url"]["url"] == "https://example.com/image.jpg"

    def test_image_with_base64(self) -> None:
        """Test converting image with base64 data."""
        parts = [
            ContentPart(
                type="image",
                media=MediaReference(
                    base64="abc123",
                    mime_type="image/png",
                ),
            )
        ]
        result = convert_content_parts(parts)

        assert len(result) == 1
        assert result[0]["type"] == "image_url"
        assert result[0]["image_url"]["url"] == "data:image/png;base64,abc123"

    def test_image_with_detail(self) -> None:
        """Test converting image with detail level."""
        parts = [
            ContentPart(
                type="image",
                media=MediaReference(
                    url="https://example.com/image.jpg",
                    mime_type="image/jpeg",
                    detail="high",
                ),
            )
        ]
        result = convert_content_parts(parts)

        assert result[0]["image_url"]["detail"] == "high"

    def test_image_with_file_path(self) -> None:
        """Test converting image with file path."""
        parts = [
            ContentPart(
                type="image",
                media=MediaReference(
                    file_path="/path/to/image.jpg",
                    mime_type="image/jpeg",
                ),
            )
        ]
        result = convert_content_parts(parts)

        assert result[0]["image_url"]["url"] == "file:///path/to/image.jpg"

    def test_image_missing_media(self) -> None:
        """Test converting image without media reference is skipped."""
        parts = [ContentPart(type="image")]
        result = convert_content_parts(parts)
        # Images without media are skipped (no fallback added)
        assert len(result) == 0

    def test_image_missing_media_with_text(self) -> None:
        """Test converting image without media but with text fallback."""
        parts = [ContentPart(type="image", text="[Placeholder image]")]
        result = convert_content_parts(parts)
        # Falls through to the else case which adds text if available
        assert len(result) == 1
        assert result[0]["type"] == "text"
        assert result[0]["text"] == "[Placeholder image]"

    def test_audio_with_url(self) -> None:
        """Test converting audio with URL."""
        parts = [
            ContentPart(
                type="audio",
                media=MediaReference(
                    url="https://example.com/audio.mp3",
                    mime_type="audio/mpeg",
                ),
            )
        ]
        result = convert_content_parts(parts)

        assert len(result) == 1
        assert result[0]["type"] == "audio"
        assert result[0]["audio_url"]["url"] == "https://example.com/audio.mp3"

    def test_audio_with_base64(self) -> None:
        """Test converting audio with base64 data."""
        parts = [
            ContentPart(
                type="audio",
                media=MediaReference(
                    base64="audio_data",
                    mime_type="audio/wav",
                ),
            )
        ]
        result = convert_content_parts(parts)

        assert result[0]["audio_data"]["data"] == "audio_data"
        assert result[0]["audio_data"]["mime_type"] == "audio/wav"

    def test_video_with_url(self) -> None:
        """Test converting video with URL."""
        parts = [
            ContentPart(
                type="video",
                media=MediaReference(
                    url="https://example.com/video.mp4",
                    mime_type="video/mp4",
                ),
            )
        ]
        result = convert_content_parts(parts)

        assert len(result) == 1
        assert result[0]["type"] == "video"
        assert result[0]["video_url"]["url"] == "https://example.com/video.mp4"

    def test_multiple_parts(self) -> None:
        """Test converting multiple content parts."""
        parts = [
            ContentPart(type="text", text="Check this image:"),
            ContentPart(
                type="image",
                media=MediaReference(
                    url="https://example.com/image.jpg",
                    mime_type="image/jpeg",
                ),
            ),
            ContentPart(type="text", text="What do you see?"),
        ]
        result = convert_content_parts(parts)

        assert len(result) == 3
        assert result[0]["type"] == "text"
        assert result[1]["type"] == "image_url"
        assert result[2]["type"] == "text"

    def test_unknown_type_with_text(self) -> None:
        """Test unknown content type with text fallback."""
        parts = [ContentPart(type="unknown", text="Fallback text")]  # type: ignore[arg-type]
        result = convert_content_parts(parts)

        assert len(result) == 1
        assert result[0]["type"] == "text"
        assert result[0]["text"] == "Fallback text"


class TestCreateMultimodalMessage:
    """Tests for create_multimodal_message function."""

    def test_single_text_returns_string(self) -> None:
        """Test single text part returns simple string content."""
        parts = [ContentPart(type="text", text="Hello")]
        message = create_multimodal_message("user", parts)

        assert isinstance(message, HumanMessage)
        assert message.content == "Hello"

    def test_human_message(self) -> None:
        """Test creating human message."""
        parts = [ContentPart(type="text", text="Question")]
        message = create_multimodal_message("user", parts)

        assert isinstance(message, HumanMessage)

    def test_ai_message(self) -> None:
        """Test creating AI message."""
        parts = [ContentPart(type="text", text="Answer")]
        message = create_multimodal_message("assistant", parts)

        assert isinstance(message, AIMessage)

    def test_system_message(self) -> None:
        """Test creating system message."""
        parts = [ContentPart(type="text", text="Instructions")]
        message = create_multimodal_message("system", parts)

        assert isinstance(message, SystemMessage)

    def test_multimodal_content_returns_list(self) -> None:
        """Test multimodal content returns list of content parts."""
        parts = [
            ContentPart(type="text", text="Check this:"),
            ContentPart(
                type="image",
                media=MediaReference(
                    url="https://example.com/image.jpg",
                    mime_type="image/jpeg",
                ),
            ),
        ]
        message = create_multimodal_message("user", parts)

        assert isinstance(message, HumanMessage)
        assert isinstance(message.content, list)
        assert len(message.content) == 2

    def test_default_to_human_message(self) -> None:
        """Test unknown role defaults to human message."""
        parts = [ContentPart(type="text", text="Text")]
        message = create_multimodal_message("unknown", parts)

        assert isinstance(message, HumanMessage)
