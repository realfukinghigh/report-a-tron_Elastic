from flask import Flask, render_template, request, redirect, url_for
import datetime
from elasticstuff import singledocs, thirdparty

docConnection = singledocs.Docs()
tpConnection = thirdparty.Thirdparty()

def viewthirdparty():
	data = tpConnection.getThirdParty()
	return render_template('viewthirdparty.html', data=data)
