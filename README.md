# Utilities to download SPOT 6-7 data from dataterra

https://openspot-dinamis.data-terra.org/

## Usage

Update the configs in `src/spotdw/config/` and run

```bash
python src/spotdw/download.py
```

```bash
python src/spotdw/pansharpen.py
```

or adapt the slurm scripts in the `scripts`directory.