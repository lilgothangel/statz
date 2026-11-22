import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

def plot_hero_winrate(df):
    fig, ax = plt.subplots()

    df = df.sort_values("winrate")

    label = df["hero"].astype(str) + " (" + df["games"].astype(str) + ")"

    bars = ax.barh(label, df.winrate)
    ax.axvline(x=50, color='gray', linestyle='--')

    ax.bar_label(bars, padding=3, fmt='%.1f')

    ax.set_title("Winrate by Hero (min 3 games)")
    ax.set_xlabel("Winrate(%)")
    ax.set_ylabel("Hero (games)")
    ax.set_xlim(0, 100)

    plt.savefig('output/hero_winrate.png', dpi=150, bbox_inches='tight')
    # plt.show()
    plt.close(fig)

def plot_cumulative_wr(df, max_games=None):
    fig, ax = plt.subplots()

    ax.plot(df.games_so_far, df.cumulative_winrate)
    ax.axhline(y=50, color='gray', linestyle='--')

    ax.set_title("Cumulative Winrate")
    ax.set_xlabel("Games")
    ax.set_ylabel("Winrate(%)")

    ax.set_xlim(1, max_games)
    ax.set_ylim(0,100)

    ax.xaxis.set_major_locator(MultipleLocator(10))

    plt.savefig('output/cumulative_winrate.png', dpi=150, bbox_inches='tight')
    # plt.show()
    plt.close(fig)


def plot_kda(df, max_games=None):
    fig, ax = plt.subplots()

    df_plot = df.head(max_games) if max_games else df
    df_plot = df_plot.iloc[::-1]
    avg_kda = df_plot.kda.mean()

    ax.scatter(df_plot.index+1, df_plot.kda)
    ax.plot(df_plot.index+1, df_plot.kda)
    ax.axhline(avg_kda, label=f"Average KDA: {avg_kda:.2f}")

    ax.set_title("KDA per Match")
    ax.set_xlabel("Games")
    ax.set_ylabel("KDA")

    ax.set_xlim(1, max_games)

    ax.xaxis.set_major_locator(MultipleLocator(5))

    ax.legend()

    plt.savefig('output/kda.png', dpi=150, bbox_inches='tight')
    # plt.show()
    plt.close(fig)

def plot_weekly(df):
    fig, ax = plt.subplots()

    week_label = df.week.astype(str) + ' (' + df.games.astype(str) + ')'
    bars = ax.bar(week_label, df.winrate)

    ax.set_title("Weekly Winrate")
    ax.set_xlabel("Week")
    ax.set_ylabel("Winrate (%)")

    ax.set_ylim(0, 110)
    ax.axhline(y=50, color='gray', linestyle='--')

    plt.xticks(rotation=45, ha='right')
    ax.bar_label(bars, padding=3, fmt='%.1f')

    plt.tight_layout()
    plt.savefig('output/weekly.png', dpi=150, bbox_inches='tight')
    # plt.show()
    plt.close(fig)

def plot_side_winrate(df):
    fig, ax = plt.subplots()

    bars = ax.bar(df.side, df.winrate)

    ax.set_title("Radiant vs Dire Winrate")
    ax.set_xlabel("Side")
    ax.set_ylabel("Winrate (%)")

    ax.set_ylim(0, 110)
    ax.axhline(y=50, color='gray', linestyle='--')


    ax.bar_label(bars, padding=3, fmt='%.1f')


    plt.tight_layout()
    plt.savefig('output/side_winrate.png', dpi=150, bbox_inches='tight')
    # plt.show()
    plt.close(fig)