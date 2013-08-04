# encoding: UTF-8
from flask import Flask,url_for,request,render_template
from werkzeug.routing import BaseConverter
app = Flask(__name__)

class RegexConverter(BaseConverter):
	def __init__(self,url_map,*item):
		super(RegexConverter,self).__init__(url_map)
		self.regex = item[0]

app.url_map.converters['regex'] = RegexConverter


@app.route('/')
def hello_world():
	return render_template('index.html')

@app.route('/<regex("http:\/\/pan.baidu.com\/share\/link\?shareid=\d+&uk=\d+"):url>/')
def baidu_get(url):
	return url

@app.route('/baidu/<id>/<uk>')
def baidu(id,uk):
	import urllib,urllib2
	from flask import jsonify
	app.logger.warning('Request id:'+id)
	app.logger.warning('Request uk:'+uk)
	url = 'http://pan.baidu.com/share/link?shareid=%s&uk=%s' %(id,uk)
	header = {
		'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14',
	}
	request = urllib2.Request(url= url,headers = header)
	html_code = urllib2.urlopen(request).read()
	import re
	match = re.search(r'dlink\\.+?(http.+?)\\"',html_code,re.MULTILINE)
	if(match):
		return jsonify(
				id=id,
				uk=uk,
				error=False,
				link=match.group(1),
				type='baidu'
			)
	else:
		return jsonify(
			id=id,
			uk=uk,
			error=True,
			type='baidu'
		)

if __name__ == '__main__':
	app.debug = True
	app.run()
