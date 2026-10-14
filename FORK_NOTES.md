# Regional X50 Ultra Complete compatibility fork

This fork is based on Tasshack/dreame-vacuum v2.0.2. Release `v2.0.2.post1`
adds `dreame.vacuum.r9446j` to the shared device registry using the existing
`r9446k` capability profile. The actual device model remains `r9446j`.
Every original model, capability definition and map key is preserved.
An upstream native `r9446j` definition takes precedence over this alias.

The regional profile is provisional. Discovery, runtime initialization,
status reporting and map rendering have been verified on one X50 Ultra
Complete with firmware `4.3.9_3684`. Cleaning and video features require
separate validation. This is not an official Tasshack release.

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
