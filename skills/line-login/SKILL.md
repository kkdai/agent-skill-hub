---
name: line-login
description: Use when integrating, building, or debugging LINE Login v2.1 (OAuth 2.0 / OpenID Connect authorization code flow, Web Apps, Native Apps, ID Tokens, profile retrieval, access token management, PKCE, and two-factor authentication).
---

# LINE Login v2.1 Reference & Development Guide

## Overview
LINE Login v2.1 is a social authentication and authorization service based on the OAuth 2.0 Authorization Code Grant flow and OpenID Connect 1.0 specifications. Integrating LINE Login into web apps or native mobile/desktop apps enables seamless registration, single sign-on (SSO), profile retrieval, and secure user identification using LINE accounts.

## When to Use
- Implementing user login and registration via LINE accounts on web or mobile applications.
- Making OAuth 2.0 authorization requests (`https://access.line.me/oauth2/v2.1/authorize`).
- Exchanging authorization codes for access tokens and OpenID Connect ID Tokens (`https://api.line.me/oauth2/v2.1/token`).
- Verifying ID tokens or Access Tokens on backend services to authenticate users securely.
- Retrieving user profile details (User ID, Display Name, Picture URL, Status Message) or email addresses.
- Managing access tokens (verification, refreshing, revoking).
- Implementing PKCE (Proof Key for Code Exchange) or configuring two-factor authentication (2FA).

---

## 1. Prerequisites & LINE Developers Console Setup

