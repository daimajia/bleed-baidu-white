# encoding: UTF-8
from flask import Flask,url_for,request,render_template
from werkzeug.routing import BaseConverter
app = Flask(__name__)

@app.route('/')
def hello_world():
	return render_template('index.html')

def getDownloadLink(url):
	import re
	from flask import jsonify
	match = re.search(r'http:\/\/(?:pan|yun).baidu.com\/share\/link\?shareid=(\d+)&uk=(\d+)',url)
	if(match):
		import urllib,urllib2
		id = match.group(1)
		uk = match.group(2)
		header = {
			'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14'
		}
		request = urllib2.Request(url = url, headers = header)
		html_code = urllib2.urlopen(request).read()

		#"md5\":\"88296788f23f16396e05e75a037bac00\"
		md5_match = re.search(r'"md5\\":\\\"(.+?)\\"',html_code)

		if(md5_match):
			md5 = md5_match.group(1)
			#dlink\\":.+?(http.+?88296788f23f16396e05e75a037bac00\?.+?sh=1)
			reg = 'dlink\\\\":.+?(http.+?' + md5 + '\?.+?sh=1)'
			print reg;
			match = re.search(reg,html_code,re.MULTILINE)
			if(match):
				return jsonify(
						url = url,
						id=id,
						uk=uk,
						error=False,
						link=match.group(1).replace("\\",""),
						type='baidu'
				)
			else:
				return jsonify(
						url=url,
						id=id,
						uk=uk,
						error=True,
						type="baidu"
					)
		else:
			return jsonify(
				url = url,
				id=id,
				uk=uk,
				error=True,
				type='baidu'
			)
	else:
		return jsonify(
				url = url,
				id=id,
				uk=uk,
				error = True,
				type = 'baidu',
			)

@app.route('/baidu/')
def baiduArgs():
	url = request.args['url'];
	if 'uk=' in url:
		return getDownloadLink(url)
	else:
		uk = request.args['uk']
		return getDownloadLink(url+ '&uk=' + uk)

@app.route('/baidu/<id>/<uk>')
def baidu(id,uk):
	return getDownloadLink('http://pan.baidu.com/share/link?shareid=%s&uk=%s' % (id , uk))

if __name__ == '__main__':
	app.debug = True
	app.run()
