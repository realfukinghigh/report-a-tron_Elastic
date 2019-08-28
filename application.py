from flask import Flask, render_template, request, redirect, url_for
from elasticstuff import search
from webhandlers import assetsflask, engagementsflask, testsflask, issuesflask, thirdpartyflask, servicesflask, statsflask, reportsflask, loginflask
from waitress import serve
import config
import flask_login
from datetime import timedelta


application = Flask(__name__)
config_values = config.StaticValues().config_file
application.config.from_object(config_values['config_type'])
application.permanent_session_lifetime = timedelta(minutes=15)

searchConnection = search.Search()

login_manager = flask_login.LoginManager()
login_manager.init_app(application)
login_manager.login_view = 'login'

@login_manager.user_loader
def user_loader(username):
    return loginflask.user_loader(username)

@application.route('/login', methods=['GET'])
def login():
	return loginflask.login()

@application.route('/loginapi', methods=['POST'])
def loginapi():
    return loginflask.loginapi()

@application.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))

@application.route('/changepassword')
def changepassword():
    return loginflask.changepassword()

@application.route('/changepasswordapi', methods=['POST'])
def changepasswordapi():
    return loginflask.changepasswordapi()

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))

@application.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Server'] = 'Report-a-Tron'
    return response

@application.route("/")
@flask_login.login_required
def main():
	return render_template('index.html')

@application.route("/createasset")
@flask_login.login_required
def createasset():
	return assetsflask.createasset()

@application.route("/error")
@flask_login.login_required
def error():
	return render_template('error.html')

@application.route("/viewassets")
@flask_login.login_required
def viewassets():
	return assetsflask.viewassets()

@application.route("/createassetapi", methods=['POST'])
@flask_login.login_required
def createassetapi():
	return assetsflask.createassetapi()

@application.route("/updateasset")
@flask_login.login_required
def updateasset():
	return assetsflask.updateasset()

@application.route("/updateassetapi", methods=['POST'])
@flask_login.login_required
def updateassetapi():
	return assetsflask.updateassetapi()

@application.route("/engagements", methods=['GET'])
@flask_login.login_required
def engagements():
	return engagementsflask.engagements()

@application.route("/createengagement", methods=['POST'])
@flask_login.login_required
def createengagement():
	return engagementsflask.createengagement()

@application.route("/openengagements")
@flask_login.login_required
def openengagements():
	return engagementsflask.openengagements()

@application.route("/viewengagements")
@flask_login.login_required
def viewengagements():
	return engagementsflask.viewengagements()

@application.route("/updateengagement")
@flask_login.login_required
def updateengagement():
	return engagementsflask.updateengagement()

@application.route("/updateengagementapi", methods=['POST'])
@flask_login.login_required
def updateengagementapi():
	return engagementsflask.updateengagementapi()

@application.route("/createtest", methods=['GET'])
@flask_login.login_required
def createtest():
	return testsflask.createtest()

@application.route("/createtestapi", methods=['POST'])
@flask_login.login_required
def createtestapi():
	return testsflask.createtestapi()

@application.route("/viewtests", methods=['GET'])
@flask_login.login_required
def viewtests():
	return testsflask.viewtests()

@application.route("/updatetest")
@flask_login.login_required
def updatetest():
	return testsflask.updatetest()

@application.route("/updatetestapi", methods=['POST'])
@flask_login.login_required
def updatetestapi():
	return testsflask.updatetestapi()

@application.route("/viewissues", methods=['GET'])
@flask_login.login_required
def viewissues():
	return issuesflask.viewissues()

@application.route("/createissue", methods=['GET'])
@flask_login.login_required
def createissue():
	return issuesflask.createissue()

@application.route("/createissueapi", methods=['POST'])
@flask_login.login_required
def createissueapi():
	return issuesflask.createissueapi()

@application.route("/updateissue", methods=['GET'])
@flask_login.login_required
def updateissue():
	return issuesflask.updateissue()

@application.route("/updateissueapi", methods=['POST'])
@flask_login.login_required
def updateissueapi():
	return issuesflask.updateissueapi()

@application.route("/linkissue", methods=['GET'])
@flask_login.login_required
def linkissue():
	return issuesflask.linkissue()

@application.route("/issuelinkapi", methods=['POST'])
@flask_login.login_required
def issuelinkapi():
	return issuesflask.issuelinkapi()

@application.route("/testreport", methods=['GET'])
@flask_login.login_required
def testreport():
	return reportsflask.testReport()

@application.route("/stats")
@flask_login.login_required
def stats():
	return render_template('stats.html')

@application.route("/viewstats")
@flask_login.login_required
def viewstats():
	return statsflask.viewstats()

@application.route("/search")
@flask_login.login_required
def search():
	searchTerm = request.args.get('searchTerm')
	data = searchConnection.search(searchTerm)
	return render_template('searchresults.html', data=data)

@application.route("/viewthirdparty")
@flask_login.login_required
def viewthirdparty():
	return thirdpartyflask.viewthirdparty()

@application.route("/createthirdparty")
@flask_login.login_required
def createthirdparty():
	return render_template('createthirdparty.html')

@application.route("/updatethirdparty")
@flask_login.login_required
def updatethirdparty():
	return thirdpartyflask.updatethirdparty()

@application.route("/updatethirdpartyapi", methods=['POST'])
@flask_login.login_required
def updatethirdpartyapi():
	return thirdpartyflask.updatethirdpartyapi()

@application.route('/viewservices')
@flask_login.login_required
def viewservices():
	return servicesflask.viewservices()

@application.route('/viewservicedetail')
@flask_login.login_required
def viewservicedetail():
	service_id = request.args.get('service_id')
	return servicesflask.viewservicedetail(service_id)

@application.route('/createservice')
@flask_login.login_required
def createservice():
	return servicesflask.createservice()

@application.route('/createserviceapi', methods=['POST'])
@flask_login.login_required
def createserviceapi():
	return servicesflask.createserviceapi()

@application.route('/updateservice')
@flask_login.login_required
def updateservice():
	service_id = request.args.get('service_id')
	return servicesflask.updateservice(service_id)

@application.route('/updateserviceapi', methods=['POST'])
@flask_login.login_required
def updateserviceapi():
	return servicesflask.updateserviceapi()

if __name__ == "__main__":
    if config_values['deployment_server'] == "waitress":
        serve(application, host=config_values['server_ip'], port=int(config_values['server_port']))
    else:
        application.run(host=config_values['server_ip'], port=int(config_values['server_port']))
