import subprocess
import os

def run(cmd):
    print(f"\n>>> {cmd}")
    subprocess.run(cmd, shell=True, check=True)

home = os.path.expanduser("~")
installer = "Miniconda3-latest-Linux-x86_64.sh"
installer_path = os.path.join(home, installer)
conda_dir = os.path.join(home, "miniconda3")
conda = f"{conda_dir}/bin/conda"

print("\n=== CHECK: Miniconda vorhanden? ===")
if os.path.exists(conda_dir):
    print("Miniconda ist bereits installiert – Installation wird übersprungen.")
else:
    print("\n=== 1. Miniconda herunterladen ===")
    run(f"wget https://repo.anaconda.com/miniconda/{installer} -O {installer_path}")

    print("\n=== 2. Installer ausführbar machen ===")
    run(f"chmod +x {installer_path}")

    print("\n=== 3. Miniconda installieren ===")
    run(f"{installer_path} -b -p {conda_dir}")

print("\n=== 4. Conda initialisieren ===")
run(f"{conda} init")

print("\n=== 5. Channels setzen ===")
channels = ["defaults", "conda-forge", "nvidia", "pytorch"]
for ch in channels:
    run(f"{conda} config --add channels {ch}")

run(f"{conda} config --set channel_priority strict")

print("\n=== 6. Base deaktivieren ===")
run(f"{conda} config --set auto_activate_base false")

print("\n=== 7. AI Environment erstellen (falls nicht vorhanden) ===")
env_path = os.path.join(conda_dir, "envs", "ai")
if os.path.exists(env_path):
    print("Environment 'ai' existiert bereits – wird übersprungen.")
else:
    run(f"{conda} create -n ai python=3.11 -y")

print("\n=== 8. AI Core Pakete installieren ===")
core_packages = (
    "numpy scipy pandas scikit-learn matplotlib seaborn "
    "transformers datasets tokenizers accelerate evaluate optimum "
    "huggingface_hub nltk category_encoders"
)
run(f"{conda} install -n ai -y {core_packages}")

print("\n=== 9. PyTorch + CUDA installieren ===")
run(f"{conda} install -n ai -y pytorch torchvision torchaudio pytorch-cuda=12.4 -c pytorch -c nvidia")

print("\n=== 10. Pip Pakete installieren ===")
run(f"{conda} run -n ai pip install requests requests_toolbelt")

print("\n=== 11. Updates durchführen ===")
run(f"{conda} update -n ai --all -y")

print("\n=== FERTIG: Deine komplette COAE AI‑Umgebung ist bereit. ===")
