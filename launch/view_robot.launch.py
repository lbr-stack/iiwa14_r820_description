from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import (
    Command,
    FindExecutable,
    LaunchConfiguration,
    PathSubstitution,
)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                name="robot_name",
                default_value="lbr",
                description="The robot's name. Links in the tf tree will be prefixed as <robot_name>_link. Same applies to joints.",
            ),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                name="robot_state_publisher",
                output="screen",
                parameters=[
                    {
                        "robot_description": Command(
                            [
                                FindExecutable(name="xacro"),
                                " ",
                                PathSubstitution(FindPackageShare("iiwa14_description"))
                                / "urdf"
                                / "iiwa14.urdf.xacro",
                                " robot_name:=",
                                LaunchConfiguration("robot_name"),
                            ]
                        )
                    },
                ],
            ),
            Node(
                package="joint_state_publisher_gui",
                executable="joint_state_publisher_gui",
                name="joint_state_publisher_gui",
                output="screen",
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                output="screen",
                arguments=[
                    [
                        "-d",
                        PathSubstitution(FindPackageShare("iiwa14_description"))
                        / "rviz"
                        / "view_robot.rviz",
                    ]
                ],
            ),
        ]
    )
