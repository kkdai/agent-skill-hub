---
name: line-liff-api
description: Use when building, debugging, or interacting with the LINE Front-end Framework (LIFF) SDK (initialization, authentication, retrieving user profiles, sending messages, and sharing target pickers).
---

# LINE LIFF API Reference

## Overview
This skill provides a structured reference for integrating and interacting with the LINE Front-end Framework (LIFF) client-side JS SDK. It covers LIFF SDK properties, initialization, authentication, user context, profile retrieval, and custom features like share target picker and scanning codes.

## When to Use
- Building web applications that run inside LINE's in-app LIFF browser or external browsers.
- Initializing the LIFF SDK using `liff.init()` to gain access to LINE features.
- Performing user authentication (`liff.login()`, `liff.logout()`, `liff.isLoggedIn()`).
- Fetching user details (`liff.getProfile()`, `liff.getDecodedIDToken()`).
- Sending messages directly to the current chat room (`liff.sendMessages()`) or selecting target friends to share content (`liff.shareTargetPicker()`).
- Getting runtime environment parameters (OS, language, LINE version, etc.).

## Core Pattern
Always call `liff.init()` as early as possible and wait for the returned promise to resolve before calling other LIFF SDK methods.

### Initialization & Login Flow (JavaScript)
```javascript
import liff from '@line/liff';

async function initializeLiff(liffId) {
  try {
    await liff.init({ liffId });
    if (!liff.isLoggedIn()) {
      // Automatically redirect to LINE Login if not logged in
      liff.login();
    } else {
      // Proceed to fetch profile or use other SDK features
      const profile = await liff.getProfile();
      console.log('User Profile:', profile);
    }
  } catch (error) {
    console.error('LIFF initialization failed:', error.code, error.message);
  }
}
```

## Quick Reference

### Methods Available Before `liff.init()`
These methods can be used to query the environment before the SDK is fully initialized:
- `liff.ready` (Promise indicating init completion)
- `liff.getOS()` (returns `'ios'`, `'android'`, or `'web'`)
- `liff.getAppLanguage()` (gets language setting of the LINE app)
- `liff.getVersion()` / `liff.getLineVersion()`
- `liff.isInClient()` (checks if running inside the LINE app)
- `liff.closeWindow()` (closes the LIFF window)

### Core SDK Methods
| Method | Return Type | Description |
| :--- | :--- | :--- |
| **`liff.init(config)`** | `Promise<void>` | Initializes the LIFF app with `liffId` |
| **`liff.isLoggedIn()`** | `Boolean` | Checks if the user is authenticated |
| **`liff.login(options)`** | `void` | Triggers LINE login flow |
| **`liff.logout()`** | `void` | Logs out the user |
| **`liff.getProfile()`** | `Promise<Profile>` | Gets user profile (name, picture, status) |
| **`liff.getDecodedIDToken()`**| `Object` | Decodes the user's ID OIDC token (contains email) |
| **`liff.sendMessages(msgs)`** | `Promise<void>` | Sends messages to current chat (max 5) |
| **`liff.shareTargetPicker(msgs)`** | `Promise<Response>`| Opens a friend picker to share messages |
| **`liff.openWindow(options)`** | `void` | Opens a URL in the LIFF browser or external browser |

## Implementation Steps

1. **Register LIFF App**: Create a LINE Login channel in the LINE Developers Console and register your LIFF app to get a `LIFF ID` and configure the `Endpoint URL`.
2. **Import SDK**: Add LIFF SDK to your project via CDN (`https://static.line-scdn.net/liff/edge/2/sdk.js`) or npm (`npm install @line/liff`).
3. **Initialize**: Call `liff.init({ liffId })`. Make sure to trigger URL changes or analytics pageviews only *after* the init promise resolves to prevent credential leakage.
4. **Acquire Scopes**: Ensure your channel is granted the necessary scopes (e.g. `profile`, `openid`, `chat_message.write`) in order to call profile or messaging APIs.
5. **Verify Tokens (Server Side)**: If you need to verify the user identity on your backend, send the raw ID token (retrieved via `liff.getIDToken()`) or Access Token to your backend and call LINE's verification endpoints.

## Common Mistakes
- **Calling Methods Before Init**: Calling methods like `liff.getProfile()` before the `liff.init()` promise has resolved.
- **Wrong Endpoint URL Pathing**: Running `liff.init()` on a URL that is not at or lower than the configured Endpoint URL in the console. Doing so causes warnings and prevents correct initialization.
- **Google Analytics Leakage**: Logging the primary redirect URL (which contains the user's access token in the query params) to Google Analytics before the init resolves. In LIFF v2.11.0+, credentials are automatically removed after resolution; trigger logging inside the `then()` block of `liff.init()`.
- **Misunderstanding OpenChat Compatibility**: LIFF applications are mostly incompatible inside LINE OpenChat (e.g., retrieving user profiles is disabled).
- **Ignoring External Browser Constraints**: Expecting features like `liff.scanCode()` or `liff.sendMessages()` to work in external mobile/desktop browsers (they are only supported in the LINE in-app LIFF browser). Use `liff.isInClient()` to check compatibility.
- **Modifying SDK Query Parameters**: Modifying query parameters like `liff.state` or `liff.referrer` manually before the initialization resolves, which breaks LIFF transitions.
