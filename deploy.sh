#!/usr/bin/env bash
set -euo pipefail

: "${S3_BUCKET:?Set S3_BUCKET to the destination S3 bucket name.}"
: "${CLOUDFRONT_DISTRIBUTION_ID:?Set CLOUDFRONT_DISTRIBUTION_ID to the CloudFront distribution ID.}"
command -v aws >/dev/null 2>&1 || { echo 'AWS CLI is required. Install it and configure deployment credentials.' >&2; exit 1; }

cd "$(dirname "${BASH_SOURCE[0]}")"

# Explicit includes keep source references, private files, and QA artifacts off S3.
# The first pass deletes stale deployed files; the second applies image caching.
aws s3 sync . "s3://${S3_BUCKET}" --delete \
  --exclude '*' \
  --include 'index.html' --include 'css/*' --include 'js/*' \
  --include 'img/*' --include 'favicon.svg' --include 'robots.txt' \
  --exclude '.git/*' --exclude 'design/*' --exclude 'SPEC.md' \
  --exclude 'deploy.sh' --exclude 'README.md' \
  --cache-control 'max-age=300'

aws s3 cp ./img/ "s3://${S3_BUCKET}/img/" --recursive \
  --cache-control 'max-age=31536000, immutable'

aws cloudfront create-invalidation \
  --distribution-id "$CLOUDFRONT_DISTRIBUTION_ID" --paths '/*'
