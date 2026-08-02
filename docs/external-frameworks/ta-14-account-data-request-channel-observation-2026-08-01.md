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
Observation time: approximately 2:18–2:25 p.m. CDT
Record type: bounded public observation
Account-data deletion request delivered: NOT ESTABLISHED
Account-relative interaction restriction: STRONGLY SUPPORTED
Exact restriction mechanism: NOT DETERMINED
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
6. Notifications and interaction evidence associated specifically with that account disappeared from the tester's notification surface.
7. Other LinkedIn surfaces remained available to the tester.
8. At approximately 2:23 p.m. CDT, the displayed profile header and a public post were visible, while LinkedIn displayed “Comments could not be loaded” and still presented an “Add a comment” field.
9. Comment submission, direct-message availability, and delivery of the account-data request were not established.
```

## Subsequent observation — approximately 2:23 p.m. CDT

The later screenshot materially narrows, but does not conclusively identify, the failure mechanism.

It establishes that the displayed profile header and public post remained visible at that moment. It also establishes that the comment surface failed to load for the tester while the application continued to expose a comment-entry field.

Taken together with the disappearance of notifications and interaction records associated only with the same account, the observed pattern strongly supports an account-relative interaction restriction or account-specific platform state. It is less consistent with a general LinkedIn outage affecting all comment surfaces.

The observation does not independently distinguish among:

```text
a member-level block or restriction
a LinkedIn moderation or enforcement state
an account-specific application or cache failure
a selective comment-access control
a transient platform defect affecting only that relationship or thread
```

## Bounded determination

This record does not determine who initiated the restriction, which LinkedIn mechanism produced it, or why it occurred.

It does not establish:

```text
that the representative intentionally blocked the tester
that the representative acted to prevent a deletion request
that LinkedIn moderation caused the condition
that the TA-14 account data was misused
that the Supabase no-reply address was intended as a privacy channel
that TA-14 refused a request it had successfully received
```

It does establish the practical effect of an account-relative request-channel failure:

> TA-14 account creation and authenticated testing were available, but the tester did not identify a usable controller contact for an account-data request. During the attempt to route that request, comments, replies, mention resolution, notifications, and comment access associated specifically with the identifiable human contact became unavailable or nonfunctional from the tester's account. The exact platform mechanism remains undetermined, and formal request delivery was not established.

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
-> account-specific human-contact surfaces became unavailable or nonfunctional
-> formal account-data request delivery not established
```

This means the available contact architecture did not provide a demonstrably usable path for exercising control over account-linked data during the recorded sequence.

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

The present record adds the operational observation that no reply-capable TA-14-controlled address was apparent and that the identifiable human-contact surfaces became account-relative and nonfunctional when the tester attempted to route an account-data request.

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

The supporting observations were preserved through contemporaneous screenshots and account observations showing:

```text
the Supabase Auth no-reply sender address
the earlier visible LinkedIn response and nested discussion
the later absence of that response and discussion
the unavailable mention or profile-reference condition
the disappearance of notifications associated specifically with the same account
the later visible profile header and public post
the “Comments could not be loaded” error while the comment field remained visible
```

These observations establish the visible state transitions experienced by the tester. They do not independently establish the actor, mechanism, motive, or platform-level cause of those transitions.

## Authority boundary

```text
account-relative restriction != confirmed member block
channel failure != proof of intentional obstruction
profile visibility != proof that every interaction channel remained available
comment-loading failure != proof of its controlling mechanism
comment disappearance != proof of actor identity
no-reply sender != accountable controller contact
account creation != informed data-handling consent
theoretical deletion right != functioning deletion mechanism
request drafted != request delivered
request undelivered != request denied
public observation != legal adjudication
historical preservation != continued processing authority
```
