# urdf-packager

A small util to turn a robot model into a single self-contained archive.

## Use

### Env setup

Create a workspace and clone the project containing the robot model,

```bash
mkdir -p ~/workspace/src
cd ~/workspace/src
git clone https://github.com/ros-navigation/nav2_minimal_turtlebot_simulation.git
```

Install the dependencies,

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
