# Regional X50 Ultra Complete compatibility fork

This fork is based on Tasshack/dreame-vacuum v2.0.2. Release `v2.0.2.post1`
adds `dreame.vacuum.r9446j` to the shared device registry using the existing
`r9446k` capability profile. The actual device model remains `r9446j`.
Every original model, capability definition and map key is preserved.
An upstream native `r9446j` definition takes precedence over this alias.

The regional profile is provisional. Discovery, runtime initialization,
status reporting and map rendering have been verified on one X50 Ultra
Complete with firmware `4.3.9_3684`. Short vacuum-only global and room tasks,
pause and return to dock were checked through Home Assistant state feedback.
These were brief command checks, not full cleaning-cycle validation. Dreame
cloud request timeouts occurred during the room test; docking succeeded after
recovery. Global cleaning controls became available with CleanGenius off, and
room controls became available with customized cleaning on. The original
settings were restored after testing.

One mopping-only room task completed on the same device after its clean-water
tank was refilled. Home Assistant reported the mop pads installed, Mopping,
4 m² covered in 5 minutes, automatic return to dock, Completed and Charging,
then the dock's post-cleaning Washing state. A water-level adjustment was
checked and restored. Post-test diagnostics confirm all changed preferences
match the baseline and the robot has no error or active cleaning task.
These observations verify reported operation; physical floor moisture has
not yet been confirmed by the owner, and long-term operation remains untested.
A cloud map-file download timed out during the wet-test window; the cleaning
task and automatic docking still completed. Cloud reliability remains a limit.

The robot's front-camera video has not been validated.
The integration's camera entities display maps, not the robot's video feed.
The maintainer's current streaming limitation is described in
[issue 656](https://github.com/Tasshack/dreame-vacuum/issues/656).
This is not an official Tasshack release.

## Installation and updates

Add `https://github.com/godely/dreame-vacuum` to HACS as an Integration custom
repository. Use the fork release, which includes `dreame_vacuum.zip`.
The integration domain remains `dreame_vacuum`; migrating repository
tracking must preserve the existing Home Assistant integration entry.
Do not install two copies of this component simultaneously.

Updates to this fork require deliberately merging and testing upstream
changes. Returning to official releases is appropriate once they include
native support for this model.

## Offline regression checks

Run `python3 -m unittest discover -s tests -v` with Python 3.12 or later.
The tests exercise the upstream discovery filter and real capability loader
without Home Assistant or cloud credentials. They also check unknown models,
existing definitions and preservation of future upstream model support.

Upstream model report: https://github.com/Tasshack/dreame-vacuum/issues/1671
