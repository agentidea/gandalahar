# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import division
import imaplib, email, re
from datetime import date


def parseMonth(month):
    if month == 'Jan':
        return 1
    if month == 'Feb':
        return 2
    if month == 'Mar':
        return 3
    if month == 'Apr':
        return 4
    if month == 'May':
        return 5
    if month == 'Jun':
        return 6
    if month == 'Jul':
        return 7
    if month == 'Aug':
        return 8
    if month == 'Sep':
        return 9
    if month == 'Oct':
        return 10
    if month == 'Nov':
        return 11
    if month == 'Dec':
        return 12

    return -1


def get_email(id, server):
    result, data = server.fetch(id, "(RFC822)")  # fetch email
    for response_part in data:
        if isinstance(response_part, tuple):
            msg = email.message_from_string(response_part[1])
            subject = msg['subject']
            from_ = msg['from']
            # if subject.find("BREAKING") != -1:
            #    subject.replace("BREAKING NEWS","")
            #    subject.replace("BREAKING","")
            # Fri, 11 Sep 2015 15:35:41 -0400
            today = date.today()
            datebits = msg['date'].split(' ')
            day = datebits[1]
            month = datebits[2]
            year = datebits[3]

            parsedMonth = parseMonth(month)
            try:
                if (today.day == int(day) and today.month == parsedMonth and today.year == int(year)):
                
                    if (subject[0:9]=='My Alerts'):
                        return None

                    return {'date': msg['date'], 'src': from_.split('<')[0].replace('"', '').strip(),
                        'subject': subject.strip()}
                else:
                    return None
            except Exception as parsex:
                return None


def proc():
    HOST = 'agentidea.com'
    USERNAME = 'grantsteinfeld'
    PASSWORD = 'jy1met2'
    notAllowedSrcs = ['GRUBHUB','FACEBOOK']
    allowedSrcs = ['NYTimes.com','FoxBusiness.com','NYTimes.com News Alert']
    server = imaplib.IMAP4(HOST)  # connect
    server.login(USERNAME, PASSWORD)  # login
    server.select('INBOX', readonly=True)  # select mailbox aka folder

    result, data = server.search(None, "ALL")  # search emails

    ids = data[0]  # data is a list.
    id_list = ids.split()  # ids is a space separated string
    # latest_email_id = id_list[-1] # get the latest

    counter = 0
    ret = []
    for id_ in id_list:
        emailInfo = get_email(id_, server)
        if emailInfo != None:
            counter = counter + 1
            emailInfo['seq'] = counter

            if emailInfo['src'].upper() in notAllowedSrcs:
                print "banning ", emailInfo
            elif emailInfo['src'].strip() in allowedSrcs:
                ret.append(emailInfo)
            else:
                print "odd man out", " ", emailInfo['src'], emailInfo['subject']

    return ret


if (__name__ == '__main__'):
    ret = proc()
    for r in ret:
        try:
            print r['src'], " :: ", r['subject']
            print "^"*8
        except Exception as printex:
            print r
            print printex

