#!/usr/bin/env bash
# Source this file to enable SISSO++ in the current shell:
#   source scripts/activate_sisso.sh
#
# Loads Intel oneAPI (MPI + MKL) and activates the sissopp_env conda env.

if [ -f /etc/profile.d/modules.sh ]; then
    # shellcheck disable=SC1091
    source /etc/profile.d/modules.sh
fi
module load intel/oneapi/2023.0.0

# shellcheck disable=SC1091
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate sissopp_env

# Make the sisso++ binary discoverable
export PATH="/home/hyunjin/sissopp/bin:$PATH"
