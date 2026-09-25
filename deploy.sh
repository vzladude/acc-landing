#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

if [[ $# -gt 1 || ( $# -eq 1 && "$1" != '--dry-run' ) ]]; then
  printf '%s\n' 'Usage: ./deploy.sh [--dry-run]' >&2
  exit 1
fi
production_url='https://inversionesacc.com/'
if [[ "${SITE_URL:-$production_url}" != "$production_url" || "${ALLOW_INDEXING:-true}" != 'true' ]]; then
  printf '%s\n' 'Refusing deployment: ACC production must use its official URL with indexing enabled.' >&2
  exit 1
fi
if [[ -z "${S3_BUCKET:-}" || -z "${CLOUDFRONT_DISTRIBUTION_ID:-}" ]]; then
  printf '%s\n' 'Set S3_BUCKET and CLOUDFRONT_DISTRIBUTION_ID from deploy/aws-production.json.' >&2
  exit 1
fi
profile="${AWS_PROFILE:-personal}"
expected_account='767397867309'
account="$(aws --profile "$profile" sts get-caller-identity --query Account --output text)"
if [[ "$account" != "$expected_account" || "$S3_BUCKET" != "acc-landing-production-${expected_account}" ]]; then
  printf '%s\n' 'Refusing deployment: account or bucket does not match ACC production.' >&2
  exit 1
fi
origin="$(aws --profile "$profile" cloudfront get-distribution-config --id "$CLOUDFRONT_DISTRIBUTION_ID" --query 'DistributionConfig.Origins.Items[0].DomainName' --output text)"
if [[ "$origin" != "${S3_BUCKET}.s3.us-east-1.amazonaws.com" ]]; then
  printf '%s\n' 'Refusing deployment: CloudFront origin does not match the ACC bucket.' >&2
  exit 1
fi

python3 scripts/build_site.py
sync_options=(--no-follow-symlinks --only-show-errors)
if [[ "${1:-}" == '--dry-run' ]]; then
  sync_options+=(--dryrun)
fi

# Upload referenced assets first; retain prior versions for cached pages/rollback.
aws --profile "$profile" s3 sync .qa/production-site "s3://${S3_BUCKET}" \
  "${sync_options[@]}" --exclude 'index.html' --exclude 'robots.txt' --exclude 'sitemap.xml' \
  --exclude 'img/*' --cache-control 'public,max-age=31536000,immutable'
aws --profile "$profile" s3 sync .qa/production-site/img "s3://${S3_BUCKET}/img" \
  "${sync_options[@]}" --cache-control 'public,max-age=31536000,immutable'

# Publish HTML last so visitors never receive a page before its assets exist.
for page in robots.txt sitemap.xml index.html; do
  if [[ -f ".qa/production-site/$page" ]]; then
    aws --profile "$profile" s3 cp ".qa/production-site/$page" "s3://${S3_BUCKET}/$page" \
      "${sync_options[@]}" --cache-control 'public,max-age=300'
  fi
done
if [[ "${1:-}" != '--dry-run' ]]; then
  aws --profile "$profile" cloudfront create-invalidation \
    --distribution-id "$CLOUDFRONT_DISTRIBUTION_ID" --paths '/*' --no-cli-pager
fi
