/**
 * Link checker script for documentation
 * Uses Linkinator to check for broken links
 */

import { LinkChecker } from 'linkinator';

const SITE_URL = 'http://localhost:4321';

async function checkLinks() {
  console.log(`Checking links at ${SITE_URL}...`);

  const checker = new LinkChecker();

  checker.on('link', (result) => {
    if (result.state === 'BROKEN') {
      console.error(`❌ ${result.url} (${result.status}) - found on ${result.parent}`);
    } else if (result.state === 'SKIPPED') {
      console.log(`⏭️  ${result.url} (skipped)`);
    }
  });

  const result = await checker.check({
    path: SITE_URL,
    recurse: true,
    linksToSkip: [
      'https://github.com/*',
      'mailto:*',
    ],
  });

  console.log('\n--- Summary ---');
  console.log(`Scanned: ${result.links.length} links`);
  console.log(`Passed: ${result.passed}`);

  const broken = result.links.filter((link) => link.state === 'BROKEN');
  if (broken.length > 0) {
    console.log(`Broken: ${broken.length}`);
    process.exit(1);
  }

  console.log('All links are valid!');
}

checkLinks().catch((error) => {
  console.error('Link check failed:', error);
  process.exit(1);
});
