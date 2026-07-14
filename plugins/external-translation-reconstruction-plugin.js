import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';

export default function externalTranslationReconstructionPlugin() {
  return {
    name: 'external-translation-reconstruction-plugin',
    async postBuild({outDir}) {
      const result = spawnSync(
        process.env.PYTHON || 'python',
        ['scripts/generate_external_translation_reconstruction_receipt.py'],
        {encoding: 'utf8', stdio: 'pipe'}
      );

      if (result.stdout) process.stdout.write(result.stdout);
      if (result.stderr) process.stderr.write(result.stderr);
      if (result.status !== 0) {
        throw new Error(`external translation reconstruction generator failed with status ${result.status}`);
      }

      const source = path.resolve('reports/external-translation/reconstruction-receipt.json');
      if (!fs.existsSync(source)) {
        throw new Error(`missing generated reconstruction receipt: ${source}`);
      }

      const payload = JSON.parse(fs.readFileSync(source, 'utf8'));
      if (payload.overall_status !== 'PASS') {
        throw new Error(`reconstruction receipt is not PASS: ${payload.overall_status}`);
      }

      const statusDir = path.join(outDir, 'status');
      fs.mkdirSync(statusDir, {recursive: true});
      const destination = path.join(statusDir, 'external-translation-reconstruction-receipt.json');
      fs.writeFileSync(destination, JSON.stringify(payload, null, 2) + '\n');
      console.log(`published ${destination}`);
    },
  };
}
