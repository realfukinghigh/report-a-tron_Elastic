import markdown
import datetime
from os import path

style = '<style>body { font-family: Verdana, Geneva, sans-serif; font-size: 16px; background-color: #f7fcff; line-height: 1.5; word-wrap: break-word; margin: 20px; padding: 45px; background-color: #fff; border: 1px solid #6a1a41; border-radius: 3px;} table { border-collapse: collapse; width: 100%; margin-bottom: 20px; border: 1px solid black;} th { background-color: #6a1a41; height: 50px; color: #fff;} th, td { text-align: center-left; border: 1px solid black; padding: 5px; text-align: left;} tr:nth-child(even) {background-color: #f2f2f2;} code { display: inline-block; overflow: visible; padding-left: 10px; padding-bottom: 10px; } pre { overflow: auto; font-size: 85%; background-color: #f6f8fa; border-radius: 3px; }</style>'

new_line = "\n"
double_new_line = "\n\n"

def get_date():
    return datetime.datetime.today().strftime('%d-%m-%y')

def writeTestReport(test_report_data):
    test_type = test_report_data[0]['_source']['test_stuff']['test_type']
    test_exec_summary = test_report_data[0]['_source']['test_stuff']['test_exec_summary']
    test_base_location = test_report_data[0]['_source']['test_stuff']['test_base_location']
    test_limitations = test_report_data[0]['_source']['test_stuff']['test_limitations']
    test_date = test_report_data[0]['_source']['test_stuff']['test_date']

    mdpath = "//templates//report.md"
    abspath = path.abspath(__file__)
    dirname = path.dirname(abspath)
    md_report = str(dirname) + mdpath

    with open(md_report, "w") as md_file:

        if test_report_data[0]['_source']['asset_stuff']:
            md_file.write("#" + test_report_data[0]['_source']['asset_stuff']['asset_name'] + "_" + test_type + "_" + test_date + double_new_line)
        md_file.write("#### Executive Summary" + double_new_line)
        md_file.write(test_exec_summary + double_new_line)

        if test_report_data[0]['_source']['asset_stuff']:
            md_file.write("| **Description** | **Detail**|" + new_line)
            md_file.write("|---|---|" + new_line)
            md_file.write("| Asset | " + test_report_data[0]['_source']['asset_stuff']['asset_name'] + new_line)
            md_file.write("| Location | " + test_base_location + new_line)
            md_file.write("| Limitations | " + test_limitations + double_new_line)

        md_file.write("#### Issue Summary" + double_new_line)

        md_file.write("|**Issue Ref** | **Issue Title** | **Rating** | **Status** | " + new_line)
        md_file.write("|--|--|--|--|" + new_line)

        for issue in test_report_data:
            issueTitle = issue['_source']['issue_stuff']['issue_title']
            issueLocation = issue['_source']['issue_stuff']['issue_location']
            issueDescription = issue['_source']['issue_stuff']['issue_description']
            issueRemediation = issue['_source']['issue_stuff']['issue_remediation']
            issueRisk = issue['_source']['issue_stuff']['issue_risk_rating']
            issueImpact = issue['_source']['issue_stuff']['issue_risk_impact']
            issueLikelihood = issue['_source']['issue_stuff']['issue_risk_likelihood']
            issueStatus = issue['_source']['issue_stuff']['issue_status']
            issueDetails = issue['_source']['issue_stuff']['issue_details']
            issueID = issue['_id']

            md_file.write("| " + str(issueID) + " | " + issueTitle + " | " + issueRisk + " | " + issueStatus + " | " + new_line)
        md_file.write(double_new_line)
        md_file.write("#### Technical Findings" + double_new_line)

        for issue in test_report_data:
            issueTitle = issue['_source']['issue_stuff']['issue_title']
            issueLocation = issue['_source']['issue_stuff']['issue_location']
            issueDescription = issue['_source']['issue_stuff']['issue_description']
            issueRemediation = issue['_source']['issue_stuff']['issue_remediation']
            issueRisk = issue['_source']['issue_stuff']['issue_risk_rating']
            issueImpact = issue['_source']['issue_stuff']['issue_risk_impact']
            issueLikelihood = issue['_source']['issue_stuff']['issue_risk_likelihood']
            issueStatus = issue['_source']['issue_stuff']['issue_status']
            issueDetails = issue['_source']['issue_stuff']['issue_details']
            issueID = issue['_id']

            md_file.write("| **Ref** | " + issueTitle + " - " + str(issueID)+ new_line)
            md_file.write("|---|---|" + new_line)
            md_file.write("| Status | " + issueStatus + new_line)
            md_file.write("| Issue Title | " + issueTitle + new_line)
            md_file.write("| Risk Rating | " + issueRisk + new_line)
            md_file.write("| Description | " + issueDescription + new_line)
            md_file.write("| Remediation | " + issueRemediation + double_new_line)

        md_file.write("#### Appendix" + double_new_line)

        for issue in test_report_data:
            if issue['_source']['issue_stuff']['issue_details']:
                md_file.write(issue['_source']['issue_stuff']['issue_title'] + " - " + str(issue['_id']) + new_line)
                md_file.write("```" + new_line)
                md_file.write(issue['_source']['issue_stuff']['issue_details'] + new_line)
                md_file.write("```" + double_new_line)
            else:
                continue

        md_file.write("**Remediation Timelines**" + double_new_line)
        md_file.write("|Issue Rating|Remediation Time|" + new_line)
        md_file.write("|----:|----|" + new_line)
        md_file.write("|Critical| 7 Days|" + new_line)
        md_file.write("|High| 30 Days|" + new_line)
        md_file.write("|Medium| 60 Days|" + new_line)
        md_file.write("|Low|180 Days|" + double_new_line)

        md_file.close()

    with open(md_report, "r") as file:

        infile = file.read()
        file.close()

    htmlpath = "//templates//convert_md.html"
    html_file = str(dirname) + htmlpath

    with open(html_file, "w") as outfile:

        content = markdown.markdown(infile, extensions=['markdown.extensions.extra'])

        outfile.write(style)
        outfile.write(content)
        outfile.close()


def writeAssetReport(issueData, engCount, testData):
    pass
