---
type: entity
slug: vendor-y
evidence-default: observed
sources: [2026-02-03-vendor-demo]
---
# Vendor Y

<!--
GUARD FIXTURE for `skip_if_frontmatter`. This page declares evidence-default
(+ sources), so its bare [observed] bullets inherit page-level provenance and must
NOT trigger observed-without-source, AND its untagged claim bullet below must NOT
trigger untagged-claim-bullet. If either rule's skip_if_frontmatter is removed or
broken, the eval's max_count guards fail (observed 1->2+, untagged 3->4+).
-->

## Claims
- Covers web, phone and partner booking channels [observed]
- Integrates with common CRM and calendar tools [observed]
- Reduces manual triage effort substantially across sites
