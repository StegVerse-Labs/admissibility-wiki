#!/usr/bin/env node
import fs from 'node:fs';
import { spawnSync } from 'node:child_process';

const WRITER = 'scripts/write-public-activation-receipt.mjs';
const OUT = 'reports/public-activation-receipt.json';
const OPTIMIZATION_RECEIPT = 'reports/optimization-target-publication-verification-receipt.json';
const REQUIRED_CHECKS = [
  'public_site_loads',
  'status_json_reachable',
  'ios_workflow_mirror_status_json_reachable',
  'governed_llm_reconstructive_search_reachable',
  'governed_llm_activation_map_reachable',
  'governed_llm_demo_overview_reachable',
  'governed_llm_demo_verification_reachable',
  'governed_llm_site_verification_reachable',
  'governed_llm_deployment_status_reachable',
  'governed_llm_archive_handoff_reachable',
  'verification_execution_authority_doctrine_reachable',
  'verification_execution_authority_status_reachable',
  'optimization_target_doctrine_reachable',
  'optimization_target_formalism_json_reachable',
  'optimization_target_publication_status_reachable',
  'external_translation_reconstruction_receipt_reachable',
  'generated_evaluation_results_reachable',
  'asro_external_framework_reachable',
  'ai_led_radiology_formalism_reachable',
  'ai_led_radiology_schema_reachable',
  'ai_led_radiology_status_reachable'
];
const RADIOLOGY_CHECKS = new Set([
  'ai_led_radiology_formalism_reachable',
  'ai_led_radiology_schema_reachable',
  'ai_led_radiology_status_reachable'
]);
const UPSTREAM_ROUTE_NAMES = [
  'verification_execution_authority_doctrine_reachable',
  'verification_execution_authority_status_reachable',
  'conceptual_inheritance_doctrine',
  'conceptual_inheritance_status',
  'conceptual_inheritance_publication_status'
];

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

if (!fs.existsSync(WRITER)) fail(`missing writer: ${WRITER}`);

fs.mkdirSync('reports', { recursive: true });
fs.rmSync(OUT, { force: true });
fs.writeFileSync(OPTIMIZATION_RECEIPT, JSON.stringify({
  schema: 'optimization_target_publication_verification_receipt.test.v1',
  verification_result: 'PASS',
  routes: Object.fromEntries(UPSTREAM_ROUTE_NAMES.map((name) => [name, {
    reachable: true,
    url: `https://stegverse-labs.github.io/admissibility-wiki/mock/${name}`,
    verifier: 'deterministic local receipt-writer validation mode'
  }]))
}, null, 2) + '\n');

const result = spawnSync(process.execPath, [WRITER], {
  stdio: 'pipe',
  encoding: 'utf8',
  env: {
    ...process.env,
    PAGE_URL: 'https://stegverse-labs.github.io/admissibility-wiki/',
    GITHUB_SHA: 'validator-local-sha',
    GITHUB_RUN_ID: 'validator-local-run',
    GITHUB_RUN_ATTEMPT: '1',
    PUBLIC_ACTIVATION_SKIP_NETWORK: '1'
  }
});

if (result.status !== 0) {
  console.error(result.stdout);
  console.error(result.stderr);
  fail('receipt writer exited non-zero');
}

if (!fs.existsSync(OUT)) fail(`writer did not create ${OUT}`);
const receipt = JSON.parse(fs.readFileSync(OUT, 'utf8'));
if (receipt.schema !== 'admissibility_wiki_public_activation_receipt.v7') fail('schema mismatch');
if (receipt.repository !== 'StegVerse-Labs/admissibility-wiki') fail('repository mismatch');
if (receipt.activation_state !== 'workflow_observed_guarded_public_routes') fail('activation_state mismatch');
if (receipt.activation_target !== 'https://stegverse-labs.github.io/admissibility-wiki/') fail('activation_target mismatch');
if (receipt.commit !== 'validator-local-sha') fail('commit binding mismatch');
if (receipt.run_id !== 'validator-local-run') fail('run_id binding mismatch');

for (const check of REQUIRED_CHECKS) {
  const value = receipt.checks?.[check];
  if (!value) fail(`missing check: ${check}`);
  const expectedStatus = RADIOLOGY_CHECKS.has(check) ? 'verified_by_writer_mock' : 'verified_by_workflow';
  if (value.status !== expectedStatus) fail(`check status mismatch: ${check}`);
  if (!value.evidence?.url) fail(`check evidence url missing: ${check}`);
}

const radiology = receipt.activation_closures?.ai_led_radiology;
if (!radiology) fail('missing AI-led radiology activation closure');
if (radiology.schema !== 'ai_led_radiology_activation_closure.v1') fail('radiology closure schema mismatch');
if (radiology.state !== 'SIMULATED_VALIDATOR_PASS') fail('radiology simulated state mismatch');
if (radiology.user_manual_action_required !== false) fail('radiology user action mismatch');
if (radiology.execution_authority_granted !== false) fail('radiology authority mismatch');

const verification = receipt.activation_closures?.verification_execution_authority;
if (!verification || verification.schema !== 'verification_execution_authority_activation_closure.v1') {
  fail('verification-execution closure mismatch');
}
if (verification.execution_authority_granted !== false) fail('verification execution authority mismatch');
if (verification.certification_authority_granted !== false) fail('verification certification authority mismatch');

