import argparse
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

def harvest_robots_and_sitemap(target_url: str) -> None:
    """Extract disallowed paths and sitemap links from web server configuration files."""
    if not target_url.startswith(("http://", "https://")):
        target_url = "https://" + target_url

    parsed_base = urllib.parse.urlparse(target_url)
    base_domain = f"{parsed_base.scheme}://{parsed_base.netloc}"

    robots_url = f"{base_domain}/robots.txt"
    print(f"[+] Fetching robots.txt from: {robots_url}\n")

    disallowed_paths = []
    sitemaps = []

    req = urllib.request.Request(robots_url, headers={"User-Agent": "SecDiscoveryBot/1.0"})

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            content = response.read().decode("utf-8", errors="ignore")
            for line in content.splitlines():
                line = line.strip()
                if line.lower().startswith("disallow:"):
                    path = line.split(":", 1)[1].strip()
                    if path:
                        disallowed_paths.append(path)
                elif line.lower().startswith("sitemap:"):
                    smap = line.split(":", 1)[1].strip()
                    if smap:
                        sitemaps.append(smap)

        print("--- Disallowed Routes Found in robots.txt ---")
        if disallowed_paths:
            for p in sorted(set(disallowed_paths)):
                print(f"  [Hidden Path] {p}")
        else:
            print("  [*] No Disallow directives identified.")

        print("\n--- Sitemaps Identified ---")
        if sitemaps:
            for s in sitemaps:
                print(f"  [Sitemap] {s}")
        else:
            print("  [*] No sitemap links listed in robots.txt.")

    except urllib.error.HTTPError as e:
        print(f"[-] Could not retrieve robots.txt (HTTP Error {e.code})")
    except Exception as e:
        print(f"[-] Error querying target: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Discover hidden endpoints from robots.txt and sitemap.xml")
    parser.add_argument("url", help="Target website URL (e.g., example.com)")
    
    args = parser.parse_args()
    harvest_robots_and_sitemap(args.url)