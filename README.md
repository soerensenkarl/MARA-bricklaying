# MARA Bricklaying

Code and raw experimental data for **Towards Autonomous Bricklaying Using Boston Dynamics Spot**.

MARA, Mobile Agile Robotic Assembly, is a workflow for autonomous brick stacking with a Boston Dynamics Spot robot and arm. The system uses AprilTag fiducials for local pick/place reference frames, Spot Autowalk missions for navigation between the supply and assembly areas, and CAD-exported JSON target poses for execution.

## Repository Contents

- `src/` - Spot execution code and JSON target files used to make the 10 result runs in the paper.
- `data/placement_accuracy_still_frames/` - top-down layer still frames used for placement accuracy analysis.
- `cad/` - Rhino files containing the experimental source/wall brick positions, labeled screenshots, and the Grasshopper JSON exporter.
- `SPOT_RUN_GUIDE.md` - setup and run instructions for Spot.
- `RESULTS.md` - index of raw result files.

## Setup

Python 3.10 was used for the robot experiments. Install the runtime dependencies with:

```powershell
python -m pip install -r requirements.txt
```

Use the Boston Dynamics SDK package version that matches the Spot software release used in the lab. The pinned versions in `requirements.txt` document the environment used here, but Spot SDK compatibility should follow Boston Dynamics' release guidance.

This repository builds on the Boston Dynamics Spot SDK. For robot operation, SDK installation, API concepts, and examples, see:

- Spot SDK documentation: https://dev.bostondynamics.com/
- Spot SDK repository: https://github.com/boston-dynamics/spot-sdk
- Spot product and operating context: https://bostondynamics.com/products/spot/

## Running Spot

The Spot SDK examples use a robot hostname/IP as a command-line argument. `spot.local` is only a placeholder for a robot address that resolves on your lab network; use the robot hostname shown in Spot Admin or the robot's reachable IP address.

For credentials, use the SDK-standard environment variables or the SDK's interactive prompt. Do not put credentials in this repository.

```powershell
$env:BOSDYN_CLIENT_USERNAME = "<spot-username>"
$env:BOSDYN_CLIENT_PASSWORD = "<spot-password>"
```

Then run:

```powershell
cd src
python sequence.py <robot-hostname-or-ip>
```

See `SPOT_RUN_GUIDE.md` for safety checks and required local setup.

## Results

Placement-accuracy still frames are stored in `data/placement_accuracy_still_frames/`. The repository includes the recorded layer images; derived pose-error tables and CAD-rendered ground-truth overlays are not included.

## License

The repository is released under the MIT License, except `src/walk.py`, which is adapted from the [Boston Dynamics Spot SDK examples](https://github.com/boston-dynamics/spot-sdk) and remains subject to the [Boston Dynamics SDK License (BDSDK-SL)](https://github.com/boston-dynamics/spot-sdk/blob/master/LICENSE).

## Notes

- Credentials are not included. The runnable code uses `bosdyn.client.util.authenticate`, which supports existing tokens, `BOSDYN_CLIENT_USERNAME` / `BOSDYN_CLIENT_PASSWORD`, and interactive login.
- Site-specific Autowalk map binaries are not included because they can contain private environment and network metadata. Record local Autowalk missions named `to_wall.walk` and `to_source.walk` before running the active sequence.
- The Python virtual environment and vendored Boston Dynamics SDK checkout are not included.
