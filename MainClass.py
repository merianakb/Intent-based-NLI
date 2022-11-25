#CreatedOn 6/7/2020
import time

from wit import Wit

from IntentDetector import intentDetector

def get_maxConfidence_intent(response):
    max_confidence=0
    index_intent=0
    i=0
    for intent in response['intents']:
        if(intent['confidence']>max_confidence):
            max_confidence=intent['confidence']
            index_intent=i
        i=i+1
    return index_intent


access_token1="EOBHRB6DBO6ZD3SGGV6IRTL6TV5RZZBE"

client=Wit(access_token=access_token1)


def chatbot_response(msg):
    try:
        start_time = time.time()
        resp=client.message(msg)
        print(resp)
        print("--- %s seconds ---" % (time.time() - start_time))
        print()
        if len(resp['intents'])==0:
            print("no intent detected")
            return

        print("intent detected:")
        print(resp['intents'])
        print()
        print("entities detected:")
        for item in resp['entities']:
            str_item=str(item)
            str_item=str_item.split(":")[0]
            print(str_item)

        if len(resp['intents'])>1:
            print("Intent composition")
            return
        intentDetector.activate(resp,msg.lower())

    except:
        return "Error"

###  Max_requestedAmount
msg11="What was the highest application requested amount?"
msg12="Give me the highest requested amount."
msg13="what is the highest requested amount for those application with loan goal Home improvement"
msg14="what is the maximum requested amount for applications with loan goal home improvement"
msg15="What is the maximum requested amount for applications with type New credit?"

### Max_CanceledOffer
msg21="What was the highest number of offer canceled"
msg22="What is the maximum number of canceled offer in the same application?"
msg23="Give me the maximum number of canceled offer in the same loan."
msg24="what is the maximum number of canceled offer for those application with requested amount 7500"
msg25="what is the maximum number of canceled offer for applications with loa goal Car"
msg26='what is the maximum number of canceled offer in applications with requested amount greater than 10000'

### Max_Contribution
msg31="What was the highest contribution number"
msg32="What was the maximum number of activities executed by the same resource"
msg33='What is the maximum number of contribution in application "Application_1688279534"'

### Application
msg41="Which application is with requested amount 7500?"
msg42="What is the ID of the applications with loan goal Existing loan takeover?"
msg43='What is the requested amount of application "Application_224758141"?'
msg44="What is the loan goal of application with requested amount 7500?"
msg45='What is the loan goal and type of "Application_224758141"?'
msg46="what is the requested amount for applications with loan goal home improvement"  ##
msg47="Which application has type New credit and loan goal Car?"
msg48="what is the type pf applications with requested amount 7500 and loan goal Car"
msg49='What is the loan goal of application with requested amount greater than 7500?'
msg410='what is the type and loan goal of application with requested amount at most 10000 ?'
msg411='Give me all applications ordered desc by the requested amount'


### Application_count
msg51="How many applications are with requested amount 30000 and loan goal Home improvement?"
msg52="What is the number of applications requested amount 30000, loan goal Home improvement and type New Credit?"
msg53="How many applications has requested amount 22000 and type limit raise?"
msg54="what is the number of application with loan goal Car?"
msg55='how many applications with loan goal Car and requested amount greater than 7000'
msg56='What is the number of application with requested amount greater or equal 10000 ?'
msg57='How many applications have requested amount at most 15000 ?'


### Contribution_count
msg61="How many activities are executed by UserCG?"
msg62="What is the number of contributions of actor UserAA?"
msg63="how many activities are executed by actor UserC in application with loan goal Car"
msg64='How many activities are executed by UserGD in in "Application_772295828"?'
msg65='How many contributions for UserBD in "Offer_1485592228"?'
msg66='How many activities are executed by each actor?'
msg67='How many activities are executed by each actor in "Application_2110141037"'
msg68='Give me the number of contributions of actors processing more than 2 applications'
msg69='How many contribution for actor UserA between 1/5/2016 10:44:41 PM and 1/7/2016 5:58:55 PM ?'


