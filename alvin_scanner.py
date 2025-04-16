import requests
import time
import argparse

# === CONFIG ===
SERPER_API_KEY = ""
HEADERS = {
    "X-API-KEY": SERPER_API_KEY,
    "Content-Type": "application/json"
}

# === CLEANED & ORGANIZED DORK LISTS ===
XSS_DORKS = [
    "site:.tr view.php?username=",
    "site:.tr inurl:categories.php?categoriesName=",
    "site:.tr inurl:/opencms/opencms/",
    "site:.tr inurl:/opencms/opencms/upload",
    "site:.tr inurl:/wp-content/plugins/wp-useronline/",
    "site:.tr inurl:.php?cmd=",
    "site:.tr inurl:.php?q=",
    "site:.tr inurl:.php?search=",
    "site:.tr inurl:.php?query=",
    "site:.tr inurl:.php?file=",
    "site:.tr inurl:.php?txt=",
    "site:.tr inurl:.php?tag=",
    "site:.tr inurl:.php?author=",
    "site:.tr inurl:.php?feedback=",
    "site:.tr inurl:.php?mail=",
    "site:.tr inurl:.php?cat=",
    "site:.tr inurl:.php?vote=",
    "site:.tr inurl:search.php?q=",
    "site:.tr inurl:haber.php?id=",
    "site:.tr inurl:mesaj.php?mesaj=",
    "site:.tr inurl:sayfa.php?sayfa=",
    "site:.tr inurl:arama.php?ara=",
    "site:.tr inurl:profil.php?kullanici=",
    "site:.tr inurl:detay.php?detay_id=",
    "site:.tr inurl:gonder.php?mesaj=",
    "site:.tr inurl:video.php?video=",
    "site:.tr inurl:blog.php?yazi=",
    "site:.tr inurl:form.php?ad=",
    "site:.tr inurl:ara.php?q=",
    'site:.tr intitle:"elFinder 2.1.53"',
    "site:.tr inurl:q=",
    "site:.tr inurl:search=",
    "site:.tr inurl:query=",
    "site:.tr inurl:lang="
]

SQLI_DORKS = [
    "site:.tr inurl:index.php?id=",
    "site:.tr inurl:product.php?id=",
    "site:.tr inurl:view.php?id=",
    "site:.tr inurl:news.php?id=",
    "site:.tr inurl:details.php?id=",
    "site:.tr inurl:category.php?id=",
    "site:.tr inurl:article.php?id=",
    "site:.tr inurl:content.php?ID=",
    "site:.tr inurl:detail.php?id=",
    "site:.tr inurl:details.php?ProdID=",
    "site:.tr inurl:gallery.php?id=",
    "site:.tr inurl:main.php?id=",
    "site:.tr inurl:news.php?id=",
    "site:.tr inurl:product.php?pid=",
    "site:.tr inurl:view.php?cid="
]



SENSITIVE_DOCS_DORKS = [
    'site:.tr intitle:"index of" "config.php"',
    'site:.tr intitle:"index of" "wp-config"',
    'site:.tr intitle:"index of" "admin"',
    'site:.tr inurl:viewfile',
    'site:.tr inurl:/admin.php',
    'site:.tr filetype:pdf "confidential"',
    'site:.tr inurl:login OR inurl:admin OR inurl:signin',
    'site:.tr intitle:"Admin Panel" inurl:admin',
    'secret inurl:js filetype:txt'
]

CCTV_DORKS = [
    'site:.tr intitle:"Live View / - AXIS" | inurl:view/index.shtml',
    'site:.tr inurl:view/view.shtml',
    'site:.tr inurl:ViewerFrame?Mode=Motion',
    'site:.tr intitle:"IPCam - Web Camera"',
    'site:.tr inurl:axis-cgi/mjpg',
    'site:.tr intitle:"WJ-NT104 Main Page"',
    'site:.tr intitle:"liveapplet"',
    'site:.tr intitle:"Network Camera NetworkCamera"',
    'site:.tr inurl:netw_tcp.shtml',
    'site:.tr intitle:"supervisioncam protocol"',
    'site:.tr inurl:/control/userimage.html',
    'site:.tr intitle:"DVR Web Client"',
    'site:.tr inurl:/app/index.html "camera"',
    'site:.tr inurl:/view/view.shtml'
]

GIT_SENSITIVE_DORKS = [
    'inurl:.git-credentials',
    'inurl:.gitconfig',
    'intext:"index of /.git" "parent directory"',
    'filetype:git -github.com inurl:"/.git"',
    '(intext:"index of /.git") ("parent directory")',
    'inurl:ORIG_HEAD',
    'intitle:"index of" ".gitignore"',
    '".git" intitle:"Index of"',
    '"Parent Directory" "Last modified" git',
    'inurl:git'
]

