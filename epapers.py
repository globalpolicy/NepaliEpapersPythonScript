from bs4 import BeautifulSoup
import urllib.request
import datetime
import os
import argparse

def findClosestDate(date,dates):
    absDiffList=[abs(datetime.datetime.strptime(listMemberDate, "%Y-%m-%d").timestamp() - datetime.datetime.strptime(date,"%Y-%m-%d").timestamp()) for listMemberDate in dates]
    closestDate=dates[absDiffList.index(min(absDiffList))]
    return closestDate

def DownloadEkantipurPaper(papername, date):
    availableIssues = GetAvailableIssues(papername)
    if date not in availableIssues:
        closestIssue=findClosestDate(date,availableIssues)
        print(f"{date} issue not found for {papername}. Downloading the closest issue {closestIssue}")
        date = closestIssue
    elif int(requestedDate[:4]) < 2017:
        print(
            f"{requestedDate} is before 2017-01-01. Inconsistently presented PDF epapers by Ekantipur before this time. Sorry can't do it.")
        return
    rootURL = 'https://epaper.ekantipur.com/'
    paperURL = rootURL + papername + '/' + date
    contents = urllib.request.urlopen(paperURL).read().decode('utf-8')
    soup = BeautifulSoup(contents, 'html.parser')
    images = soup.find_all('img', {'class': 'imgSection'})
    if not os.path.exists(f"{papername}"):
        os.mkdir(f"{papername}")
    if not os.path.exists(f"{papername}/{date}"):
        os.mkdir(f"{papername}/{date}")
    for page in images:
        pageNumber = page['data-page-num']
        pageImage = rootURL + page['data-original']
        urllib.request.urlretrieve(pageImage, f"{papername}/{date}/{pageNumber}.jpg")
    print(f'{papername} done')


def GetAvailableIssues(paperName):
    webpageUrl = f'https://epaper.ekantipur.com/{paperName}/'
    contents = urllib.request.urlopen(webpageUrl).read().decode('utf-8')
    soup = BeautifulSoup(contents, 'html.parser')
    scripts = soup.find_all('script')
    for script in scripts:
        scriptBody = ''.join(script.contents)
        startIndex = scriptBody.find('availableIssues')
        if startIndex != -1:
            startIndex = scriptBody.find('[', startIndex)
            endIndex = scriptBody.find(']', startIndex)
            listStr = scriptBody[startIndex + 1: endIndex].replace('"', '')
            issueDates = listStr.split(',')
            return issueDates


argparser = argparse.ArgumentParser(description='Retrieve popular Nepal-based newspapers as epapers in image format.')
argparser.add_argument('-K', '--kantipur', action='store_true', help='Download Kantipur daily')
argparser.add_argument('-k', '--kathmandupost', action='store_true', help='Download The Kathmandu Post daily')
argparser.add_argument('-N', '--nari', action='store_true', help='Download Nari')
argparser.add_argument('-S', '--saptahik', action='store_true', help='Download Saptahik weekly')
argparser.add_argument('-n', '--nepal', action='store_true', help='Download Nepal')
argparser.add_argument('-0', '--showissuedates', action='store_true',
                       help='Show the available issues for specified papers')
argparser.add_argument('issuedate', help='Required issue date (YYYY-MM-DD) in AD. Defaults to current date if not provided', nargs='?',
                       default=datetime.date.today().strftime("%Y-%m-%d"))
args = argparser.parse_args()
argsDict = vars(args)

if (argsDict['showissuedates']):  # only output the issue dates of specified papers; no image retrieval
    if argsDict['kantipur']:
        print(20 * '-')
        print("Available issue dates for Kantipur daily")
        print(20 * '-')
        kantipurIssues = GetAvailableIssues('kantipur')
        print(kantipurIssues)
    if argsDict['kathmandupost']:
        print(20 * '-')
        print("Available issue dates for The Kathmandu Post daily")
        print(20 * '-')
        kathmandupostIssues = GetAvailableIssues('kathmandupost')
        print(kathmandupostIssues)
    if argsDict['nari']:
        print(20 * '-')
        print("Available issue dates for Nari")
        print(20 * '-')
        nariIssues = GetAvailableIssues('nari')
        print(nariIssues)
    if argsDict['saptahik']:
        print(20 * '-')
        print("Available issue dates for Saptahik")
        print(20 * '-')
        saptahikIssues = GetAvailableIssues('saptahik')
        print(saptahikIssues)
    if argsDict['nepal']:
        print(20 * '-')
        print("Available issue dates for Nepal")
        print(20 * '-')
        nepalIssues = GetAvailableIssues('nepal')
        print(nepalIssues)
    print(
        "Note: Before 2017-01-01, Ekantipur used the pdf format for their epapers and in no particular consistent manner at that. Therefore, do limit your queries to after the stated date.")
    exit(0)

requestedDate = argsDict['issuedate']
try:
    _ = datetime.datetime.strptime(requestedDate, "%Y-%m-%d")
except ValueError as ve:
    print("Date error :")
    print("Please input date in the correct format (YYYY-MM-DD)")
    exit(1)

if argsDict['kantipur']:
    DownloadEkantipurPaper('kantipur', requestedDate)
if argsDict['kathmandupost']:
    DownloadEkantipurPaper('kathmandupost', requestedDate)
if argsDict['nari']:
    DownloadEkantipurPaper('nari', requestedDate)
if argsDict['saptahik']:
    DownloadEkantipurPaper('saptahik', requestedDate)
if argsDict['nepal']:
    DownloadEkantipurPaper('nepal', requestedDate)
