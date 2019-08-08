from flask import Flask, render_template, request, redirect, url_for
import datetime
from elasticstuff import stats

statConnection = stats.Stats()

def viewstats():

    reportatron_stats = statConnection.getReportatronStats()
    #insight_stats = rapid7.getInsightStats()

    return render_template('viewstats.html', reportatron_stats=reportatron_stats)
