from plugins.choice.models import choice
from core.models import action, conduct
from core import helpers, workers

class _requestChoice(action._action):
	message = str()

	def run(self,data,persistentData,actionResult):
		if "choice" in data["plugin"]:
			actionResult["result"] = True
			actionResult["rc"] = 100
			return actionResult
		message = helpers.evalString(self.message,{"data" : data})
		token = choice._choice().new(message,data["conductID"],data["triggerID"],data["flowID"],data,self.acl)
		actionResult["data"]["token"] = token
		actionResult["data"]["uri"] = "plugin/choice/{0}/".format(token)
		actionResult["result"] = False
		actionResult["rc"] = 300
		return actionResult

class _choiceTrigger(action._action):

	def run(self,data,persistentData,actionResult):
		answered = choice._choice().getAsClass(query={ "complete" : False, "answerTime" : { "$gt" : 0 } })
		for answeredItem in answered:
			answeredItem.complete = True
			c = conduct._conduct().getAsClass(id=answeredItem.conductID)
			if c and len(c) > 0:
				c = c[0]
				data = answeredItem.data
				data["plugin"]["choice"] = True
				data["callingTriggerID"] = answeredItem.triggerID
				if answeredItem.answer:
					workers.workers.new("trigger:{0}".format(answeredItem._id),c.triggerHandler,(answeredItem.flowID,data,False,True))
			answeredItem.update(["complete"])
		actionResult["result"] = True
		actionResult["rc"] = 0
		return actionResult
