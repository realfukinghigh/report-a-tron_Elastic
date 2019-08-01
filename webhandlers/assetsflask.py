from flask import Flask, render_template, request, redirect, url_for
import datetime
from elasticstuff import assets, singledocs

assetConnection = assets.Assets()
docConnection = singledocs.Docs()

def newapp():
   return render_template('newapp.html')

def thedata():
    data = assetConnection.getAssets()
    return render_template('thedata.html', data=data)

def createapp():
	_assetName = request.form['assetName']
	_assetType = request.form['assetType']
	_assetOwner = request.form['assetOwner']
	_assetNotes = request.form['assetNotes']
	_assetInternetFacing = request.form['assetInternetFacing']
	try:
		timenow = datetime.datetime.now().isoformat().split(".")[0]
		assetConnection.createAsset(_assetName, _assetType, _assetOwner, timenow, _assetNotes, _assetInternetFacing)
		return redirect(url_for("thedata"))
	except:
		return redirect(url_for("error"))

def updateasset():
	_assetID = request.args.get('assetID')
	data = docConnection.getDoc(_assetID)
	return render_template('updateasset.html', data=data)

def updateassetapi():
	_assetID = request.form['assetId']
	_assetName = request.form['assetName']
	_assetType = request.form['assetType']
	_assetOwner = request.form['assetOwner']
	_assetNotes = request.form['assetNotes']
	_assetInternetFacing = request.form['assetInternetFacing']
	try:
		assetConnection.updateAsset(_assetID, _assetName, _assetType, _assetOwner, _assetNotes, _assetInternetFacing)
		return redirect(url_for("thedata"))
	except:
		return redirect(url_for("error"))
