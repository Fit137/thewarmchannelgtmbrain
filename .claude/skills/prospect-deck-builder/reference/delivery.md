# Delivery

Load for: sending the deck, hosting it, and taking it down.

The deck is a private document about one company, made without being asked. How it arrives is part of what it says. It arrives once, to one person, from the founder by name, with nothing watching what the reader does with it.

## What is sent

- **The send build.** Never the present build. `deck_check.py` prints which one a file is, and the file's build comment says "Audience: send".
- **Either a private link to the interactive file, or the PDF,** or both: the link in the message, the PDF on request.

## The private link

The interactive file is one self-contained HTML file with no network requests, so it can be hosted anywhere that serves a static file, and it keeps working if the reader downloads it.

| Requirement | Why |
|---|---|
| A long random path, for example `/s/7f3k9q2m/`, never the company's name | The address itself must not reveal who the deck is for, or be guessable |
| Not listed, not linked from anywhere, not in a sitemap | Nobody finds it who was not sent it |
| No indexing: the file carries `noindex, nofollow, noarchive`, and the host adds the same as a header where it can | Search engines never see it |
| No analytics, no pixel, no tracking script on the host | The file promises "Nothing you type leaves this page". The host must not break that |
| The founder's own domain once it exists. Until then, a reputable static host | A newly registered or unfamiliar domain, or a link shortener, reads as phishing, especially to a security buyer |
| HTTPS | Obviously |

**Never published as a public page,** never posted to a gallery, a portfolio or a social network, and never published through a tool that makes pages public or shareable by default, such as an artifact or page publishing service. A page in a prospect's branding, published, would look like their page.

## The PDF

`screenshot.py --pdf`, or the browser's print from the send build: the home layer, then one slide per page. It is the copy that gets forwarded to a CFO, so the home layer has to make the argument alone, which it does by design. Name it `[slug]_strategy_v1.pdf`.

## Never an HTML attachment

Mail gateways treat attached HTML as a phishing payload, and a security buyer has been trained to treat it the same way. If the reader wants the interactive file offline, the link lets them download it.

For a first message to a security buyer, attach nothing at all: people in that role are told not to open attachments from senders they do not know. The link, and the offer of a PDF, is enough.

## The message

One researched approach, from the founder by name, to one person: the strategy skill's `reference/approach.md` and the brain's `templates/prospect-approach.md`, prepared-strategy variant. No sequence. No follow-up to a non-reply. No read receipt.

## Log it

- In the workspace `log.md`: the date sent, the version, the format (link, PDF), the link's path, and the take-down date.
- In the brain's `ops/pipeline.md`: the stage and the date, by ID, never a person's name.

## Take it down

Remove the hosted file, and record the date in `log.md`, at the first of:

- the anchor moment has passed and there was no reply,
- the prospect declined or asked us to stop,
- ninety days after sending,
- a new version replaced it. An UPGRADE gets a new link. The v1 link is taken down only once v2 is sent, and never overwritten in place, because the reader may refer back to what they were sent.

## Never

- Reuse the deck, a slide or a sentence for another company.
- Show it to another prospect as an example, or describe it publicly with the company identifiable.
- Treat a reply, a forward or an open as a result. The proof set stays empty until a client engagement produces something real.
