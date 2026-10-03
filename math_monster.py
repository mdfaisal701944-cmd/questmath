import streamlit as st
import random
import time
import json
import os

st.set_page_config(page_title="QuestMath: UFC & MMA Arena", page_icon="🥊", layout="wide")

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
    # Check if player already exists in leaderboard; update if higher score
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

def reset_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        try:
            os.remove(LEADERBOARD_FILE)
        except Exception:
            pass

def trigger_sound(sound_type):
    js_code = (
        "<script>"
        "(function() {"
        "  try {"
        "    const AudioCtx = window.AudioContext || window.webkitAudioContext;"
        "    const ctx = new AudioCtx();"
        "    const type = '" + sound_type + "';"
        "    function makeNoise() {"
        "      const b = ctx.createBuffer(1, ctx.sampleRate * 0.4, ctx.sampleRate);"
        "      const d = b.getChannelData(0);"
        "      for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;"
        "      return b;"
        "    }"
        "    function shot(freq, dur, gainVal) {"
        "      const now = ctx.currentTime;"
        "      const src = ctx.createBufferSource();"
        "      src.buffer = makeNoise();"
        "      const f = ctx.createBiquadFilter();"
        "      f.type = 'lowpass';"
        "      f.frequency.setValueAtTime(freq, now);"
        "      f.frequency.exponentialRampToValueAtTime(80, now + dur);"
        "      const g = ctx.createGain();"
        "      g.gain.setValueAtTime(gainVal, now);"
        "      g.gain.exponentialRampToValueAtTime(0.001, now + dur);"
        "      src.connect(f); f.connect(g); g.connect(ctx.destination);"
        "      src.start(now); src.stop(now + dur);"
        "    }"
        "    if (type === 'pistol') shot(2600, 0.2, 1.2);"
        "    else if (type === 'rifle') shot(2200, 0.3, 1.4);"
        "    else if (type === 'shotgun') shot(1400, 0.45, 1.8);"
        "    else if (type === 'sniper') shot(1100, 0.6, 2.2);"
        "    else if (type === 'smg') {"
        "      [0, 0.08, 0.16].forEach(d => setTimeout(() => shot(2800, 0.15, 1.1), d * 1000));"
        "    } else if (type === 'win') {"
        "      [523, 659, 783, 1046].forEach((fr, i) => {"
        "        setTimeout(() => {"
        "          const o = ctx.createOscillator(); const g = ctx.createGain();"
        "          o.frequency.value = fr; g.gain.setValueAtTime(0.4, ctx.currentTime);"
        "          g.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.25);"
        "          o.connect(g); g.connect(ctx.destination); o.start(); o.stop(ctx.currentTime + 0.25);"
        "        }, i * 100);"
        "      });"
        "    } else if (type === 'miss') {"
        "      const o = ctx.createOscillator(); const g = ctx.createGain();"
        "      o.type = 'sawtooth'; o.frequency.setValueAtTime(140, ctx.currentTime);"
        "      o.frequency.linearRampToValueAtTime(60, ctx.currentTime + 0.25);"
        "      g.gain.setValueAtTime(0.6, ctx.currentTime); g.gain.linearRampToValueAtTime(0.01, ctx.currentTime + 0.25);"
        "      o.connect(g); g.connect(ctx.destination); o.start(); o.stop(ctx.currentTime + 0.25);"
        "    }"
        "  } catch(e) {}"
        "})();"
        "</script>"
    )
    st.components.v1.html(js_code, height=0, width=0)

