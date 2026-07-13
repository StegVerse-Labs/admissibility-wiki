#!/usr/bin/env python3
from __future__ import annotations

import io
import json
import os
import re
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports/external-chat-activation-evidence-acquisition.json"
STAGING = ROOT / "reports/external-chat-activation-evidence-source.json"
OWNER = "StegVerse-Labs"
REPO = "Site"
WORKFLOW_NAME = "Site Task Runner"
ARTIFACT_PREFIX = "external-chat-activation-evidence-"
RUN_ID_RE = re.compile(r"^external-chat-activation-evidence-(\d+)-(\d+)$")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def token() -> str | None:
    return (
        os.getenv("STEGVERSE_SITE_ARTIFACT_TOKEN", "").strip()
        or os.getenv("GITHUB_TOKEN", "").strip()
        or None
    )


def headers(auth: str | None) -> dict[str, str]:
    values = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "StegVerse-External-Chat-Evidence-Acquirer",
    }
    if auth:
        values["Authorization"] = f"Bearer {auth}"
    return values


def api_json(url: str, auth: str | None) -> dict[str, Any]:
    request = urllib.request.Request(url, headers=headers(auth))
    with urllib.request.urlopen(request, timeout=30) as response:
        value = json.loads(response.read().decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError("GitHub API response must be a JSON object")
    return value


def api_bytes(url: str, auth: str | None) -> bytes:
    request = urllib.request.Request(url, headers=headers(auth))
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def write_report(payload: dict[str, Any]) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def boundary() -> dict[str, bool]:
    return {
        "acquisition_is_deployment_authority": False,
        "acquisition_is_repository_mutation_authority": False,
        "acquisition_is_publication_authority": False,
        "acquisition_is_certification": False,
        "acquisition_creates_standing": False,
    }


def skip(reason: str, *, authenticated: bool) -> int:
    write_report(
        {
            "schema_version": "1.0.0",
            "record_type": "external_chat_activation_evidence_acquisition",
            "generated_at": now_iso(),
            "state": "SKIPPED",
            "reason": reason,
            "source_repository": f"{OWNER}/{REPO}",
            "source_workflow": WORKFLOW_NAME,
            "authenticated_request": authenticated,
            "projection_written": False,
            "authority_boundary": boundary(),
        }
    )
    print(f"EXTERNAL CHAT ACTIVATION ACQUISITION: SKIP - {reason}")
    return 0


def main() -> int:
    auth = token()
    authenticated = auth is not None

    try:
        runs = api_json(
            f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs"
            "?branch=main&status=completed&per_page=50",
            auth,
        )
        candidates = [
            run
            for run in runs.get("workflow_runs", [])
            if isinstance(run, dict)
            and run.get("name") == WORKFLOW_NAME
            and run.get("head_branch") == "main"
            and run.get("conclusion") == "success"
        ]
        if not candidates:
            return skip("no_successful_site_task_runner_run_found", authenticated=authenticated)

        selected = max(candidates, key=lambda item: int(item.get("run_number") or 0))
        run_id = int(selected["id"])
        head_sha = str(selected.get("head_sha") or "")
        artifacts = api_json(
            f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs/{run_id}/artifacts?per_page=100",
            auth,
        )
        matches = [
            artifact
            for artifact in artifacts.get("artifacts", [])
            if isinstance(artifact, dict)
            and not artifact.get("expired")
            and str(artifact.get("name", "")).startswith(ARTIFACT_PREFIX)
        ]
        if not matches:
            return skip("successful_run_has_no_activation_evidence_artifact", authenticated=authenticated)
        artifact = max(matches, key=lambda item: int(item.get("id") or 0))
        name = str(artifact["name"])
        match = RUN_ID_RE.match(name)
        if not match or int(match.group(1)) != run_id:
            raise ValueError("artifact name does not bind selected workflow run")

        try:
            archive = api_bytes(str(artifact["archive_download_url"]), auth)
        except urllib.error.HTTPError as exc:
            if exc.code in {401, 403, 404} and not authenticated:
                return skip("public_artifact_download_requires_authentication", authenticated=False)
            raise

        with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
            names = [item for item in bundle.namelist() if item.endswith("external-chat-activation-evidence.json")]
            if len(names) != 1:
                raise ValueError("artifact must contain exactly one activation evidence JSON file")
            payload = json.loads(bundle.read(names[0]).decode("utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("activation evidence artifact must contain a JSON object")
        if str(payload.get("workflow_run_id")) != str(run_id):
            raise ValueError("payload workflow_run_id does not match selected run")
        if payload.get("commit_sha") != head_sha:
            raise ValueError("payload commit_sha does not match selected run head_sha")
        if payload.get("repository") != f"{OWNER}/{REPO}":
            raise ValueError("payload repository identity mismatch")

        STAGING.parent.mkdir(parents=True, exist_ok=True)
        STAGING.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        write_report(
            {
                "schema_version": "1.0.0",
                "record_type": "external_chat_activation_evidence_acquisition",
                "generated_at": now_iso(),
                "state": "ACQUIRED_EXACT_ARTIFACT",
                "source_repository": f"{OWNER}/{REPO}",
                "source_workflow": WORKFLOW_NAME,
                "source_run_id": str(run_id),
                "source_run_attempt": match.group(2),
                "source_commit_sha": head_sha,
                "artifact_id": str(artifact["id"]),
                "artifact_name": name,
                "artifact_expired": False,
                "authenticated_request": authenticated,
                "staged_path": str(STAGING.relative_to(ROOT)),
                "source_evidence_sha256": payload.get("evidence_sha256"),
                "observed_result": payload.get("result"),
                "mutation_required_disabled": payload.get("post_deployment_live_verification", {}).get("mutation_required_disabled"),
                "projection_written": False,
                "authority_boundary": boundary(),
            }
        )
    except (urllib.error.HTTPError, urllib.error.URLError, KeyError, ValueError, zipfile.BadZipFile, json.JSONDecodeError) as exc:
        write_report(
            {
                "schema_version": "1.0.0",
                "record_type": "external_chat_activation_evidence_acquisition",
                "generated_at": now_iso(),
                "state": "FAIL_CLOSED",
                "reason": str(exc),
                "source_repository": f"{OWNER}/{REPO}",
                "source_workflow": WORKFLOW_NAME,
                "authenticated_request": authenticated,
                "projection_written": False,
                "authority_boundary": boundary(),
            }
        )
        print(f"EXTERNAL CHAT ACTIVATION ACQUISITION: FAIL - {exc}")
        return 1

    print(f"EXTERNAL CHAT ACTIVATION ACQUISITION: PASS - run {run_id}, artifact {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
