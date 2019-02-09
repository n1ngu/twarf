# TWARF

A FOSS Web Application Firewall developed atop the Python Twisted framework.

Roadmap:
- DDOS mitigation measures on HTTP layer (solve your synfloods elsewhere)
- URL whitelisting
- Anti SQL injection
- Anti XSS
- Anti CSRF

## Why Twarf?

Deploy your app behind this reverse proxy so as to:
- Retain technological sovereignty on your stack
- Avoid the need to stablish trust with a WAF provider

## Why a Web Application Firewall at all?

It's dangerous out there. Bad things eventually happen and sometimes
apps can't be fixed or hardened themselves. Hire a doorman!

## What Twarf is not

Twarf (nor any WAF) is not an excuse to develop your apps recklessly.
