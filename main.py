from flask import Flask,request
app=Flask(__name__)
content=""
sanitize=lambda x:"".join(["&#"+str(ord(i))+";" for i in x])
styles="""*{background-color:#000;font-family:"Courier New",Courier,monospace,mono;color:#fff;font-size:25px;}
.box{border:#888 0.2ch solid;}"""

@app.route("/",methods=["GET","POST"])
def index():
	global content
	if(request.method=="GET"):
		return("<style>"+styles+"""</style><form action="/" method="POST">
<input name="alias" type="text" required="required" placeholder="Alias"/><br/>
<textarea rows=4 columns=10 placeholder="Message" name="msg"></textarea><br/>
<input type="submit" name="Send"/><br><pre>"""+content+"</pre>",200,{"Content-Type":"text/html;charset=utf-8"})
	if(request.method=="POST"):
		alias=request.form.get("alias")
		content+="<b>"+sanitize(alias)+"</b><br><br><div class=\"box\">"+sanitize(request.form.get("msg"))+"</div><!--\n-->"
		return("<style>"+styles+"""</style><form action="/" method="POST">
<input name="alias" type="text" required="required" placeholder="Alias" """+"value=\""+alias+"\""+"""/><br/>
<textarea rows=4 columns=10 placeholder="Message" name="msg"></textarea><br/>
<input type="submit" name="Send"/><br><pre>"""+content+"</pre>",200,{"Content-Type":"text/html;charset=utf-8"})

@app.route("/delete_content",methods=["GET","POST"])
def delete_content():
	global content
	if(request.method=="GET"):
		return("<form action=\"/delete.php\" method=\"POST\">\
<input type=\"text\" name=\"code\" required>\
<input type=\"submit\" name=\"Submit\">\
</form>",200,{"Content-Type":"text/html;charset=utf-8"})
	if(request.method=="POST"):
		if(0):#flask.request.form[0].code==flask.request.url): #Probably should make this more secure...
			content=""
			return("CONTENT RESET",200,{"Content-Type":"text/plain;charset=utf-8"})
			print("content has been reset")
		else:
			return("CONTENT NOT RESET",200,{"Content-Type":"text/plain;charset=utf-8"})

@app.route("/content.var")
def contenttxt():
	global content
	return(content,200,{"Content-Type":"text/plain;charset=utf-8"})

if(__name__=="__main__"):
	app.run(host="127.0.0.1",port=5000,debug=0)
