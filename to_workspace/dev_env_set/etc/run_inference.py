import sys
import os
from pathlib import Path
import cv2
import numpy as np
import torch
import torchvision.transforms as T
from tqdm import tqdm

# --- PATH FIXER ---
current_path = Path(__file__).parent.absolute()
root_path = current_path 

libero_path = root_path / "LIBERO"
if libero_path.exists():
    sys.path.append(str(libero_path))
sys.path.append(str(root_path))
# ------------------

try:
    from libero.libero import benchmark, get_libero_path
    from libero.libero.envs import OffScreenRenderEnv
except ImportError:
    print("❌ Critical Error: Could not import LIBERO.")
    sys.exit(1)

from flower.evaluation.utils import load_mode_from_safetensor

def get_transforms():
    """
    Transforms to match the model's training configuration.
    112x112 resolution, Normalized with CLIP stats.
    """
    return T.Compose([
        T.ToTensor(),
        T.Resize((112, 112), antialias=True),
        T.Normalize(
            mean=[0.48145466, 0.4578275, 0.40821073],
            std=[0.26862954, 0.26130258, 0.27577711]
        )
    ])

def run_inference():
    print(f"--- STEP 3: FLOWER VLA Inference Test (Root Mode) ---")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}")

    # 1. Load Model
    checkpoint_dir = root_path / "checkpoints/flower_libero_10"
    print(f"Loading model from: {checkpoint_dir}")
    
    try:
        model = load_mode_from_safetensor(checkpoint_dir)
    except Exception as e:
        print(f"❌ Model Load Error: {e}")
        return

    model = model.to(device)
    model.eval()
    model.reset()
    print("✅ Model loaded successfully.")

    # 2. Setup Environment
    benchmark_name = "libero_10"
    benchmark_dict = benchmark.get_benchmark_dict()
    benchmark_instance = benchmark_dict[benchmark_name]()
    
    task_id = 1
    task = benchmark_instance.get_task(task_id)
    print(f"Task: {task.name}")
    print(f"Instruction: '{task.language}'")

    bddl_folder = get_libero_path("bddl_files")
    bddl_file = os.path.join(bddl_folder, task.problem_folder, task.bddl_file)

    env_args = {
        "bddl_file_name": bddl_file,
        "camera_heights": 224,
        "camera_widths": 224,
        "render_gpu_device_id": 0
    }
    
    env = OffScreenRenderEnv(**env_args)
    obs = env.reset()

    # 3. Run Loop
    transforms = get_transforms()
    video_path = root_path / "inference_result.mp4"
    video_writer = cv2.VideoWriter(str(video_path), cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (448, 224))
    
    print("Starting simulation...")
    
    goal_dict = {"lang_text": task.language}

    print("Warming up physics...")
    for _ in range(20): 
        obs, _, _, _ = env.step(np.zeros(7))

    for step in tqdm(range(400)):
        img_static = obs['agentview_image'] 
        img_gripper = obs['robot0_eye_in_hand_image']
        
        if img_static is None or img_gripper is None:
            print("❌ Error: Environment returned None for images.")
            break

        # --- FIX: Add Time Dimension (B, T, C, H, W) ---
        # unsqueeze(0) for Batch -> (1, C, H, W)
        # unsqueeze(0) again for Time -> (1, 1, C, H, W)
        static_tensor = transforms(img_static).unsqueeze(0).unsqueeze(0).to(device)
        gripper_tensor = transforms(img_gripper).unsqueeze(0).unsqueeze(0).to(device)
        
        obs_dict = {
            "rgb_obs": {
                "rgb_static": static_tensor,
                "rgb_gripper": gripper_tensor
            },
            # Robot state also usually needs (B, T, D) shape
            "robot_obs": torch.tensor(obs['robot0_joint_pos']).unsqueeze(0).unsqueeze(0).to(device),
            "gripper_states": torch.tensor(obs['robot0_gripper_qpos']).unsqueeze(0).unsqueeze(0).to(device)
        }

        with torch.no_grad():
            action_tensor = model.step(obs_dict, goal_dict)
        
        action = action_tensor.detach().cpu().numpy().flatten()
        
        obs, reward, done, info = env.step(action)
        
        # Render
        combined_img = np.concatenate((img_static, img_gripper), axis=1)
        if combined_img.dtype != np.uint8:
            combined_img = (combined_img * 255).astype(np.uint8)
        combined_img = cv2.cvtColor(combined_img, cv2.COLOR_RGB2BGR)
        video_writer.write(combined_img)
        
        if done:
            print("🎉 Success! The robot completed the task.")
            break

    video_writer.release()
    env.close()
    print(f"✅ Video saved to {video_path}")

if __name__ == "__main__":
    run_inference()