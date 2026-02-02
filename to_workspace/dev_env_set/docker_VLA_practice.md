### 계획
- [x] 실습 구상 
- [x] ~~calvin 실행~~
- [x] Libero 실행
- [x] Flower VLA 실행
- [x] Docker에 담기
    - [x] ~/.bashrc 색 변경
    - [ ] run_robot.py 리팩토링, 실시간 출력 및 저장 방식 변경
        - [x] scene id가 총 몇개인지 체크
    - [ ] 현재 상태 커밋 및 푸쉬
        - [ ] 테스트 시행
- [ ] 깃허브 업로드 
    - [ ] 현재 리포 정리
    - [ ] 리드미 새로 작성
    - [ ] 포크하고 업로드
- [ ] 개발 방식 정리 및 커밋

도커 실습으로 VLA를 도커에 담아 배포해볼 예정이다.

### FLOWER: Democratizing Generalist Robot Policies with Efficient Vision-Language-Action Flow Policies

https://intuitive-robots.github.io/flower_vla/
https://www.arxiv.org/pdf/2509.04996

![alt text](image.png)

작년에 발표된 이 VLA 모델은 거의 모든 벤치마크에서 최우수 성적을 거뒀음에도 VRAM이 거의 필요하지 않다. 

단일 이미지에서는 3GB 미안, 일반 추론시 8GB만 필요하다고 해서 현재 내 환경에서 안성맞춤이다.

- Finetuning 및 평가용 버전을 이용해볼 예정이다.

https://github.com/intuitive-robots/flower_vla_calvin


```bash
git clone --recurse-submodules git@github.com:intuitive-robots/flower_vla_calvin.git
export flower_calvin_ROOT=$(pwd)/flower_vla_calvin
```

```bash
cd $flower_calvin_ROOT
conda create -n flower_cal python=3.9
conda activate flower_cal
cd calvin_env/tacto
pip install -e .
cd ..
pip install -e .
cd ..
cd LIBERO
pip install -r requirements.txt
pip install -e .
pip install numpy~=1.23
cd ..
pip install setuptools==57.5.0
cd pyhash-0.9.3
python setup.py build
python setup.py install
cd ..

pip install -r requirements.txt
```




- 시뮬레이션 관련 추가 설치.
```bash
# Install the tactile simulator (tacto)
cd calvin_env/tacto
pip install -e .

# Install the CALVIN environment itself
cd .. 
pip install -e .

# Go back to the root
cd ..
```

https://huggingface.co/collections/mbreuss/flower-vla
https://huggingface.co/mbreuss/flower_calvin_d


```
mkdir -p checkpoints
huggingface-cli download mbreuss/flower_calvin_d --local-dir checkpoints
```

- 일단 calvin 벤치마크 리포도 다운받음. 이용안하면 삭제할 것.

```
git clone git@github.com:mees/calvin.git
```



Hum... are you sure we can go from this? Shouldn't we not doing test for like actually testing the simulation things or something?

hulc_data_module.py 수정
```py
    def train_dataloader(self):
        return {
            key: DataLoader(
                dataset,
                batch_size=dataset.batch_size,
                num_workers=dataset.num_workers,
                pin_memory=True,
                shuffle=True,
                persistent_workers=True,  # Keep workers alive between epochs
                prefetch_factor=2,
            )
            for key, dataset in self.train_datasets.items()
        }

    def val_dataloader(self):
        return  {
            key: DataLoader(
                dataset,
                batch_size=dataset.batch_size,
                num_workers=dataset.num_workers,
                persistent_workers=True,  # Keep workers alive between epochs
                pin_memory=True,
            )
            for key, dataset in self.val_datasets.items()
        }
```

