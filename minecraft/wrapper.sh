#!/usr/bin/env bash

set -e

# Load config from ROMs
if [ -d "/rom" ]; then
    # First, source the base config if it exists
    if [ -f "/rom/base/.env" ]; then
        echo "Sourcing /rom/base/.env..."
        set -a
        # shellcheck disable=SC1091
        . "/rom/base/.env"
        set +a
    else
        echo "No /rom/base/.env found, skipping base config sourcing..."
    fi

    # Source other configs, if they exist
    while IFS= read -r env_file; do
        if [ "$env_file" != "/rom/base/.env" ]; then  # Skip the base config
            echo "Sourcing $env_file..."
            set -a
            # shellcheck disable=SC1091
            . "$env_file"
            set +a
        fi
    done < <(find /rom -maxdepth 2 -type f -name ".env" 2>/dev/null)
else
    echo "No /rom directory found, skipping config sourcing..."
fi

# Start SSH server
echo "Starting SSH server..."

export HOME=/root
if test ! -z "$PUBKEY"; then
    echo "$PUBKEY" >> "$HOME/.ssh/authorized_keys"
    echo "Added provided public key to authorized_keys."
else
    echo "No PUBKEY provided. SSH access will not be available."
fi

/usr/sbin/sshd -h /etc/ssh/ssh_host_ecdsa_key -p 2222

echo "Current environment after setup:"
env | sort

echo ""
echo "Environment setup complete. Continuing from the original entrypoint..."
echo ""
exec "$@"
