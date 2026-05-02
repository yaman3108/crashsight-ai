# Labelling Guide: PLANE_FOREST

## Class Description
Commercial or private aircraft crashed into forested terrain, visible from satellite as a clearing, burn scar, debris trail, or scattered wreckage among trees.

## What to Look For
- **Burn scars**: Dark patches in otherwise green forest canopy, often elongated in the direction of impact.
- **Clearings**: Unnatural gaps in dense forest that don't follow logging or road patterns.
- **Debris trails**: Linear patterns of disturbed vegetation extending 100-500m.
- **Wreckage**: Metallic reflections or unnatural shapes visible among trees.

## Bounding Box Guidelines
- Draw the bounding box tightly around the **entire visible impact area**, including any debris trail.
- If a burn scar extends beyond the main wreckage, include it.
- Do not include surrounding undisturbed forest.

## Hard Negatives (Things That Look Similar But Aren't)
- Natural forest clearings or meadows
- Logging roads and clear-cut areas
- Lightning-caused burn scars (typically smaller and more circular)
- Landslide scars
- Construction sites in rural areas

## Confidence Flags
- **HIGH**: Clear wreckage visible, obvious unnatural pattern in forest.
- **MEDIUM**: Suspicious clearing or scar, but no clearly visible wreckage.
- **LOW**: Could be a natural feature; needs second opinion.

## Example Sources for Known Sites
- Aviation Safety Network database entries with GPS coordinates
- Wikipedia articles on major aviation accidents with aerial photographs
- NTSB reports with crash location maps