```py
    def train_dataloader(self):
        return {
            key: DataLoader(
                dataset,
                batch_size=dataset.batch_size,
                num_workers=dataset.num_workers,
                pin_memory=True,
                shuffle=True,
                persistent_workers=dataset.num_workers > 0, # Keep workers alive between epochs
                prefetch_factor=2,
            )
            for key, dataset in self.train_datasets.items()
        }

    def val_dataloader(self):
        return  {
            key: DataLoader(
                dataset,
                batch_size=dataset.batch_size,
                num_workers=dataset.num_workers,
                persistent_workers=dataset.num_workers > 0, # Keep workers alive between epochs
                pin_memory=True,
            )
            for key, dataset in self.val_datasets.items()
        }
```


```bash
(flower_cal) theo@theo-OMEN:~/flower_vla_calvin$ python check_joints.py
pybullet build time: Jan 29 2025 23:20:52
🔍 Inspecting Robot: /home/theo/flower_vla_calvin/calvin_env/data/franka_panda/panda.urdf
✅ Robot loaded with 14 total joints/links.

========================================
ID    | Name                 | Type
========================================
0     | panda_joint1         | Revolute (Arm?)
1     | panda_joint2         | Revolute (Arm?)
2     | panda_joint3         | Revolute (Arm?)
3     | panda_joint4         | Revolute (Arm?)
4     | panda_joint5         | Revolute (Arm?)
5     | panda_joint6         | Revolute (Arm?)
6     | panda_joint7         | Revolute (Arm?)
7     | panda_joint8         | Fixed
8     | panda_hand_joint     | Fixed
9     | panda_finger_joint1  | Prismatic (Gripper?)
10    | panda_finger_joint2  | Prismatic (Gripper?)
11    | panda_grasptarget_hand | Fixed
12    | camera_joint         | Fixed
13    | tcp_joint            | Fixed
========================================

💡 SUGGESTED CONFIG:
arm_joint_ids: [0, 1, 2, 3, 4, 5, 6]
gripper_joint_ids: [9, 10]

```


- 계속 시름해도 잘 안됨.

robot.py 수정이 필요할 수도 있음.

