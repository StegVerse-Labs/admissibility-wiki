#!/usr/bin/env node
import fs from 'node:fs';

const outDir = 'reports';
const outPath = `${outDir}/public-activation-receipt.json`;
const optimizationReceiptPath = `${outDir}/optimization-target-publication-verification-receipt.json`;
const baseUrl = process.env.PAGE_URL || 'https://stegverse-labs.github.io/admissibility-wiki/';
const commit = process.env.GITHUB_SHA || null;
const runId = process.env.GITHUB_RUN_ID || null;
const runAttempt = process.env.GITHUB_RUN_ATTEMPT || null;
const skipNetwork = process.env.PUBLIC_ACTIVATION_SKIP_NETWORK === '1';

const urls = {
  public_site_loads: baseUrl,
  status_json_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/status/admissibility-wiki-status.json',
  ios_workflow_mirror_status_json_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/status/ios-workflow-mirror-status.json',
  governed_llm_reconstructive_search_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-reconstructive-search',
  governed_llm_activation_map_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-activation-map',
  governed_llm_demo_overview_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-demo-overview',
  governed_llm_demo_verification_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-demo-verification',
  governed_llm_site_verification_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-site-verification',
  governed_llm_deployment_status_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-deployment-status',
  governed_llm_archive_handoff_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/governance/governed-llm-archive-handoff',
  verification_execution_authority_doctrine_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/governance/verification-vs-execution-authority',
  verification_execution_authority_status_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/status/verification-execution-authority-status.json',
  optimization_target_doctrine_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/formalisms/optimization-target-binding-at-commit',
  optimization_target_formalism_json_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/formalisms/optimization-target-binding-at-commit.v0.1.json',
  optimization_target_publication_status_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/status/optimization-target-binding-publication-verification.json',
  external_translation_reconstruction_receipt_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/status/external-translation-reconstruction-receipt.json',
  generated_evaluation_results_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/external-frameworks/evaluation-results',
  asro_external_framework_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/external-frameworks/asro',
  ai_led_radiology_formalism_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/formalisms/ai-led-radiology-execution-boundary',
  ai_led_radiology_schema_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/schemas/ai-led-radiology-execution-case.schema.json',
  ai_led_radiology_status_reachable: 'https://stegverse-labs.github.io/admissibility-wiki/status/ai-led-radiology-execution-status.json'
};

const radiologyChecks = new Set([
  'ai_led_radiology_formalism_reachable',
  'ai_led_radiology_schema_reachable',
  'ai_led_radiology_status_reachable'
]);
const verificationAuthorityChecks = new Set([
  'verification_execution_authority_doctrine_reachable',
  'verification_execution_authority_status_reachable'
]);
const conceptualInheritanceChecks = new Set([
  'conceptual_inheritance_doctrine',
  'conceptual_inheritance_status',
  'conceptual_inheritance_publication_status'
]);
const meshPeers = [
  { id: 'stegverse-site', root: 'https://stegverse-labs.github.io/Site/' },
  { id: 'admissibility-wiki', root: 'https://stegverse-labs.github.io/admissibility-wiki/' },
  { id: 'stegguardian-wiki', root: 'https://stegverse-002.github.io/stegguardian-wiki/' },
  { id: 'stegtalk-wiki', root: 'https://stegverse-labs.github.io/stegtalk-wiki/' }
];

async function observeUrl(url) {
  if (skipNetwork) return { result: 'PASS', url, http_status: 200, verifier: 'deterministic local mock' };
  try {
    const response = await fetch(url, { redirect: 'follow' });
    const body = await response.text();
    return {
      result: response.ok && body.trim() ? 'PASS' : 'SOURCE_BLOCKED_FAIL_CLOSED',
      url,
      http_status: response.status,
      response_bytes: Buffer.byteLength(body),
      verifier: 'scripts/write-public-activation-receipt-base.mjs live fetch'
    };
  } catch (error) {
    return { result: 'SOURCE_BLOCKED_FAIL_CLOSED', url, error: String(error), verifier: 'scripts/write-public-activation-receipt-base.mjs live fetch' };
  }
}

