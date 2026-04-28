# 🖥️ monitor-geometry-calculator (ASCII)

**Monitor Geometry Visualizer** makes a small ASCII drawing, which represents your current monitor settings. Below the drawing you can find a table with **DEVICE ID**, **WIDTH**, **HEIGHT**, **OFFSETS**, **RESOLUTION** and **ORIENT**.

### ✨ How to use it?

1. `git clone https://github.com/norwagov/monitor-geometry-calculator/`
2. `cd monitor-geometry-calculator`
3. `python monitor-geometry-calculator.py`

### 🎨 Example output

```
===========================================  ASCII MONITOR GEOMETRY VIEWER  ============================================


    ╔[2]═════════════════════╗╔[1]══════════════════════════════╗
    ║                        ║║                                 ║
    ║                        ║║                                 ║
    ║                        ║║                                 ║
    ║  \\.\DISPLAY15         ║║                                 ║
    ║1920 x 1080             ║║                                 ║
    ║x=-1920,  y=0           ║║                                 ║
    ║Landscape               ║║* \\.\DISPLAY1                   ║╔[4]══════════════════╗
    ║                        ║║2560 x 1440                      ║║                     ║
    ║                        ║║x=0,  y=0                        ║║                     ║
    ║                        ║║Landscape                        ║║  \\.\DISPLAY2       ║
    ║                        ║║                                 ║║1600 x 900           ║
    ║                        ║║                                 ║║x=2560,  y=534       ║
    ╚════════════════════════╝║                                 ║║Landscape            ║
                              ║                                 ║║                     ║
                   ╔[3]══════╗║                                 ║║                     ║
                   ║  \\.\DI ║║                                 ║║                     ║
                   ║800 x 60 ║║                                 ║║                     ║
                   ║x=-800,  ║╚═════════════════════════════════╝╚═════════════════════╝
                   ║Landscap ║
                   ║         ║
                   ║         ║
                   ╚═════════╝







  +-----+--------------------------+---------+---------+----------+----------+-------------+-----------+------------+
  | #   | Device                   | Width   | Height  | X        | Y        | Resolution  | Aspect    | Orient.    |
  +-----+--------------------------+---------+---------+----------+----------+-------------+-----------+------------+
  | 1   | *\\.\DISPLAY1            | 2560    | 1440    | 0        | 0        | 2560x1440   | 16:9      | Landscape  |
  | 2   | \\.\DISPLAY15            | 1920    | 1080    | -1920    | 0        | 1920x1080   | 16:9      | Landscape  |
  | 3   | \\.\DISPLAY16            | 800     | 600     | -800     | 1093     | 800x600     | 4:3       | Landscape  |
  | 4   | \\.\DISPLAY2             | 1600    | 900     | 2560     | 534      | 1600x900    | 16:9      | Landscape  |
  +-----+--------------------------+---------+---------+----------+----------+-------------+-----------+------------+

  Monitors found   : 4
  Primary          : \\.\DISPLAY1
  Desktop span     : 6080 x 1693 px
  Total pixel area : 7,680,000 px^2
  Portrait screens : 0
```
