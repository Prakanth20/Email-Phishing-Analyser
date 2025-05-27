import re
import string
from urllib.parse import urlparse

# List of known spoofed/suspicious domains
SPOOFED_DOMAINS = [
    'secure-paypal.com', 'banksecure.com', 'apple-id.com', 'login-alert.com'
]

# Expanded list of urgent/threatening phrases
URGENT_PHRASES = [
    "your account has been suspended", "respond within", "immediately",
    "verify your information", "unauthorized access", "login attempt",
    "limited access", "urgent action", "account will be locked",
    "immediate action required", "account will be permanently locked",
    "to secure your"
]

# Expanded list of common phishing spelling/grammar issues
COMMON_ERRORS = [
    "informations", "suspanded", "being blocked", "click hear", "verfy",
    "temporarly", "unautorized", "verifiy", "acces", "securify"
]

def extract_urls(text):
    """Extract all URLs, including those in parentheses or ending with punctuation."""
    return re.findall(r'https?://[^\s)\]]+', text)

def detect_mismatched_urls(urls):
    """Detect if a legitimate-looking domain hides a malicious link."""
    mismatched = []
    for url in urls:
        domain = urlparse(url).netloc.lower()
        if "paypal.com" in url and not domain.endswith("paypal.com"):
            mismatched.append(url)
    return mismatched

def extract_sender_domain(email_text):
    for line in email_text.splitlines():
        if line.lower().startswith("from:"):
            match = re.search(r'[\w\.-]+@([\w\.-]+)', line)
            if match:
                return match.group(1).lower()
    return ""

def analyze_email(email_text):
    print("\n=== Phishing Email Analyzer ===")

    normalized = email_text.lower().translate(str.maketrans('', '', string.punctuation))

    sender_domain = extract_sender_domain(email_text)
    spoofed = any(domain in sender_domain for domain in SPOOFED_DOMAINS)
    print(f"[+] Spoofed sender domain detected: {'Yes' if spoofed else 'No'}")

    # Normalize text for better matching
    normalized = email_text.lower().translate(str.maketrans('', '', string.punctuation))

    # 1. Check for spoofed sender domain
    spoofed = any(domain in normalized for domain in SPOOFED_DOMAINS)
    print(f"[+] Spoofed sender domain detected: {'Yes' if spoofed else 'No'}")

    # 2. Extract and evaluate URLs
    urls = extract_urls(email_text)
    print(f"[+] URLs found: {urls if urls else 'None'}")

    mismatches = detect_mismatched_urls(urls)
    print(f"[+] Mismatched/malicious URLs: {mismatches if mismatches else 'None'}")

    # 3. Detect urgency phrases
    urgent = [phrase for phrase in URGENT_PHRASES if phrase in normalized]
    print(f"[+] Urgent language found: {urgent if urgent else 'None'}")

    # 4. Check for spelling/grammar errors
    errors = [error for error in COMMON_ERRORS if error in normalized]
    print(f"[+] Spelling/grammar issues found: {errors if errors else 'None'}")

    # 5. Final verdict
    if spoofed or mismatches or urgent or errors:
        print("\n🚨 Potential phishing email detected!")
    else:
        print("\n✅ Email appears to be safe (no obvious phishing traits).")

    print("==============================\n")

# Main function to receive input
def main():
    print("📧 Paste the full email content below (press Enter twice to finish):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    email_content = "\n".join(lines)
    analyze_email(email_content)

if __name__ == "__main__":
    main()
