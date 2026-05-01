# sequence.py - final paper experiment sequence, with SDK-standard auth.
import argparse
import json
from pathlib import Path

import bosdyn.client
import bosdyn.client.util
import bosdyn.mission.client
from bosdyn.client.lease import LeaseClient, LeaseKeepAlive
from bosdyn.client.robot_command import RobotCommandClient, blocking_stand

import pick_brick as pick
import place_brick
import walk


SCRIPT_DIR = Path(__file__).resolve().parent


def parse_args():
    parser = argparse.ArgumentParser(description="Run the MARA Spot bricklaying sequence.")
    bosdyn.client.util.add_base_arguments(parser)
    parser.add_argument("--wall", default=str(SCRIPT_DIR / "wall.json"),
                        help="Path to wall target JSON. Rows are [x, y, z] or [x, y, z, yaw_deg].")
    parser.add_argument("--source", default=str(SCRIPT_DIR / "source.json"),
                        help="Path to source target JSON. Rows are [x, y, z] or [x, y, z, yaw_deg].")
    parser.add_argument("--to-wall", default="to_wall.walk",
                        help="Autowalk mission from the source area to the wall.")
    parser.add_argument("--to-source", default="to_source.walk",
                        help="Autowalk mission from the wall back to the source area.")
    return parser.parse_args()


def load_targets(path):
    with Path(path).open("r", encoding="utf-8") as f:
        rows = json.load(f)

    targets = []
    for row in rows:
        if len(row) == 3:
            x, y, z = map(float, row)
            yaw = 0.0
        else:
            x, y, z, yaw = float(row[0]), float(row[1]), float(row[2]), float(row[3])
        targets.append((x, y, z, yaw))
    return targets


def main():
    options = parse_args()
    bosdyn.client.util.setup_logging(options.verbose)

    brick_targets = load_targets(options.wall)
    source_targets = load_targets(options.source)

    sdk = bosdyn.client.create_standard_sdk(
        "MARA_Sequence",
        [bosdyn.mission.client.MissionClient],
    )

    robot = sdk.create_robot(options.hostname)
    bosdyn.client.util.authenticate(robot)
    robot.time_sync.wait_for_sync()

    assert not robot.is_estopped(), "Robot is E-Stopped. Configure external E-Stop first."
    assert robot.has_arm(), "This sequence expects a Spot with an arm."

    lease_client = robot.ensure_client(LeaseClient.default_service_name)
    with LeaseKeepAlive(lease_client, must_acquire=True, return_at_exit=True):
        print("Powering on.")
        robot.power_on(timeout_sec=20)
        assert robot.is_powered_on(), "Power on failed."

        cmd_client = robot.ensure_client(RobotCommandClient.default_service_name)
        print("Standing.")
        blocking_stand(cmd_client, timeout_sec=20)

        num_iterations = min(len(brick_targets), len(source_targets))
        print(f"Running {num_iterations} iterations.")

        for i in range(num_iterations):
            sx, sy, sz, syaw_deg = source_targets[i]
            x, y, z, yaw_deg = brick_targets[i]
            iteration = i + 1
            print(f"Sequence {iteration}/{num_iterations}")

            pick.run(robot, target=(sx, sy, sz), yaw_deg=syaw_deg)

            walk_ok = walk.play_named(robot, options.to_wall)
            assert walk_ok, f"Autowalk {options.to_wall} failed."

            place_brick.run(robot, target=(x, y, z), yaw_deg=yaw_deg)

            walk_ok = walk.play_named(robot, options.to_source)
            assert walk_ok, f"Autowalk {options.to_source} failed."

        print("All bricks complete. Powering off with safe sit.")
        robot.power_off(cut_immediately=False, timeout_sec=20)

    print("Lease returned. Done.")


if __name__ == "__main__":
    main()
