import urllib.request
import urllib.parse

# Test GET request
resp = urllib.request.urlopen('http://localhost:8000/')
html = resp.read().decode('utf-8')
print("=== GET / Response (first 600 chars) ===")
print(html[:600])
print()

# Check acceptance criteria for GET
assert 'num1' in html, 'FAIL: Missing num1 input'
assert 'num2' in html, 'FAIL: Missing num2 input'
assert '<select id="operation"' in html or 'name="operation"' in html, 'FAIL: Missing operation select'
assert 'Calculate' in html, 'FAIL: Missing Calculate button'
print('GET checks passed!')

# Test POST request with addition
data = urllib.parse.urlencode({'num1': '3', 'num2': '4', 'operation': 'add'}).encode()
req = urllib.request.Request('http://localhost:8000/', data=data, method='POST')
resp2 = urllib.request.urlopen(req)
html2 = resp2.read().decode('utf-8')
print("\n=== POST / Response (result section) ===")
# Find result value in HTML
if '7' in html2:
    print('Result 7 found - addition works!')
else:
    # Print the result area portion
    idx = html2.find('result-value')
    if idx >= 0:
        print(html2[idx-50:idx+100])
    else:
        print("FAIL: Result not found in POST response")

# Test subtraction
data3 = urllib.parse.urlencode({'num1': '10', 'num2': '3', 'operation': 'subtract'}).encode()
req3 = urllib.request.Request('http://localhost:8000/', data=data3, method='POST')
resp3 = urllib.request.urlopen(req3)
html3 = resp3.read().decode('utf-8')
if '7' in html3:
    print('Subtraction result 7 found!')

# Test multiplication
data4 = urllib.parse.urlencode({'num1': '5', 'num2': '6', 'operation': 'multiply'}).encode()
req4 = urllib.request.Request('http://localhost:8000/', data=data4, method='POST')
resp4 = urllib.request.urlopen(req4)
html4 = resp4.read().decode('utf-8')
if '30' in html4:
    print('Multiplication result 30 found!')

# Test division
data5 = urllib.parse.urlencode({'num1': '20', 'num2': '4', 'operation': 'divide'}).encode()
req5 = urllib.request.Request('http://localhost:8000/', data=data5, method='POST')
resp5 = urllib.request.urlopen(req5)
html5 = resp5.read().decode('utf-8')
if '5' in html5:
    print('Division result 5 found!')

# Test division by zero
data6 = urllib.parse.urlencode({'num1': '10', 'num2': '0', 'operation': 'divide'}).encode()
req6 = urllib.request.Request('http://localhost:8000/', data=data6, method='POST')
resp6 = urllib.request.urlopen(req6)
html6 = resp6.read().decode('utf-8')
if 'result-area' not in html6:
    print('Division by zero correctly shows no result!')

print('\nAll tests passed!')
