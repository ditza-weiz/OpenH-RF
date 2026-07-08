for file in /home/projects/yonina/data/OpenH-RF/thyroid_test/subjects/*; do bsub -q short -R rusage[mem=16384] -R affinity[thread*8] uv run -- python -u upload_to_drive.py "$file"; done