# 12 UFC Superstars (Real Static Verified Images)
CHARACTERS = {
    "Khabib Nurmagomedov": {
        "price": 500,
        "title": "The Eagle (29-0 Undefeated Legend)",
        "icon": "🦅",
        "img": "https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/2611557.png&w=350&h=254"
    },
    "Conor McGregor": {
        "price": 420,
        "title": "The Notorious Champ",
        "icon": "🇮🇪",
        "img": "https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/3022677.png&w=350&h=254"
    },
    "Jon Jones": {
        "price": 360,
        "title": "Bones (Heavyweight GOAT)",
        "icon": "👑",
        "img": "https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/2335639.png&w=350&h=254"
    },
    "Khamzat Chimaev": {
        "price": 300,
        "title": "Borz (Smash Everybody)",
        "icon": "🐺",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Khamzat_Chimaev_2022_%28cropped%29.png/330px-Khamzat_Chimaev_2022_%28cropped%29.png"
    },
    "Islam Makhachev": {
        "price": 250,
        "title": "P4P King & Lightweight Champ",
        "icon": "🥋",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Islam_Makhachev_2022_UFC_belt_%28cropped%29.png/330px-Islam_Makhachev_2022_UFC_belt_%28cropped%29.png"
    },
    "Alex Pereira": {
        "price": 200,
        "title": "Poatan (Stone Hands)",
        "icon": "🗿",
        "img": "https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/4898396.png&w=350&h=254"
    },
    "Israel Adesanya": {
        "price": 160,
        "title": "The Last Stylebender",
        "icon": "⚡",
        "img": "https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/3154170.png&w=350&h=254"
    },
    "Charles Oliveira": {
        "price": 120,
        "title": "Do Bronx (Submission King)",
        "icon": "🦁",
        "img": "https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/2504169.png&w=350&h=254"
    },
    "Dustin Poirier": {
        "price": 80,
        "title": "The Diamond",
        "icon": "💎",
        "img": "https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/2508115.png&w=350&h=254"
    },
    "Justin Gaethje": {
        "price": 50,
        "title": "The Highlight",
        "icon": "💥",
        "img": "https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/2984180.png&w=350&h=254"
    },
    "Max Holloway": {
        "price": 25,
        "title": "Blessed (BMF)",
        "icon": "🌴",
        "img": "https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/2614933.png&w=350&h=254"
    },
    "Sean O'Malley": {
        "price": 0,
        "title": "Suga Show (Starter Fighter)",
        "icon": "🍭",
        "img": "https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/4285679.png&w=350&h=254"
    }
}

FF_GUNS = {
    "G18 Pistol": {"price": 0, "bonus": 0, "icon": "🔫", "type": "pistol", "desc": "Standard sidearm"},
    "SCAR": {"price": 45, "bonus": 25, "icon": "🎯", "type": "rifle", "desc": "Solid assault firepower"},
    "MP40": {"price": 90, "bonus": 45, "icon": "⚡", "type": "smg", "desc": "Double streak multiplier"},
    "M1887 Shotgun": {"price": 160, "bonus": 85, "icon": "💥", "type": "shotgun", "desc": "Devastating close-range blast"},
    "AWM Sniper": {"price": 250, "bonus": 130, "icon": "🔭", "type": "sniper", "desc": "Extreme sniper impact"}
}

MONSTERS = [
    {"name": "Grumble Goblin", "img": "https://api.dicebear.com/7.x/bottts/svg?seed=GrumbleArena&backgroundColor=b6e3f4", "max_hp": 100},
    {"name": "Shadow Dragon", "img": "https://api.dicebear.com/7.x/bottts/svg?seed=ShadowDragonX&backgroundColor=ffdfbf", "max_hp": 180},
    {"name": "Titan Mecha", "img": "https://api.dicebear.com/7.x/bottts/svg?seed=TitanWarriorZ&backgroundColor=ffd5dc", "max_hp": 260},
]

TIMER_MAP = {
    "1-4s (Blitz)": 4,
    "1-8s (Normal)": 8,
    "1-15s (Medium)": 15,
    "1-20s (Hard)": 20,
    "1-25s (Titan)": 25,
}

def generate_question(op, lvl, sec):
    if op == "Multiplication (×)":
        if sec <= 4: n1, n2 = random.randint(2, 5), random.randint(2, 5)
        elif sec <= 8: n1, n2 = random.randint(3, 9), random.randint(3, 9)
        elif sec <= 15: n1, n2 = random.randint(6, 12), random.randint(6, 12)
        else: n1, n2 = random.randint(11, 20), random.randint(6, 15)
        return n1, n2, "×", n1 * n2
    elif op == "Addition (+)":
        if sec <= 4: n1, n2 = random.randint(5, 20), random.randint(5, 20)
        elif sec <= 8: n1, n2 = random.randint(20, 60), random.randint(15, 50)
        elif sec <= 15: n1, n2 = random.randint(50, 150), random.randint(40, 100)
        else: n1, n2 = random.randint(150, 500), random.randint(100, 400)
        return n1, n2, "+", n1 + n2
    elif op == "Subtraction (−)":
        if sec <= 4: n1 = random.randint(10, 25); n2 = random.randint(2, n1 - 1)
        elif sec <= 8: n1 = random.randint(30, 80); n2 = random.randint(10, n1 - 1)
        else: n1 = random.randint(80, 250); n2 = random.randint(20, n1 - 1)
        return n1, n2, "−", n1 - n2
    else:
        ans = random.randint(2, 10)
        n2 = random.randint(2, 6)
        return ans * n2, n2, "÷", ans

