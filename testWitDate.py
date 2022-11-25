from wit import Wit

access_token1="EOBHRB6DBO6ZD3SGGV6IRTL6TV5RZZBE"

client=Wit(access_token=access_token1)

msg='today is meriana'
msg1='today and yesterday'
msg2='last week'
msg3='last 2 weeks'
msg4='before 01-03-2021 and after 01-01-2021'
msg5='last monday'
resp=client.message(msg5)
print(resp)
for dt in resp['entities']:
    if dt=='wit$datetime:datetime':
        i=0
        for item in resp['entities'][dt]:
            if resp['entities'][dt][i]['type']=='interval':
                date_keys=resp['entities'][dt][i].keys()
                if 'to' in date_keys:
                    print("to "+resp['entities'][dt][i]['to']['value'])
                if 'from' in date_keys:
                    print("from "+resp['entities'][dt][i]['from']['value'])
            #direct value
            else:
                print(resp['entities'][dt][i]['value'])
            i = i + 1