### Offer_Offered
msg71='What are the offered amounts in "Application_203309822"'
msg72='Give me all offers in "Application_203309822"'
msg73='Which offer was sent by actor UserAA in "Application_2110141037"' #no activity name detected
msg74='Which offers was sent in "Application_2110141037"?'
msg75='What is the monthly cost and offered amount of offers offered in "Application_203309822"?'
msg76='Give me the offers offered for applications with requested amount 25000.'
msg77='What was the offers in "Application_2110141037"'
msg78='Give me all offers for applications with requested amount less than 15000'
msg79='Give all offered offers in applications with loan goal Car and requested amount at least 7500'
msg710='Give me all offers offered in applications with requested amount greater than 10000 ' \
       'and having offered amount lesser or equal 5000 '
msg711='Give me all offers in each application ordered by their offered amount'
msg712='Give me all offers offered today'


### Actor_Contribution
msg81='Who was involved in processing "Application_203309822"?'
msg82='Which actor has cancelled the offer in "Application_1765444083"?' #wrong activity name
msg83='Who has performed the cancellation of applications with loan goal Car?' #wrong activity name
msg84='Who has contributed in processing offer "Offer_1492567221"?' #return
msg85='Which actor has performed the creation of offers in application "Application_1765444083"?' #wrong activity name
msg86='Give me all actors involved in processing each application with type New credit'
msg87='Give the actors contributed in application "Application_1688279534" ordered desc by the number of their contribution'
msg88='Which actors has 3 contributions in each application with more than or equal 2 offers'


### Actor_Contribution_count
msg91='How many actors are involved in processing "Application_2110141037"?'
msg92='How many actors has contributed in processing offer "Offer_1485592228"?'
msg93='How many actors are responsible for validating application?'
msg94='What is the number of actor performing the creation of offers in application "Application_1765444083"?' #wrong activity name
msg95='How many actors contributing in offer creation?'
msg96='How many actors are involved in each application'
msg97='How many actors are involved in processing more than 2 applications'
msg98='Give me the number of actors contributed in each application'
msg99='Give me the number of actors with more than 3 contributions in each application'
msg910='Give me the number of actors contributed in each application with 2 offers'
msg911='Give me the number of actors contributed in each application ordered by the number of contribution'
msg912='Give me the number of actors with at least 2 contributions in each applications with more than 2 offers'


### Application_Affected
msg101='Which application was incomplete?'
msg102='Which application was validated by actor UserAA?'
msg103='Which applications are affected by actor UserAB'
msg104='Give me all applications  with loan goal Car ordered by the number of activities executed'
msg105='Which applications are affected by less than 5 actors'
msg106='Give me all applications affected by more than 3 actors with 2 offers and ordered by their requested amount'
msg107='Give me all applications with more than  2 offers affected by more than 3 actors and ordered by their requested amount'

### Offer_CanceledOffer_count
msg111='How many offers was cancelled in application "Application_1765444083"?'
msg112='How many offers was cancelled in application with loan goal Home improvement?'
msg113='What is the number of canceled offers in application "Application_1765444083"?'
msg114='What is the number of cancelled offer for each application'
msg115='How many cancelled offer in each application?'
msg116='What is the number of cancelled offer for each application with requested amount 10000'
msg117='how many cancelled offers for each application with loan goal Car'
msg118='how many offers was cancelled with offered amount less than 5000 in applications with requested amount greater than 7000 '
msg119='how many cancelled offers in each applications with requested amount more than 6000 '
msg1110='how many cancelled offer in each application ordered by the requested amount'


### Composition  ###
msg_1='which application has the maximum requested amount'
msg_2='how many actors are involved in processing application with the highest requested amount'
msg_3='what is the loan goal of application with highest requested amount'

msg='how many actor participate in each'
msg00='Give me all aplications ordered'

### test numerical conditions ###
t1='Which actors are involved in each application having 2 offers  and a requested amount exceeding 15000'
t2='Which actors are involved in each application with at least 2  offers'
t3='Which applications are affected by less than 5 actors'
t4='Which actors has  3 contributions in each application with more than or equal 2 offers'
t5='which application have requested amount 10000'
t6='which actors are involved in each application with 2 offers'

test='How many offers were canceled in each application with a request for 6000 minimum'

re=chatbot_response(test)








