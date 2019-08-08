from flask import Flask, render_template, request, redirect, url_for
import datetime
from elasticstuff import reports
import reportcreator

reportConnection = reports.Reports()

def testReport():

    test_id = request.args.get('test_id')

    test_issue_data = reportConnection.getTestReport('test_id')

    reportcreator.writeTestReport(test_issue_data)

    return render_template('convert_md.html')