```
import logging

import numpy as np
import pybullet as p

from calvin_env.robot.mixed_ik import MixedIK

# A logger for this file
log = logging.getLogger(__name__)


class Robot:
    def __init__(
        self,
        filename,
        base_position,
        base_orientation,
        initial_joint_positions,
        max_joint_force,
        gripper_force,
        arm_joint_ids,
        gripper_joint_ids,
        gripper_joint_limits,
        tcp_link_id,
        end_effector_link_id,
        cid,
        use_nullspace,
        max_velocity,
        use_ik_fast,
        euler_obs,
        lower_joint_limits=(-2.8973, -1.7628, -2.8973, -3.0718, -2.8973, -0.0175, -2.8973),
        upper_joint_limits=(2.8973, 1.7628, 2.8973, -0.0698, 2.8973, 3.7525, 2.8973),
        max_rel_pos=0.02,
        max_rel_orn=0.05,
        magic_scaling_factor_pos=1,
        magic_scaling_factor_orn=1,
        use_target_pose=True,
        **kwargs,
    ):
        log.info("Loading robot")
        self.cid = cid
        self.filename = filename
        self.use_nullspace = use_nullspace
        self.max_velocity = max_velocity
        self.use_ik_fast = use_ik_fast
        self.base_position = base_position
        self.base_orientation = p.getQuaternionFromEuler(base_orientation)
        self.arm_joint_ids = arm_joint_ids
        self.initial_joint_positions = np.array(initial_joint_positions)
        self.gripper_joint_ids = gripper_joint_ids
        self.max_joint_force = max_joint_force
        self.gripper_force = gripper_force
        self.gripper_joint_limits = gripper_joint_limits
        self.tcp_link_id = tcp_link_id
        # Setup constraint
        self.prev_ee_orn = p.getQuaternionFromEuler([0, 0, 0])
        self.robot_uid = None
        self.end_effector_link_id = end_effector_link_id
        self.gripper_action = 1
        self.ll = self.ul = self.jr = self.rp = None
        self.ll_real = np.array(lower_joint_limits)
        self.ul_real = np.array(upper_joint_limits)
        self.mixed_ik = None
        self.euler_obs = euler_obs
        self.max_rel_pos = max_rel_pos
        self.max_rel_orn = max_rel_orn
        self.magic_scaling_factor_pos = magic_scaling_factor_pos
        self.magic_scaling_factor_orn = magic_scaling_factor_orn
        self.target_pos = None
        self.target_orn = None
        self.use_target_pose = use_target_pose
        # self.reconfigure = False

    def load(self):
        self.robot_uid = p.loadURDF(
            fileName=self.filename,
            basePosition=self.base_position,
            baseOrientation=self.base_orientation,
            useFixedBase=True,
            physicsClientId=self.cid,
        )
        self.add_base_cylinder()
        # create a constraint to keep the fingers centered
        c = p.createConstraint(
            self.robot_uid,
            self.gripper_joint_ids[0],
            self.robot_uid,
            self.gripper_joint_ids[1],
            jointType=p.JOINT_GEAR,
            jointAxis=[1, 0, 0],
            parentFramePosition=[0, 0, 0],
            childFramePosition=[0, 0, 0],
            physicsClientId=self.cid,
        )
        p.changeConstraint(c, gearRatio=-1, erp=0.1, maxForce=50, physicsClientId=self.cid)
        num_dof = p.computeDofCount(self.robot_uid)
        # lower limits for null space (todo: set them to proper range)
        self.ll = [-7] * num_dof
        # upper limits for null space (todo: set them to proper range)
        self.ul = [7] * num_dof
        # joint ranges for null space (todo: set them to proper range)
        self.jr = [7] * num_dof
        # restposes for null space
        self.rp = list(self.initial_joint_positions) + [self.gripper_joint_limits[1]] * 2
        self.reset()
        self.mixed_ik = MixedIK(
            self.robot_uid,
            self.cid,
            self.ll_real,
            self.ul_real,
            self.base_position,
            self.base_orientation,
            self.tcp_link_id,
            self.ll,
            self.ul,
            self.jr,
            self.rp,
            self.use_ik_fast,
            threshold_pos=0.03,
            threshold_orn=0.1,
            weights=(10, 8, 6, 6, 2, 2, 1),
            num_angles=30,
        )

    def add_base_cylinder(self):
        """
        TODO: this should happen in load(), but that would break compatibility with old recorded data
        """
        pos = self.base_position.copy()
        pos[2] /= 2
        angle = p.getEulerFromQuaternion(self.base_orientation)[2]
        pos[0] -= np.cos(angle) * 0.05
        pos[1] -= np.sin(angle) * 0.05
        cylinder = p.createVisualShape(
            shapeType=p.GEOM_CYLINDER,
            rgbaColor=[1, 1, 1, 1],
            radius=0.13,
            length=self.base_position[2],
            visualFramePosition=pos,
        )
        p.createMultiBody(baseVisualShapeIndex=cylinder)

    def reset(self, robot_state=None):
        if robot_state is None:
            gripper_state = self.gripper_joint_limits[1]
            joint_states = self.initial_joint_positions
        else:
            joint_indices = [i for i, x in enumerate(self.get_observation_labels()) if x.startswith("robot_joint")]
            joint_states = robot_state[joint_indices]
            gripper_state = robot_state[self.get_observation_labels().index("gripper_opening_width")] / 2

        assert len(joint_states) == len(self.arm_joint_ids)
        for i, _id in enumerate(self.arm_joint_ids):
            p.resetJointState(self.robot_uid, _id, joint_states[i], physicsClientId=self.cid)
            p.setJointMotorControl2(
                bodyIndex=self.robot_uid,
                jointIndex=_id,
                controlMode=p.POSITION_CONTROL,
                force=self.max_joint_force,
                targetPosition=joint_states[i],
                maxVelocity=self.max_velocity,
                physicsClientId=self.cid,
            )
        for i in self.gripper_joint_ids:
            p.resetJointState(self.robot_uid, i, gripper_state, physicsClientId=self.cid)
            p.setJointMotorControl2(
                bodyIndex=self.robot_uid,
                jointIndex=i,
                controlMode=p.POSITION_CONTROL,
                force=self.gripper_force,
                targetPosition=gripper_state,
                maxVelocity=1,
                physicsClientId=self.cid,
            )
        tcp_pos, tcp_orn = p.getLinkState(self.robot_uid, self.tcp_link_id, physicsClientId=self.cid)[:2]
        if self.euler_obs:
            tcp_orn = p.getEulerFromQuaternion(tcp_orn)
        self.target_pos = np.array(tcp_pos)
        self.target_orn = np.array(tcp_orn)

    def get_observation(self):
        """
        returns:
        - robot_state: ndarray (16,)
            - tcp_pos: robot_state[:3]
            - tcp_orn: robot_state[3:7] (quat) / [3:6] (euler)
            - gripper_opening_width: robot_state[7:8] (quat) / [6:7] (euler)
            - arm_joint_states: robot_state[8:15] (quat) / [7:14] (euler)
            - gripper_action: robot_state[15:] (quat) / [14:] (euler)
        - robot_info: Dict
        """
        tcp_pos, tcp_orn = p.getLinkState(self.robot_uid, self.tcp_link_id, physicsClientId=self.cid)[:2]
        if self.euler_obs:
            tcp_orn = p.getEulerFromQuaternion(tcp_orn)
        gripper_opening_width = (
            p.getJointState(self.robot_uid, self.gripper_joint_ids[0], physicsClientId=self.cid)[0]
            + p.getJointState(self.robot_uid, self.gripper_joint_ids[1], physicsClientId=self.cid)[0]
        )
        arm_joint_states = []
        for i in self.arm_joint_ids:
            arm_joint_states.append(p.getJointState(self.robot_uid, i, physicsClientId=self.cid)[0])
        robot_state = np.array([*tcp_pos, *tcp_orn, gripper_opening_width, *arm_joint_states, self.gripper_action])
        robot_info = {
            "tcp_pos": tcp_pos,
            "tcp_orn": tcp_orn,
            "gripper_opening_width": gripper_opening_width,
            "arm_joint_states": arm_joint_states,
            "gripper_action": self.gripper_action,
            "uid": self.robot_uid,
            "contacts": p.getContactPoints(bodyA=self.robot_uid, physicsClientId=self.cid),
        }
        return robot_state, robot_info

    def get_observation_labels(self):
        tcp_pos_labels = [f"tcp_pos_{ax}" for ax in ("x", "y", "z")]
        if self.euler_obs:
            tcp_orn_labels = [f"tcp_orn_{ax}" for ax in ("x", "y", "z")]
        else:
            tcp_orn_labels = [f"tcp_orn_{ax}" for ax in ("x", "y", "z", "w")]
        return [
            *tcp_pos_labels,
            *tcp_orn_labels,
            "gripper_opening_width",
            *[f"robot_joint_{i}" for i in self.arm_joint_ids],
            "gripper_action",
        ]

    def relative_to_absolute(self, action):
        assert len(action) == 7
        action = np.copy(action)
        rel_pos, rel_orn, gripper = np.split(action, [3, 6])
        rel_pos *= self.max_rel_pos * self.magic_scaling_factor_pos
        rel_orn *= self.max_rel_orn * self.magic_scaling_factor_orn
        if self.use_target_pose:
            self.target_pos += rel_pos
            self.target_orn += rel_orn
            return self.target_pos, self.target_orn, gripper
        else:
            tcp_pos, tcp_orn = p.getLinkState(self.robot_uid, self.tcp_link_id, physicsClientId=self.cid)[:2]
            tcp_orn = p.getEulerFromQuaternion(tcp_orn)
            abs_pos = np.array(tcp_pos) + rel_pos
            abs_orn = np.array(tcp_orn) + rel_orn
            return abs_pos, abs_orn, gripper

    def apply_action(self, action):
        jnt_ps = None
        if isinstance(action, dict):
            if action["type"] == "joint_rel":
                current_joint_states = np.array(list(zip(*p.getJointStates(self.robot_uid, self.arm_joint_ids)))[0])
                assert len(action["action"]) == 8
                rel_jnt_ps = action["action"][:7]
                jnt_ps = current_joint_states + rel_jnt_ps
                self.gripper_action = int(action["action"][-1])
            elif action["type"] == "joint_abs":
                assert len(action["action"]) == 8
                jnt_ps = action["action"][:7]
                self.gripper_action = int(action["action"][-1])
            elif action["type"] == "cartesian_rel":
                assert len(action["action"]) == 7
                target_ee_pos, target_ee_orn, self.gripper_action = self.relative_to_absolute(action["action"])
                if len(target_ee_orn) == 3:
                    target_ee_orn = p.getQuaternionFromEuler(target_ee_orn)
                jnt_ps = self.mixed_ik.get_ik(target_ee_pos, target_ee_orn)
            elif action["type"] == "cartesian_abs":
                if len(action["action"]) == 3:
                    # if action is a tuple
                    target_ee_pos, target_ee_orn, self.gripper_action = action["action"]
                elif len(action["action"]) == 7:
                    target_ee_pos = action["action"][:3]
                    target_ee_orn = action["action"][3:6]
                    self.gripper_action = int(action["action"][-1])
                elif len(action["action"]) == 8:
                    target_ee_pos = action["action"][:3]
                    target_ee_orn = action["action"][3:7]
                    self.gripper_action = int(action["action"][-1])
                else:
                    raise ValueError
                if len(target_ee_orn) == 3:
                    target_ee_orn = p.getQuaternionFromEuler(target_ee_orn)
                jnt_ps = self.mixed_ik.get_ik(target_ee_pos, target_ee_orn)
        else:
            if len(action) == 7:
                action = self.relative_to_absolute(action)
            target_ee_pos, target_ee_orn, self.gripper_action = action

            assert len(target_ee_pos) == 3
            assert len(target_ee_orn) in (3, 4)
            # automatically transform euler actions to quaternion
            if len(target_ee_orn) == 3:
                target_ee_orn = p.getQuaternionFromEuler(target_ee_orn)
            jnt_ps = self.mixed_ik.get_ik(target_ee_pos, target_ee_orn)

        if not isinstance(self.gripper_action, int) and len(self.gripper_action) == 1:
            self.gripper_action = self.gripper_action[0]
        assert self.gripper_action in (-1, 1)

        self.control_motors(jnt_ps)

    def control_motors(self, joint_positions):
        for i in range(self.end_effector_link_id):
            # p.resetJointState(self.robot_uid, i, jnt_ps[i])
            p.setJointMotorControl2(
                bodyIndex=self.robot_uid,
                jointIndex=i,
                controlMode=p.POSITION_CONTROL,
                force=self.max_joint_force,
                targetPosition=joint_positions[i],
                maxVelocity=self.max_velocity,
                physicsClientId=self.cid,
            )

        self.control_gripper(self.gripper_action)

    def control_gripper(self, gripper_action):
        if gripper_action == 1:
            gripper_finger_position = self.gripper_joint_limits[1]
            gripper_force = self.gripper_force / 100
        else:
            gripper_finger_position = self.gripper_joint_limits[0]
            gripper_force = self.gripper_force
        for id in self.gripper_joint_ids:
            p.setJointMotorControl2(
                bodyIndex=self.robot_uid,
                jointIndex=id,
                controlMode=p.POSITION_CONTROL,
                targetPosition=gripper_finger_position,
                force=gripper_force,
                maxVelocity=1,
                physicsClientId=self.cid,
            )

    def serialize(self):
        return {
            "uid": self.robot_uid,
            "info": p.getBodyInfo(self.robot_uid, physicsClientId=self.cid),
            "pose": p.getBasePositionAndOrientation(self.robot_uid, physicsClientId=self.cid),
            "joints": p.getJointStates(
                self.robot_uid,
                list(range(p.getNumJoints(self.robot_uid, physicsClientId=self.cid))),
                physicsClientId=self.cid,
            ),
            "gripper_action": self.gripper_action,
        }

    def reset_from_storage(self, data):
        p.resetBasePositionAndOrientation(
            bodyUniqueId=self.robot_uid, posObj=data["pose"][0], ornObj=data["pose"][1], physicsClientId=self.cid
        )
        num_joints = len(data["joints"])
        assert num_joints == p.getNumJoints(self.robot_uid, physicsClientId=self.cid)
        for i, (value, velocity, *_) in enumerate(data["joints"]):
            p.resetJointState(
                bodyUniqueId=self.robot_uid,
                jointIndex=i,
                targetValue=value,
                targetVelocity=velocity,
                physicsClientId=self.cid,
            )
            p.setJointMotorControl2(
                bodyIndex=self.robot_uid,
                jointIndex=i,
                controlMode=p.POSITION_CONTROL,
                force=self.max_joint_force,
                targetPosition=value,
                maxVelocity=self.max_velocity,
                physicsClientId=self.cid,
            )
        self.control_gripper(data["gripper_action"])

    def __str__(self):
        return f"{self.filename} : {self.__dict__}"

```


