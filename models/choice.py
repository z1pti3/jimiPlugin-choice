import secrets
import time

from core import db, helpers, logging

class _choice(db._document):
    data = dict()
    token = str()
    message = str()
    conductID = str()
    triggerID = str()
    flowID = str()
    answer = bool()
    answerTime = int()
    complete = bool()

    _dbCollection = db.db["choice"]

    def new(self, message, conductID, triggerID, flowID, data, acl):
        self.message = message
        self.conductID = conductID
        self.triggerID = triggerID
        self.flowID = flowID
        self.data = data
        self.acl = acl
        self.token = secrets.token_urlsafe(64)
        super(_choice, self).new()
        return self.token
