import flask,hashlib,uuid
app=flask.Flask(__name__)
content=""
sanitize=lambda x:"".join(["&#"+str(ord(i))+";" for i in x])
styles="""*{background-color:#000;font-family:"Courier New",Courier,monospace,mono;color:#fff;font-size:25px;}
.box{border:#888 0.2ch solid;}"""
pastes={}

@app.route("/",methods=["GET","POST"])
def index():
	global content
	if(flask.request.method=="GET"):
		return("<style>"+styles+"""</style><form action="/" method="POST">
<input name="alias" type="text" required="required" placeholder="Alias"/><br/>
<textarea rows=4 columns=10 placeholder="Message" name="msg"></textarea><br/>
<input type="submit" name="Send"/><br><pre>"""+content+"</pre>",200,{"Content-Type":"text/html;charset=utf-8"})
	if(flask.request.method=="POST"):
		content+="<b>"+sanitize(flask.request.form["alias"])+"</b><br><br><div class=\"box\">"+sanitize(flask.request.form["msg"])+"</div><!--\n-->"
		return("<style>"+styles+"""</style><form action="/" method="POST">
<input name="alias" type="text" required="required" placeholder="Alias" """+"value=\""+flask.request.form["alias"]+"\""+"""/><br/>
<textarea rows=4 columns=10 placeholder="Message" name="msg"></textarea><br/>
<input type="submit" name="Send"/><br><pre>"""+content+"</pre>",200,{"Content-Type":"text/html;charset=utf-8"})

@app.route("/delete_content",methods=["GET","POST"])
def delete_content():
	global content
	if(flask.request.method=="GET"):
		return("<form action=\"/delete.php\" method=\"POST\">\
<input type=\"text\" name=\"code\" required>\
<input type=\"submit\" name=\"Submit\">\
</form>",200,{"Content-Type":"text/html;charset=utf-8"})
	if(flask.request.method=="POST"):
		if(0):#flask.request.form[0].code==flask.request.url): #Probably should make this more secure...
			content=""
			return("CONTENT RESET",200,{"Content-Type":"text/plain;charset=utf-8"})
			print("content has been reset")
		else:
			return("CONTENT NOT RESET",403,{"Content-Type":"text/plain;charset=utf-8"})

@app.route("/paste/")
def pasteindex():
	return(styles+"<a href=\"/paste/new\">Create a new paste</a><br><a href=\"/paste/all\">View all pastes</a>",200,{"Content-Type":"text/html;charset=utf-8"})

@app.route("/paste/new",methods=["GET","POST"])
def newpaste():
	if(flask.request.method=="GET"):
		return(styles+"""<form action="/paste/new" method="POST">
<textarea name="code" rows=4 columns=10 placeholder="Paste"></textarea>
<input type="submit" value="Create Paste">
</form>""")
	if(flask.request.method=="POST"):
		pastes[uuid.uuid5(uuid.UUID("00000000-0000-0000-0000-000000000000"),flask.request.form["code"])]=flask.request.form["code"]
		return(styles+"<a href=\"/paste/view/"+uuid.uuid5(uuid.UUID("00000000-0000-0000-0000-000000000000"),flask.request.form["code"])+"\">Your paste!</a>")

@app.route("/paste/view/<guid>")
def getpaste(guid):
	return(pastes[guid],200,{"Content-Type":"text/plain;charset=utf-8"})

@app.route("/paste/all")
def allpastes():
	return(styles+"<br>\n".join([f"<a href=\"/paste/view/{i}\">{i}</a>" for i in pastes]),200,{"Content-Type":"text/html;charset=utf-8"})

@app.route("/content.var")
def contenttxt():
	global content
	return(content,200,{"Content-Type":"text/plain;charset=utf-8"})

if(__name__=="__main__"):
	app.run(host="127.0.0.1",port=5000,debug=0)
