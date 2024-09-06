# Singularity slurm demo

The repository demonstrates a simple setup to build and run [singularity](https://sylabs.io/guides/latest/user-guide) containers on a computing cluster with no direct access to docker.
Key highlights:
1. [Vagrant](https://github.com/hashicorp/vagrant) is used to provision a VM with docker installed.
2. The docker image is built in the VM and exported to a tar file.
3. The tar file is synced from the guest VM to the host and converted to a singularity container.
4. Two sample images from the nvidia NGC catalog are used: [tensorflow](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/tensorflow) and [pytorch](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/pytorch).

Prerequisites:
1. Set up passwordless ssh to the computing cluster. In this repository, the host is named `eden`.
2. Update hard-coded strings based on your needs (e.g. the docker image name).

## Usage

### Local

For development purposes, here are the scripts and commands which can be run locally:
1. `./scripts/build_image.sh` – Build docker image.
2. `docker run mikomel/demo:latest python demo/main.py -n 5` – Run docker container.
3. `docker save --output ~/docker/mikomel-demo-latest.tar mikomel/demo:latest` – Save docker image to a tar file.
4. `singularity build ~/singularity/mikomel-demo-latest.sif docker-archive://~/docker/mikomel-demo-latest.tar` – Build a singularity container from the tar file.
5. `singularity run ~/singularity/mikomel-demo-latest.sif python demo/main.py -n 5` – Run the singularity container.

### Remote

To sync files between local and remote machines, run the following locally:
```bash
./scripts/remote/rsync.sh
```
The project files are mounted to the running container (see `--bind` in `submit.sh`), which allows to update code running in the container without rebuilding the whole image. 

To build the singularity container from scratch, run the following on the remote machine:
```bash
sbatch ./scripts/remote/build.sh
```
It will build the singularity container in a VM provisioned by Vagrant.
This has to be run each time your dependencies change (or generally the content of the Dockerfile).

The created file will have a timestamp in its suffix to support multiple versions.
For easier use, reference the created file in a symbolic link that points to a static path, e.g.: 
```bash
ln -sf ~/singularity/mikomel-demo_2024-09-06_07-57-41.sif ~/singularity/mikomel-demo-latest.sif
```

To run a container with the sample script, run:
```bash
sbatch ./scripts/remote/submit.sh demo/main.py -n 5
```

Output logs of the job can be viewed with:
```bash
tail -f slurm-<JOB_ID>.out
```

Alternatively, plain Python can be used to run the scripts without singularity:
```bash
sbatch scripts/remote/run.sh demo/main.py -n 5
```
