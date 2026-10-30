# Manufacturing30 4.0 — evidence and release scope

## Tested source

Source commit: `648ab945ef089629807fc47bf3848bc06c61e50f`.

Verification execution: https://github.com/poemcheng/cyut-machining-textbook/actions/runs/41104019445

The Node and BOTH browser suites completed successfully. The overall workflow subsequently failed at the repository write-back step because its GitHub App token could not modify a workflow file. This was a deployment-permission failure, not a passing whole-workflow status. Release publication therefore uses the authorized repository connector, and the ongoing verification workflow is changed to read-only testing without self-modifying workflow files.

## Observed results

- 123 Node tests passed; 0 failures.
- Thirty chapter WebGL scenes and their field profiles rendered; all had finite transforms and nonzero draw calls.
- Existing A/B experiment, quiz, reload persistence, invalid-input rejection, JSON export and teacher import passed.
- UR5e: 7 source links, 6 joints, 121,789 triangles, 27 render meshes.
- TM5-900: 7 source links, 6 joints, 209,670 triangles, 23 render meshes.
- Browser FK vs independently computed source-origin fixtures: maximum absolute position residual 4.45e-16 metres (numerical agreement only; not real-robot accuracy).
- Official model selection, joint input, home pose, concept/industrial view switching, field controls and rapid chapter switching passed.
- 390-pixel mobile viewport navigation and controls passed; this is not physical-device certification.
- Both browser reports contain 0 uncaught page errors and 0 failed resource requests.
- Browser suite timestamps: 2026-10-30 18:07:35–18:11:29 UTC.

Actual screenshots and raw JSON reports are in the run artifact `manufacturing30-realworld-v4` (artifact ID 12999724303, 30-day retention). Subsequent main-branch verification runs also produce a self-contained offline course ZIP with the three raw test reports.

## Model and field boundaries

There are 15 authored representative field layouts, 27 source-backed manufacturer/device cases, and TWO imported official robot visual models. These are different counts and must not be conflated.

The layouts are not surveyed real factories. Other manufacturer cases are references beside generic educational machinery, not claims that corresponding OEM CAD was imported. Robot meshes retain BSD-3-Clause licenses, pinned upstream revisions and SHA-256 provenance. Kinematics are nominal and uncalibrated to any physical serial number. No collision, dynamic, tooling or machine-safety certification is claimed. Chapter 29's planar two-link analytic exercise remains distinct from the six-axis robot visual/FK model.

The release removes an accidental runner-specific `node_modules` symlink and adds ignore rules. No browser application code differs from the tested source above.