```
cd $flower_calvin_ROOT
conda create -n flower_cal python=3.9 -y
conda activate flower_cal
```

```
# Force install the binary version
pip install --upgrade --force-reinstall --no-cache-dir --only-binary :all: mujoco
```

```
cd ~/flower_vla_calvin/egl_probe

cat > egl_probe/CMakeLists.txt << 'EOF'
cmake_minimum_required(VERSION 3.10)
project(egl_probe)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Find packages
find_package(PythonInterp REQUIRED)
find_package(PythonLibs REQUIRED)
find_package(X11 REQUIRED)

include_directories(${PYTHON_INCLUDE_DIRS})
include_directories(.)
include_directories(glad)
include_directories(${X11_INCLUDE_DIR})

# Shared source files
set(COMMON_SOURCES
    "glad/egl.cpp"
    "glad/gl.cpp"
    "glad/glx_dyn.cpp"
)

# --- Target 1: query_devices ---
add_executable(query_devices "query_devices.cpp" ${COMMON_SOURCES})
target_link_libraries(query_devices ${PYTHON_LIBRARIES})
target_link_libraries(query_devices ${X11_LIBRARIES})
target_link_libraries(query_devices EGL GL dl)

# --- Target 2: test_device ---
add_executable(test_device "test_device.cpp" ${COMMON_SOURCES})
target_link_libraries(test_device ${PYTHON_LIBRARIES})
target_link_libraries(test_device ${X11_LIBRARIES})
target_link_libraries(test_device EGL GL dl)

# Output directory
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR})
EOF
```

