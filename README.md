# DC Bus

Single-phase 230 V AC, 50 Hz input rectified to a 320 V DC bus.

## Features

- 230 V AC / 50 Hz single-phase input
- 320 V DC bus
- Bulk capacitors rated for 5 A current ripple with less than 20 V ripple at 50 Hz
- Precharge circuit to limit inrush current
- Bleeder resistor to discharge the bulk capacitors in under 5 minutes after power-off

## Board

![DC Bus PCB](output/board.png)

## Schematic

![DC Bus schematic](output/schematic.png)

The generated PDF is available at [output/schematic.pdf](output/schematic.pdf).

## Project Files

- `DCBus.kicad_pro` - KiCad project
- `DCBus.kicad_sch` - schematic
- `DCBus.kicad_pcb` - PCB layout
- `output/` - generated board/schematic images, schematic PDF, and check reports
- `output/erc.json`, `output/drc.json` - ERC and DRC reports
- `bom/ibom.html` - interactive bill of materials

## Design Checks

Reports: [ERC JSON](output/erc.json) and [DRC JSON](output/drc.json).

## Generation

Board render:

```sh
kicad-cli pcb render --output output/board.png --rotate '-45,0,135' --width 1920 --height 1080 DCBus.kicad_pcb
```

Schematic PDF:

```sh
kicad-cli sch export pdf -o output/schematic.pdf DCBus.kicad_sch
```

Gerbers and drill files:

```sh
mkdir -p build/gerbers
kicad-cli pcb export gerbers --layers F.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts -o build/gerbers DCBus.kicad_pcb
kicad-cli pcb export drill --generate-report --report-path build/gerbers/DCBus-drill.rpt -o build/gerbers DCBus.kicad_pcb
cd build/gerbers && python3 -m zipfile -c ../DCBus-gerbers.zip *
```

Design checks:

```sh
kicad-cli sch erc --format json --severity-all -o output/erc.json DCBus.kicad_sch
kicad-cli pcb drc --format json --severity-all -o output/drc.json DCBus.kicad_pcb
```