def set_new_question():
    sec = TIMER_MAP.get(st.session_state.timer_choice, 8)
    n1, n2, sym, a = generate_question(st.session_state.operation, st.session_state.level, sec)
    st.session_state.num1 = n1
    st.session_state.num2 = n2
    st.session_state.symbol = sym
    st.session_state.ans = a
    st.session_state.q_start = time.time()
    st.session_state.q_id += 1

# Initializations
if "level" not in st.session_state: st.session_state.level = 0
if "score" not in st.session_state: st.session_state.score = 0
if "streak" not in st.session_state: st.session_state.streak = 0
if "player_hp" not in st.session_state: st.session_state.player_hp = 100
if "guns_owned" not in st.session_state: st.session_state.guns_owned = ["G18 Pistol"]
if "equipped_gun" not in st.session_state: st.session_state.equipped_gun = "G18 Pistol"
if "costumes_owned" not in st.session_state: st.session_state.costumes_owned = ["Sean O'Malley"]
if "equipped_costume" not in st.session_state or st.session_state.equipped_costume not in CHARACTERS:
    st.session_state.equipped_costume = "Sean O'Malley"
if "operation" not in st.session_state: st.session_state.operation = "Multiplication (×)"
if "timer_choice" not in st.session_state or st.session_state.timer_choice not in TIMER_MAP:
    st.session_state.timer_choice = "1-8s (Normal)"
if "q_start" not in st.session_state: st.session_state.q_start = time.time()
if "q_id" not in st.session_state: st.session_state.q_id = 0
if "saved" not in st.session_state: st.session_state.saved = False
if "play_sound" not in st.session_state: st.session_state.play_sound = None
if "input_counter" not in st.session_state: st.session_state.input_counter = 0

curr_sec = TIMER_MAP.get(st.session_state.timer_choice, 8)
curr_mon = MONSTERS[st.session_state.level % len(MONSTERS)]
hero = CHARACTERS.get(st.session_state.equipped_costume, CHARACTERS["Sean O'Malley"])
gun = FF_GUNS.get(st.session_state.equipped_gun, FF_GUNS["G18 Pistol"])

if "mon_hp" not in st.session_state: st.session_state.mon_hp = curr_mon["max_hp"]

if "num1" not in st.session_state:
    set_new_question()

if st.session_state.play_sound:
    trigger_sound(st.session_state.play_sound)
    st.session_state.play_sound = None

