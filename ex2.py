"""
Sử dụng pandas để đọc và in ra thông tin những pokemon có "Speed" lớn hơn 80 và "Attack" lớn hơn 52 trong file pokemon.cvs. Sử dụng matplotlib vẽ một biểu đồ bất kì từ nội dung đã đọc được(show ra màn hình)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    input_path = "./Input/pokemon.csv"

    pokemon = pd.read_csv(input_path)
    print(pokemon.columns)

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
    ax = by_type.plot(x="Type", y=["Attack_Mean", "Defense_Mean"], kind="bar", title="Average of Attack and Defense", figsize=(12, 8))
    ax.legend(["Attack_Mean", "Defense_Mean"])

    plt.show()

