# Manufacturing30 2.0 — deployment and verification record

Published course: https://poemcheng.github.io/cyut-machining-textbook/manufacturing30/

## Reproducible evidence

- Authored source commit: `cd29b865573b8c3ff52aa82e6081aa04fb6ca818`.
- Tested vendored runtime and generated model register: `891f0a77435f84f5fe497d22132f0a8e313824e0`.
- Verification run: https://github.com/poemcheng/cyut-machining-textbook/actions/runs/41064545644
- Browser execution: 2026-10-30 13:38:32–13:39:22 UTC (21:38:32–21:39:22 Asia/Taipei).
- Node model/content checks: 110 passed, 0 failed.
- Thirty chapter WebGL scenes rendered successfully; each had three numeric outputs, positive draw-call counts, and no non-finite object transforms.
- Passed: wireframe and clipping controls, A/B laboratory comparison, formative quiz, persistence after reload, invalid-input rejection, JSON export, teacher JSON import, and 390-pixel mobile viewport navigation.
- Browser report: 0 uncaught page errors and 0 failed resource requests.
- Desktop and mobile screenshots plus thirty scene screenshots are available in the run's `manufacturing30-verification` artifact, together with the self-contained course ZIP. GitHub artifact retention is 30 days.

Environment: GitHub Actions Ubuntu, Node.js 22, Playwright 1.56.1 Chromium, Three.js 0.164.1. Headless rendering uses WebGL with software-rendering support; this is not a benchmark of any physical GPU. Mobile verification refers to viewport/layout and interaction checks, not an actual iOS or Android device certification.

## Scope

This release provides one representative interactive laboratory and its complete learning workflow for each of the thirty public textbook chapter headings. Original explanatory text, 30 analytic models, 30 independently constructed scenes, 60 concept questions, and 30 parameterized numeric question slots are included. It does not reproduce the textbook or claim to cover every subsection, machine, or exercise.

All runtime dependencies are vendored under this subdirectory. No CDN is required to run the published release or the offline package. Local execution still requires an HTTP static server rather than file:// navigation.

Software verification does not establish experimentally calibrated material behavior, CAE fidelity, actual machine safety, or educational effectiveness. Chapter-specific assumptions and validity limits remain part of the course.

The pre-existing lathe/milling textbook homepage and files are preserved. This publication adds the independent `docs/manufacturing30/` subtree.
