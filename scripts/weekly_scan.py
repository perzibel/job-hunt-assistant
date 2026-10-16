"""Weekly job scan, driven by <workspace>/job_scan/config.json.

Queries the public Greenhouse / Ashby / Lever job-board APIs of the companies in the config,
filters roles by title, location and pay, and writes <workspace>/job_scan/scan_results.json.
Roles already reviewed are listed in <workspace>/job_scan/seen.json (keys "company|title").
Usage: python weekly_scan.py --workspace <path-to-workspace>
"""
import argparse, json, re, html, sys, os, datetime, urllib.request, concurrent.futures as cf

sys.stdout.reconfigure(encoding="utf-8")


def get(u):
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=25) as r:
            return json.load(r)
    except Exception:
        return None


def strip(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", html.unescape(s or ""))))


def gh(c):
    d = get(f"https://boards-api.greenhouse.io/v1/boards/{c}/jobs?content=true") or {}
    return [dict(co=c, title=j["title"].strip(), loc=(j.get("location") or {}).get("name", ""), txt=strip(j.get("content")),
                 url=j["absolute_url"], comp="", workplace="") for j in d.get("jobs", [])]


def ashby(c):
    d = get(f"https://api.ashbyhq.com/posting-api/job-board/{c}?includeCompensation=true") or {}
    out = []
    for j in d.get("jobs", []):
        loc = " / ".join([j.get("location") or ""] + [x.get("location", "") for x in j.get("secondaryLocations") or []])
        out.append(dict(co=c, title=j["title"].strip(), loc=loc, txt=j.get("descriptionPlain", ""), url=j["jobUrl"],
                        comp=(j.get("compensation") or {}).get("compensationTierSummary") or "",
                        workplace=j.get("workplaceType") or ""))
    return out


def lever(c):
    d = get(f"https://api.lever.co/v0/postings/{c}?mode=json")
    if not isinstance(d, list):
        return []
    return [dict(co=c, title=j["text"].strip(), loc=(j.get("categories") or {}).get("location", "") or "",
                 txt=j.get("descriptionPlain", "") + " " + " ".join(strip(l.get("content")) for l in j.get("lists", [])),
                 url=j["hostedUrl"], comp="", workplace=j.get("workplaceType", "") or "") for j in d]


PAY = re.compile(r"(€|£|\$|EUR|GBP|USD|PLN|zł|CHF)\s?(\d[\d,.]*)\s?([kK])?\s?(?:-|–|to)\s?(?:€|£|\$|EUR|GBP|USD|PLN|zł|CHF)?\s?(\d[\d,.]*)\s?([kK])?", re.I)


def annual_pay(text, fx):
    """Return (low, high) annual pay in the config currency from the first range found, or None."""
    m = PAY.search(text or "")
    if not m:
        return None
    cur = m.group(1).upper()
    try:
        num = lambda s, k: float(s.replace(",", "").rstrip(".")) * (1000 if k else 1)
        lo, hi = num(m.group(2), m.group(3)), num(m.group(4), m.group(5) or m.group(3))
    except ValueError:
        return None
    if hi < 1000:  # "120 - 140" meaning thousands
        lo, hi = lo * 1000, hi * 1000
    if hi < 60000 and re.search(r"per month|monthly|/\s?month|miesi", text[m.start():m.end() + 80], re.I):
        lo, hi = lo * 12, hi * 12
    rate = fx.get(cur, fx.get(m.group(1), 1.0))
    return round(lo * rate), round(hi * rate)


def rx(pattern):
    return re.compile(pattern, re.I) if pattern else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", required=True)
    d = os.path.join(ap.parse_args().workspace, "job_scan")
    cfg = json.load(open(os.path.join(d, "config.json"), encoding="utf-8"))

    title_in, title_ex = rx(cfg.get("title_include")), rx(cfg.get("title_exclude"))
    desc_req = rx(cfg.get("description_require"))
    loc_in, loc_ex, target = rx(cfg.get("location_include")), rx(cfg.get("location_exclude")), rx(cfg.get("target_locations"))
    floor = cfg.get("pay_floor_annual") or 0
    fx = cfg.get("fx_to_currency", {})
    exclude = {c.lower() for c in cfg.get("exclude_companies", [])}
    high = {c.lower() for c in cfg.get("high_payers", [])}

    jobs = [(gh, c) for c in set(cfg.get("greenhouse", []))] + [(ashby, c) for c in set(cfg.get("ashby", []))] + \
           [(lever, c) for c in set(cfg.get("lever", []))]
    rows = []
    with cf.ThreadPoolExecutor(24) as ex:
        for r in ex.map(lambda t: t[0](t[1]), jobs):
            rows += r

    seen_path = os.path.join(d, "seen.json")
    seen = set(json.load(open(seen_path, encoding="utf-8"))) if os.path.exists(seen_path) else set()

    out, keys = [], set()
    for j in rows:
        t, loc, txt = j["title"], j["loc"], j["txt"]
        if j["co"].lower() in exclude or (title_in and not title_in.search(t)) or (title_ex and title_ex.search(t)):
            continue
        if desc_req and not desc_req.search(txt):
            continue
        if loc_in and not loc_in.search(loc):
            continue
        # An excluded place wins unless the location also names an included place
        # (generic "remote" doesn't count, so "Remote - US" is dropped but "Remote US / Berlin" is kept).
        if loc_ex and loc_ex.search(loc) and not (loc_in and loc_in.search(re.sub(r"remote", "", loc, flags=re.I))):
            continue
        key = f'{j["co"]}|{t.lower()}'
        if key in keys:
            continue
        keys.add(key)
        hybrid = bool(re.search(r"hybrid|anchor days|in[- ]office|days (a|per) week in|office[- ]centric|on-?site", txt + " " + j["workplace"], re.I))
        remote = bool(re.search(r"remote", loc + " " + j["workplace"], re.I)) and not hybrid
        pay = annual_pay(j["comp"], fx) or annual_pay(txt, fx)
        if not floor:
            pay_status = "no-floor"
        elif pay:
            pay_status = "meets" if pay[1] >= floor else "below"
        else:
            pay_status = "unpublished-high-payer" if j["co"].lower() in high else "unpublished"
        location_ok = (remote and cfg.get("allow_remote", True)) or not target or bool(target.search(loc))
        out.append(dict(company=j["co"], title=t, location=loc, url=j["url"], remote=remote, hybrid_or_office=hybrid,
                        location_ok=location_ok, pay_annual=pay, currency=cfg.get("currency", ""), pay_status=pay_status,
                        new=key not in seen, key=key,
                        years=min([int(y) for y in re.findall(r"(\d+)\+?\s*(?:or more\s*)?years", txt, re.I) if int(y) < 20], default=None),
                        excerpt=txt[:3500]))

    ok_pay = {"meets", "no-floor", "unpublished-high-payer"} | ({"unpublished"} if cfg.get("keep_unpublished_pay") else set())
    keep = [o for o in out if o["location_ok"] and o["pay_status"] in ok_pay]
    json.dump(dict(date=datetime.date.today().isoformat(), scanned=len(rows), candidates=keep,
                   rejected=[{k: o[k] for k in ("company", "title", "location", "pay_status", "location_ok")} for o in out if o not in keep]),
              open(os.path.join(d, "scan_results.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(rows)} jobs scanned; {len(out)} role matches; {len(keep)} pass location + pay; "
          f"{sum(o['new'] for o in keep)} new since last review")
    for o in keep:
        where = "remote" if o["remote"] else ("hybrid/office" if o["hybrid_or_office"] else "?")
        print(f'{"NEW " if o["new"] else "    "}{o["company"]:<14}| {o["title"][:55]:<55}| {o["location"][:35]:<35}| '
              f'{where} | {o["pay_status"]} {o["pay_annual"] or ""}')


if __name__ == "__main__":
    main()
