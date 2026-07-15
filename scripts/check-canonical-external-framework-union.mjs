#!/usr/bin/env node
import fs from 'node:fs';

const INVENTORY_PATH = 'static/external-frameworks/canonical-union-inventory.v1.json';
const REGISTRY_PATH = 'docs/external-frameworks/index.json';
const ASSOCIATIONS_PATH = 'static/external-frameworks/sidebar-page-associations.v1.json';
const DISPOSITIONS_PATH = 'static/external-frameworks/registry-navigation-dispositions.v1.json';

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exit(1);
}

function readJson(path) {
  if (!fs.existsSync(path)) fail(`missing JSON artifact: ${path}`);
  try {
    return JSON.parse(fs.readFileSync(path, 'utf8'));
  } catch (error) {
    fail(`invalid JSON in ${path}: ${error.message}`);
  }
}

function resolvePaths(inventory, entry) {
  const pageSlug = entry.page_slug || entry.record_id;
  return {
    page: inventory.path_conventions.page.replace('{page_slug}', pageSlug),
    manifest: inventory.path_conventions.manifest.replace('{record_id}', entry.record_id),
    report: inventory.path_conventions.report.replace('{record_id}', entry.record_id)
  };
}

const inventory = readJson(INVENTORY_PATH);
const registry = readJson(REGISTRY_PATH);
const associations = readJson(ASSOCIATIONS_PATH);
const dispositions = readJson(DISPOSITIONS_PATH);

if (inventory.schema !== 'external_framework_canonical_union_inventory.v1') fail('unexpected canonical union inventory schema');
if (inventory.repository !== 'StegVerse-Labs/admissibility-wiki') fail('unexpected canonical union inventory repository');
if (!Array.isArray(inventory.entries)) fail('canonical union inventory entries must be an array');
if (!Array.isArray(registry.entries)) fail('docs registry entries must be an array');
if (!Array.isArray(associations.entries)) fail('sidebar association entries must be an array');
if (!Array.isArray(dispositions.entries)) fail('navigation disposition entries must be an array');

const registryById = new Map(registry.entries.map(entry => [entry.framework_id, entry]));
const sidebarIds = new Set(
  associations.entries
    .filter(entry => entry.page_type === 'framework')
    .map(entry => entry.framework_id)
);
const dispositionById = new Map(dispositions.entries.map(entry => [entry.framework_id, entry]));
const inventoryIds = new Set();
let externalCount = 0;
let internalCount = 0;
let sidebarCount = 0;
let nonPublicCount = 0;
let internalNavigationCount = 0;

for (const entry of inventory.entries) {
  for (const field of ['record_id', 'record_type', 'external_framework', 'navigation_state']) {
    if (!(field in entry)) fail(`canonical inventory entry missing ${field}: ${entry.record_id || '<unknown>'}`);
  }
  if (inventoryIds.has(entry.record_id)) fail(`duplicate canonical inventory record_id: ${entry.record_id}`);
  inventoryIds.add(entry.record_id);

  const registryEntry = registryById.get(entry.record_id);
  if (!registryEntry) fail(`canonical inventory record missing from docs registry: ${entry.record_id}`);

  const paths = resolvePaths(inventory, entry);
  if (registryEntry.path !== paths.page) fail(`canonical page path mismatch for ${entry.record_id}: registry=${registryEntry.path}, inventory=${paths.page}`);
  if (registryEntry.manifest_path !== paths.manifest) fail(`canonical manifest path mismatch for ${entry.record_id}`);
  for (const [label, path] of Object.entries(paths)) {
    if (!fs.existsSync(path)) fail(`canonical ${label} file missing for ${entry.record_id}: ${path}`);
  }

  const report = readJson(paths.report);
  if (report.framework_id !== entry.record_id) fail(`compatibility report framework_id mismatch for ${entry.record_id}`);
  if (report.framework_manifest !== paths.manifest) fail(`compatibility report manifest path mismatch for ${entry.record_id}`);

  if (entry.external_framework === true) {
    externalCount += 1;
    if (entry.record_type !== 'external_framework') fail(`external record_type mismatch for ${entry.record_id}`);
  } else {
    internalCount += 1;
    if (entry.record_type !== 'internal_ecosystem_record') fail(`internal record_type mismatch for ${entry.record_id}`);
  }

  if (entry.navigation_state === 'public_sidebar') {
    sidebarCount += 1;
    if (!sidebarIds.has(entry.record_id)) fail(`public_sidebar record absent from sidebar associations: ${entry.record_id}`);
    if (dispositionById.has(entry.record_id)) fail(`public_sidebar record must not have disposition: ${entry.record_id}`);
  } else if (entry.navigation_state === 'non_public_explicit') {
    nonPublicCount += 1;
    const disposition = dispositionById.get(entry.record_id);
    if (!disposition || disposition.navigation_state !== 'non_public_explicit') fail(`missing non-public disposition for ${entry.record_id}`);
    if (sidebarIds.has(entry.record_id)) fail(`non-public record appears in sidebar associations: ${entry.record_id}`);
  } else if (entry.navigation_state === 'internal_record') {
    internalNavigationCount += 1;
    const disposition = dispositionById.get(entry.record_id);
    if (!disposition || disposition.navigation_state !== 'internal_record') fail(`missing internal-record disposition for ${entry.record_id}`);
    if (entry.external_framework !== false) fail(`internal_record must set external_framework=false: ${entry.record_id}`);
    if (sidebarIds.has(entry.record_id)) fail(`internal record appears as framework sidebar page: ${entry.record_id}`);
  } else {
    fail(`unsupported navigation_state for ${entry.record_id}: ${entry.navigation_state}`);
  }
}

if (inventoryIds.size !== registryById.size) fail(`canonical inventory/docs registry count mismatch: inventory=${inventoryIds.size}, registry=${registryById.size}`);
for (const frameworkId of registryById.keys()) {
  if (!inventoryIds.has(frameworkId)) fail(`docs registry record missing from canonical inventory: ${frameworkId}`);
}

const expected = inventory.counts || {};
if (expected.records !== inventory.entries.length) fail('canonical inventory records count is stale');
if (expected.external_frameworks !== externalCount) fail('canonical inventory external_frameworks count is stale');
if (expected.internal_records !== internalCount) fail('canonical inventory internal_records count is stale');
if (expected.public_sidebar !== sidebarCount) fail('canonical inventory public_sidebar count is stale');
if (expected.non_public_explicit !== nonPublicCount) fail('canonical inventory non_public_explicit count is stale');
if (expected.internal_record !== internalNavigationCount) fail('canonical inventory internal_record count is stale');

console.log(`OK: ${INVENTORY_PATH}`);
console.log(`canonical_union_records=${inventory.entries.length}`);
console.log(`canonical_union_external_frameworks=${externalCount}`);
console.log(`canonical_union_internal_records=${internalCount}`);
console.log(`canonical_union_public_sidebar=${sidebarCount}`);
console.log(`canonical_union_non_public_explicit=${nonPublicCount}`);
console.log(`canonical_union_internal_navigation=${internalNavigationCount}`);
console.log('canonical_union_inventory_guard=ENFORCED');
