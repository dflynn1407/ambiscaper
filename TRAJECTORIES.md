# Moving Sound Sources in AmbiScaper

AmbiScaper supports dynamic, moving sound sources. You can define how a sound moves over its duration by replacing static `('const', value)` distributions with `('trajectory', ...)` distributions for the `event_azimuth` and `event_elevation` parameters in `AmbiScaper.add_event()`.

AmbiScaper processes azimuth and elevation trajectories **jointly in 3D Cartesian space**. This guarantees that interpolations always follow the **shortest great-circle path** along the unit sphere and naturally avoids wrap-around issues (e.g., smoothly panning directly from 350° to 10° across the 0° mark, rather than sweeping backwards across the entire sphere).

There are three ways to define a trajectory:

## 1. Linear Trajectories
A linear trajectory provides a smooth, shortest-path transition between a start angle and an end angle over the duration of the event.

**Syntax:** `('trajectory', 'linear', start_angle_rad, end_angle_rad)`

**Example:**
```python
import numpy as np

# Pan from 350 degrees to 10 degrees (crossing the 0-degree mark seamlessly)
start_az = 350 * np.pi / 180
end_az = 10 * np.pi / 180

asc.add_event(
    source_file=('const', 'speech.flac'),
    event_time=('const', 0.0),
    event_duration=('const', 3.0),
    event_azimuth=('trajectory', 'linear', start_az, end_az),
    event_elevation=('const', 0.0) # Elevation remains static
    # ... other parameters ...
)
```

## 2. Waypoints Trajectories
A waypoints trajectory allows you to specify a list of angles. AmbiScaper will smoothly interpolate between these points, distributing them evenly across the event's duration. 

**Syntax:** `('trajectory', 'waypoints', [angle1, angle2, angle3, ...])`

**Example:**
```python
# Move the sound up from below, to the horizon, and then above
asc.add_event(
    source_file=('const', 'drone.flac'),
    event_time=('const', 0.0),
    event_duration=('const', 5.0),
    event_azimuth=('const', np.pi / 2), # Static on the Y-axis
    event_elevation=('trajectory', 'waypoints', [-np.pi/4, 0.0, np.pi/4])
    # ... other parameters ...
)
```

## 3. Custom Function Trajectories
For complete control, you can pass a custom Python function. AmbiScaper will pass a NumPy array of time values `t` (in seconds, ranging from `0` to `event_duration`) to your function. Your function must return a NumPy array of angles of the same shape.

**Syntax:** `('trajectory', 'custom', my_function)`

**Example:**
```python
def spiral_azimuth(t):
    # Rotate one full circle (2*pi) every second
    return 2 * np.pi * t

asc.add_event(
    source_file=('const', 'flute.flac'),
    event_time=('const', 0.0),
    event_duration=('const', 4.0),
    event_azimuth=('trajectory', 'custom', spiral_azimuth),
    event_elevation=('trajectory', 'linear', 0, np.pi/2) # Spiraling upwards
    # ... other parameters ...
)
```

## JAMS Annotations
When generating the JAMS annotation file (`.jams`), AmbiScaper will automatically record the trajectory types. For custom functions, it will safely serialize the function's name (e.g., `"spiral_azimuth"`) to maintain valid JSON output.