```
rm -rf build dist egl_probe.egg-info egl_probe/build
python setup.py build
python setup.py install
```

```
cd $flower_calvin_ROOT/LIBERO
pip install -r requirements.txt
pip install -e .
```

```
# 1. Fix Numpy for FLOWER compatibility
pip install "numpy~=1.23"

# 2. Downgrade Setuptools (Required for PyHash/Gym)
pip install setuptools==57.5.0

# 3. Install PyHash
cd $flower_calvin_ROOT/pyhash-0.9.3
python setup.py build
python setup.py install
```

```
python -c "import egl_probe; print('SUCCESS: Found devices:', egl_probe.get_available_devices())"
```


---

calvin 문제가 계속 해결이 안돼서 일단 Libero로 선회.

- ~~홈에 `.mujoco` 설치함, 끝나고 삭제할 것~~. <- 삭제 완료

- 무조코 설치 문제 발생

- transformer 버전 문제 발생


VLA 작동에 성공했다!!

![alt text](image-1.png)

`run_inference.py`

### 필요 의존성

```
# 1. Create clean environment
conda create -n flower_cal python=3.9 -y
conda activate flower_cal

# 2. Install MuJoCo (Binary version to avoid build errors)
pip install --upgrade --force-reinstall --no-cache-dir --only-binary :all: mujoco
```

