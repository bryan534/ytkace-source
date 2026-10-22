import json, urllib.request, re
rels = json.load(urllib.request.urlopen("https://api.github.com/repos/itzzace/ytkace/releases?per_page=100"))
icon = "https://avatars.githubusercontent.com/u/318309682?v=4"
desc = "YTKACE is a free, open-source YouTube enhancer and downloader for iOS with SponsorBlock, background playback, player controls, and interface customization including liquid glass."
versions, ios16_added = [], False
for r in rels:
    if r["draft"] or r["prerelease"]: continue
    for a in r["assets"]:
        m = re.match(r"YTKACE_([\d.]+)_YouTube_(iOS16_)?([\d.]+)\.ipa$", a["name"])
        if not m: continue
        legacy = bool(m.group(2))
        if legacy or m.group(3) == "21.33.6": continue  # iOS 17+ builds only
        versions.append({
            "version": m.group(3),
            "buildVersion": m.group(3),
            "date": r["published_at"],
            "localizedDescription": f"YTKACE {m.group(1)}" + (" (iOS 16 build)" if legacy else "") + "\n\n" + (r["body"] or "").strip(),
            "downloadURL": a["browser_download_url"],
            "size": a["size"],
            **({"sha256": a["digest"].split(":",1)[1]} if (a.get("digest") or "").startswith("sha256:") else {}),
            "minOSVersion": "17.0",
        })
app = {"name": "YTKACE", "bundleIdentifier": "com.google.ios.youtube", "developerName": "itzzace",
       "subtitle": "Open-source YouTube enhancer and downloader", "localizedDescription": desc,
       "iconURL": icon, "tintColor": "#FF0033", "category": "entertainment",
       "screenshots": [f"https://raw.githubusercontent.com/itzzace/ytkace/main/screenshots/framed/{n}.png" for n in
                       ["video-player","glass-home","download-library","sponsorblock-settings","settings"]],
       "versions": versions, "appPermissions": {"entitlements": [], "privacy": {}}}
src = {"name": "YTKACE", "subtitle": app["subtitle"], "description": desc, "website": "https://github.com/itzzace/ytkace",
       "iconURL": icon, "tintColor": "#FF0033", "featuredApps": ["com.google.ios.youtube"], "apps": [app], "news": []}
json.dump(src, open("store.json","w"), indent=2, ensure_ascii=False)
print(len(versions), "versions")
