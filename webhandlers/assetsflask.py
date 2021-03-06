from flask import Flask, render_template, request, redirect, url_for
import datetime
from elasticstuff import assets, singledocs, thirdparty

assetConnection = assets.Assets()
docConnection = singledocs.Docs()
tpConnection = thirdparty.Thirdparty()

def createasset():
    return render_template('createasset.html')

def viewassets():
    data = assetConnection.getAssets()
    return render_template('viewassets.html', data=data)

def createassetapi():
    asset_name = request.form['asset_name']
    asset_type = request.form['asset_type']
    asset_owner = request.form['asset_owner']
    asset_notes = request.form['asset_notes']
    asset_internet_facing = request.form['asset_internet_facing']
    try:
        timenow = datetime.datetime.now().isoformat().split(".")[0]
        asset_id = assetConnection.createAsset(asset_name, asset_type, asset_owner, timenow, asset_notes, asset_internet_facing)

        if asset_type == "Third Party":
            print("third party")
            tpConnection.createThirdParty(asset_id, asset_name, asset_owner)

        return redirect(url_for("viewassets"))

    except:
        return redirect(url_for("error"))

def updateasset():
    asset_id = request.args.get('asset_id')
    data = docConnection.getDoc(asset_id)
    return render_template('updateasset.html', data=data)

def updateassetapi():
    asset_id = request.form['asset_id']
    asset_name = request.form['asset_name']
    asset_type = request.form['asset_type']
    asset_owner = request.form['asset_owner']
    asset_notes = request.form['asset_notes']
    asset_internet_facing = request.form['asset_internet_facing']

    try:
        assetConnection.updateAsset(asset_id, asset_name, asset_type, asset_owner, asset_notes, asset_internet_facing)
        return redirect(url_for("viewassets"))
    except:
        return redirect(url_for("error"))
