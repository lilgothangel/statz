from api import get_data
import stats



def show_winrate(matches):
    print(f"Winrate: {stats.count_wr(matches):.2f}%")
    print(f"Radiant wr: {stats.wr_side(matches, True):.2f}%")
    print(f"Dire wr: {stats.wr_side(matches, False):.2f}%")


def show_kda(matches, heroes):
    best_match = max(matches, key=stats.count_kd)
    worst_match = min(matches, key = stats.count_kd)

    for match in matches:
        print(f'Match {match['match_id']} - KDA {round(stats.count_kd(match), 2)}')


    #неправильно
    heroes_by_id = {hero['id']: hero for hero in heroes}
    hero = heroes_by_id.get(match['hero_id'])
    #####

    print(f'Best KDA - {hero['localized_name']} - {stats.count_kd(best_match):.2f}')

    print(f'Worst KDA - {hero['localized_name']} - {stats.count_kd(worst_match):.2f}')

    print(f"Average KDA - {stats.avg_kda(matches):.2f}") 

    print("HERO K D A")
    for match in matches:
        print(hero['localized_name'], match['kills'], match['deaths'], match['assists']) #неправильно имя чара выводится

def show_time(matches): 
    minutes, seconds = divmod(round(stats.avg_time(matches)), 60)

    print(f"Avg match time - {minutes}:{seconds:02d} min")

if __name__ == "__main__":
    matches, heroes = get_data()

    show_winrate(matches)
    show_kda(matches, heroes)
    show_time(matches)