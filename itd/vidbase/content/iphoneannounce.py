from five import grok
from zope import schema
from plone.namedfile import field as namedfile
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder
import urbanairship

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

    liveurl = schema.TextLine(
        title=_(u"Live Streaming Media Link"),
        description=_(u"The link for the media player to play the live stream, e.g., http://media.mandsworks.com/kylive/kylive.sdp/playlist.m3u8"),
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


class View(grok.View):
    grok.context(Iiphoneannounce)
    grok.require('zope2.View')

    #import pdb; pdb.set_trace()
    def ua_json(self):
        """ returns the json payload
        """

        context = aq_inner(self.context)
        #import pdb; pdb.set_trace()
#{"aps": {"badge": 0, "alert": "View the Live KY Lottery Drawing?", "sound": "its_time_to_play.aif"},"url": "http://media.mandsworks.com/kylive/kylive.sdp/playlist.m3u8"}
        badge = context.badge
        alert = context.alert
        appkey = context.appkey
        appmaster = context.appmaster
        liveurl = context.liveurl
        payload = '{"aps": {"badge": badge, "alert": alert, "sound": soundalert}, "url": liveurl}'
        return payload

