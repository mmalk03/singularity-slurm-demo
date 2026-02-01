#!/usr/bin/env bash

#SBATCH --constraint=dgx
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16GB
#SBATCH --gpus=1
#SBATCH --time=0-1:00:00
#SBATCH --partition=short
#SBATCH --export=ALL
#SBATCH --account=mandziuk-lab

module load singularity

date
echo "SLURMD_NODENAME: ${SLURMD_NODENAME}"
echo "SLURM_JOB_ID: ${SLURM_JOB_ID}"
echo "CUDA_VISIBLE_DEVICES: ${CUDA_VISIBLE_DEVICES}"
echo "singularity version: $(singularity version)"
echo "nvidia-container-cli info: $(nvidia-container-cli info)"

nvidia-smi

echo "Training command: python ${1}" "${@:2}"

user_dir="/home2/faculty/mmalkinski"
group_dir="/mnt/evafs/groups/mandziuk-lab/mmalkinski"

singularity exec \
  --nv \
  --env CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES}" \
  --env XDG_CACHE_HOME="/app/cache" \
  --env XDG_CONFIG_HOME="/app/cache/config" \
  --env XDG_DATA_HOME="/app/cache/data" \
  --env HF_HOME="/app/cache/huggingface" \
  --env VLLM_CACHE="/app/cache/vllm" \
  --env FLASHINFER_WORKSPACE_BASE="/app/cache/flashinfer" \
  --env TRITON_CACHE_DIR="/app/cache/triton" \
  --env PYTHONPATH="/app/code" \
  --env VLLM_NO_USAGE_STATS=1 \
  --pwd "/app/code" \
  --workdir "/app/code" \
  --bind "${user_dir}/projects/singularity-slurm-demo:/app/code:rw" \
  --bind "${group_dir}/cache:/app/cache:rw" \
  --bind "${group_dir}/datasets:/app/datasets:rw" \
  "${group_dir}/singularity/mikomel-demo-vllm-latest.sif" \
  python3 "${1}" "${@:2}"
date