const checks = Object.fromEntries(Object.entries(urls).filter(([name]) => !radiologyChecks.has(name)).map(([name, url]) => [
  name,
  { status: 'verified_by_workflow', evidence: { url, verifier: (name.startsWith('optimization_target_') || verificationAuthorityChecks.has(name) || name === 'external_translation_reconstruction_receipt_reachable') ? 'scripts/check_governed_llm_deployment_status.py run by verify-public-pages' : 'verify-public-pages job curl --fail with retries' } }
]));

for (const name of radiologyChecks) {
  const observation = await observeUrl(urls[name]);
  checks[name] = {
    status: observation.result === 'PASS' ? (skipNetwork ? 'verified_by_writer_mock' : 'verified_by_writer') : 'SOURCE_BLOCKED_FAIL_CLOSED',
    evidence: observation
  };
}

let optimizationTargetReceipt = null;
if (fs.existsSync(optimizationReceiptPath)) {
  optimizationTargetReceipt = JSON.parse(fs.readFileSync(optimizationReceiptPath, 'utf8'));
  if (!['PASS', 'FAIL_CLOSED'].includes(optimizationTargetReceipt.verification_result)) throw new Error('governed documentation publication verification receipt has invalid result');
}
const observedRoutes = optimizationTargetReceipt?.routes || {};
for (const name of verificationAuthorityChecks) {
  const route = observedRoutes[name];
  if (!route || route.reachable !== true) throw new Error(`verification-authority route is not confirmed in publication receipt: ${name}`);
}
for (const name of conceptualInheritanceChecks) {
  const route = observedRoutes[name];
  if (!route || route.reachable !== true) throw new Error(`conceptual-inheritance route is not confirmed in publication receipt: ${name}`);
}

const radiologyEvidence = Object.fromEntries([...radiologyChecks].map((name) => [name, checks[name]]));
const radiologyComplete = [...radiologyChecks].every((name) => ['verified_by_writer', 'verified_by_writer_mock'].includes(checks[name]?.status));
const radiologyActivationClosure = {
  schema: 'ai_led_radiology_activation_closure.v1', goal_id: 'ai-led-radiology-execution-boundary',
  state: skipNetwork ? 'SIMULATED_VALIDATOR_PASS' : (radiologyComplete ? 'WORKFLOW_OBSERVED_PUBLICATION_COMPLETE' : 'SOURCE_BLOCKED_FAIL_CLOSED'),
  commit, run_id: runId, run_attempt: runAttempt, evidence: radiologyEvidence,
  all_required_public_routes_verified: radiologyComplete,
  manual_task_requirement: 'NONE', user_manual_action_required: false,
  authority_granted: false, clinical_authority_granted: false, execution_authority_granted: false,
  handoff_reconciliation_required_for_continuation: false,
  continuation_source: 'docs/AI_LED_RADIOLOGY_MIRROR_HANDOFF.md'
};

const verificationAuthorityActivationClosure = {
  schema: 'verification_execution_authority_activation_closure.v1', goal_id: 'verification-vs-execution-authority', state: 'WORKFLOW_OBSERVED_PUBLICATION_COMPLETE',
  commit, run_id: runId, run_attempt: runAttempt,
  evidence: Object.fromEntries([...verificationAuthorityChecks].map((name) => [name, observedRoutes[name]])),
  all_required_public_routes_verified: true, manual_task_requirement: 'NONE', user_manual_action_required: false,
  authority_granted: false, execution_authority_granted: false, certification_authority_granted: false, downstream_mutation_authority_granted: false,
  continuation_source: 'docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md',
  non_claims: ['Route reachability is bounded publication evidence only.','Independent verification remains evidence input and does not become execution authority.','Publication does not grant action-level admissibility or permission to execute.']
};

