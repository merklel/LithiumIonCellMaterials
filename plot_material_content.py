
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import locale

USEPGF = 1
fontsize=11

locale.setlocale(locale.LC_ALL, "de_DE.utf8")
if USEPGF:
    import matplotlib
    matplotlib.use("pgf")
    matplotlib.rcParams.update({
        "pgf.texsystem": "pdflatex",
        'font.family': 'serif',
        'text.usetex': True,
        'pgf.rcfonts': False,
        'axes.formatter.use_locale': True,
        "pgf.preamble": [
             "\\usepackage{siunitx}",          # load additional packages
             ]
    })




def plot_materials(gc, inactive_masses, mass_ahg, masses_density, total_mass_ah_g, total_mass_density, total_mass, cell_count):


    print(0)



    ################ Plot Density Method ######################

    mp_density = pd.DataFrame(
        {
            "Al": inactive_masses['mAl_collector'] + masses_density["mAl"],
            "Cu": inactive_masses['mCu_collector'],
            "Separator": inactive_masses['mSep'],
            "Stahl": inactive_masses['mCasing'] + inactive_masses["mass_terminals"],
            "Li": masses_density["mLi"],
            "Ni": masses_density["mNi"],
            "Mn": masses_density["mMn"],
            "Co": masses_density["mCo"],
            "Fe": masses_density["mFe"],
            "P": masses_density["mP"],
            "Elektrolyt": total_mass_density['mass_electrolyte'],
        },index=[0]
    )

    mp_ah = pd.DataFrame(
        {
            "Al": inactive_masses['mAl_collector'] + mass_ahg["mAl"],
            "Cu": inactive_masses['mCu_collector'],
            "Separator": inactive_masses['mSep'],
            "Stahl": inactive_masses['mCasing'] + inactive_masses["mass_terminals"],
            "Li": mass_ahg["mLi"],
            "Ni": mass_ahg["mNi"],
            "Mn": mass_ahg["mMn"],
            "Co": mass_ahg["mCo"],
            "Fe": mass_ahg["mFe"],
            "P": mass_ahg["mP"],
            "Elektrolyt": total_mass_ah_g['mass_electrolyte'],
        }, index=[0]
    )


    tum_colors = sns.color_palette([
        "#0065BD",
        "#000000",
        "#003359",
        "#005293",
        "#333333",
        "#7F7F7F",
        "#64A0C8",
        "#98C6EA",
        # "#DAD7CB",
        "#E37222",
        "#A2AD00"]*2)


    # del zeros
    mp_density = mp_density.replace(0, np.nan)
    mp_density = mp_density.dropna(axis=1)
    mp_ah = mp_ah.replace(0, np.nan)
    mp_ah = mp_ah.dropna(axis=1)


    ################### 2 Methods Plot ######################################
    f, axs = plt.subplots(1, 2, figsize=(6.3, 4), sharey=True)
    sns.barplot(data=mp_density, ax=axs[0], palette=tum_colors)
    sns.barplot(data=mp_ah, ax=axs[1], palette=tum_colors)

    axs[0].set_title("Dichte-basierte Methode", fontsize=fontsize)
    axs[1].set_title("Kapazitäts-basierte Methode", fontsize=fontsize)

    axs[0].set_ylabel("Gewicht in g")

    axs[0].set_xticklabels(axs[0].get_xticklabels(), rotation = -25, ha="left")
    axs[1].set_xticklabels(axs[1].get_xticklabels(), rotation = -25, ha="left")

    f.savefig("plots/results/masses_cell.png", bbox_inches="tight")
    f.savefig("plots/results/masses_cell.pgf", bbox_inches="tight")


    ################### density and scale up to vehicle #####################
    f, axs = plt.subplots(1, 2, figsize=(6.3, 4), sharey=False)
    sns.barplot(data=mp_density, ax=axs[0], palette=tum_colors)
    sns.barplot(data=(mp_density*264/1000), ax=axs[1], palette=tum_colors)

    axs[0].set_title("Dichte-basierte Methode Zelllevel", fontsize=fontsize)
    axs[1].set_title("Dichte-basierte Methode Packebene", fontsize=fontsize)

    axs[0].set_ylabel("Gewicht in g")
    axs[1].set_ylabel("Gewicht in Kg")

    axs[0].set_xticklabels(axs[0].get_xticklabels(), rotation = -25, ha="left")
    axs[1].set_xticklabels(axs[1].get_xticklabels(), rotation = -25, ha="left")


    f.savefig("plots/results/masses_density_pack.png", bbox_inches="tight")
    f.savefig("plots/results/masses_density_pack.pgf", bbox_inches="tight")




    ################### 2 Methods Plot in one axis #########################
    col_names = mp_density.columns.values

    mp_density = mp_density.transpose()
    mp_density.rename(columns={0: 'Gewicht'}, inplace=True)

    mp_density["Methode"] = ["Dichtebasiert"]*len(mp_density)
    mp_density["Material"] = mp_density.index

    mp_ah = mp_ah.transpose()
    mp_ah.rename(columns={0: 'Gewicht'}, inplace=True)

    mp_ah["Methode"] = ["Ah-basiert"] * len(mp_ah)
    mp_ah["Material"] = mp_ah.index

    df_combined = mp_density.append(mp_ah)


    # combined_data = combined_data.set_index([["Density", "Ah-Methode"]])

    f, axs = plt.subplots(1, 1, figsize=(6.3, 4), sharey=True)
    sns.barplot(data=df_combined, x="Material", y="Gewicht", hue="Methode", ax=axs, palette=tum_colors)

    # sns.barplot(data=mp_density, ax=axs, palette=tum_colors)
    # sns.barplot(data=mp_ah, ax=axs, palette=tum_colors)

    axs.set_title("Vergleich der Methoden", fontsize=fontsize)
    # axs[1].set_title("Kapazitäts-basierte Methode", fontsize=fontsize)

    axs.set_ylabel("Gewicht in g")

    axs.set_xticklabels(axs.get_xticklabels(), rotation=-25, ha="left")

    f.savefig("plots/results/masses_cell_one_axis.png", bbox_inches="tight")
    f.savefig("plots/results/masses_cell_one_axis.pgf", bbox_inches="tight")


    plt.show()