#!/bin/bash

# Apply kernel security parameters
sysctl -w net.ipv4.conf.all.rp_filter=1
sysctl -w net.ipv4.conf.default.rp_filter=1

# Limit container capabilities
setcap -r /usr/local/bin/python3.9

# Configure AppArmor
cat << EOF > /etc/apparmor.d/shieldnet-profile
#include <tunables/global>

profile shieldnet flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>
  
  # Allow python execution
  /usr/local/bin/python3.9 mr,

  # Deny write access except logs
  deny /app/** w,
  /app/logs/** rw,
  
  # Network restrictions
  deny network raw,
  deny network packet,
}
EOF

apparmor_parser -r /etc/apparmor.d/shieldnet-profile
