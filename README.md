# Alvin Dork Scanner

![Alvin](./image.png)

This script utilizes Google Dorking techniques via the [Serper API](https://serper.dev/) to search for potentially vulnerable websites or exposed information based on predefined lists of search queries (dorks).

## Features

* Alvin scans Google using specific dorks categorized into:
    * Cross-Site Scripting (XSS) - Primarily focused on `.tr` domains.
    * SQL Injection (SQLi) - Primarily focused on `.tr` domains.
    * Sensitive Documents & Exposures - General dorks for potentially leaked files, configurations, etc.
    * Exposed CCTV/DVR Panels - Dorks to find accessible camera interfaces.
* Alvin scanner uses the fast and efficient Serper API for search results.
* Configurable number of search result pages to scan per dork.
* Command-line interface for selecting dork categories.
* Outputs unique found links to a specified file (`vulnerable_links.txt` by default).
* Includes a delay between requests (`time.sleep(1.5)`) to avoid hitting API rate limits too quickly.

## Requirements

* Python 3.x
* `requests` library (`pip install requests`)
* A Serper API Key (Get one from [serper.dev](https://serper.dev/))

## Installation

1.  **Clone or Download:** Get the script file (`dork_scanner.py` - replace with the actual filename).
2.  **Install Dependencies:**
    ```bash
    pip install requests
    ```

## Configuration

**IMPORTANT:** You **MUST** replace the placeholder API key in the script with your own Serper API key.

1.  Open the script file (`dork_scanner.py`).
2.  Find the line:
    ```python
    SERPER_API_KEY = "YOUR_SERPER_API_KEY"  # Replace with your actual key
    ```
3.  Replace `"YOUR_SERPER_API_KEY"` with your **actual Serper API key**.
4.  Save the file.

**Keep your API key confidential!** Do not share it or commit it to public repositories.

## Usage

Run the script from your terminal. You need to specify at least one dork category to scan.

```bash
python your_script_name.py [options]
```

### Options

* `--xss`: Scan using the XSS dorks list.
* `--sqli`: Scan using the SQLi dorks list.
* `--sensitive-documents`: Scan using the sensitive documents/exposures dorks list.
* `--cctv`: Scan using the CCTV/DVR dorks list.
* `--output <filename>`: Specify the name for the output file (default: `vulnerable_links.txt`).
* `-h`, `--help`: Show the help message and exit.

### Execution Flow

1.  Run the script with desired category flags (e.g., `--xss --sqli`).
2.  If no category flag is provided, the script will print the help message and exit.
3.  The script will prompt you to enter the number of Google search result pages you want to scan for *each* dork.
4.  It will then iterate through the selected dorks, query the Serper API, and print progress.
5.  Found links will be collected.
6.  Finally, unique links will be saved to the specified output file.

### Examples

* **Scan for XSS and SQLi vulnerabilities, scanning 5 pages per dork:**
    ```bash
    python alvin_scanner.py --xss --sqli
    # Script will ask: How many pages to scan per dork? Enter 5
    ```
* **Scan for Sensitive Documents and CCTV panels, scanning 3 pages per dork, saving to `exposed_systems.txt`:**
    ```bash
    python alvin_scanner.py --sensitive-documents --cctv --output exposed_systems.txt
    # Script will ask: How many pages to scan per dork? Enter 3
    ```
* **Scan for all categories, scanning 2 pages per dork:**
    ```bash
    python alvin_scanner.py --xss --sqli --sensitive-documents --cctv
    # Script will ask: How many pages to scan per dork? Enter 2
    ```

### Output

Alvin script generates a text file (default: `vulnerable_links.txt`) containing a list of unique URLs found during the scan, with each URL on a new line.

### Disclaimer

⚠️ **This tool is intended for educational and research purposes ONLY.**

* Using this script for unauthorized scanning or accessing systems you do not have explicit permission to test is **illegal and unethical**.
* The authors and contributors are not responsible for any misuse or damage caused by this script.
* You are solely responsible for your actions and for complying with all applicable laws and terms of service (including Google's and Serper's).
* Use this tool responsibly and only on systems you own or have explicit, written permission to test.