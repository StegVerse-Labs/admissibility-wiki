package stegverse.capture

# Deterministic capture policy for observed-evidence collection.
# This policy is test material only. It does not grant execution authority.

default allow := false

allow if {
  input.actor == "alice"
  input.action == "read"
  input.resource == "document-1"
  input.approval == true
}

reason := "approved read request" if allow
reason := "request does not satisfy capture policy" if not allow
