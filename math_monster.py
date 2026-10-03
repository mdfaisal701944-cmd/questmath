import streamlit as st
import random
import time
import json
import os

st.set_page_config(page_title="QuestMath: UFC Arena", page_icon="🥊", layout="centered")

LEADERBOARD_FILE = "leaderboard.json"

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return sorted(data, key=lambda x: x.get("score", 0), reverse=True)
        except Exception:
            return []
    return []

def save_score(name, score, level):
    board = load_leaderboard()
    existing = next((item for item in board if item["name"].strip().lower() == name.strip().lower()), None)
    if existing:
        if score > existing["score"]:
            existing["score"] = score
            existing["level"] = level
    else:
        board.append({"name": name.strip(), "score": score, "level": level})
    board = sorted(board, key=lambda x: x["score"], reverse=True)[:5]
    try:
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(board, f, indent=2)
    except Exception:
        pass

CHARACTERS = {
    "Sean O'Malley": {"price": 0, "title": "Suga Show", "icon": "🍭", "img": "https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/4285679.png&w=260&h=200"},
    "Max Holloway": {"price": 25, "title": "Blessed BMF", "icon": "🌴", "img": "https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/2614933.png&w=260&h=200"},
    "Jon Jones": {"price": 360, "title": "Bones GOAT", "icon": "👑", "img": "https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/2335639.png&w=260&h=200"},
    "Conor McGregor": {"price": 420, "title": "The Notorious", "icon": "🇮🇪", "img": "https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/3022677.png&w=260&h=200"},
    "Khabib Nurmagomedov": {"price": 500, "title": "The Eagle", "icon": "🦅", "img": "https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/2611557.png&w=260&h=200"}
}

FF_GUNS = {
    "G18 Pistol": {"price": 0, "bonus": 0, "icon": "🔫"},
    "SCAR": {"price": 45, "bonus": 25, "icon": "🎯"},
    "MP40": {"price": 90, "bonus": 45, "icon": "⚡"},
    "AWM Sniper": {"price": 250, "bonus": 130, "icon": "🔭"}
}

MONSTERS = [
    {"name": "Grumble Goblin", "img": "https://api.dicebear.com/7.x/bottts/svg?seed=GrumbleArena&backgroundColor=b6e3f4", "max_hp": 100, "stage": "Round 1"},
    {"name": "Shadow Dragon", "img": "https://api.dicebear.com/7.x/bottts/svg?seed=ShadowDragonX&backgroundColor=ffdfbf", "max_hp": 180, "stage": "Round 2"},
    {"name": "Titan Mecha", "img": "https://api.dicebear.com/7.x/bottts/svg?seed=TitanWarriorZ&backgroundColor=ffd5dc", "max_hp": 260, "stage": "Round 3"}
]

TIMER_MAP = {
    "Normal (8s)": 8,
    "Blitz (4s)": 4,
    "Easy (15s)": 15
}

def generate_q(sec):
    n1 = random.randint(2, 9)
    n2 = random.randint(2, 9)
    ans = n1 * n2
    opts = {ans}
    while len(opts) < 4:
        wrong = ans + random.choice([-6, -4, -2, -1, 1, 2, 3, 5])
        if wrong > 0 and wrong != ans:
            opts.add(wrong)
    opt_list = list(opts)
    random.shuffle(opt_list)
    return n1, n2, ans, opt_list

def set_new_question():
    sec = TIMER_MAP.get(st.session_state.timer_choice, 8)
    n1, n2, a, opts = generate_q(sec)
    st.session_state.num1 = n1
    st.session_state.num2 = n2
    st.session_state.ans = a
    st.session_state.options = opts
    st.session_state.q_start = time.time()
    st.session_state.q_id += 1

if "game_started" not in st.session_state: st.session_state.game_started = False
if "level" not in st.session_state: st.session_state.level = 0
if "score" not in st.session_state: st.session_state.score = 0
if "streak" not in st.session_state: st.session_state.streak = 0
if "player_hp" not in st.session_state or st.session_state.player_hp <= 0: st.session_state.player_hp = 100
if "equipped_costume" not in st.session_state: st.session_state.equipped_costume = "Sean O'Malley"
if "equipped_gun" not in st.session_state: st.session_state.equipped_gun = "G18 Pistol"
if "timer_choice" not in st.session_state: st.session_state.timer_choice = "Normal (8s)"
if "q_start" not in st.session_state: st.session_state.q_start = time.time()
if "q_id" not in st.session_state: st.session_state.q_id = 0
if "last_msg" not in st.session_state: st.session_state.last_msg = None

safe_level = min(max(0, st.session_state.level), len(MONSTERS) - 1)
curr_mon = MONSTERS[safe_level]
hero = CHARACTERS.get(st.session_state.equipped_costume, CHARACTERS["Sean O'Malley"])
gun = FF_GUNS.get(st.session_state.equipped_gun, FF_GUNS["G18 Pistol"])
curr_sec = TIMER_MAP.get(st.session_state.timer_choice, 8)

