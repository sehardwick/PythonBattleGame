

import random
from .magic import Spell

#set colors for terminal
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#init Person class
class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]


#generate damage using random number between attack low and attack high
    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

#take damage
    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

#healing
    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

#get hp/max hp/mp/max mp
    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

#reduce magic points
    def reduce_mp(self, cost):
        self.mp -= cost

#choose action
    def choose_action(self):
        i = 1
        print("\n" + "    " + bcolors.BOLD + self.name + bcolors.ENDC)
        print(bcolors.OKBLUE + bcolors.BOLD + "    ACTIONS" + bcolors.ENDC)
        for item in self.actions:
            print("        " + str(i) + ".", item)
            i += 1

#choose magic
    def choose_magic(self):
        i = 1
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "    MAGIC" + bcolors.ENDC)
        for spell in self.magic:
            print("        " + str(i) + ".", spell.name, "(cost:", str (spell.cost) + ")")
            i += 1

#choose target
    def choose_target(self, enemies):
        i = 1
        print("\n" + bcolors.FAIL + bcolors.BOLD + "    TARGET:" + bcolors.ENDC)
        for enemy in enemies:
            if enemy.get_hp() != 0:
                print("        " + str(i) + ".", enemy.name)
                i += 1
        choice = int(input("    Choose target:")) - 1
        return choice

#choose inventory item
    def choose_item(self):
        i = 1

        print("\n" + bcolors.OKGREEN + bcolors.BOLD + "    ITEMS:" + bcolors.ENDC)
        for item in self.items:
            print("        " + str(i) + ".", item["item"].name + ":", item["item"].description,
                  " (x" + str(item["quantity"]) + ")")
            i += 1

#get enemy hp/mp stats
    def get_enemy_stats(self):
        enemy_hp_bar = ""
        enemy_bar_ticks = (self.hp / self.maxhp) * 100 / 2

        while enemy_bar_ticks > 0:
            enemy_hp_bar += "█"
            enemy_bar_ticks -= 1
        while len(enemy_hp_bar) < 50:
            enemy_hp_bar += " "
        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""
        if len(hp_string) < 11:
            decreased_hp = 11 - len(hp_string)
            while decreased_hp > 0:
                current_hp += " "
                decreased_hp -= 1
            current_hp += hp_string
        else:
            current_hp = hp_string
        print(bcolors.BOLD + self.name + "             " + bcolors.ENDC +
              current_hp + " |" + bcolors.FAIL + enemy_hp_bar + bcolors.ENDC + "|   ")

#define get_stats function for hp/mp bars
    def get_stats(self):
        hp_bar = ""
        hp_bar_ticks = (((self.hp/self.maxhp) * 100) / 4)
        mp_bar = ""
        mp_bar_ticks = (((self.mp/self.maxmp) * 100) / 10)

        while hp_bar_ticks > 0:
            hp_bar += "█"
            hp_bar_ticks -= 1
        while mp_bar_ticks > 0:
            mp_bar += "█"
            mp_bar_ticks -= 1
        while len(hp_bar) < 25:
            hp_bar += " "
        while len(mp_bar) < 10:
            mp_bar += " "

#remove white space from hp/mp when hp/mp variable drops below 9 chars
        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""
        if len(hp_string) < 9:
            decreased_hp = 9 - len(hp_string)
            while decreased_hp > 0:
                current_hp += " "
                decreased_hp -= 1
            current_hp += hp_string
        else:
            current_hp = hp_string

        mp_string = str(self.mp) + "/" + str(self.maxmp)
        current_mp = ""
        if len(mp_string) < 7:
            decreased_mp = 7 - len(mp_string)
            while decreased_mp > 0:
                current_mp += " "
                decreased_mp -= 1
            current_mp += mp_string
        else:
            current_mp = mp_string

#print status bars at beginning of each turn
        #print("                                 _________________________           __________")
        print(bcolors.BOLD + self.name + "                " + bcolors.ENDC +
              current_hp + " |" + bcolors.OKGREEN + hp_bar + bcolors.ENDC + "|   " +
              current_mp + " |" + bcolors.OKBLUE + mp_bar + bcolors.ENDC + "|")

    def choose_enemy_spell(self):
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        magic_dmg = spell.generate_damage()

        pct = self.hp / self.maxhp * 100
        if self.mp < spell.cost or spell.type == "white" and pct > 50:
            self.choose_enemy_spell()
        else:
            return spell, magic_dmg
