# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import division
import imaplib, email, re

def get_email(id, server):
    result, data = server.fetch(id, "(RFC822)") # fetch email
    for response_part in data:
        if isinstance(response_part, tuple):
            msg = email.message_from_string(response_part[1])
            subject = msg['subject']
            from_ = msg['from']
            #if subject.find("BREAKING") != -1:
            #    subject.replace("BREAKING NEWS","")
            #    subject.replace("BREAKING","")
            return {'date': msg['date'],'src': from_.split('<')[0].replace('"','').strip(),'subject': subject.strip() }

def proc():

    HOST = 'agentidea.com'
    USERNAME = 'grantsteinfeld'
    PASSWORD = 'jy1met2'

    server = imaplib.IMAP4(HOST) # connect
    server.login(USERNAME, PASSWORD) # login
    server.select('INBOX',readonly=True) # select mailbox aka folder

    result, data = server.search(None, "ALL") # search emails

    ids = data[0] # data is a list.
    id_list = ids.split() # ids is a space separated string
    #latest_email_id = id_list[-1] # get the latest

    counter=0
    ret=[]
    for id_ in id_list:
        emailInfo = get_email(id_, server)
        if emailInfo != None:
            counter = counter + 1
            emailInfo['seq'] = counter
            ret.append(emailInfo)
    return ret


if (__name__=='__main__'):
    ret = proc()
    for r in ret:
	print ret
