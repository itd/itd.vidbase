from five import grok
from zope import schema
import zope.event
import zope.lifecycleevent
from z3c.relationfield.schema import RelationChoice, RelationList
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.app.container.interfaces import IObjectAddedEvent
from zope.component import getUtility
from zope.component import getAdapter
from z3c.form import button, field
from zLOG import LOG, ERROR

from plone.namedfile import field as namedfile
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.dexterity.content import Item
from plone.directives import form, dexterity

import urbanairship
from itd.vidbase import _
from itd.vidbase.config import *
from itd.vidbase.interfaces import IIphoneAnnounceAdapter

livestatus_vocab = SimpleVocabulary((
    SimpleTerm(title=u'Live Stream - On-Air!!!', value="live"),
    SimpleTerm(title=u'off-air', value='off'),
    ))

class Iiphoneannounce(form.Schema):
    """
    Sends notification to Urban Airship
    """

    # -*- Your Zope schema definitions here ... -*-
    title = schema.TextLine(
        title=_(u"Title"),
        description=_(u'A short descriptive title for this iPhone announcement, e.g., "NY-Announce"'),
        required=True,
    )

    form.fieldset('technical',
        label=u"Technical info",
        fields=["badge", "appkey", "appmaster", "appsecret"]
        )

    form.fieldset('payload',
        label=u"Payload Data",
        fields=["sound", "alert", "liveurl", "offairurl"]
        )

    sound = schema.TextLine(
        title=_(u"Sound"),
        description=_(u"The name of the sound file that will be played when the alert is sent"),
        required=False,
        )

    alert = schema.Text(
        title=_(u"alert"),
        description=_(u"The text that's sent to the iPhone"),
        required=True,
        )

    liveurl = schema.TextLine(
        title=_(u"Live Streaming Media Link"),
        description=_(u"The link for the media player to play the live stream, e.g., http://media.mandsworks.com/kylive/kylive.sdp/playlist.m3u8"),
        required=False,
        )

    offairurl = schema.TextLine(
        title=_("Off-air URL"),
        description=_(u"When the live stream is not playing, this will play http://media.mandsworks.com/vod/nokylive.m4v/playlist.m3u8"),
        required=False,
        )

    appkey = schema.TextLine(
        title=_(u"app key"),
        description=_(u"Don't edit this either unless you know exactly what you are doing!"),
        required=False,
        )

    appmaster = schema.TextLine(
        title = _(u"app master"),
        description = _(u"Uh, uh, uhh... only if you know exactly what you are doing!"),
        required = False,
        )

    appsecret = schema.TextLine(
        title = _(u"app secret"),
        description = _(u"Come on... haven't you figured it out by now? Don't touch, monkey boy!"),
        required=False,
        )

    livestatus = schema.Choice(
        title = _(u"Live Status"),
        description = _(u"Set to 'live' when the broadcast is active."),
        vocabulary =  livestatus_vocab,
        )

    onoffair = schema.Bool(
        title = _(u"On- or Off-Air"),
        description = _(u""),
        )

@grok.subscribe(Iiphoneannounce, IObjectModifiedEvent)
def whenModifying(iphoneannounce, event):
    adapter = IIphoneAnnounceAdapter(iphoneannounce)
    if iphoneannounce.livestatus == 'live':
        adapter.push_ua()

@grok.subscribe(Iiphoneannounce, IObjectAddedEvent)
def whenAdding(iphoneannounce, event):
    adapter = IIphoneAnnounceAdapter(iphoneannounce)
    if iphoneannounce.livestatus == 'live':
        adapter.push_ua()

class Iphoneannounce(Item):
    """Custom object's methods
    """
##    def ua_json(self):
##        """ returns the json payload
##        """
##        sound = self.sound
##        alert = self.alert
##        appkey = self.appkey
##        appmaster = self.appmaster
##        liveurl = self.liveurl
##        payload = {"aps": {"alert": alert, "sound": sound}, "url": liveurl}
##        return payload


class IphoneAnnounceXmlView(grok.View):
    grok.context(Iiphoneannounce)
    grok.require('zope2.View')
    grok.name('iphoneannounce.xml')

    def urlForXml(self):
        obj = self.context
        if obj.onoffair == True:
            return obj.liveurl
        else:
            return obj.offairurl


