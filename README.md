# urdf-packager

A small util to turn a robot model into a single self-contained archive.

## Use

### Env setup

Create a ROS 2 ready environment:

```bash
lxc launch ubuntu:22.04 urdf-exporter --config=user.user-data="$(curl -L https://gist.githubusercontent.com/artivis/1fcfcc38f1cb8c087e27ebda5484f2ef/raw/ros-bare.cloud-init.yaml)"
```

Shell inside the environment as the `ubuntu` user:

```bash
lxc exec urdf-exporter --mode interactive -- /bin/sh -xac $@ubuntu - exec /bin/login -p -f
```

Create a workspace and clone the project:

```bash
mkdir -p ~/workspace/src
cd ~/workspace/src
git clone https://github.com/ros-navigation/nav2_minimal_turtlebot_simulation.git
```

Install the dependencies:

```bash
source /opt/ros/*/setup.bash
rosdep install --from-path . -y -i
```

```bash
apt install python3-pip
python3 -m pip install resolve_robotics_uri_py xacro
```

### Convert XACRO to SDF

```bash
xacro -o output.sdf path/to/input.sdf.xacro
```

```bash
xacro -o /tmp/gz_waffle.sdf ~/workspace/src/nav2_minimal_turtlebot_simulation/nav2_minimal_tb3_sim/urdf/gz_waffle.sdf.xacro
```

### Make it self-contained

```bash
python3 main.py path/to/output.sdf -p path/to/original/package/source
```

```bash
python3 main.py /tmp/gz_waffle.sdf -p ~/workspace/src/nav2_minimal_turtlebot_simulation
```

This creates the `model.tar.gz` archive in the `./` folder.
