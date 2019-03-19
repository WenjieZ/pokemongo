import numpy as np
import pandas as pd
from utils import equilibrium


species = pd.read_excel('UW PokéDex GO.xlsx', sheet_name='0.0.1 Pokémon Dex Data', header=1, nrows=453, index_col='Shorthand' 
                       , skiprows=[163], usecols=[4, 9, 16, 17, 19, 20, 21], names=['Final', 'Type1','Type2','Atk','Def','Sta'])
species = species.rename(index={'Shorthand': 'Name'})
species = species.fillna('Empty')
species.Atk += 15
species.Def += 15
species.Sta += 15

species_moves = pd.read_excel('UW PokéDex GO.xlsx', sheet_name='0.1.1 Pokémon GO Moves', header=1, nrows=392
                             , skiprows=[133], usecols=[1, 2, 3, 4, 5, 6])

moves = pd.read_excel('UW PokéDex GO.xlsx', sheet_name='0.1.2 Attack Dex (GO)', header=0, usecols=[0, 1, 2, 4, 5, 7]
                     , index_col='Move', names=['Type', 'Fast', 'Power', 'Energy', 'Duration'])
moves.Duration /= 1000

effi = pd.read_excel('UW PokéDex GO.xlsx', sheet_name='0.3.1 Type Table', header=0
                     , usecols=[0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]).T
effi **= np.log(1.6) / np.log(1.4)


pokemon = pd.read_csv("stats.csv", sep='\t', nrows=0)

for i in range(len(species_moves)):
    if species.loc[species_moves.Pokémon[i], "Final"]:
        for j in range(1, 3):
            if pd.notna(species_moves.iloc[i, j]):
                for k in range(3, 6):
                    if pd.notna(species_moves.iloc[i, k]):
                        pokemon = pokemon.append(species.loc[species_moves.Pokémon[i]])
                        pokemon.ix[-1, 'Name'] = pokemon.index[-1]
                        pokemon.ix[-1, 'Fast'] = species_moves.iloc[i, j]
                        pokemon.ix[-1, 'Charge'] = species_moves.iloc[i, k]
                        pokemon.ix[-1, 'Type_F'] = moves.loc[pokemon.iloc[-1].Fast].Type
                        pokemon.ix[-1, 'Type_C'] = moves.loc[pokemon.iloc[-1].Charge].Type
                        pokemon.ix[-1, 'Power1'] = moves.loc[pokemon.iloc[-1].Fast].Power
                        pokemon.ix[-1, 'Energy1'] = moves.loc[pokemon.iloc[-1].Fast].Energy
                        pokemon.ix[-1, 'Time1'] = moves.loc[pokemon.iloc[-1].Fast].Duration
                        pokemon.ix[-1, 'Stab1'] = 1.2 if pokemon.iloc[-1].Type_F in (pokemon.iloc[-1].Type1, pokemon.iloc[-1].Type2) else 1
                        pokemon.ix[-1, 'Power2'] = moves.loc[pokemon.iloc[-1].Charge].Power
                        pokemon.ix[-1, 'Energy2'] = moves.loc[pokemon.iloc[-1].Charge].Energy
                        pokemon.ix[-1, 'Time2'] = moves.loc[pokemon.iloc[-1].Charge].Duration
                        pokemon.ix[-1, 'Stab2'] = 1.2 if pokemon.iloc[-1].Type_C in (pokemon.iloc[-1].Type1, pokemon.iloc[-1].Type2) else 1

n = len(pokemon)                    

n = len(pokemon)                    
payoff = np.zeros((n, n))

for i in range(n):
    for j in range(n):
        attacker, defender = pokemon.iloc[i], pokemon.iloc[j]
        attacker_power = attacker.Atk * attacker.Def * attacker.Sta
        defender_power = defender.Atk * defender.Def * defender.Sta * 2

        fast_damage = attacker.Power1 * attacker.Stab1 * effi.loc[attacker.Type_F, defender.Type1] * effi.loc[attacker.Type_F, defender.Type2]
        charge_damage= attacker.Power2 * attacker.Stab2 * effi.loc[attacker.Type_C, defender.Type1] * effi.loc[attacker.Type_C, defender.Type2]
        weight = attacker.Energy1 / attacker.Energy2
        attacker_dps = (fast_damage + weight * charge_damage) / (attacker.Time1 + weight * attacker.Time2)
        attacker_dps = max(attacker_dps, fast_damage / attacker.Time1)
                
        fast_damage = defender.Power1 * defender.Stab1 * effi.loc[defender.Type_F, attacker.Type1] * effi.loc[defender.Type_F, attacker.Type2]
        charge_damage= defender.Power2 * defender.Stab2 * effi.loc[defender.Type_C, attacker.Type1] * effi.loc[defender.Type_C, attacker.Type2]
        weight = defender.Energy1 / defender.Energy2
        defender_dps = (fast_damage + weight * charge_damage) / (defender.Time1 + 2 + weight * (defender.Time2 + 2))
        
        payoff[i, j] = np.log(attacker_power * attacker_dps / defender_power / defender_dps)


p, q = equilibrium(payoff, 10000)
p[abs(p)<0.01] = 0
q[abs(q)<0.01] = 0

dfp = pokemon.iloc[p.nonzero()].copy()
dfp['Weight'] = p[p.nonzero()]
dfq = pokemon.iloc[q.nonzero()].copy()
dfq['Weight'] = q[q.nonzero()]

with open('metalist.csv', 'w') as f:
    f.write('--------Attack List---------\n')
    f.write(dfp.to_csv())
    f.write('--------Defend List---------\n')
    f.write(dfq.to_csv())