```
cd flower_vla_calvin/egl_probe
```

egl_probe/CMakeLists.txt을 다음 파일로 교체:
`to_workspace/dev_env_set/etc/CMakeLists.txt`

```
rm -rf build dist
python setup.py build
python setup.py install
```

위 의존성이 굉장히 많은 시간을 소비했음.

```
# 1. Install LIBERO (Simulation Env)
cd ../LIBERO
pip install -r requirements.txt
pip install -e .

# 2. Install FLOWER Dependencies (Main Repo)
cd ..
# Edit requirements.txt: Comment out 'mujoco' lines to protect our binary install
pip install -r requirements.txt

# 3. Install PyHash (Dependency)
cd pyhash-0.9.3
python setup.py build
python setup.py install
```

```
pip install transformers==4.42.4
```

해당 빌드 과정이 굉장히 오래걸림. 인내심을 가질것.
```
MAX_JOBS=3 pip install flash-attn --no-build-isolation
```


## 하지만 리베로10으로는 일반화 성능이 너무 떨어진다.

너무 작은 데이터셋에서 배워서 그런 듯?

그래소 일단 리베로90을 사용해보기로 했다.

`huggingface-cli download mbreuss/flower_libero_90 --local-dir checkpoints/flower_libero_90`

환경을 생각보다 많이탄다.

