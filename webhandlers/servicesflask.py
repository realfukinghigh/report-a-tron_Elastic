from flask import Flask, render_template, request, redirect, url_for
import datetime
from elasticstuff import singledocs, services, assets

docConnection = singledocs.Docs()
serviceConnection = services.Services()
assetConnection = assets.Assets()

def viewservices():

    data = serviceConnection.getServices()
    return render_template('viewservices.html', data=data)

def viewservicedetail(service_id):

    data = serviceConnection.getServiceDetail(service_id)
    return render_template('viewservicedetail.html', data=data)

def createservice():

    data = assetConnection.getAssets()
    return render_template('createservice.html', data=data)

def createserviceapi():

    service_name = request.form['service_name']
    service_owner = request.form['service_owner']
    service_has_assets = request.form['service_has_assets']

    asset_list = []
    for asset_id in service_has_assets.split(','):
        asset_list.append(asset_id)

    try:
        serviceConnection.createService(service_name, service_owner, asset_list)
        return redirect(url_for("viewservices"))

    except:
        return redirect(url_for("error"))

def updateservice(service_id):

    data = serviceConnection.getServiceDetail(service_id)
    asset_data = assetConnection.getAssets()
    return render_template('updateservice.html', data=data, asset_data=asset_data)

def updateserviceapi():

    service_name = request.form['service_name']
    service_owner = request.form['service_owner']
    service_has_assets = request.form['service_has_assets']
    service_id = request.form['service_id']

    asset_list = []
    for asset_id in service_has_assets.split(','):
        asset_list.append(asset_id)

    try:
        serviceConnection.updateService(service_id, service_name, service_owner, asset_list)
        return redirect(url_for("viewservices"))

    except Exception as error:
        return redirect(url_for("error"))
