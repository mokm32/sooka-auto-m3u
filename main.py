import requests
from datetime import datetime

# API & channel config
TOKEN_URL = "https://api.sooka.my/token"  # ganti ikut endpoint sebenar
LICENSE_URL = "https://license.sooka.my/{cid}"
MPD_URL = "https://l01.dp.sooka.my/{cid}/linear/index.mpd"

CHANNELS = {
    "601": {
        "name": "Sooka Channel 601",
        "contentId": "7e61c7b6-0aa1-4e1b-978f-5247a3757f73",
        "logo": "https://example.com/logo601.png"
    }
    # Tambah channel lain di sini
}

HEADERS = {
    "Content-Type": "application/json",
    "Origin": "https://sooka.my",
    "Referer": "https://sooka.my/"
}

PAYLOAD_BASE = {
    "type": 0,
    "cdnList": [],
    "isWMAuthEnabled": True,
    "isCDNAuthEnabled": True,
    "action": "stream",
    "contentType": "linear",
    "deviceType": "WEB",
    "entitlementList": ["SVOD003"],  # ubah ikut entitlement anda
    "intersection": ["SVOD003"],
}

def fetch_token(cid, contentId):
    payload = PAYLOAD_BASE.copy()
    payload["laContentId"] = cid
    payload["contentId"] = contentId
    resp = requests.post(TOKEN_URL, json=payload, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()["data"]["token"]

def build_m3u():
    out = "#EXTM3U\n"
    for cid, ch in CHANNELS.items():
        token = fetch_token(cid, ch["contentId"])
        out += f"""
#KODIPROP:inputstreamaddon=inputstream.adaptive
#KODIPROP:inputstream.adaptive.manifest_type=mpd
#KODIPROP:inputstream.adaptive.license_type=com.widevine.alpha
#KODIPROP:inputstream.adaptive.license_key={LICENSE_URL.format(cid=cid)}|Authorization=Bearer {token}|R{{"headers":["User-Agent=Mozilla/5.0","Origin=https://sooka.my","Referer=https://sooka.my/"]}}
#EXTINF:-1 tvg-id="{cid}" tvg-logo="{ch["logo"]}",{ch["name"]}
{MPD_URL.format(cid=cid)}
"""
    with open("sooka_auto.m3u", "w", encoding="utf-8") as f:
        f.write(out.strip())
    print("[OK]", datetime.utcnow(), "sooka_auto.m3u updated")

if __name__ == "__main__":
    build_m3u()