if "mon_hp" not in st.session_state or st.session_state.mon_hp <= 0:
    st.session_state.mon_hp = curr_mon["max_hp"]

if "num1" not in st.session_state or "options" not in st.session_state:
    set_new_question()

# LOBBY SCREEN
if not st.session_state.game_started:
    st.title("🥊 QuestMath: UFC Octagon")
    st.write(f"🥋 **Fighter:** {hero['icon']} {st.session_state.equipped_costume}")
    st.write(f"🔫 **Weapon:** {gun['icon']} {st.session_state.equipped_gun}")
    st.write(f"⭐ **Coins:** {st.session_state.score}")
    st.info("Solve fast • Select correct strike option • Defeat 3 Monster Bosses!")
    
    if st.button("🚀 START FIGHT", use_container_width=True):
        st.session_state.game_started = True
        st.session_state.player_hp = 100
        st.session_state.level = 0
        st.session_state.mon_hp = MONSTERS[0]["max_hp"]
        st.session_state.last_msg = None
        set_new_question()
        st.rerun()

# FIGHT SCREEN
else:
    current_round_num = st.session_state.level + 1
    total_rounds = len(MONSTERS)

    st.subheader(f"🥊 {curr_mon['stage']}: {curr_mon['name']}")
    st.write(f"⭐ Coins: **{st.session_state.score}** | 🔥 Streak: **{st.session_state.streak}x**")
    st.write(f"❤️ Your HP: **{st.session_state.player_hp}/100** | 👾 Monster HP: **{st.session_state.mon_hp}/{curr_mon['max_hp']}**")

    # KNOCKED OUT
    if st.session_state.player_hp <= 0:
        st.error(f"💀 KNOCKED OUT! Final Score: {st.session_state.score}")
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.player_hp = 100
            st.session_state.score = 0
            st.session_state.level = 0
            st.session_state.mon_hp = MONSTERS[0]["max_hp"]
            st.session_state.last_msg = None
            set_new_question()
            st.rerun()

    # ROUND WON / FINISH
    elif st.session_state.mon_hp <= 0:
        st.balloons()
        if st.session_state.level >= total_rounds - 1:
            st.success("🏆👑 UFC WORLD CHAMPION! All Rounds Defeated!")
            if st.button("Play Again from Start 🔄", use_container_width=True):
                st.session_state.level = 0
                st.session_state.mon_hp = MONSTERS[0]["max_hp"]
                st.session_state.player_hp = 100
                st.session_state.game_started = False
                st.session_state.last_msg = None
                set_new_question()
                st.rerun()
        else:
            st.success(f"🎉 VICTORY! {curr_mon['name']} defeated!")
            if st.button("Next Round ➡️", use_container_width=True):
                st.session_state.level += 1
                st.session_state.mon_hp = MONSTERS[st.session_state.level]["max_hp"]
                st.session_state.score += 50
                st.session_state.last_msg = None
                set_new_question()
                st.rerun()

    # ACTIVE COMBAT
    else:
        st.image(curr_mon["img"], width=120)
        st.progress(float(max(0, min(100, int(st.session_state.mon_hp * 100 / curr_mon['max_hp'])))) / 100.0)

        if st.session_state.last_msg:
            m_type, m_txt = st.session_state.last_msg
            if m_type == "hit":
                st.success(m_txt)
            else:
                st.error(m_txt)

        st.info(f"### 🔥 What is: {st.session_state.num1} × {st.session_state.num2} ?")

        selected_ans = None
        for opt_val in st.session_state.options:
            if st.button(f"⚡ Strike: {opt_val}", key=f"btn_{st.session_state.q_id}_{opt_val}", use_container_width=True):
                selected_ans = opt_val

        if selected_ans is not None:
            taken = time.time() - st.session_state.q_start
            GRACE = 2.0

            if taken > (curr_sec + GRACE):
                st.session_state.player_hp = max(0, st.session_state.player_hp - 20)
                st.session_state.streak = 0
                st.session_state.last_msg = ("timeout", "⏰ TIME UP! Opponent hit back for -20 HP!")
            elif selected_ans == st.session_state.ans:
                dmg = 35 + gun["bonus"]
                st.session_state.mon_hp = max(0, st.session_state.mon_hp - dmg)
                st.session_state.score += 20
                st.session_state.streak += 1
                st.session_state.last_msg = ("hit", f"💥 HIT! Dealt -{dmg} Damage!")
            else:
                st.session_state.streak = 0
                st.session_state.player_hp = max(0, st.session_state.player_hp - 10)
                st.session_state.last_msg = ("wrong", f"❌ Wrong! Correct answer: {st.session_state.ans}")

            set_new_question()
            st.rerun()

    if st.button("🚪 Exit to Lobby"):
        st.session_state.game_started = False
        st.rerun()