# Sidebar
with st.sidebar:
    st.title("🏆 Leaderboard")
    current_board = load_leaderboard()
    if current_board:
        for idx, entry in enumerate(current_board):
            medal = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else f"#{idx+1}"
            st.write(f"{medal} **{entry['name']}** — {entry['score']} pts (Round {entry.get('level', 1)})")
    else:
        st.caption("No records yet. Be the first to claim victory!")

    if st.button("🗑️ Reset Leaderboard", help="Clear all saved high scores"):
        reset_leaderboard()
        st.success("Leaderboard cleared!")
        st.rerun()

    st.markdown("---")
    st.title("🥋 UFC Fighters (P4P Roster)")
    st.write(f"💰 Available Coins: **{st.session_state.score}**")
    for c_name, c_info in CHARACTERS.items():
        c1, c2 = st.columns([2, 1])
        c1.write(f"{c_info['icon']} **{c_name}**")
        c1.caption(f"{c_info['title']} • {c_info['price']} Coins")
        with c2:
            if c_name in st.session_state.costumes_owned:
                if st.session_state.equipped_costume == c_name:
                    st.write("🥊 Selected")
                elif st.button("Equip", key=f"w_{c_name}"):
                    st.session_state.equipped_costume = c_name
                    st.rerun()
            else:
                if st.button(f"{c_info['price']} 🪙", key=f"bc_{c_name}"):
                    if st.session_state.score >= c_info["price"]:
                        st.session_state.score -= c_info["price"]
                        st.session_state.costumes_owned.append(c_name)
                        st.session_state.equipped_costume = c_name
                        st.session_state.play_sound = "win"
                        st.rerun()
                    else:
                        st.error("Insufficient coins!")

    st.markdown("---")
    st.title("🔫 Armory")
    for g_name, g_info in FF_GUNS.items():
        c1, c2 = st.columns([2, 1])
        c1.write(f"{g_info['icon']} **{g_name}** (+{g_info['bonus']} Dmg)")
        c1.caption(f"_{g_info['desc']}_")
        with c2:
            if g_name in st.session_state.guns_owned:
                if st.session_state.equipped_gun == g_name:
                    st.write("✅ Ready")
                elif st.button("Arm", key=f"e_{g_name}"):
                    st.session_state.equipped_gun = g_name
                    st.session_state.play_sound = g_info["type"]
                    st.rerun()
            else:
                if st.button(f"{g_info['price']} 🪙", key=f"b_{g_name}"):
                    if st.session_state.score >= g_info["price"]:
                        st.session_state.score -= g_info["price"]
                        st.session_state.guns_owned.append(g_name)
                        st.session_state.equipped_gun = g_name
                        st.session_state.play_sound = g_info["type"]
                        st.rerun()
                    else:
                        st.error("Insufficient coins!")

    st.markdown("---")
    if st.button("🧪 Recovery Shake (+40 HP) - 30 Coins"):
        if st.session_state.score >= 30:
            if st.session_state.player_hp >= 100:
                st.warning("Health points already full!")
            else:
                st.session_state.score -= 30
                st.session_state.player_hp = min(100, st.session_state.player_hp + 40)
                st.success("Health restored! ❤️")
                st.rerun()
        else:
            st.error("Insufficient coins!")

    st.markdown("---")
    t_choice = st.selectbox(
        "⏱️ Attack Timer:", 
        list(TIMER_MAP.keys()), 
        index=list(TIMER_MAP.keys()).index(st.session_state.timer_choice)
    )
    if t_choice != st.session_state.timer_choice:
        st.session_state.timer_choice = t_choice
        set_new_question()
        st.rerun()

    op_choice = st.selectbox(
        "Operation Mode:", 
        ["Multiplication (×)", "Addition (+)", "Subtraction (−)", "Division (÷)"], 
        index=["Multiplication (×)", "Addition (+)", "Subtraction (−)", "Division (÷)"].index(st.session_state.operation)
    )
    if op_choice != st.session_state.operation:
        st.session_state.operation = op_choice
        set_new_question()
        st.rerun()

