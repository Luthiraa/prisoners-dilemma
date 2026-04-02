# Prisoner's Dilemma Experiment Harness

The main simulator is [pd_experiment.py](/D:/prisoner's dilemma/pd_experiment.py).

It implements the strategy list in [strategies.md](/D:/prisoner's dilemma/strategies.md) in two forms:

- direct named strategies such as `tft`, `grim`, `wsls`, `gtft`, `grdtft`, `omegatft`
- parameterized family strategies such as `cp:0.7`, `r:1,1,0`, `s:1,0,1,0`, `zd:0.75,0.25,0.5,0.25`, `fsm:...`, `ann:...`, `lookerup:...`

Some entries in `strategies.md` are underspecified in the file itself, so the implementation uses executable defaults for those strategy families:

- `APavlov`
- `OmegaTFT`
- `GOOD`
- `LookerUp`
- `ANN`
- `FSM`
- `DA` uses `A` for abstain, scored as `0,0`

## Quick Runs

Single match:

```powershell
python .\pd_experiment.py --mode match --player-a tft --player-b grim --rounds 25
```

Tournament as JSON:

```powershell
python .\pd_experiment.py --mode tournament --rounds 100 --format json
```

Tournament as CSV for plotting:

```powershell
python .\pd_experiment.py --mode tournament --rounds 100 --format csv --output tournament.csv
```

Custom strategy set:

```powershell
python .\pd_experiment.py --mode tournament --strategies "cu,du,tft,gtft,grim,wsls,p5,r:1,1,0,s:1,0,1,0,set-2,extort-2,gen-2"
```

## Notes

- Default payoffs are the canonical `T=5, R=3, P=1, S=0`.
- Output is deterministic for a fixed seed.
- Tournament CSV output is row-based and easy to load into pandas, polars, R, or matplotlib workflows.
