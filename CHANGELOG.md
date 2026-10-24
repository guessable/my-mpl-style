# Changelog

All notable changes to this project are documented here. The format loosely
follows [Keep a Changelog](https://keepachangelog.com/) and the project uses
[Semantic Versioning](https://semver.org/).

## [0.3.2] - 2026-10-24

### Fixed

- Restored the outward tick direction that regressed in 0.3.1, while keeping
  support for both mplot3d hook variants: `_draw_ticks` (matplotlib < 3.11.2)
  and `_get_updated_ticks` (matplotlib >= 3.11.2).

## [0.3.1] - 2026-10-24

### Fixed

- `ax_setting3D()` now works with matplotlib 3.11.2, where the private
  `_draw_ticks` hook was replaced by `_get_updated_ticks`. Tick lengths and z
  labels are applied by wrapping the tick line and label `draw` methods, which
  works with both drawing implementations.

## [0.3.0] - 2026-10-24

### Added

- `ax_setting3D()` gains `box_on`, `ztick_length`, `xtick_length` and
  `ytick_length`. Tick marks are projected and scaled to the longest axis, and
  the z tick labels follow their tick endpoints.
- Input validation for limits, ticks, tick lengths and `box_aspect`.
- Private helpers moved to `my_mpl_style._utils`; `plot_rc` and
  `ax_setting3D` remain the only public functions.

### Changed

- **Breaking:** `ax_setting3D()` no longer draws the separate grey back-edge
  line; the box is drawn with pane outlines instead, controlled by `box_on`.
- Requires matplotlib 3.10+ (for the mplot3d draw hooks) and NumPy 1.24+.

## [0.2.2] - 2026-10-20

### Added

- Three new examples with rendered figures: `examples/Intersecting_planes.py`
  (orthogonal colour slices in one 3D box), `examples/isosurface.py`
  (marching-cubes isosurfaces of phase-field snapshots) and
  `examples/tri_surface.py` (colour-mapped and wireframe triangular meshes).
- `examples` optional dependency (`numpy`, `scikit-image`).

### Documentation

- README gains an "Example" gallery with all four figures, placed just before
  the license section.

## [0.2.1] - 2026-10-20

### Documentation

- README embeds the demo figure with an absolute URL, so it renders on both
  GitHub and PyPI; the license and changelog links are absolute too.
- `pyproject.toml` publishes the homepage, repository, issues and changelog
  URLs now that the project lives at
  <https://github.com/guessable/my-mpl-style>.

## [0.2.0] - 2026-10-20

### Added

- `plot_rc()` gains `save_dpi`, `save_bbox` and `save_pad_inches`, which preset
  the `savefig` defaults (300 dpi, tight bounding box, 0.05 in padding) so
  `fig.savefig("figure.png")` is print-ready without extra arguments.
- `plot_rc()` gains `font_family` and `font_serif` to choose the font stack.

### Changed

- **Breaking:** `ax_setting3D()` now requires `xticks`, `yticks` and `zticks`.
  Callers that set ticks with `ax.set(xticks=...)` must pass them to
  `ax_setting3D()` instead, so that limits, ticks and the grey back edge are
  computed from the same final axes state.
- Type hints tightened: `font_serif` is a `Sequence[str]` with an immutable
  tuple default, `save_bbox` is a `Literal["tight", "standard"]`, tick
  arguments accept any `Sequence[float]`, and `ax` is annotated as `Axes3D`.

## [0.1.0] - 2026-10-19

### Added

- First public release: `plot_rc()` and `ax_setting3D()`.
