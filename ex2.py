"""
Sử dụng pandas để đọc và in ra thông tin những pokemon có "Speed" lớn hơn 80 và "Attack" lớn hơn 52 trong file pokemon.cvs. Sử dụng matplotlib vẽ một biểu đồ bất kì từ nội dung đã đọc được(show ra màn hình)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import os
from ScientificPythonPackages import utils

if __name__ == '__main__':
    input_path = "./Input/pokemon.csv"
    output_dir = "./Ex2_Output"
    utils.mkdirs(output_dir)

    pokemon = pd.read_csv(input_path)
    print(pokemon.columns)
    print(pokemon.info())
    print(pokemon.head())
    print(pokemon[pokemon.Name.isnull()])

    selected_cols = ['#', 'Name', 'Type 1', 'Type 2', 'Speed', 'Attack']
    selected_pokemons = pokemon[(pokemon.Speed > 80) & (pokemon.Attack > 52)][selected_cols]

    print(selected_pokemons[selected_pokemons['Type 1'] == selected_pokemons['Type 2']])

    # Compute data to plot
    # Compute sum and size of attack and defense group by 'type 1' column
    by_type1 = pokemon.groupby('Type 1').agg({
        "Attack": ["sum", "size"],
        "Defense": ["sum", "size"]
    })
    by_type1 = by_type1.rename(
        columns={"Attack": "Attack 1", "Defense": "Defense 1"})

    # Compute sum and size of attack and defense group by 'type 2' column
    by_type2 = pokemon.groupby('Type 2').agg({
        "Attack": ["sum", "size"],
        "Defense": ["sum", "size"]
    })
    by_type2 = by_type2.rename(
        columns={"Attack": "Attack 2", "Defense": "Defense 2"})

    # Join 2 data frame
    by_type = pd.merge(by_type1, by_type2, left_index=True, right_index=True)

    # Compute mean of attack and defense
    by_type["Attack_Mean"] = (by_type["Attack 1", "sum"] + by_type["Attack 2", "sum"]) / (by_type["Attack 1", "size"] + by_type["Attack 2", "size"])
    by_type["Defense_Mean"] = (by_type["Defense 1", "sum"] + by_type["Defense 2", "sum"]) / (by_type["Defense 1", "size"] + by_type["Defense 2", "size"])

    by_type = by_type.reset_index()
    by_type = by_type.rename(columns={"Type 1": "Type"})

    print(by_type)

    # Plot data
    fig, axes = plt.subplots(nrows=1, ncols=2, sharey=True)

    by_type.plot(x="Type", y=["Attack_Mean"], kind="barh", title="Average Attack", figsize=(12, 8), ax=axes[0], color="orange")
    by_type.plot(x="Type", y=["Defense_Mean"], kind="barh", title="Average Defense", figsize=(12, 8), ax=axes[1], color="b")
    # axes[0][0].bar(by_type.Type, by_type.Attack_Mean)
    # axes[0][0].bar(by_type.Type, by_type.Defense_Mean)
    axes[0].legend("")
    axes[1].legend("")
    plt.savefig(os.path.join(output_dir, "Average_Attack_Defense.jpg"), dpi=100)

    # Plot heat map to compare relation of each couple pokemon
    pokemon_type_list = by_type.Type.tolist()
    # pokemon_type_list.append("Untype")
    print("List pokemon type : ", pokemon_type_list)
    num_pokemon_types = len(pokemon_type_list)

    map_type_index = {
        pokemon_type_list[idx]: idx for idx in range(len(pokemon_type_list))
    }

    heat_map = np.zeros((num_pokemon_types, num_pokemon_types), dtype=np.int32)

    # Loop through each row in pokemon data
    print("========")
    print(pokemon.head())
    for idx in pokemon.index:
        type1 = pokemon.loc[idx]["Type 1"]
        type2 = pokemon.loc[idx]["Type 2"]

        type1 = "Untype" if type(type1) is float and math.isnan(type1) else type1
        type2 = "Untype" if type(type2) is float and math.isnan(type2) else type2

        if type1 != "Untype" and type2 != "Untype":

            type1_idx = map_type_index.get(type1)
            type2_idx = map_type_index.get(type2)

            heat_map[type1_idx, type2_idx] += 1
            heat_map[type2_idx, type1_idx] += 1

        print("Type 1 : {}, Type 2 : {}".format(type1, type2))
        # break

    print("Heat map : ")
    print(heat_map)

    fig, ax = plt.subplots(figsize=(12, 8))
    im = ax.imshow(heat_map)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax)
    cbarlabel = "Number pokemons"
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    ax.set_xticks(np.arange(num_pokemon_types))
    ax.set_yticks(np.arange(num_pokemon_types))
    ax.set_xticklabels(pokemon_type_list)
    ax.set_yticklabels(pokemon_type_list)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(num_pokemon_types):
        for j in range(num_pokemon_types):
            text = ax.text(j, i, heat_map[i, j],  ha="center", va="center", color="w")

    ax.set_title("Compare pokemon type")
    fig.tight_layout()

    plt.savefig(os.path.join(output_dir, "Compare_Pokemon_Type.jpg"), dpi=100)
    plt.show()


    sel_pok = pokemon[
        ((pokemon["Type 1"] == "Water") & (pokemon["Type 2"] == "Fire")) |
        ((pokemon["Type 1"] == "Fire") & (pokemon["Type 2"] == "Water"))
    ]

    print(sel_pok)
