# 3DGradient Edit (Geode mod, GD 2.2081)

Build 3D shapes in the GD editor with gradient triggers. See `about.md` for what it does.

> **Before building:** open `mod.json` and change `yourname.3dgradient-edit` and `YourName`
> to your own name (keep the id lowercase, e.g. `kyle.3dgradient-edit`).

## Get the `.geode` file (no programming tools needed)

A `.geode` contains a compiled program, so it has to be built by a compiler. GitHub will do that for free:

1. Make a free account at github.com and create a **new repository** (Public is fine).
2. Upload everything in this folder to it (**Add file > Upload files**, drag the contents in).
   Make sure the hidden `.github` folder goes up too. On Windows turn on *View > Show > Hidden items* first.
   If it won't upload, use **Add file > Create new file**, name it `.github/workflows/build.yml`, and paste in the contents of that file.
3. Open the **Actions** tab. The *Build Geode Mod* workflow starts by itself (or press *Run workflow*). It takes about 10 minutes.
4. When it is green, open the run and download **Build Output** at the bottom. Unzip it: the `.geode` file is inside.
5. Put the `.geode` file in your Geometry Dash folder under `geode/mods/` and start the game.

The workflow builds Windows, macOS, Android32 and Android64 together into one `.geode`.
If you only play on one platform you can delete the other entries from the `matrix` in `.github/workflows/build.yml`.

## Build it yourself instead

Install the [Geode CLI](https://docs.geode-sdk.org/getting-started/geode-cli), then:

```
geode sdk install
geode sdk update 5.11.2
geode build
```

`mod.json` targets Geode **5.11.2**. The build refuses to run if your SDK's major.minor version differs.

## Using it

1. Open a level in the editor and press the cube button (by default next to Undo / Redo; you can change this in the mod's settings). On PC you can also press **F6**.
2. Pick a shape with the arrows. Drag the preview to turn it. Use **Spin** / **Reset** as needed.
3. The **Color** and **Shadow** swatches at the top pick which color you are editing. The ID next to each is the color channel the mod chose for it. Drag in the square, the hue bar or the sliders, or type a hex code.
   Tap a Recent / Saved swatch and press **use** to apply it; **add** stores the current color; **Save** / **Load** keep one snapshot of shape + colors.
4. Optional: select points in the list on the right to change their X / Y / Z, duplicate, add or remove them.
5. Press **Convert into gradient triggers**. The new objects are placed in the middle of your screen (and normally left selected),
   and a single Undo should remove them all.

## Render parts

The **Render parts** setting splits every face into parts x parts cells (1 to 512). 1 gives one gradient per face;
higher values let the shading change across each surface. Every cell is a gradient trigger and every corner a point
object with its own group ID, and GD has 9999 group IDs, so large grids can't be built. As a guide, a cube tops out
around 56 x 56 (about 19,000 objects). Above 128 x 128 the settings page warns that it may lag low end devices.

## Fonts

The UI text uses the Rubik font (SIL Open Font License). The ready-made bitmap fonts live in `fontfiles/` and are
copied into the mod by the `"files"` entry in `mod.json`. To change the fonts or their size, edit and run
`tools/make_fonts.py` (needs `pip install pillow fonttools`); the source `.ttf` files are in `tools/fonts/`.

## Tests

The geometry core (`src/core/Shape3D.hpp`) has no Geode dependency and is tested natively:

```
g++ -std=c++20 -O1 -Wall -Wextra tests/core_test.cpp -o core_test && ./core_test
```

## Layout

```
mod.json            mod info + settings
src/core/           shapes, hull, projection, shading, level-string generation (tested)
src/ui/             3D preview, custom picker widgets and the popup
src/main.cpp        editor button hook
resources/          UI sprites cut from your sprite sheets (plus the editor button)
fontfiles/          ready-made Rubik bitmap fonts
tools/              script that generates fontfiles/ (optional)
logo.png            your mod icon
```
