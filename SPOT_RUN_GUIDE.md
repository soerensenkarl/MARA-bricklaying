# Spot Run Guide

## Requirements

- Boston Dynamics Spot with arm.
- External E-Stop configured and tested.
- AprilTag fiducials visible at the supply and assembly areas.
- Valid local Autowalk maps for the current physical setup.
- Python dependencies from `requirements.txt`.

Spot operation and SDK usage are documented by Boston Dynamics:

- Spot SDK documentation: https://dev.bostondynamics.com/
- Spot SDK repository: https://github.com/boston-dynamics/spot-sdk

## Robot Address And Credentials

`spot.local` is a placeholder, not a required value. Use a hostname or IP address that resolves from the computer running the script, for example the robot hostname shown in Spot Admin or the robot's reachable IP address on the lab network.

The runnable code follows the Boston Dynamics SDK authentication helper, `bosdyn.client.util.authenticate(robot)`. That helper tries, in order:

- an existing robot auth token,
- `BOSDYN_CLIENT_USERNAME` and `BOSDYN_CLIENT_PASSWORD`,
- an interactive username/password prompt.

For non-interactive use, set the SDK-standard environment variables:

```powershell
$env:BOSDYN_CLIENT_USERNAME = "<spot-username>"
$env:BOSDYN_CLIENT_PASSWORD = "<spot-password>"
```

Do not commit credential files, passwords, robot tokens, or `.env` files.

## Run

```powershell
cd src
python sequence.py <robot-hostname-or-ip>
```

You can override the local run inputs if needed:

```powershell
python sequence.py <robot-hostname-or-ip> --wall wall.json --source source.json --to-wall to_wall.walk --to-source to_source.walk
```

The active source expects these files/folders next to `sequence.py`:

- `wall.json` - target brick positions.
- `source.json` - brick pickup positions.
- `to_wall.walk` - locally recorded Autowalk mission from supply area to assembly area.
- `to_source.walk` - locally recorded Autowalk mission from assembly area back to supply area.
- `pick_brick.py`, `place_brick.py`, `walk.py` - manipulation and navigation modules.

`src/` contains the code and JSON target files used to make the 10 result runs in the paper.
