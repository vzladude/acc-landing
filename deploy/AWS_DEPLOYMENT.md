# ACC AWS deployment

Production URL: **https://inversionesacc.com/**. Both `www` and `/index.html` redirect to the canonical root, preserving paths and encoded/repeated query parameters. HTTP redirects to HTTPS. The temporary CloudFront hostname redirects to the official site.

## Resources

Created for ACC in AWS account `767397867309` using profile `personal`, region `us-east-1`, with infrastructure adapted from the existing IHM project. ACC has a separate bucket, distribution, certificate, edge function, WAF, and CloudFormation stack.

- Stack: `acc-landing-production`.
- Bucket: `acc-landing-production-767397867309`.
- Distribution: `E29C4VUSCEAMTM` (`d32q0ufgl5k5s8.cloudfront.net`).
- Existing hosted zone: `Z05695902OJ8GCHX96L36`.
- Certificate and Free subscription ARNs: `aws-production.json`.

`aws-stack.yaml` manages encrypted private S3, OAC signed origin access, a distribution-scoped bucket read policy, HTTPS, compression, managed cache/security header policies, a dedicated WAF IP rate rule, and canonical redirects. Public S3 access is blocked. The certificate covers root and www; CloudFormation creates the DNS validation CNAMEs. Keep these CNAMEs for renewal. The bucket is retained on stack deletion.

`ActivateDns=false` supports initial provisioning and TLS-validating pre-cutover checks. Production uses **`ActivateDns=true`**, managing root/www A and AAAA aliases in the existing hosted zone. For updates, preserve that parameter:

```sh
aws --profile personal cloudformation deploy --region us-east-1 \
  --stack-name acc-landing-production --template-file deploy/aws-stack.yaml \
  --parameter-overrides HostedZoneId=Z05695902OJ8GCHX96L36 ActivateDns=true \
  --no-fail-on-empty-changeset
```

Review infrastructure changes with a change set before execution. Preserve mail, ownership-verification, and certificate-validation records during future DNS changes. At migration start, the zone contained only NS and SOA records, and registrar/public delegation matched the hosted zone.

## Cost and subscription lifecycle

The dedicated CloudFront **Free / ACTIVE** plan includes this distribution, its WAF, and the attached Route 53 zone. AWS currently allows three Free plans per account; this is the second. The baseline includes 1 million requests and 100 GB per month, plus S3 Standard storage credits. Sustained usage above allowances may affect delivery; this is not unlimited capacity. Domain renewal and S3 request charges are separate, and initial provisioning can incur small prorated charges. The total AWS account bill is not guaranteed to be zero.

The pricing subscription is managed outside CloudFormation. It was created with the official PricingPlanManager API, `planFamily=CloudFront`, `planTier=FREE`, and the distribution, WAF and hosted-zone ARNs. AWS CLI 2.32.17 predates that API, so provisioning used isolated Boto3 1.43.102 under ignored `.qa/aws-venv/`; daily uploads need only AWS CLI and Python 3.

Do not cancel the plan or detach its resources casually: CloudFront/WAF/Route 53 can return to usage-based billing. Deleting the CloudFormation stack does not manage or cancel this separate subscription. Review the subscription before retiring the site.

References: [AWS plan pricing](https://aws.amazon.com/cloudfront/pricing/), [plan coverage and quotas](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/flat-rate-pricing-plan.html), [subscription API](https://docs.aws.amazon.com/PricingPlanManager/latest/UserGuide/getting-started-pricingplanmanager-api.html).

## Publish

```sh
export AWS_PROFILE=personal
export S3_BUCKET=acc-landing-production-767397867309
export CLOUDFRONT_DISTRIBUTION_ID=E29C4VUSCEAMTM
./deploy.sh --dry-run
./deploy.sh
```

The deployment refuses missing variables, incorrect account/bucket/origin, temporary canonical URLs, and non-indexable production releases. `scripts/build_site.py` includes only static runtime file types from the designated source directories plus HTML, robots and sitemap. It handles inline SVG image references and CSS backgrounds. All image bytes stay unchanged; assets receive SHA-256-based names. The production stylesheet is embedded in HTML after rewriting background-image paths, avoiding a render-blocking round trip while retaining the separate editable source stylesheet. The release manifest is saved outside the public directory.

Immutable assets upload first. Robots, sitemap and HTML upload last with five-minute caching. Old assets are retained; the script never deletes S3 files during a release. Source documentation, infrastructure, tests, SDKs, and verification evidence are excluded from the upload. GitHub commits do not deploy AWS automatically. The Pages workflow now publishes only the relocation notice after migration verification.

## Verification and rollback

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
node --test tests/redirect.test.cjs
python3 scripts/build_site.py
npx html-validate index.html .qa/production-site/index.html deploy/pages-redirect.html
bash -n deploy.sh
git diff --check
```

Before switching DNS, TLS was checked with `curl --connect-to` using the actual certificate/host name, never by disabling certificate verification. The preflight checks compare every public file to the release SHA-256 manifest, inspect cache headers, test redirect/query preservation, and confirm S3/source files are inaccessible. Repeat on the public domain after DNS activation, then check mobile/desktop, menu, images, WhatsApp, map, canonical, sitemap and robots. Evidence is stored under ignored `.qa/` and summarized in `IMPLEMENTATION_NOTES.md`.

To roll back content, check out a previously verified AWS-enabled commit in a separate checkout, retain the official domain metadata, run checks, and publish with the same bucket/distribution. Earlier assets remain available, and uploading HTML last avoids broken cached pages. Do not revert to an old GitHub Pages canonical URL. An initial-launch DNS rollback can set `ActivateDns=false`, removing only the four stack-managed aliases while retaining the existing zone and certificate validation records; this makes the domain unavailable until a replacement is set. Prefer rolling back content for a content-only issue.

The migration does not configure form delivery, GA4, or Search Console. Those phases require their own integration and end-to-end verification. No IHM measurement identifier is copied to ACC.