const conceptualInheritanceActivationClosure = {
  schema: 'conceptual_inheritance_publication_closure.v1', goal_id: 'conceptual-inheritance-provenance-standing', state: 'WORKFLOW_OBSERVED_PUBLICATION_COMPLETE',
  commit, run_id: runId, run_attempt: runAttempt,
  evidence: Object.fromEntries([...conceptualInheritanceChecks].map((name) => [name, observedRoutes[name]])),
  all_required_public_routes_verified: true, manual_task_requirement: 'NONE', user_manual_action_required: false,
  authorship_determined: false, ownership_determined: false, infringement_determined: false, derivation_determined: false,
  origin_claim_standing_granted: false, execution_authority_granted: false, release_authority_granted: false, downstream_mutation_authority_granted: false,
  handoff_reconciliation_required_for_continuation: false,
  continuation_source: 'docs/CONCEPTUAL_INHERITANCE_MIRROR_HANDOFF.md',
  non_claims: ['Similarity alone is not proof of derivation.','Unresolved provenance is not certification of independence.','Publication evidence does not decide authorship, ownership, infringement, intent, or origin-claim standing.']
};

const meshObservations = [];
for (const peer of meshPeers) {
  const root = await observeUrl(peer.root);
  const peerBase = peer.root.replace(/\/$/, '');
  const registry = await observeUrl(`${peerBase}/status/ecosystem-documentation-endpoints.json`);
  const health = await observeUrl(`${peerBase}/status/cross-wiki-health-status.json`);
  meshObservations.push({ peer_id: peer.id, root, registry, health });
}
const completePeerCount = meshObservations.filter((item) => item.root.result === 'PASS' && item.registry.result === 'PASS' && item.health.result === 'PASS').length;
const documentationMeshClosure = {
  schema: 'documentation_mesh_observation_closure.v1', goal_id: 'documentation-mesh-live-peer-observation',
  state: skipNetwork ? 'SIMULATED_VALIDATOR_PASS' : (completePeerCount === meshPeers.length ? 'WORKFLOW_OBSERVED_MESH_COMPLETE' : 'SOURCE_BLOCKED_FAIL_CLOSED'),
  commit, run_id: runId, run_attempt: runAttempt, observations: meshObservations,
  peer_count: meshPeers.length, complete_peer_count: completePeerCount,
  manual_task_requirement: 'NONE', user_manual_action_required: false,
  cross_repo_authority_granted: false, standing_conferred: false, execution_authority_granted: false, downstream_mutation_authority_granted: false,
  handoff_reconciliation_required_for_continuation: false,
  continuation_source: 'docs/ADMISSIBILITY_WIKI_MIRROR_HANDOFF.md'
};

const receipt = {
  schema: 'admissibility_wiki_public_activation_receipt.v7',
  receipt_id: `public-activation.workflow.${runId || 'unknown'}.${runAttempt || '0'}`,
  created_at: new Date().toISOString(), repository: 'StegVerse-Labs/admissibility-wiki',
  activation_target: 'https://stegverse-labs.github.io/admissibility-wiki/', activation_state: 'workflow_observed_guarded_public_routes',
  commit, run_id: runId, run_attempt: runAttempt, checks,
  activation_closures: { ai_led_radiology: radiologyActivationClosure, verification_execution_authority: verificationAuthorityActivationClosure, conceptual_inheritance: conceptualInheritanceActivationClosure, documentation_mesh: documentationMeshClosure },
  linked_receipts: { optimization_target_publication_verification: optimizationTargetReceipt ? optimizationReceiptPath : null, external_translation_reconstruction: 'https://stegverse-labs.github.io/admissibility-wiki/status/external-translation-reconstruction-receipt.json', ai_led_radiology_execution: 'reports/ai-led-radiology-execution-receipt.json' },
  authority_granted: false, release_authority_granted: false, downstream_mutation_authority_granted: false,
  manual_tasks_required: [], user_manual_action_required: false,
  non_claims: ['This receipt records workflow-observed public route reachability only.','This receipt does not prove admissibility.','This receipt does not grant publication authority.','This receipt does not create provider governance.','This receipt does not create external indexing.','This receipt does not certify clinical performance or authorize medical practice.','This receipt does not convert verification or certification into execution authority.','This receipt does not decide authorship, ownership, infringement, derivation, or origin-claim standing.','Documentation-mesh reachability does not grant cross-repository authority or standing.','This receipt does not replace GitHub Pages deployment records.'],
  next_action: 'Retain this uploaded receipt as bounded automated evidence. Source-blocked observations remain automation-owned and create no user task.'
};
fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(outPath, JSON.stringify(receipt, null, 2) + '\n');
console.log(`wrote ${outPath}`);
