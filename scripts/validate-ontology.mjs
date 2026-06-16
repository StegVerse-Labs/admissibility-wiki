import fs from 'node:fs';

const artifactPath = 'static/ontology/admissibility-vocabulary.v0.1.json';
const raw = fs.readFileSync(artifactPath, 'utf8');
const data = JSON.parse(raw);

const allowedPostures = new Set([
  'conceptual',
  'implemented',
  'experimental',
  'proposed',
  'external',
]);

const requiredRootFields = [
  'schema_version',
  'artifact_id',
  'title',
  'publisher',
  'generated_for',
  'terms',
];

const requiredTermFields = [
  'id',
  'label',
  'category',
  'definition',
  'page',
  'posture',
  'related_terms',
];

const errors = [];

for (const field of requiredRootFields) {
  if (!(field in data)) {
    errors.push(`Missing root field: ${field}`);
  }
}

if (!Array.isArray(data.terms)) {
  errors.push('Root field terms must be an array.');
} else {
  const ids = new Set();

  for (const [index, term] of data.terms.entries()) {
    for (const field of requiredTermFields) {
      if (!(field in term)) {
        errors.push(`Term ${index} missing field: ${field}`);
      }
    }

    if (typeof term.id === 'string') {
      if (!/^[a-z0-9_]+$/.test(term.id)) {
        errors.push(`Term ${term.id} has invalid id format. Use lowercase letters, numbers, and underscores.`);
      }

      if (ids.has(term.id)) {
        errors.push(`Duplicate term id: ${term.id}`);
      }
      ids.add(term.id);
    }

    if (typeof term.page === 'string' && !term.page.startsWith('/')) {
      errors.push(`Term ${term.id ?? index} page must start with /.`);
    }

    if (!allowedPostures.has(term.posture)) {
      errors.push(`Term ${term.id ?? index} has invalid posture: ${term.posture}`);
    }

    if (!Array.isArray(term.related_terms)) {
      errors.push(`Term ${term.id ?? index} related_terms must be an array.`);
    }
  }
}

if (errors.length > 0) {
  console.error('Ontology validation failed:');
  for (const error of errors) {
    console.error(`- ${error}`);
  }
  process.exit(1);
}

console.log(`Ontology validation passed: ${data.terms.length} terms checked.`);
