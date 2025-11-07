from fastapi import FastAPI, Query, HTTPException
import httpx
from bs4 import BeautifulSoup
import re
import asyncio

app = FastAPI(title="Cloud Vulnerability Tracker")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sources
DOC_URLS = {
    "gke": "https://docs.cloud.google.com/kubernetes-engine/security-bulletins",
    "compute": "https://docs.cloud.google.com/compute/docs/security-bulletins",
    "sql": "https://docs.cloud.google.com/sql/docs/security-bulletins",
    "mesh": "https://docs.cloud.google.com/service-mesh/docs/security-bulletins",
}

CLIENT_KEYWORDS = [
    "you must", "you should", "update your", "apply patches",
    "manual upgrade", "take action", "requires action", "perform",
    "self-service maintenance", "customer", "manually"
]
GCP_KEYWORDS = [
    "google has applied", "google has started", "automatically patched",
    "google cloud has rolled out", "no action required", "handled automatically",
    "google will", "google cloud has released"
]


def heuristic_classify(text: str):
    t = text.lower()
    client_flag = any(kw in t for kw in CLIENT_KEYWORDS)
    gcp_flag = any(kw in t for kw in GCP_KEYWORDS)

    if client_flag and gcp_flag:
        return "Both"
    elif client_flag:
        return "Client"
    elif gcp_flag:
        return "GCP"
    else:
        return "Unknown"


async def scrape_bulletins(url: str):
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        resp = await client.get(url)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    results = []

    for header in soup.find_all(["h2", "h3"], id=re.compile(r"^gcp-\d{4}-\d{3}")):
        bulletin_id = header.get("id")
        title = header.get_text(strip=True)
        section = header.find_next("table")
        text = section.get_text(" ", strip=True) if section else ""

        cves = sorted(set(re.findall(r"CVE-\d{4}-\d{4,7}", text)))
        if not cves:
            continue

        managed = heuristic_classify(text)

        results.append({
            "id": bulletin_id,
            "title": title,
            "cves": cves,
            "summary": text[:300] + "..." if len(text) > 300 else text,
            "managed": managed,
            "url": f"{url}#{bulletin_id}"
        })
    return results


@app.get("/bulletins")
async def get_bulletins(product: str = Query(None, description="np. gke, compute, sql, mesh (opcjonalnie)")):
    if product:
        if product not in DOC_URLS:
            raise HTTPException(status_code=400, detail=f"Unknown service: {product}")
        data = await scrape_bulletins(DOC_URLS[product])
        return {"product": product, "count": len(data), "bulletins": data}

    # Brak parametru = wszystkie źródła
    tasks = [scrape_bulletins(url) for url in DOC_URLS.values()]
    results_all = await asyncio.gather(*tasks)
    merged = [item for sublist in results_all for item in sublist]
    return {"product": "all", "count": len(merged), "bulletins": merged}


@app.get("/stats")
async def get_stats():
    tasks = [scrape_bulletins(url) for url in DOC_URLS.values()]
    results_all = await asyncio.gather(*tasks)
    merged = [item for sublist in results_all for item in sublist]

    counts = {"GCP": 0, "Client": 0, "Both": 0, "Unknown": 0}
    for item in merged:
        counts[item["managed"]] = counts.get(item["managed"], 0) + 1

    return {"total": len(merged), "by_managed": counts}


@app.get("/health")
def health():
    return {"status": "ok"}
