import uuid

from core import plugin, model
from core.models import conduct, trigger, webui
from plugins.choice.models import action

class _choice(plugin._plugin):
    version = 1.0

    def install(self):
        # Register models
        model.registerModel("choice","_choice","_document","plugins.choice.models.choice",True)
        model.registerModel("choiceRequest","_requestChoice","_action","plugins.choice.models.action")
        model.registerModel("choiceTrigger","_choiceTrigger","_action","plugins.choice.models.action",True)

        c = conduct._conduct().new("choiceCore")
        c = conduct._conduct().getAsClass(id=c.inserted_id)[0]
        t = trigger._trigger().new("choiceCore")
        t = trigger._trigger().getAsClass(id=t.inserted_id)[0]
        a = action._choiceTrigger().new("choiceCore")
        a = action._choiceTrigger().getAsClass(id=a.inserted_id)[0]
       
        c.triggers = [t._id]
        flowTriggerID = str(uuid.uuid4())
        flowActionID = str(uuid.uuid4())
        c.flow = [
            {
                "flowID" : flowTriggerID,
                "type" : "trigger",
                "triggerID" : t._id,
                "next" : [
                    {"flowID": flowActionID, "logic": True }
                ]
            },
            {
                "flowID" : flowActionID,
                "type" : "action",
                "actionID" : a._id,
                "next" : []
            }
        ]
        webui._modelUI().new(c._id,{ "ids":[ { "accessID":"0","delete": True,"read": True,"write": True } ] },flowTriggerID,0,0,"")
        webui._modelUI().new(c._id,{ "ids":[ { "accessID":"0","delete": True,"read": True,"write": True } ] },flowActionID,100,0,"")
        c.acl = { "ids":[ { "accessID":"0","delete": True,"read": True,"write": True } ] }
        c.enabled = True
        c.update(["triggers","flow","enabled","acl"])
        t.acl = { "ids":[ { "accessID":"0","delete": True,"read": True,"write": True } ] }
        t.schedule = "60-90s"
        t.enabled = True
        t.update(["schedule","enabled","acl"])
        a.acl = { "ids":[ { "accessID":"0","delete": True,"read": True,"write": True } ] }
        a.enabled = True
        a.update(["enabled","acl"])
        return True

    def uninstall(self):
        # deregister models
        model.deregisterModel("choice","_choice","_document","plugins.choice.models.choice")
        model.deregisterModel("choice","_choice","_action","plugins.choice.models.action")
        model.deregisterModel("choiceTrigger","_choiceTrigger","_action","plugins.choice.models.action")
        return True

    def upgrade(self,LatestPluginVersion):
        pass