AWS_SENSITIVE_DORKS = [
    'site:http://s3.amazonaws.com intitle:index.of.bucket',
    'site:http://amazonaws.com inurl:".s3.amazonaws.com/"',
    'site:.s3.amazonaws.com "Company"',
    'intitle:index.of.bucket',
    'site:http://s3.amazonaws.com intitle:Bucket loading',
    'site:*.amazonaws.com inurl:index.html',
    '"Bucket Date Modified"'
]

DB_SENSITIVE_DORKS = [
    'inurl:db.sql',
    'inurl:db.sqlite',
    'inurl:setup.sql',
    'inurl:mysql.sql',
    'inurl:users.sql',
    'inurl:backup.sql',
    'inurl:db filetype:sql',
    'inurl:backup filetype:sql',
    'create table filetype:sql',
    '"-- MySQL dump" "Server version" "Table structure for table"',
    'inurl:/db/websql/',
    'filetype:sql'
]

MODERN_TECH_DORKS = [
    'site:.tr inurl:/api/',
    'site:.tr inurl:/graphql',
    'site:.tr filetype:json inurl:(config | settings | credentials)',
    'site:.tr inurl:swagger filetype:yaml',
    'site:.tr inurl:openapi filetype:json',
    'site:.tr intext:"api_key" filetype:js',
    'site:.tr inurl:endpoint filetype:json',
    'site:.tr intext:"Bearer token" ext:log',
    'site:.tr inurl:/rest/ filetype:json',
    'site:.tr inurl:/.well-known/ filetype:json',
    'site:.tr inurl:/api/ intext:"error"',
    'site:.tr inurl:/graphql intext:"query"',
    'site:.tr intext:"api_key" ext:txt',
    'site:.tr inurl:(/v1/ | /v2/) filetype:json'
]

def search_dork(query, page=1):
    payload = {
        "q": query,
        "gl": "tr",
        "hl": "tr",
        "num": 10,
        "page": page
    }
    response = requests.post("https://google.serper.dev/search", json=payload, headers=HEADERS)
    response.raise_for_status()
    results = response.json()
    return [item["link"] for item in results.get("organic", [])]

def run_dorks(dorks, start_page, max_pages):
    all_links = set()
    for dork in dorks:
        print(f"[+] Dork: {dork}")
        for page in range(start_page, start_page + max_pages):
            try:
                links = search_dork(dork, page=page)
                print(f"    → Page {page}: {len(links)} result(s)")
                all_links.update(links)
                time.sleep(1.5)
            except Exception as e:
                print(f"[-] Error on dork '{dork}' page {page}: {e}")
    return all_links

def main():
    parser = argparse.ArgumentParser(description="🇹🇷 Google Dork Scanner for Turkish Targets")
    parser.add_argument("--xss", action="store_true", help="Scan XSS dorks")
    parser.add_argument("--sqli", action="store_true", help="Scan SQLi dorks")
    parser.add_argument("--sensitive-documents", action="store_true", help="Scan for sensitive documents and rare exposures")
    parser.add_argument("--cctv", action="store_true", help="Scan for exposed CCTV and DVR panels")
    parser.add_argument("--modern-tech", action="store_true", help="Scan for modern technology exposures (API, JSON, etc.)")
    parser.add_argument("--git-sensitive", action="store_true", help="Scan for exposed Git repositories and credentials")
    parser.add_argument("--aws", action="store_true", help="Scan for exposed AWS S3 buckets and cloud assets")
    parser.add_argument("--db", action="store_true", help="Scan for exposed SQL/database dumps")
    parser.add_argument("--output", type=str, default="vulnerable_links.txt", help="Output file name")

    args = parser.parse_args()

    if not any([args.xss, args.sqli, args.sensitive_documents, args.cctv, args.modern_tech]):
        parser.print_help()
        return

    try:
        max_pages = int(input("🔢 How many pages to scan per dork? "))
        start_page = int(input("⏩ From which page should the scan start? "))
    except ValueError:
        print("❌ Invalid input. Please enter a valid number.")
        return

    selected_dorks = []
    if args.xss:
        selected_dorks.extend(XSS_DORKS)
    if args.sqli:
        selected_dorks.extend(SQLI_DORKS)
    if args.sensitive_documents:
        selected_dorks.extend(SENSITIVE_DOCS_DORKS)
    if args.cctv:
        selected_dorks.extend(CCTV_DORKS)
    if args.modern_tech:
        selected_dorks.extend(MODERN_TECH_DORKS)
    if args.git_sensitive:
        selected_dorks.extend(GIT_SENSITIVE_DORKS)
    if args.aws:
        selected_dorks.extend(AWS_SENSITIVE_DORKS)
    if args.db:
        selected_dorks.extend(DB_SENSITIVE_DORKS)



    links = run_dorks(selected_dorks, start_page, max_pages)

    with open(args.output, "w", encoding="utf-8") as f:
        for link in sorted(links):
            f.write(link + "\n")

    print(f"\n[✓] Done. {len(links)} links saved to {args.output}")

if __name__ == "__main__":
    main()