# Modes

Load for: deciding what kind of work a request is, before doing any of it.

| The situation | Mode | Output |
|---|---|---|
| A company has been spotted and nothing exists yet | **BUILD**, version 1 | A strategy from public information, handed to the deck builder |
| The prospect replied, a call happened, and they shared numbers or their named list | **UPGRADE**, version 2 | The same strategy rebuilt on their numbers, with the coverage read |
| A strategy exists and is about to be sent, but is old, or the brain or their calendar has moved | **REFRESH** | The same version, re-verified and re-dated |
| The gate says NO-GO, they declined, asked us to stop, or never replied | **STOP** | A logged close, an archived workspace, nothing further sent |

## BUILD

Phases 0 to 10 in order, in one workspace. The gate comes first and decides whether the rest happens. Public information only. Every figure about the prospect is `{TBD}`. The calculator is empty. The output is `strategy.json` with `mode: BUILD`, `version: v1`, handed to `new_deck.py`.

Typical effort: two to four working days of founder time, in sessions of one or two phases each, with a review between sessions. That cost is why the gate exists.

## UPGRADE

Triggered by the prospect, never by us: they booked the call, and on it they shared numbers or sent their named account list.

1. Record everything they supplied as **P0** rows: what, by which role, on what date, on a call or in a document. Nothing they said in passing becomes a number on a slide without their agreement to use it.
2. Run the coverage read on their list with the brain's `templates/coverage-read.md`. The counts that were `{TBD}` in the tiers table and the approached count get real values, as P0-derived rows.
3. Revisit the footprint with their internal calendar, if they shared it: moments that were invisible from outside go on the map, scored the same way.
4. Prefill the calculator only with their numbers, with `prefill_note` naming the role and the date.
5. Set the measures' targets with them, from their history. The report format is still IN BUILD and says so.
6. Re-run the envelope: an UPGRADE often happens weeks later, and the brain may have moved.
7. `mode: UPGRADE`, `version: v2`. Build a new deck. The v1 deck is kept as it was sent.

An UPGRADE is still not a scope. No price, no promise, no contract language: those wait on D1, D2 and D4.

## REFRESH

Before sending anything older than thirty days, and whenever the brain's commit or the prospect's public calendar has changed.

1. Re-run the envelope and diff it against the one in the workspace.
2. Re-verify every register row captured more than ninety days ago: `evidence_check.py` lists them.
3. Move the footprint to the next edition of any event that has passed, and re-check the anchor still leaves a six-week window after a first call.
4. Re-run every check in phase 10.
5. Keep the version. Move `date`. Log what changed in `log.md`.

## STOP

Any of these ends the work:

- The gate says NO-GO.
- They declined, or asked not to be contacted.
- They never replied. A non-reply is an answer. There is no follow-up, no second approach on the same strategy, and no "checking in".
- A conflict appeared: D6, an active engagement, a partner commitment.

Then:

1. Log the reason in `log.md` and the brain's pipeline, by ID, against `reference/icp-client.md` where it applies.
2. Take down the private deck link if one was used, and record the date.
3. Move the workspace to `<root>/_archive/<slug>/`. It is never reused for another company: no sentence about one prospect is ever recycled into another's strategy.
4. If something learned changes the market picture (a new objection, a competitor move), it goes to the brain's `ops/signal-log.md` as a signal, without the prospect's name if the founder prefers.
