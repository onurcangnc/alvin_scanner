import requests
import time
import argparse
import uuid

# === CONFIG ===
SERPER_API_KEY = ""  
HEADERS = {
    "X-API-KEY": SERPER_API_KEY,
    "Content-Type": "application/json"
}

# === DORK LISTS ===
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
    '"intitle:"elFinder 2.1.53""',
    'inurl:/wp-content/plugins/ "xss"',
    'inurl:(login.php?user=)',
    'inurl:(search.php?term=) "xss"',
    'inurl:(index.php?page=) "xss"'
]

SQLI_DORKS = [
    "site:.tr inurl:index.php?id=",
    "site:.tr inurl:product.php?id=",
    "site:.tr inurl:view.php?id=",
    "site:.tr inurl:news.php?id=",
    "site:.tr inurl:item.php?id=",
    "site:.tr inurl:details.php?id=",
    "site:.tr inurl:category.php?id=",
    "site:.tr inurl:showproduct.php?prodid=",
    "site:.tr inurl:catalog.php?catid=",
    "site:.tr inurl:search.php?q=",
    'site:.tr intext:"You have an error in your SQL syntax"',
    'site:.tr intext:"Warning: mysql_fetch_array()" ext:php',
    'site:.tr intext:"Unclosed quotation mark" AND intext:"Microsoft OLE DB Provider for SQL Server" AND intext:"80040e14"',
    'inurl:(admin.php?id=) "sqli"',
    'inurl:(product.php?prod_id=) "sql injection"',
    'inurl:(newsdetail.php?newsid=)',
    'intext:"sql error" ext:php'
]

SENSITIVE_DOCS_DORKS = [
    'filetype:sql password',
    'filetype:log inurl:"password.log"',
    'filetype:xls inurl:"email.xls"',
    'filetype:mdb inurl:"users.mdb"',
    'filetype:ini inurl:"flashFXP.ini"',
    'intitle:"index of" "config.php"',
    'intitle:"index of" "wp-config"',
    'intitle:"index of" "admin"',
    'filetype:bak inurl:"htaccess|passwd|shadow"',
    'intitle:"index of" "upload_image.php"',
    'intitle:"index of" "Production.json"',
    'intitle:"index of" "schema.sql"',
    'inurl:viewfile',
    'filetype:cnf my.cnf',
    'filetype:wsdl wsdl',
    'filetype:inc intext:setcookie',
    'inurl:php.ini filetype:ini',
    'filetype:pem intext:private',
    'filetype:config config intext:appSettings "User ID"',
    'inurl:/admin.php',
    'filetype:json inurl:config',
    'filetype:yaml inurl:api',
    'inurl:swagger filetype:json',
    'filetype:env intext:API_KEY',
    'intitle:"index of" ".git"',
    'intext:"password" ext:log',
    'filetype:pdf "confidential"'
]

CCTV_DORKS = [
    'intitle:"Live View / - AXIS" | inurl:view/index.shtml',
    'inurl:view/view.shtml',
    'inurl:ViewerFrame?Mode=Motion',
    'intitle:"IPCam - Web Camera"',
    'inurl:axis-cgi/mjpg',
    'intitle:"WJ-NT104 Main Page"',
    'intitle:"liveapplet"',
    'intitle:"Network Camera NetworkCamera"',
    'inurl:netw_tcp.shtml',
    'intitle:"supervisioncam protocol"',
    'inurl:/control/userimage.html',
    'intitle:"DVR Web Client"',
    'inurl:/app/index.html "camera"'
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
    'inurl:/api/ intext:"error"',
    'inurl:/graphql intext:"query"',
    'intext:"api_key" ext:txt',
    'inurl:(/v1/ | /v2/) filetype:json'
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

def run_dorks(dorks, max_pages):
    all_links = set()
    for dork in dorks:
        print(f"[+] Dork: {dork}")
        for page in range(1, max_pages + 1):
            try:
                links = search_dork(dork, page=page)
                print(f"    → Page {page}: {len(links)} result(s)")
                all_links.update(links)
                time.sleep(1.5)
            except Exception as e:
                print(f"[-] Error on dork '{dork}' page {page}: {e}")
    return all_links

def main():
    parser = argparse.ArgumentParser(description="Google Dork Scanner")
    parser.add_argument("--xss", action="store_true", help="Scan XSS dorks")
    parser.add_argument("--sqli", action="store_true", help="Scan SQLi dorks")
    parser.add_argument("--sensitive-documents", action="store_true", help="Scan for sensitive documents and rare exposures")
    parser.add_argument("--cctv", action="store_true", help="Scan for exposed CCTV and DVR panels")
    parser.add_argument("--modern-tech", action="store_true", help="Scan for modern technology exposures (API, JSON, etc.)")
    parser.add_argument("--output", type=str, default="vulnerable_links.txt", help="Output file name")

    args = parser.parse_args()

    if not any([args.xss, args.sqli, args.sensitive_documents, args.cctv, args.modern_tech]):
        parser.print_help()
        return

    try:
        max_pages = int(input("🔢 How many pages to scan per dork? "))
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

    links = run_dorks(selected_dorks, max_pages)

    with open(args.output, "w", encoding="utf-8") as f:
        for link in sorted(links):
            f.write(link + "\n")

    print(f"\n[✓] Done. {len(links)} links saved to {args.output}")


if __name__ == "__main__":
    main()