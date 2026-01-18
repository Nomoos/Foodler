# How to Fix kupi.cz DNS Resolution Issue

## Problem Summary

The original test showed: **kupi.cz: ❌ NOT ACCESSIBLE (DNS resolution fails)**

This was due to a **temporary network/DNS issue** at the time of testing. The domain `www.kupi.cz` could not be resolved from the GitHub Actions environment.

## Current Status ✅

**The DNS issue is now RESOLVED!** The website is accessible:

```
DNS Resolution: ✅ Working
www.kupi.cz → 104.26.11.94, 172.67.70.35, 104.26.10.94 (Cloudflare)

HTTP Connectivity: ✅ Working
Status: 200 OK
Server: Cloudflare
```

## Why Did This Happen?

The DNS failure was likely caused by one of these temporary issues:

1. **Temporary DNS propagation delay** - Cloudflare DNS changes take time
2. **Network routing issues** - Temporary connectivity problems in GitHub Actions
3. **Rate limiting** - Too many requests to DNS servers
4. **Cloudflare protection** - Temporary blocking of requests
5. **GitHub Actions network restrictions** - Transient firewall rules

## Solutions & Workarounds

### 1. **Retry with Backoff** (Recommended)

Add retry logic to handle temporary DNS failures:

```python
import time
import requests
from requests.exceptions import RequestException

def fetch_with_retry(url, max_retries=3, backoff=2):
    """Fetch URL with exponential backoff retry"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response
        except RequestException as e:
            if attempt < max_retries - 1:
                wait_time = backoff ** attempt
                print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
```

### 2. **Use Alternative DNS Servers**

Configure Python to use public DNS (Google, Cloudflare):

```python
import socket
import dns.resolver

# Use Cloudflare DNS
resolver = dns.resolver.Resolver()
resolver.nameservers = ['1.1.1.1', '1.0.0.1']

# Or use Google DNS
resolver.nameservers = ['8.8.8.8', '8.8.4.4']
```

### 3. **Direct IP Connection** (Emergency Fallback)

Use Cloudflare IPs directly with Host header:

```python
headers = {
    'Host': 'www.kupi.cz',
    'User-Agent': 'Mozilla/5.0...'
}

# Use direct IP
response = requests.get('https://104.26.11.94', headers=headers, verify=True)
```

### 4. **Check DNS Before Scraping**

Add a health check function:

```python
def check_kupi_accessibility():
    """Check if kupi.cz is accessible"""
    try:
        # Try DNS resolution
        socket.gethostbyname('www.kupi.cz')
        
        # Try HTTP connection
        response = requests.head('https://www.kupi.cz', timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"kupi.cz not accessible: {e}")
        return False
```

### 5. **Environment-Specific Configuration**

Use different scraping strategies based on environment:

```python
import os

if os.environ.get('GITHUB_ACTIONS'):
    # GitHub Actions environment - use more robust settings
    TIMEOUT = 30
    MAX_RETRIES = 5
    USE_PROXY = True
else:
    # Local environment - standard settings
    TIMEOUT = 10
    MAX_RETRIES = 3
    USE_PROXY = False
```

## Testing the Fix

Run the web access test again to verify:

```bash
# Full test
python test_web_access_report.py

# Quick test
python -c "
from src.scrapers.kupi_scraper import KupiCzScraper
with KupiCzScraper() as scraper:
    soup = scraper.fetch_page('https://www.kupi.cz')
    print('✅ Connected!' if soup else '❌ Failed')
"
```

## Next Steps

### Current Issue: HTML Parsing Needs Update

While DNS is working, the scraper needs HTML structure updates:

```
✅ DNS Resolution: Fixed
✅ HTTP Connection: Working
❌ Product Extraction: Not working (HTML selectors need update)
```

The website structure has changed. Current selectors:
```python
# Old (not working):
product_elements = soup.find_all('div', class_='product-item')

# Need to investigate actual structure
```

To fix product extraction, we need to:
1. Analyze current HTML structure
2. Update CSS selectors in `kupi_scraper.py`
3. Test with real products

## Monitoring

To prevent future issues, add monitoring:

```python
import logging

def log_scraper_health():
    """Log scraper health metrics"""
    try:
        # Test DNS
        dns_ok = bool(socket.gethostbyname('www.kupi.cz'))
        
        # Test HTTP
        http_ok = requests.head('https://www.kupi.cz', timeout=5).ok
        
        logging.info(f"Scraper Health: DNS={dns_ok}, HTTP={http_ok}")
    except Exception as e:
        logging.error(f"Scraper unhealthy: {e}")
```

## Summary

| Issue | Status | Solution |
|-------|--------|----------|
| DNS Resolution | ✅ Fixed | Was temporary - now working |
| HTTP Connectivity | ✅ Working | Cloudflare serving content |
| Product Extraction | ❌ Needs work | Update HTML selectors |

## Recommendations

1. **Immediate**: DNS is working - no action needed
2. **Short-term**: Add retry logic for robustness
3. **Medium-term**: Update HTML parsers to match current structure
4. **Long-term**: Consider kupi.cz API if available

---

**Last Updated:** 2026-01-18  
**Status:** DNS issue resolved, HTML parsing needs update
