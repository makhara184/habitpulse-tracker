# HabitPulse Tracker

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Zero Dependencies](https://img.shields.io/badge/Dependencies-Stdlib%20Only-22c55e?style=flat-square)

A minimalist terminal habit tracker with streak calculation, 14-day ASCII heatmaps, and CSV export—written using Python's standard library only.

## Usage

```bash
python3 habitpulse.py log "Morning Walk"
python3 habitpulse.py status
python3 habitpulse.py export habits.csv
```

## Run Tests
```bash
python3 -m unittest discover -s tests
```

## License
MIT License — see [LICENSE](LICENSE).


## Studio Makhara browser app

Open the [installable browser app](./app/) for a portable companion to this project. Data stays in local browser storage; see [app/README.md](./app/README.md) for setup and limits.