# Main Arena
st.markdown("<h1 style='text-align: center; color: #ff3333;'>🥊 QuestMath: UFC Octagon Arena ⚔️</h1>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.metric("⭐ Coins", st.session_state.score)
col2.metric("🔥 KO Streak", f"{st.session_state.streak}x")
col3.metric("🔫 Weapon", f"{gun['icon']} {st.session_state.equipped_gun}")
col4.metric("🥋 Fighter", f"{hero['icon']} {st.session_state.equipped_costume}")

st.divider()

if st.session_state.player_hp <= 0:
    st.error(f"💀 KNOCKED OUT! Final Score: {st.session_state.score} | Round Reached: {st.session_state.level + 1}")
    
    if not st.session_state.saved:
        with st.form("save_form"):
            p_name = st.text_input("Enter Fighter Name for Hall of Fame:", max_chars=14, placeholder="Enter your name...")
            if st.form_submit_button("💾 Save Score"):
                if p_name.strip():
                    save_score(p_name.strip(), st.session_state.score, st.session_state.level + 1)
                    st.session_state.saved = True
                    st.success("Score registered in the Leaderboard! 🏆")
                    st.rerun()
                else:
                    st.warning("Please type a valid name before saving.")
    else:
        st.info("Score has been saved to the Leaderboard!")

    if st.button("Rematch 🔄", use_container_width=True):
        st.session_state.player_hp = 100
        st.session_state.score = 0
        st.session_state.level = 0
        st.session_state.mon_hp = MONSTERS[0]["max_hp"]
        st.session_state.saved = False
        set_new_question()
        st.rerun()

elif st.session_state.mon_hp <= 0:
    trigger_sound("win")
    st.balloons()
    st.success(f"🎉 AND NEW! Defeated {curr_mon['name']} by TKO!")
    if st.button("Next Round ➡️", use_container_width=True):
        st.session_state.level += 1
        st.session_state.mon_hp = MONSTERS[st.session_state.level % len(MONSTERS)]['max_hp']
        st.session_state.score += 50
        set_new_question()
        st.rerun()

else:
    c_left, c_mid, c_right = st.columns([3, 1, 3])
    
    with c_left:
        st.markdown(f"<center><b>{hero['icon']} {st.session_state.equipped_costume}</b><br><span style='color: #ffaa00;'>{hero['title']}</span></center>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; margin: 10px 0;">
                <img src="{hero['img']}" 
                     referrerpolicy="no-referrer" 
                     crossorigin="anonymous"
                     onerror="this.onerror=null; this.src='https://api.dicebear.com/7.x/initials/svg?seed={st.session_state.equipped_costume}&backgroundColor=b71c1c';"
                     style="width: 190px; height: 190px; object-fit: cover; object-position: top; background: #1c1c1c; border-radius: 16px; border: 3px solid #ff4444; box-shadow: 0 4px 15px rgba(255, 68, 68, 0.4);">
            </div>
            """,
            unsafe_allow_html=True
        )
        st.progress(max(0.0, min(1.0, st.session_state.player_hp / 100.0)))
        st.write(f"<center><b>HP: {st.session_state.player_hp} / 100</b></center>", unsafe_allow_html=True)
        
    with c_mid:
        st.markdown("<h1 style='text-align: center; color: #ffaa00; margin-top: 60px;'>VS</h1>", unsafe_allow_html=True)
        
    with c_right:
        st.markdown(f"<center><b>👾 {curr_mon['name']}</b><br><span style='color: #c084fc;'>Arena Challenger</span></center>", unsafe_allow_html=True)
        st.image(curr_mon["img"], width=190)
        st.progress(max(0.0, min(1.0, st.session_state.mon_hp / curr_mon["max_hp"])))
        st.write(f"<center><b>HP: {st.session_state.mon_hp} / {curr_mon['max_hp']}</b></center>", unsafe_allow_html=True)

    timer_style = (
        "<style>"
        "@keyframes shrinkTimer_" + str(st.session_state.q_id) + " {"
        "  0% { width: 100%; background-color: #00ff7f; }"
        "  70% { width: 30%; background-color: #ffaa00; }"
        "  100% { width: 0%; background-color: #ff2222; }"
        "}"
        ".t-box { width: 100%; background: #222; border-radius: 8px; height: 14px; overflow: hidden; margin-top: 15px; }"
        ".t-fill_" + str(st.session_state.q_id) + " { height: 100%; width: 100%; animation: shrinkTimer_" + str(st.session_state.q_id) + " " + str(curr_sec) + "s linear forwards; }"
        "</style>"
        "<div class='t-box'><div class='t-fill_" + str(st.session_state.q_id) + "'></div></div>"
    )
    st.markdown(timer_style, unsafe_allow_html=True)

    st.info(f"### 🔥 What is: **{st.session_state.num1} {st.session_state.symbol} {st.session_state.num2}** ?")

    user_input = st.number_input(
        "Enter your answer:",
        value=None,
        step=1,
        key=f"user_ans_box_{st.session_state.input_counter}",
        placeholder="Type answer here..."
    )

    if st.button(f"⚡ STRIKE WITH {st.session_state.equipped_gun.upper()}!", use_container_width=True):
        taken = time.time() - st.session_state.q_start
        GRACE = 2.0

        if user_input is None:
            st.warning("⚠️ Please enter a number in the answer field before attacking!")
        elif taken > (curr_sec + GRACE):
            st.session_state.player_hp = max(0, st.session_state.player_hp - 20)
            st.session_state.streak = 0
            st.session_state.play_sound = "miss"
            st.error(f"⏰ TIME UP! You took {int(taken)}s. Opponent countered for -20 HP!")
            st.session_state.input_counter += 1
            set_new_question()
            time.sleep(0.4)
            st.rerun()
        else:
            if user_input == st.session_state.ans:
                st.session_state.play_sound = gun["type"]
                streak_bonus = st.session_state.streak * (10 if st.session_state.equipped_gun == "MP40" else 5)
                dmg = 30 + streak_bonus + gun["bonus"]
                st.session_state.mon_hp = max(0, st.session_state.mon_hp - dmg)
                st.session_state.score += 20
                st.session_state.streak += 1
                st.success(f"💥 CLEAN HIT! Dealt -{dmg} Damage with {st.session_state.equipped_gun}!")
            else:
                st.session_state.streak = 0
                st.session_state.player_hp = max(0, st.session_state.player_hp - 10)
                st.session_state.play_sound = "miss"
                st.error(f"❌ Incorrect answer! Correct answer was: {st.session_state.ans}. Countered for -10 HP!")

            st.session_state.input_counter += 1
            set_new_question()
            time.sleep(0.4)
            st.rerun()