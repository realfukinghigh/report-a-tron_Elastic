from flask import Flask, render_template, request, redirect, url_for
from elasticstuff import search
from webhandlers import assetsflask, engagementsflask, testsflask, issuesflask, thirdpartyflask, servicesflask, statsflask, reportsflask, loginflask
from waitress import serve
import config
import flask_login


app = Flask(__name__)
config_values = config.StaticValues().config_file
app.config.from_object(config_values['config_type'])
print(app.config)

searchConnection = search.Search()

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def user_loader(username):
    return loginflask.user_loader(username)

@app.route('/login', methods=['GET'])
def login():
	return loginflask.login()

@app.route('/loginapi', methods=['POST'])
def loginapi():
    return loginflask.loginapi()

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))

@app.after_request
def set_response_headers(response):
	response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
	response.headers['Pragma'] = 'no-cache'
	response.headers['Expires'] = '0'
	return response

@app.route("/")
@flask_login.login_required
def main():
	return render_template('index.html')

@app.route("/createasset")
@flask_login.login_required
def createasset():
	return assetsflask.createasset()

@app.route("/error")
@flask_login.login_required
def error():
	return render_template('error.html')

@app.route("/viewassets")
@flask_login.login_required
def viewassets():
	return assetsflask.viewassets()

@app.route("/createassetapi", methods=['POST'])
@flask_login.login_required
def createassetapi():
	return assetsflask.createassetapi()

@app.route("/updateasset")
@flask_login.login_required
def updateasset():
	return assetsflask.updateasset()

@app.route("/updateassetapi", methods=['POST'])
@flask_login.login_required
def updateassetapi():
	return assetsflask.updateassetapi()

@app.route("/engagements", methods=['GET'])
@flask_login.login_required
def engagements():
	return engagementsflask.engagements()

@app.route("/createengagement", methods=['POST'])
@flask_login.login_required
def createengagement():
	return engagementsflask.createengagement()

@app.route("/openengagements")
@flask_login.login_required
def openengagements():
	return engagementsflask.openengagements()

@app.route("/viewengagements")
@flask_login.login_required
def viewengagements():
	return engagementsflask.viewengagements()

@app.route("/updateengagement")
@flask_login.login_required
def updateengagement():
	return engagementsflask.updateengagement()

@app.route("/updateengagementapi", methods=['POST'])
@flask_login.login_required
def updateengagementapi():
	return engagementsflask.updateengagementapi()

@app.route("/createtest", methods=['GET'])
@flask_login.login_required
def createtest():
	return testsflask.createtest()

@app.route("/createtestapi", methods=['POST'])
@flask_login.login_required
def createtestapi():
	return testsflask.createtestapi()

@app.route("/viewtests", methods=['GET'])
@flask_login.login_required
def viewtests():
	return testsflask.viewtests()

@app.route("/updatetest")
@flask_login.login_required
def updatetest():
	return testsflask.updatetest()

@app.route("/updatetestapi", methods=['POST'])
@flask_login.login_required
def updatetestapi():
	return testsflask.updatetestapi()

@app.route("/viewissues", methods=['GET'])
@flask_login.login_required
def viewissues():
	return issuesflask.viewissues()

@app.route("/createissue", methods=['GET'])
@flask_login.login_required
def createissue():
	return issuesflask.createissue()

@app.route("/createissueapi", methods=['POST'])
@flask_login.login_required
def createissueapi():
	return issuesflask.createissueapi()

@app.route("/updateissue", methods=['GET'])
@flask_login.login_required
def updateissue():
	return issuesflask.updateissue()

@app.route("/updateissueapi", methods=['POST'])
@flask_login.login_required
def updateissueapi():
	return issuesflask.updateissueapi()

@app.route("/linkissue", methods=['GET'])
@flask_login.login_required
def linkissue():
	return issuesflask.linkissue()

@app.route("/issuelinkapi", methods=['POST'])
@flask_login.login_required
def issuelinkapi():
	return issuesflask.issuelinkapi()

@app.route("/testreport", methods=['GET'])
@flask_login.login_required
def testreport():
	return reportsflask.testReport()

@app.route("/stats")
@flask_login.login_required
def stats():
	return render_template('stats.html')

@app.route("/viewstats")
@flask_login.login_required
def viewstats():
	return statsflask.viewstats()

@app.route("/search")
@flask_login.login_required
def search():
	searchTerm = request.args.get('searchTerm')
	data = searchConnection.search(searchTerm)
	return render_template('searchresults.html', data=data)

@app.route("/viewthirdparty")
@flask_login.login_required
def viewthirdparty():
	return thirdpartyflask.viewthirdparty()

@app.route("/createthirdparty")
@flask_login.login_required
def createthirdparty():
	return render_template('createthirdparty.html')

@app.route("/updatethirdparty")
@flask_login.login_required
def updatethirdparty():
	return thirdpartyflask.updatethirdparty()

@app.route("/updatethirdpartyapi", methods=['POST'])
@flask_login.login_required
def updatethirdpartyapi():
	return thirdpartyflask.updatethirdpartyapi()

@app.route('/viewservices')
@flask_login.login_required
def viewservices():
	return servicesflask.viewservices()

@app.route('/viewservicedetail')
@flask_login.login_required
def viewservicedetail():
	service_id = request.args.get('service_id')
	return servicesflask.viewservicedetail(service_id)

@app.route('/createservice')
@flask_login.login_required
def createservice():
	return servicesflask.createservice()

@app.route('/createserviceapi', methods=['POST'])
@flask_login.login_required
def createserviceapi():
	return servicesflask.createserviceapi()

@app.route('/updateservice')
@flask_login.login_required
def updateservice():
	service_id = request.args.get('service_id')
	return servicesflask.updateservice(service_id)

@app.route('/updateserviceapi', methods=['POST'])
@flask_login.login_required
def updateserviceapi():
	return servicesflask.updateserviceapi()

if __name__ == "__main__":
	serve(app, host=config_values['server_ip'], port=int(config_values['server_port']))
