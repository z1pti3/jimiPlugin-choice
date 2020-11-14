from flask import Blueprint, render_template, redirect
from flask import current_app as app

from core import api

import time
import json

from plugins.choice.models import choice

pluginPages = Blueprint('choicePages', __name__, template_folder="templates")

@pluginPages.route("/choice/",methods=["GET"])
def mainPage():
    # Only show last 5 days still active
    foundChoices = choice._choice().query(query={ "creationTime" : { "$gt" : time.time()-432000 } , "complete" : False })["results"]
    result = []
    for foundChoice in foundChoices:
        result.append(foundChoice)
    return render_template("choice.html", result=result)

@pluginPages.route("/choice/<token>/",methods=["GET"])
def askAnswer(token):
    foundChoice = choice._choice().getAsClass(sessionData=api.g.sessionData,query={ "token" : token, "answerTime" : 0 })
    if len(foundChoice) == 1:
        foundChoice = foundChoice[0]
        return render_template("answer.html", message=foundChoice.message, token=token, CSRF=api.g.sessionData["CSRF"])
    else:
        return render_template("complete.html")

@pluginPages.route("/choice/<token>/",methods=["POST"])
def setAnswer(token):
    foundChoice = choice._choice().getAsClass(sessionData=api.g.sessionData,query={ "token" : token })[0]
    data = json.loads(api.request.data)
    if foundChoice.answerTime == 0:
        if data["answer"]:
            foundChoice.answer = True
            foundChoice.answerTime = int(time.time())
            foundChoice.update(["answer","answerTime"])
        else:
            foundChoice.answer = False
            foundChoice.answerTime = int(time.time())
            foundChoice.update(["answer","answerTime"])
    return {},200
