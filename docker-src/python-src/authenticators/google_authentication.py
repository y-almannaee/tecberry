# Reference implementation of Google Authentication
# Your authenticator implementation must model off of this one,
# and must export the same functions, global variables, and/or
# interfaces into the EXPORTED class

# Place your authenticators into app_data/authenticators
# You may have multiple. Make sure the routes aren't the same between them
# Access to the authenticators folder is basically access to the admin
# account so protect access to the Raspberry Pi storage

from uuid import uuid4
from aiohttp import web
import pathlib, os, pickle
from datetime import timedelta
from loguru import logger

from cryptography.fernet import Fernet, InvalidToken
from yarl import URL
import google_auth_oauthlib.flow
import googleapiclient.discovery

work_dir = pathlib.Path(__file__).parent.resolve() / "google_auth_items"
work_dir.mkdir(parents=True, exist_ok=True)
# You may place secret files in the same directory as this script (app_data/authenticators)
CLIENT_SECRETS_FILE = work_dir / "client_secrets.json"

auth_scopes = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]
candy_scopes = ["https://www.googleapis.com/auth/drive.file"]
hostname = os.environ.get("HOSTNAME", "localhost:3636")
schema = "https" if os.environ.get("SECURE", "") else "http"
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

namespace = "google"

# If you don't want to implement your own auth
# just edit the below function to verify your users
# return the status (200 = ok, 401 = forbidden) followed
# by the reason for being rejected
async def verify_credentials(info):
    if info.get("hd", "") != "aus.edu":
        return (401, "You are not from AUS")
    return 200


async def start_registration(request):
    if await get_credentials(
        request.app["db"],
        request.cookies.get("id", "").replace("google:", ""),
        request.cookies.get("key", "").replace("google:", ""),
    ):
        return web.Response(status=303, headers={"Location": "/"})

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=auth_scopes
    )
    flow.redirect_uri = f"{schema}://{hostname}/api/google/ingest"

    auth_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )
    response = web.Response(status=303, headers={"Location": auth_url})
    response.set_cookie("for", state, secure=True, httponly=True)
    response.set_cookie(
        "prev_state",
        request.get("Referer", "")
        if request.get("Referer", "")
        else request.get("X-Original-State", "/"),
    )
    logger.info("Attempt to Google authorize,", state)
    return response


async def handle_credentials(request):
    state = request.cookies.get("for", "")
    scopes_granted = request.query.get("scope", "")
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=scopes_granted, state=state
    )
    flow.redirect_uri = f"{schema}://{hostname}/api/google/ingest"
    flow.fetch_token(authorization_response=str(request.url))
    credentials = flow.credentials

    person = googleapiclient.discovery.build("oauth2", "v2", credentials=credentials)
    stored_info = person.userinfo().get().execute()
    stored_info.pop("verified_email")
    verified = await verify_credentials(stored_info)

    if verified != 200:
        return web.Response(verified[0], text=verified[1])

    # The primary key for this authenticator is the 'id' value of the account
    hkey = f"google:{stored_info.get('id')}"
    uuid = uuid4()
    secret_key = Fernet.generate_key()
    fernet = Fernet(secret_key)
    encrypted_creds = fernet.encrypt(pickle.dumps(credentials))

    stored_info["pfp"] = stored_info.get("picture")
    stored_info["rank"] = 0

    async with request.app["db"].pipeline(transaction=True) as pipe:
        ok = await (
            pipe.hset(hkey, mapping=stored_info)
            .set(f"cookies:{uuid}", hkey, ex=timedelta(days=3))
            .set(f"{hkey}:credentials", encrypted_creds)
            .execute()
        )

    if not all(ok[1:]):
        return web.Response(
            status=500, text="Couldn't store your credentials. Try again"
        )

    prev_state = URL(request.cookies.get("prev_state", "/")).path
    response = web.Response(status=303, headers={"Location": prev_state})
    response.del_cookie("for")
    response.set_cookie("id", f"google:{uuid}")
    response.set_cookie("key", f"google:{secret_key.decode()}")
    return response


async def google_drive_transfer(request):
    credentials = await get_credentials(
        request.app["db"], request.cookies.get("id", "").replace("google:", "")
    )
    if credentials and candy_scopes[0] in credentials.scopes:
        return web.Response(text="GDrive token")
    else:
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, scopes=(auth_scopes + candy_scopes)
        )
        flow.redirect_uri = f"{schema}://{hostname}/api/google/ingest"

        auth_url, state = flow.authorization_url(
            access_type="offline", include_granted_scopes="true"
        )
        response = web.Response(status=303, headers={"Location": auth_url})
        response.set_cookie("for", state)
        return response


async def get_credentials(db, uuid, key):
    try:
        hkey = (await db.get(f"cookies:{uuid}")).decode()
    except AttributeError:
        return ""
    encrypted_creds = await db.get(f"{hkey}:credentials")
    if encrypted_creds == None:
        return ""
    fernet = Fernet(key)
    try:
        decrypted_credentials = fernet.decrypt(encrypted_creds)
    except InvalidToken:
        return ""
    try:
        credentials = pickle.loads(decrypted_credentials)
    except TypeError:
        return ""
    if credentials.valid:
        await db.expire(f"cookies:{uuid}", timedelta(days=3))
        return credentials
    try:
        credentials.refresh(None)
    except:
        return ""
    return credentials


# These paths will be prefixed with /api
# It is also a good idea to start with your auth
# name as the directory in the path (eg. /google/)
routes = [
    # Only one route is technically needed
    # The first route in the list is the one that will be
    # called when a user first presses on login. In this
    # example the other routes exist as additional functions
    # to handle Google authentication, and for Drive API
    web.get(
        f"/{namespace}/request", start_registration
    ),  # This will become /api/google/request
    # Not mandatory
    web.get(f"/{namespace}/ingest", handle_credentials),
    web.get(f"/{namespace}/move_to_drive", google_drive_transfer),
]

# These are used to define what the button looks like on your website
button_text = "Sign-in with Google"
button_classes_tailwindcss = "bg-blue-600 !text-slate-50 hover:bg-blue-500"