const conceptual = receipt.activation_closures?.conceptual_inheritance;
if (!conceptual || conceptual.schema !== 'conceptual_inheritance_publication_closure.v1') {
  fail('conceptual inheritance closure mismatch');
}
if (conceptual.goal_id !== 'conceptual-inheritance-provenance-standing') fail('conceptual inheritance goal mismatch');
if (conceptual.state !== 'WORKFLOW_OBSERVED_PUBLICATION_COMPLETE') fail('conceptual inheritance state mismatch');
if (conceptual.all_required_public_routes_verified !== true) fail('conceptual inheritance route verification mismatch');
for (const key of [
  'conceptual_inheritance_doctrine',
  'conceptual_inheritance_status',
  'conceptual_inheritance_publication_status'
]) {
  if (conceptual.evidence?.[key]?.reachable !== true) fail(`conceptual inheritance evidence mismatch: ${key}`);
}
if (conceptual.manual_task_requirement !== 'NONE') fail('conceptual inheritance manual task mismatch');
if (conceptual.user_manual_action_required !== false) fail('conceptual inheritance user action mismatch');
if (conceptual.authorship_determined !== false) fail('conceptual inheritance authorship boundary mismatch');
if (conceptual.ownership_determined !== false) fail('conceptual inheritance ownership boundary mismatch');
if (conceptual.infringement_determined !== false) fail('conceptual inheritance infringement boundary mismatch');
if (conceptual.derivation_determined !== false) fail('conceptual inheritance derivation boundary mismatch');
if (conceptual.origin_claim_standing_granted !== false) fail('conceptual inheritance standing boundary mismatch');
if (conceptual.execution_authority_granted !== false) fail('conceptual inheritance execution authority mismatch');
if (conceptual.release_authority_granted !== false) fail('conceptual inheritance release authority mismatch');
if (conceptual.downstream_mutation_authority_granted !== false) fail('conceptual inheritance downstream authority mismatch');
if (conceptual.handoff_reconciliation_required_for_continuation !== false) fail('conceptual inheritance reconciliation mismatch');

const mesh = receipt.activation_closures?.documentation_mesh;
if (!mesh) fail('missing documentation mesh closure');
if (mesh.schema !== 'documentation_mesh_observation_closure.v1') fail('documentation mesh closure schema mismatch');
if (mesh.goal_id !== 'documentation-mesh-live-peer-observation') fail('documentation mesh goal mismatch');
if (mesh.state !== 'SIMULATED_VALIDATOR_PASS') fail('documentation mesh simulated state mismatch');
if (mesh.peer_count !== 4 || mesh.complete_peer_count !== 4) fail('documentation mesh peer coverage mismatch');
if (!Array.isArray(mesh.observations) || mesh.observations.length !== 4) fail('documentation mesh observations mismatch');
for (const observation of mesh.observations) {
  for (const key of ['root', 'registry', 'health']) {
    if (observation[key]?.result !== 'PASS') fail(`documentation mesh mock observation failed: ${observation.peer_id}.${key}`);
    if (!observation[key]?.url) fail(`documentation mesh observation URL missing: ${observation.peer_id}.${key}`);
  }
}
if (mesh.manual_task_requirement !== 'NONE') fail('documentation mesh manual task mismatch');
if (mesh.user_manual_action_required !== false) fail('documentation mesh user action mismatch');
if (mesh.cross_repo_authority_granted !== false) fail('documentation mesh authority mismatch');
if (mesh.standing_conferred !== false) fail('documentation mesh standing mismatch');
if (mesh.execution_authority_granted !== false) fail('documentation mesh execution authority mismatch');
if (mesh.downstream_mutation_authority_granted !== false) fail('documentation mesh downstream authority mismatch');
if (mesh.handoff_reconciliation_required_for_continuation !== false) fail('documentation mesh reconciliation mismatch');

const quantum = receipt.activation_closures?.quantum_security;
if (!quantum || quantum.schema !== 'quantum_security_public_route_observation.v1') fail('quantum-security closure mismatch');
if (quantum.state !== 'SIMULATED_VALIDATOR_PASS') fail('quantum-security simulated state mismatch');
if (quantum.execution_authority_granted !== false) fail('quantum-security authority mismatch');
if (quantum.downstream_mutation_authority_granted !== false) fail('quantum-security downstream authority mismatch');

const reconstructionUrl = receipt.linked_receipts?.external_translation_reconstruction;
if (reconstructionUrl !== 'https://stegverse-labs.github.io/admissibility-wiki/status/external-translation-reconstruction-receipt.json') {
  fail('external translation reconstruction receipt binding mismatch');
}
if (receipt.linked_receipts?.ai_led_radiology_execution !== 'reports/ai-led-radiology-execution-receipt.json') {
  fail('AI-led radiology execution receipt binding mismatch');
}
if (receipt.linked_receipts?.quantum_security_public_route_observation !== 'reports/quantum-security-public-route-observation.json') {
  fail('quantum-security receipt binding mismatch');
}

const nonClaims = receipt.non_claims || [];
if (!nonClaims.some((claim) => claim.includes('does not create provider governance'))) fail('missing provider governance non-claim');
if (!nonClaims.some((claim) => claim.includes('does not certify clinical performance'))) fail('missing clinical-performance non-claim');
if (!nonClaims.some((claim) => claim.includes('does not grant cross-repository authority'))) fail('missing mesh authority non-claim');
if (!nonClaims.some((claim) => claim.includes('does not decide authorship'))) fail('missing conceptual inheritance non-claim');

fs.rmSync(OPTIMIZATION_RECEIPT, { force: true });
console.log('public activation receipt writer OK');