1. **Create Channel**:
   - Go to [LINE Developers Console](https://developers.line.biz/console/).
   - Select a Provider and create a **LINE Login** channel.
2. **Configure Callback URL**:
   - Under the **LINE Login** tab, specify one or more Callback URLs (Redirect URIs).
   - The Callback URL must match character-for-character with the `redirect_uri` parameter used during authorization.
3. **Email Address Permission**:
   - If your application requires access to the user's email address, go to the **Basic settings** tab -> **OpenID Connect** -> click **Apply** under Email address permission.
   - Upload screenshots showing how your app requests and uses user email addresses.
4. **Require Two-Factor Authentication (2FA)**:
   - Admins can enforce 2FA on the channel under the **LINE Login** tab.
   - Enforcing 2FA forces users logging in with email/password or QR code on untrusted devices to enter a 4-digit verification code sent to their LINE app.

---

## 2. OAuth 2.0 Web Login Flow

### Step 1: Redirect to Authorization URL
When the user clicks the "Log in with LINE" button, redirect them to:

```http
GET https://access.line.me/oauth2/v2.1/authorize
```

#### Query Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `response_type` | String | **Required** | Must be `code`. |
| `client_id` | String | **Required** | LINE Login Channel ID. |
| `redirect_uri` | String | **Required** | URL-encoded callback URL registered in the console. |
| `state` | String | **Required** | A unique, random anti-CSRF token generated per session. |
| `scope` | String | **Required** | Space-separated list of scopes (`profile`, `openid`, `email`). E.g., `profile%20openid%20email`. |
| `nonce` | String | Optional | Replay protection token returned in the ID Token payload. |
| `prompt` | String | Optional | Controls consent/auth screen display (`consent`, `none`, `login`). |
| `max_age` | Number | Optional | Maximum elapsed time in seconds since user's last authentication. |
| `ui_locales` | String | Optional | Language tags for LINE Login UI (e.g. `zh-TW`, `en-US`). |
| `bot_prompt` | String | Optional | Displays option to add a LINE Official Account as a friend (`normal` or `aggressive`). |
| `initial_amr_display` | String | Optional | Set to `lineqr` to display QR code login by default instead of email login. |
| `switch_amr` | Boolean | Optional | Set to `false` to hide login method toggle buttons. Default `true`. |
| `disable_auto_login` | Boolean | Optional | Set to `true` to disable automatic login. Default `false`. |
| `code_challenge` | String | Optional | Base64URL-encoded SHA256 hash of `code_verifier` for PKCE support. |
| `code_challenge_method` | String | Optional | Must be `S256` if PKCE is used. |
| `response_mode` | String | Optional | Response parameter delivery mode (`query`, `form_post`, `jwt`, `query.jwt`, `form_post.jwt`). Default `query`. |

#### Example Authorization Request URL:
```url
https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id=1234567890&redirect_uri=https%3A%2F%2Fexample.com%2Fcallback&state=abc123state&scope=profile%20openid%20email&nonce=xyz789nonce
```

---

### Step 2: Receive Authorization Response

Upon completion, LINE redirects back to your `redirect_uri`.

#### Success Response:
```
https://example.com/callback?code=AUTH_CODE_HERE&state=abc123state&friendship_status_changed=true
```
- `code`: Authorization code valid for **10 minutes** (single use).
- `state`: Must be verified against the state saved in user session.
- `friendship_status_changed`: Returns `true` if `bot_prompt` was set and user changed friendship status.

#### Error Response:
```
https://example.com/callback?error=ACCESS_DENIED&error_description=The+user+denied+the+request.&state=abc123state
```
- Common Error Codes:
  - `ACCESS_DENIED`: User canceled the login/consent screen.
  - `INVALID_REQUEST`: Query parameters invalid.
  - `INVALID_SCOPE`: Scopes malformed (e.g. `email` specified without `openid`).
  - `LOGIN_REQUIRED` / `INTERACTION_REQUIRED`: Prompt set to `none` but user interaction was required.

---

### Step 3: Issue Access Token & ID Token

Make a server-to-server POST request to exchange the `code` for tokens.

```http
POST https://api.line.me/oauth2/v2.1/token
Content-Type: application/x-www-form-urlencoded
```

#### Request Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `grant_type` | String | **Required** | Must be `authorization_code`. |
| `code` | String | **Required** | Authorization code received in callback. |
| `redirect_uri` | String | **Required** | Must match the `redirect_uri` sent in Step 1. |
| `client_id` | String | **Required** | LINE Login Channel ID. |
| `client_secret` | String | **Required** | LINE Login Channel Secret (server-side only). |
| `code_verifier` | String | Optional | The original verifier string if PKCE was used in Step 1. |

#### Response JSON:
```json
{
  "access_token": "eyJhbGci...",
  "expires_in": 2592000,
  "id_token": "eyJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "rFdeggRhTnP...",
  "scope": "profile openid",
  "token_type": "Bearer"
}
```
- `access_token`: Valid for **30 days**.
- `expires_in`: Time remaining in seconds (e.g., 2,592,000 seconds = 30 days).
- `id_token`: OpenID Connect JWT token containing user identity details (returned if `openid` scope was requested).
- `refresh_token`: Token to get a new access token, valid for **90 days**.

---

## 3. Core API Reference

### 1. Verify ID Token (Server-Side Verification)
Verify the signature and claims of an ID Token via LINE API.

```http
POST https://api.line.me/oauth2/v2.1/verify
Content-Type: application/x-www-form-urlencoded

id_token=ID_TOKEN_STRING&client_id=CHANNEL_ID
```
Optional params: `nonce`, `user_id`.

#### Response Payload (Decoded JWT Claims):
```json
{
  "iss": "https://access.line.me",
  "sub": "U1234567890abcdef1234567890abcdef",
  "aud": "1234567890",
  "exp": 1600000000,
  "iat": 1599996400,
  "nonce": "xyz789nonce",
  "amr": ["pwd"],
  "name": "Line User Display Name",
  "picture": "https://profile.line-scdn.net/...",
  "email": "user@example.com"
}
```

### 2. Get User Profile
Fetch user profile details using the Access Token.

```http
GET https://api.line.me/v2/profile
Authorization: Bearer {access_token}
```

#### Response JSON:
```json
{
  "userId": "U1234567890abcdef1234567890abcdef",
  "displayName": "Line User",
  "pictureUrl": "https://profile.line-scdn.net/...",
  "statusMessage": "Hello World!"
}
```

### 3. Verify Access Token
Check validity and remaining expiration time of an Access Token.

```http
GET https://api.line.me/oauth2/v2.1/verify?access_token={access_token}
```

#### Response JSON:
```json
{
  "client_id": "1234567890",
  "expires_in": 2591998,
  "scope": "profile openid"
}
```

### 4. Refresh Access Token
Get a new Access Token using a valid `refresh_token`.

```http
POST https://api.line.me/oauth2/v2.1/token
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token&refresh_token={refresh_token}&client_id={client_id}&client_secret={client_secret}
```

### 5. Revoke Access Token
Invalidate an active Access Token.

```http
POST https://api.line.me/oauth2/v2.1/revoke
Content-Type: application/x-www-form-urlencoded

access_token={access_token}&client_id={client_id}&client_secret={client_secret}
```

---

## 4. Implementation Code Snippets

### Node.js (Express / Fetch) Example Flow

```javascript
import express from 'express';
import crypto from 'crypto';

const app = express();
const CLIENT_ID = process.env.LINE_LOGIN_CHANNEL_ID;
const CLIENT_SECRET = process.env.LINE_LOGIN_CHANNEL_SECRET;
const REDIRECT_URI = 'https://example.com/auth/line/callback';

// 1. Step 1: Initiate LINE Login
app.get('/login/line', (req, res) => {
  const state = crypto.randomBytes(16).toString('hex');
  const nonce = crypto.randomBytes(16).toString('hex');
  
  // Store state and nonce in user session / cookie
  res.cookie('oauth_state', state, { httpOnly: true, secure: true });
  res.cookie('oauth_nonce', nonce, { httpOnly: true, secure: true });

  const authUrl = new URL('https://access.line.me/oauth2/v2.1/authorize');
  authUrl.searchParams.append('response_type', 'code');
  authUrl.searchParams.append('client_id', CLIENT_ID);
  authUrl.searchParams.append('redirect_uri', REDIRECT_URI);
  authUrl.searchParams.append('state', state);
  authUrl.searchParams.append('scope', 'profile openid email');
  authUrl.searchParams.append('nonce', nonce);

  res.redirect(authUrl.toString());
});

// 2. Step 2 & 3: Handle Callback & Exchange Tokens
app.get('/auth/line/callback', async (req, res) => {
  const { code, state, error, error_description } = req.query;
  const savedState = req.cookies?.oauth_state;
  const savedNonce = req.cookies?.oauth_nonce;

  if (error) {
    return res.status(400).send(`Login failed: ${error_description || error}`);
  }

  // Anti-CSRF verification
  if (!state || state !== savedState) {
    return res.status(403).send('Invalid state parameter (CSRF detected)');
  }

  try {
    // Token Exchange Request
    const tokenResponse = await fetch('https://api.line.me/oauth2/v2.1/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        grant_type: 'authorization_code',
        code,
        redirect_uri: REDIRECT_URI,
        client_id: CLIENT_ID,
        client_secret: CLIENT_SECRET,
      }),
    });

    const tokens = await tokenResponse.json();
    if (!tokenResponse.ok) throw new Error(tokens.error_description || 'Token error');

    // Verify ID Token
    const verifyResponse = await fetch('https://api.line.me/oauth2/v2.1/verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        id_token: tokens.id_token,
        client_id: CLIENT_ID,
        nonce: savedNonce,
      }),
    });

    const idTokenPayload = await verifyResponse.json();

    // Authenticated user identity
    const userId = idTokenPayload.sub;
    const email = idTokenPayload.email;
    const name = idTokenPayload.name;

    console.log('Logged in LINE user:', { userId, name, email });
    res.send(`Welcome ${name}! User ID: ${userId}`);
  } catch (err) {
    console.error('LINE Login Error:', err);
    res.status(500).send('Authentication failed');
  }
});
```

---

## 5. Security Checklist & Common Pitfalls

1. **State Validation (CSRF)**:
   - Always generate a strong random `state` string per session and store it securely in a server-side session or encrypted HTTP-only cookie. Reject any callback where `state` does not match.
2. **Nonce Verification (Replay Attack Prevention)**:
   - Always generate a `nonce` string when requesting `openid` scope, and verify that the `nonce` in the returned ID token matches.
3. **Never Expose Client Secret**:
   - `client_secret` must ONLY be used on secure backend servers. Never send or hardcode `client_secret` in frontend HTML/JS, mobile apps, or public repositories.
4. **Use PKCE for Mobile / Public Clients**:
   - Native mobile apps and Single Page Applications (SPAs) without a secret backend must implement **PKCE** (`code_challenge` and `code_verifier`) with `code_challenge_method=S256`.
5. **LIFF Integration Distinction**:
   - When building inside LINE Front-end Framework (LIFF), do NOT manually construct the `access.line.me` URL. Instead, use the LIFF SDK methods (`liff.init()`, `liff.login()`, `liff.getProfile()`, `liff.getDecodedIDToken()`).
6. **Graceful Handling of Optional Scopes**:
   - Users may deny optional permissions or fail to share email addresses. Ensure your app handles missing email or profile data without crashing.
