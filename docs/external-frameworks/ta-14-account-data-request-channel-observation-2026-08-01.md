---
title: TA-14 Account-Data Request Channel Observation
sidebar_label: TA-14 Account-Data Request Channel
slug: /external-frameworks/ta-14-account-data-request-channel-observation-2026-08-01
---

# TA-14 Account-Data Request Channel Observation

## Record status

```text
Framework: TA-14
Observation date: 2026-08-01
Observation time: approximately 2:18–2:22 p.m. CDT
Record type: bounded public observation
Account-data deletion request delivered: NOT ESTABLISHED
Cause of contact-channel failure: NOT DETERMINED
Intentional obstruction: NOT CLAIMED
Authority granted: none
```

## Observed sequence

The tester created and used an account in the TA-14 environment as part of the previously documented public-demonstration review.

Before submitting additional account-linked activity, the tester sought a functioning channel through which to request:

```text
confirmation of retained personal data
access to account-linked information
closure of the TA-14 account
deletion of personal and account-linked data
identification of any data that could not be deleted
identification of retention periods and third-party processors
written confirmation of completed deletion
```

The following conditions were observed:

```text
1. The visible account-confirmation email originated from Supabase Auth.
2. The displayed sender address was noreply@mail.app.supabase.io.
3. No reply-capable TA-14 privacy, account-deletion, or data-rights address was identified in that message.
4. A public TA-14 response on LinkedIn and the nested replies beneath it were later no longer visible from the tester's account.
5. The LinkedIn mention or profile reference for the TA-14 representative returned an unavailable or nonexistent-page result from the tester's account.
6. That condition prevented use of the intended private-message channel to deliver the account-specific notice or request an accountable privacy contact.
```

## Bounded determination

This record does not determine why the LinkedIn comment, replies, mention, or profile reference became unavailable.

It does not establish:

```text
that the representative intentionally blocked the tester
that the representative acted to prevent a deletion request
that LinkedIn moderation caused the condition
that the TA-14 account data was misused
that the Supabase no-reply address was intended as a privacy channel
that TA-14 refused a request it had successfully received
```

It does establish an operational request-channel failure:

> TA-14 account creation and authenticated testing were available, but the tester did not identify a usable controller contact for an account-data request, and the only identifiable human contact channel became unavailable when the tester attempted to submit or route that request.

## Governance significance

A data-rights mechanism is not operational merely because a user may theoretically possess a right to request access or deletion.

The operational path must permit the user to:

```text
identify the responsible controller
submit the request through a functioning channel
complete proportionate identity verification
receive acknowledgment
receive a substantive response
appeal a denial or incomplete response
obtain confirmation of account closure and processor propagation
```

The observed state was instead:

```text
account creation available
-> account-linked testing performed
-> data-handling boundary not established
-> automated Supabase no-reply address observed
-> no accountable TA-14 privacy contact identified
-> intended human-contact channel unavailable
-> formal account-data request delivery not established
```

This means the available contact architecture did not provide a demonstrably usable path for exercising control over account-linked data.

## Relationship to the prior TA-14 determination

This observation supplements, but does not replace, the TA-14 Testing Support Determination dated 2026-08-01.

The earlier determination recorded that meaningful testing required account creation without a sufficiently established public boundary for:

```text
data minimization
retention duration
deletion procedure
secondary use
owner access
analytics or profiling
non-reuse for commercial or model-development purposes
```

The present record adds a later operational observation: when the tester attempted to identify and use a deletion or privacy-request channel, no reply-capable TA-14-controlled address was apparent and the intended direct-message route was unavailable.

## Resolution path

TA-14 may resolve the request-channel issue by publicly providing or directly delivering:

```text
a functioning privacy or data-rights contact
a functioning account-deletion route
the identity of the responsible controller
the applicable privacy and retention terms
a method for authenticated requests
a response and appeal procedure
written confirmation of account closure and deletion completion
```

Publication of such a route would resolve the channel-access defect prospectively. It would not erase the historical observation that the route was not apparent or usable at the recorded time.

## Evidence boundary

The supporting observations were preserved through contemporaneous screenshots showing:

```text
the Supabase Auth no-reply sender address
the earlier visible LinkedIn response and nested discussion
the later absence of that response and discussion
the unavailable mention or profile-reference condition
```

These screenshots establish the visible state transitions observed by the tester. They do not independently establish the actor, mechanism, motive, or platform-level cause of those transitions.

## Authority boundary

```text
channel failure != proof of intentional obstruction
profile unavailability != confirmed profile deletion
comment disappearance != proof of actor identity
no-reply sender != accountable controller contact
account creation != informed data-handling consent
theoretical deletion right != functioning deletion mechanism
request drafted != request delivered
request undelivered != request denied
public observation != legal adjudication
historical preservation != continued processing authority
```
