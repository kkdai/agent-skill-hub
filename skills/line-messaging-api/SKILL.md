---
name: line-messaging-api
description: Use when building, debugging, or interacting with the LINE Messaging API (webhook events, signature verification, sending replies/broadcasts/multicasts, and managing rich menus).
---

# LINE Messaging API Reference

## Overview
This skill provides a structured reference for integrating and interacting with the LINE Messaging API. It covers common specifications, webhook handling, signature verification, message formats, and rich menu management.

## When to Use
- Implementing webhook endpoints to receive messages and event objects from the LINE Platform.
- Verifying the webhook request signatures (`x-line-signature`) for security.
- Sending reply, push, multicast, or broadcast messages.
- Fetching user profile information or downloading user-sent media content (images, videos, audio, files).
- Creating and managing rich menus (uploading images, linking/unlinking rich menus to users).

## Core Pattern
Always perform signature validation on incoming webhooks before processing events, and immediately return a `200 OK` response to the LINE Platform.

### Webhook Signature Validation (Python)
```python
import hmac
import hashlib
import base64

# Validate header 'x-line-signature'
channel_secret = "YOUR_CHANNEL_SECRET"
body = request_raw_body_string

hash = hmac.new(
    channel_secret.encode('utf-8'),
    body.encode('utf-8'),
    hashlib.sha256
).digest()

signature = base64.b64encode(hash).decode('utf-8')
# Compare signature with the request header (case-insensitive header keys)
is_valid = hmac.compare_digest(signature, request_headers.get('x-line-signature'))
```

## Quick Reference

### Domain Names
| Domain name | Purpose |
| --- | --- |
| `api.line.me` | Standard API endpoints (messages, profiles, rich menus, etc.) |
| `api-data.line.me` | Media data endpoints (downloads/uploads of messages, rich menu images, audience files) |

### Essential Endpoints
| API Endpoint | Method | Path | Description |
| :--- | :--- | :--- | :--- |
| **Send Reply** | `POST` | `/v2/bot/message/reply` | Reply using a short-lived `replyToken` |
| **Send Push** | `POST` | `/v2/bot/message/push` | Send a push message to a specific user, group, or room |
| **Send Multicast** | `POST` | `/v2/bot/message/multicast` | Send push messages to multiple users (max 500) |
| **Send Broadcast** | `POST` | `/v2/bot/message/broadcast` | Send message to all friends |
| **Get Message Content** | `GET` | `/v2/bot/message/{messageId}/content` | Get media content (image, video, etc.) *via api-data.line.me* |
| **Start Loading** | `POST` | `/v2/bot/chat/loading/start` | Display loading indicator in chat |
| **Create Rich Menu** | `POST` | `/v2/bot/richmenu` | Create a new rich menu object |
| **Upload Rich Menu Image**| `POST` | `/v2/bot/richmenu/{richMenuId}/content` | Upload JPEG or PNG image *via api-data.line.me* |
| **Link Rich Menu** | `POST` | `/v2/bot/user/{userId}/richmenu/{richMenuId}` | Link rich menu to a specific user |

## Implementation Steps

1. **Obtain Credentials**: Set up a channel on the LINE Developers Console and copy the **Channel Secret** and **Channel Access Token**.
2. **Setup Route**: Create an HTTPS route matching your registered Webhook URL.
3. **Verify & Respond**: Verify the signature in `x-line-signature`. Return HTTP `200 OK` status immediately, even if the webhook contains an empty event array.
4. **Process Events**: Loop through `events[]`. Handle common event types:
   - `message`: User sent a message. Access message detail (e.g. `event.message.text`).
   - `follow` / `unfollow`: User added or blocked the LINE Official Account.
   - `postback`: User triggered a postback action (e.g. rich menu click, template button).
5. **Construct Payloads**: When replying or pushing, format message objects appropriately (e.g., `{ "type": "text", "text": "Hello" }`).

## Common Mistakes
- **Wrong Domain for Uploads/Downloads**: Attempting to upload rich menu images or download message content using `api.line.me` instead of `api-data.line.me` will fail.
- **Reusing/Delaying Reply Tokens**: Reply tokens expire quickly and are one-time use. Use them immediately, or fall back to Push messages if processing is slow.
- **Case-Sensitive Header Access**: Webhook header field names can be case-insensitive (e.g., `X-Line-Signature` vs `x-line-signature`). Parse them case-insensitively.
- **Exceeding Size Limits**: The payload size limit for messaging APIs is 2MB. Ensure your attachment/text payloads do not exceed this limit.
- **Not Handling Standby Mode**: If the bot's mode is `standby` (another module is active), avoid sending messages to prevent user confusion.
