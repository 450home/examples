#!/usr/bin/env bash
# Deletes all Unikraft Cloud resources created during a test run.
#
# Usage:  UKC_TEST_ID=<run-id> ./scripts/cleanup-test-resources.sh
#
# The script is intentionally lenient: each deletion is attempted with --force
# and failures are logged but do not abort the script, so a partial cleanup
# never masks other resources.

set -euo pipefail

: "${UKC_TEST_ID:?UKC_TEST_ID must be set}"

FILTER="name~=\"^.*${UKC_TEST_ID}\""

echo "==> Cleaning up test resources for run ID: ${UKC_TEST_ID}"

echo "--> Deleting instances..."
unikraft instances delete \
    --filter "${FILTER}" \
    --force || echo "Warning: instance deletion failed or nothing to delete"

echo "--> Deleting instance templates..."
unikraft instances templates delete \
    --filter "${FILTER}" \
    --force || echo "Warning: instance template deletion failed or nothing to delete"

echo "--> Deleting volumes..."
unikraft volumes delete \
    --filter "${FILTER}" \
    --force || echo "Warning: volume deletion failed or nothing to delete"

echo "--> Deleting images..."
IMAGE_FILTER="ref~=\"^.*${UKC_TEST_ID}\""
IMAGES=$(unikraft images list \
    --filter "${IMAGE_FILTER}" \
    --field ref \
    --output raw 2>/dev/null \
    | jq -r '.[].name' 2>/dev/null || true)

if [[ -z "${IMAGES}" ]]; then
    echo "    No images to delete."
else
    while IFS= read -r image; do
        echo "    Deleting image: ${image}"
        unikraft images delete "${image}" \
            || echo "Warning: failed to delete image ${image}"
    done <<< "${IMAGES}"
fi

echo "==> Cleanup complete."
