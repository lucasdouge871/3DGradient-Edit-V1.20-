# 3DGradient Edit Changelog

## v1.2.0

- New setting **Render parts** (1 to 512): splits every face of the shape into parts x parts cells, so shading can change across a surface instead of being one blend per face. Each part becomes a gradient trigger. The live preview draws up to 16 x 16.
- Setting it above 128 x 128 shows a warning: "this may lag some low end devices".
- Every point needs its own group ID and GD only has 9999, so a shape can only be converted up to a certain size (about 56 x 56 for a cube). If the chosen value is too big, Convert explains why and tells you the largest value that fits. Nothing is created in that case.

## v1.1.1

- Fixed the build failing at the packaging step. The Rubik fonts are now generated ahead of time and shipped in `fontfiles/`, instead of being converted during the build.
- The red handles now change color to match the part of the picker they sit on: the saturation square shows the chosen color, the hue bar shows the hue, and the Opacity / Red / Green / Blue sliders show the color under them.

## v1.1.0

- Fixed the editor button growing far too large when pressed.
- New look: your UI art is used throughout (window frame, panels, buttons, icons) and all text is set in Rubik.
- New custom color picker: saturation/brightness square, hue bar, and Opacity / Red / Green / Blue sliders, all with the red-circle handle.
- Pick up colors from the Recent / Saved swatches and apply them with **use**; **add** stores the current color in Saved.
- **Save** / **Load** keep one snapshot of your shape and both colors.

## v1.0.1

- The editor button is now placed next to the editor's own Undo / Redo buttons by default, so it can't end up hidden in a corner.
- New backup way in: press **F6** in the editor (PC).
- Only one 3DGradient Edit window can be open at a time.

## v1.0.0

- First release.
