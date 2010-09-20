Introduction
============

itd.vidbase is a really basic video asset management tool-set
based on Plone 4.0 and using plone.app.dexterity content types.

A goal of the process is to maximize uptime and simplify
content delivery. The content will still be delivered when
the Plone application is off-line.

Video assets will be managed in Plone and pushed out to a
content delivery service such as a wowza media server or
some other content delivery service.

Plone will produce various various RSS/XML feeds, implemented
as views on the video folders. The intention is to have these
XML-ish views consumed by some mechanism and likely served-up
by Apache, Nginx, or some CDN.

A sample Python script will be provided that consumes an XML
feed and pushes it to the XML delivery servers.

But I want it to do more
=========================
This product is intentionally light. In the future we
can add optional behaviors (groovy dexterity mojo) and
views to support specific use cases such as passing-off
data to iTunes or YouTube.