작동이 된다!!

하지만 일반화 성능이 생각보다 구리다.


Close the top drawer of the cabinet and pick up the chocolate box.

![alt text](interactive_Close_the_top_drawer.gif)

Pick up the chocolate bax and put it into th cabinet.

![alt text](run_pick_up_the_chocolat.gif)

Pick the chocolate box and put it on the bowl.

![alt text](run_Pick_the_chocolate_b.gif)

Close the top drawer and open the bottom drawer.

![alt text](run_Close_the_top_drawer.gif)



도커 컨테이너 실행.

docker run --rm -it \
  --device nvidia.com/gpu=0 \
  -v $(pwd)/checkpoints:/app/checkpoints \
  -v $(pwd)/interactive_logs:/app/interactive_logs \
  flower_vla:v2 /bin/bash

위 명령어로 checkpoint 폴더어와 interactive_logs도 VOLUME으로 마운트할 수 있다.

### 도커 이미지 안에 설치한 것들

pip install pytorch-lightning
pip install bddl
pip install easydict
pip install matplotlib
pip install moviepy imageio imageio-ffmpeg
pip install "numpy<2"
pip install einops-exts
pip install timm
pip install "transformers==4.42.4" "huggingface-hub>=0.23.0" accelerate

지금보니 리베로 의존성이 설치가 안됨. 도커파일에서 빠짐.

```
cd LIBERO
pip install -r requirements.txt  # <--- THIS IS THE MISSING KEY
pip install -e .
```

apt update
apt install nautilus -y
apt install tree -y


- [x] ~/.bashrc 색 변경
- [ ] run_robot.py 리팩토링, 실시간 출력 및 저장 방식 변경
    - [x] scene id가 총 몇개인지 체크
- [ ] 현재 상태 커밋 및 푸쉬
    - [ ] 테스트 시행
- [ ] 깃허브 업로드 
    - [ ] 현재 리포 정리
    - [ ] 리드미 새로 작성
    - [ ] 포크하고 업로드
- [ ] 개발 방식 정리 및 커밋


아래 처럼 scene id를 args으로 만들 수 있게 만듬. (0~89)

`python run_robot.py --scene_id 10`