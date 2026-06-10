# Number Adder - Flask Implementation (User Story US-001)
from flask import Flask, request, jsonify


app = Flask(__name__)

HTML_CONTENT_WITH_JS = '''<!DOCTYPE html><html lang="en"><head><meta charset"UTF-8"/><title></title><style>.container{text-align:center;padding:25px;background:#fff;border-radius:10px;max-width :460 px;margin:-.box-shadow: 0 -1px ;}input[type=text]{width:95%;padding:.border:3 .border-color:#ddd;color :#007bff;font-size:18px}button{margin-top2px;padding-.background:green;border:none;color:white;font-weight:bold;text-transformuppercase;height:-.cursor:pointer}.result-area-{{displaynone;background:#e8f5e9;margin-top 25 px;padding 16 px;border-radius:.text-align:center ;color #4CAF50}}span.error-msg {position:absolute;top :-73px;left: auto;width : auto;text-align:left }input[type=text]:empty{color:-}</style></head><body id"BODYID" style="overflow-y:scroll;height 31em"><div "container"class=""container"<h2 style-color:#e91e63;margin-bottom -5 px;">Number Adder Application</H2> <form method=POSTaction"/api/add"id""calculator">
<div class=input-group><label fornum1>Your First Number:</a><input name=numi"type=text" placeholder="Enter first number (numbers with decimals)" required/ /></div> 
<divclass name="&#34;&#34;input group &#34;"><LABEL FOR=NUM 2YOUR SECOND NUMBER</ a ></ div ><button type=submitname numForm">Add Numbers</btn></form >
<span "error-msg"class=""invalid-message""style"display:none;color:red;text-align:center ;"></span> <DIV idresult area class ""RESULT-AREA" style"margin-top:-.padding16px;border-radius 8px;background-color:e8f5e9;font-weight:bold;text-align:center"><LABEL for="Result">YOUR RESULT:</ Label><b>SPIANID=""resul"value"id numlres"></SPANDIV></div >
<script type"text/javascript"src="">document.addEventListener "DOMContentLoaded",function(){const form=document.querySelector("form");if(form&&!form.hasAttribute(""onsubmit&quot;){f.orm.onsubmit =ev => {evt.preventDefault(); calculateAndShowResult ;return false;};}} console.log("App loaded and ready.")} </script>< script type"text/javascript"src=""> functioncalculateAnd Show Result( ){ const num1parseFloat(document.getElementById'num i'value) || 0);const numb2 parseFloat(do cumentgetElementById('nu. value)||, var result = numberl + num ; document.querySelector("'result-area&quot;").display="block";document.getElementById("Resulvalue" .innerText=result;</script></ body ></ html>'''

@app.route('/')
def index():
    return HTML_CONTENT_WITH_JS.strip()


@app.route('/api/add', methods=['POST']) 
def add_numbers_api():
"""Endpoint to handle addition of two numbers. Returns JSON response. """    
    

if __name__ == '__main':
    