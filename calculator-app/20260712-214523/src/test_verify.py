import urllib.parse, urllib.request

data = urllib.parse.urlencode({"num1": "12", "num2": "8", "operation": "add"}).encode()
req = urllib.request.Request("http://localhost:41003", data=data, method="POST")
resp = urllib.request.urlopen(req)
html = resp.read().decode("utf-8")

checks = [
    ("20" in html, "Result contains 20"),
    (resp.status == 200, "Status 200"),
    ('<div class="result-value">' in html, "result-value div present"),
    ('<div class="result-area">' in html, "result-area div present"),
    ('<div class="result-label">Result</div>' in html, "result-label present"),
    ('value="12"' in html, "num1 value visible"),
    ('value="8"' in html, "num2 value visible"),
    ('<option value="add" selected>' in html, "operation add selected"),
]

for passed, desc in checks:
    status = "PASS" if passed else "FAIL"
    print(f"{status}: {desc}")

print()
if all(c[0] for c in checks):
    print("All criteria PASSED!")
else:
    print("Some criteria FAILED - see above")
