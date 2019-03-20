# Pokemon GO
Using Nash Equlibrium to build minimal PvE lists for Pokémon GO.

This repo uses the Nash Equilibrium to build a minimalist PvE list for Pokémon GO: With few Pokémon, you are able to seize all gyms and defend against all gym invaders. 
This practice allows you to concentrate your resources on few Pokémon and build an all-round strong team.

## Dependencies
This repo is Python 3 and depends on the following package:
- numpy
- pandas <=v0.23 (v0.24 won't work)
- xlrd

## Usage
```shell
$ python pokemongo.py
```

The results is stored in the `metalist.txt` file by default.

A Jupyter notebook with the same name is provided as the demo.

## Branches
- **master**: timeout as win condition in gym battles
- **raid**: boss raid

## Acknowledgement
The dataset is contributed by Reddit user [UW_Unknown_Warrior](https://www.reddit.com/user/UW_Unknown_Warrior).

Also thanks to [Vince Knight](https://github.com/drvinceknight) for helpful discussion.
