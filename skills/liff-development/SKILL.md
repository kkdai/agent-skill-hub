---
name: liff-development
description: Use when building, debugging, or implementing LINE Front-end Framework (LIFF) applications. Refers to official LIFF API documentation and specifications (https://developers.line.biz/en/reference/liff/index.html.md).
---

# LINE Front-end Framework (LIFF) Development Reference & API Guide

## Overview
The LINE Front-end Framework (LIFF) allows developers to build rich web applications running inside the LINE app (in-app LIFF browser) or in external web browsers. This guide provides full reference specifications for the LIFF SDK (v2.x), covering environment checks, initialization, authentication, user context, profile retrieval, messaging, permanent links, and error handling.

Official Documentation Reference: [LINE LIFF API Reference (index.html.md)](https://developers.line.biz/en/reference/liff/index.html.md)

## When to Use
- Building web apps that run inside the LINE in-app browser or standard web browsers.
- Initializing the LIFF SDK using `liff.init({ liffId })`.
- Handling user authentication (`liff.login()`, `liff.logout()`, `liff.isLoggedIn()`).
- Retrieving user details (`liff.getProfile()`, `liff.getDecodedIDToken()`, `liff.getAccessToken()`).
- Retrieving runtime context (`liff.getContext()`, `liff.getOS()`, `liff.getLanguage()`, `liff.isInClient()`).
- Sending messages or sharing content (`liff.sendMessages()`, `liff.shareTargetPicker()`).
- Generating permanent LIFF URLs (`liff.permanentLink.createUrl()`).
- Handling error objects (`LiffError`) and debugging LIFF app initialization issues.

---

## 1. Installation & Setup

### Package Manager
```bash
npm install @line/liff
# or
yarn add @line/liff
```

### CDN Script Tag
```html
<script src="https://static.line-scdn.net/liff/edge/2/sdk.js"></script>
```

---

## 2. Initialization & Properties

### `liff.init()`
Initializes the LIFF SDK. Must be called before executing any other LIFF API methods.

```javascript
import liff from '@line/liff';

liff.init({
  liffId: "YOUR_LIFF_ID",
  withLoginOnExternalBrowser: false // Optional: auto-login in external browser
})
.then(() => {
  // LIFF SDK is initialized
  if (!liff.isLoggedIn()) {
    liff.login();
  } else {
    // Proceed with app logic
  }
})
.catch((err) => {
  console.error("LIFF Init Failed", err.code, err.message);
});
```

### Essential Properties
- `liff.id`: Holds the LIFF app ID string passed during initialization (returns `null` prior to `liff.init()`).
- `liff.ready`: A `Promise` object that resolves when `liff.init()` completes. Can be hooked even before `liff.init()` is invoked.

### Methods Safe to Call BEFORE `liff.init()`
The following methods/properties can be safely accessed prior to `liff.init()` completion:
- `liff.ready`
- `liff.getOS()`
- `liff.getAppLanguage()`
- `liff.getVersion()`
- `liff.getLineVersion()`
- `liff.isInClient()`
- `liff.closeWindow()`

---

## 3. Environment & Context Verification

| Method | Description | Return Type |
| :--- | :--- | :--- |
| `liff.isInClient()` | Checks if the LIFF app is running inside the LINE in-app browser (`true`) or external browser (`false`). | `Boolean` |
| `liff.getOS()` | Returns the user's OS (`ios`, `android`, `web`). | `String` |
| `liff.getAppLanguage()` | Returns language code of LINE app (e.g., `zh-TW`, `en-US`, `ja-JP`). | `String` |
| `liff.getVersion()` | Returns LIFF SDK version (e.g., `"2.23.0"`). | `String` |
| `liff.getLineVersion()` | Returns LINE client app version (returns `null` in external browser). | `String` \| `null` |
| `liff.getContext()` | Returns current screen/chat context object. | `Object` \| `null` |

### `liff.getContext()` Payload Structure
```json
{
  "type": "utou", // "utou" (1-on-1), "group", "room", "external", "none"
  "utouId": "...",
  "roomId": "...",
  "groupId": "...",
  "userId": "U1234...",
  "endpointUrl": "https://example.com/liff-app/",
  "viewType": "full", // "compact", "tall", "full"
  "accessTokenHash": "...",
  "availability": {
    "shareTargetPicker": { "permission": true, "minVer": "10.3.0" },
    "multipleLiffTransition": { "permission": true, "minVer": "10.1.0" },
    "subwindowOpen": { "permission": true, "minVer": "10.1.0" },
    "scanCode": { "permission": true, "minVer": "9.3.0" }
  }
}
```

---

## 4. User Authentication & Profile API

### Authentication Methods
- `liff.isLoggedIn()`: Returns `true` if user is logged in.
- `liff.login(loginConfig?)`: Redirects user to LINE OAuth 2.1 login screen. Accepts optional `{ redirectUri }`.
- `liff.logout()`: Logs out user (only effective when running in external browser).
- `liff.getAccessToken()`: Returns raw OAuth 2.0 access token string.
- `liff.getDecodedIDToken()`: Returns decoded OpenID Connect ID token JWT claims.

### `liff.getProfile()`
Retrieves profile of the logged-in user.

```javascript
liff.getProfile()
  .then((profile) => {
    console.log(profile.userId);       // User ID
    console.log(profile.displayName);  // Display name
    console.log(profile.pictureUrl);   // Profile picture URL
    console.log(profile.statusMessage);// Status message
  })
  .catch((err) => console.error(err));
```

### `liff.getFriendship()`
Checks if the user has added the LINE Official Account linked to the LIFF channel as a friend.

```javascript
liff.getFriendship().then((data) => {
  if (data.friendFlag) {
    console.log("User is friend with official account");
  }
});
```

---

## 5. Messaging & Feature APIs

### `liff.sendMessages(messages)`
Sends messages on behalf of the user directly into the active chat room (in-app browser only).

```javascript
if (liff.isApiAvailable('sendMessages')) {
  liff.sendMessages([
    {
      type: 'text',
      text: 'Hello from LIFF!'
    },
    {
      type: 'flex',
      altText: 'Flex Message',
      contents: { /* Flex Container JSON */ }
    }
  ])
  .then(() => console.log('Message sent'))
  .catch((err) => console.error('Error sending message:', err));
}
```

### `liff.shareTargetPicker(messages, options?)`
Opens target picker modal allowing the user to send messages to selected friends or groups.

```javascript
if (liff.isApiAvailable('shareTargetPicker')) {
  liff.shareTargetPicker([
    {
      type: 'text',
      text: 'Check out this awesome LIFF app!'
    }
  ])
  .then((res) => {
    if (res) console.log("Message shared successfully");
    else console.log("Target picker closed by user");
  })
  .catch((err) => console.error("Share target picker error:", err));
}
```

### Window & Navigation Controls
- `liff.openWindow({ url, external })`: Opens a URL in in-app webview or external browser (`external: true`).
- `liff.closeWindow()`: Closes the LIFF app window inside LINE app.
- `liff.permanentLink.createUrl()`: Generates a permanent URL (`https://liff.line.me/{liffId}/path`) that preserves query parameters.

```javascript
const permanentUrl = liff.permanentLink.createUrl();
console.log("Permanent URL:", permanentUrl);
```

---

## 6. Error Handling (`LiffError`)

LIFF API errors return a `LiffError` object containing `code`, `message`, and optional `cause`.

| Error Code | Meaning / Resolution |
| :--- | :--- |
| `INIT_FAILED` | Initialization failed. Verify `liffId` and Endpoint URL setting in LINE Console. |
| `INVALID_ARGUMENT` | Passed parameters are invalid or missing required keys. |
| `UNAUTHORIZED` | User is not logged in, or attempted feature without granted scopes/permissions. |
| `FORBIDDEN` | Feature not supported in current environment (e.g. calling `sendMessages` in external browser). |
| `INVALID_CONFIG` | Endpoint URL mismatch or invalid LIFF configuration. |
| `INVALID_ID_TOKEN` | Failed to decode or verify ID Token. |
| `EXCEPTION_IN_SUBWINDOW` | Target picker or secondary window timed out (>10 mins) or encountered subwindow error. |

---

## 7. Essential Development Best Practices

1. **Endpoint URL Boundary**:
   - `liff.init()` must be executed at or under the exact **Endpoint URL** registered in LINE Developers Console. Calling `init()` on parent or unrelated paths will trigger warnings and cause multi-tab view failures.
2. **Post-Init URL Redirects**:
   - Never perform `window.location.replace()` or `history.pushState()` BEFORE `liff.init()` resolves. URL modifications prior to `init()` resolution break state token parsing.
3. **Environment Guarding**:
   - Always verify feature availability using `liff.isApiAvailable('sendMessages')` or `liff.isInClient()` before invoking in-app specific features.
4. **Security & Access Tokens**:
   - Do not log or transmit the primary redirect URL (containing `access_token=...`) to external analytics tools before `liff.init()` resolves, as credentials will be in the URL query string on older SDK versions.
