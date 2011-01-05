from five import grok
from zope import schema
from plone.namedfile import field as namedfile
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder

from plone.directives import form, dexterity

from itd.vidbase import _

class Iiphoneannounce(form.Schema):
    """
    Sends notification to Urban Airship
    """

    # -*- Your Zope schema definitions here ... -*-
    form.fieldset('technical',
            label=u"Technical info",
            fields=["badge", "appkey", "appmaster", "appsecret"]
        )

    sound = schema.TextLine(
        title=_(u"sound"),
        description=_(u"The name of the sound file that will be played when the alert is sent"),
        required=False,
    )


    alert = schema.Text(
        title=_(u"alert"),
        description=_(u"The text that's sent to the iPhone"),
        required=True,
    )

    badge = schema.TextLine(
        title=_(u"badge"),
        description=_(u"Do not edit this unless you know exactly what you are doing!"),
        required=False,
    )

    appkey = schema.TextLine(
        title=_(u"app key"),
        description=_(u"Don't edit this either unless you know exactly what you are doing!"),
        required=False,
    )

    appmaster = schema.TextLine(
        title=_(u"app master"),
        description=_(u"Uh, uh, uhh... only if you know exactly what you are doing!"),
        required=False,
    )

    appsecret = schema.TextLine(
        title=_(u"app secret"),
        description=_(u"Come on... haven't you figured it out by now? Don't touch, monkey boy!"),
        required=False,
    )

