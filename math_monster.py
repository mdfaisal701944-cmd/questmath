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
        "    const type = '" + str(sound_type) + "';"
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

# ALL 12 UFC SUPERSTARS
CHARACTERS = {
    "Sean O'Malley": {"price": 0, "title": "Suga Show", "icon": "🍭", "img": "https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/4285679.png&w=260&h=200"},
    "Max Holloway": {"price": 25, "title": "Blessed BMF", "icon": "🌴", "img": "https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/2614933.png&w=260&h=200"},
    "Justin Gaethje": {"price": 50, "title": "The Highlight", "icon": "💥", "img": "https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/2984180.png&w=260&h=200"},
    "Dustin Poirier": {"price": 80, "title": "The Diamond", "icon": "💎", "img": "https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/2508115.png&w=260&h=200"},
    "Charles Oliveira": {"price": 120, "title": "Do Bronx", "icon": "🦁", "img": "https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/2504169.png&w=260&h=200"},
    "Israel Adesanya": {"price": 160, "title": "Stylebender", "icon": "⚡", "img": "https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/3154170.png&w=260&h=200"},
    "Alex Pereira": {"price": 200, "title": "Poatan", "icon": "🗿", "img": "https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/4898396.png&w=260&h=200"},
    "Islam Makhachev": {"price": 250, "title": "P4P King", "icon": "🥋", "img": "https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/3153839.png&w=260&h=200"},
    "Khamzat Chimaev": {"price": 300, "title": "Borz", "icon": "🐺", "img": "https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/4422324.png&w=260&h=200"},
    "Jon Jones": {"price": 360, "title": "Bones GOAT", "icon": "👑", "img": "https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/2335639.png&w=260&h=200"},
    "Conor McGregor": {"price": 420, "title": "The Notorious", "icon": "🇮🇪", "img": "https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/3022677.png&w=260&h=200"},
    "Khabib Nurmagomedov": {"price": 500, "title": "The Eagle", "icon": "🦅", "img": "https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/2611557.png&w=260&h=200"}
}

# ALL GUNS & ARMORY
FF_GUNS = {
    "G18 Pistol": {"price": 0, "bonus": 0, "icon": "🔫", "type": "pistol", "desc": "Standard sidearm"},
    "SCAR": {"price": 45, "bonus": 25, "icon": "🎯", "type": "rifle", "desc": "Assault rifle"},
    "MP40": {"price": 90, "bonus": 45, "icon": "⚡", "type": "smg", "desc": "High speed bursts"},
    "M1887 Shotgun": {"price": 160, "bonus": 85, "icon": "💥", "type": "shotgun", "desc": "Heavy blast"},
    "AWM Sniper": {"price": 250, "bonus": 130, "icon": "🔭", "type": "sniper", "desc": "Maximum damage"}
}

# 3 MONSTER BOSS ROUNDS
MONSTERS = [
    {"name": "Grumble Goblin", "img": "https://api.dicebear.com/7.x/bottts/svg?seed=GrumbleArena&backgroundColor=b6e3f4", "max_hp": 100, "stage": "Round 1 (Challenger Match)"},
    {"name": "Shadow Dragon", "img": "https://api.dicebear.com/7.x/bottts/svg?seed=ShadowDragonX&backgroundColor=ffdfbf", "max_hp": 180, "stage": "Round 2 (Title Eliminator)"},
    {"name": "Titan Mecha", "img": "https://api.dicebear.com/7.x/bottts/svg?seed=TitanWarriorZ&backgroundColor=ffd5dc", "max_hp": 260, "stage": "Round 3 (World Championship)"}
]

TIMER_MAP = {
    "1-4s (Blitz)": 4,
    "1-8s (Normal)": 8,
    "1-15s (Medium)": 15,
    "1-20s (Hard)": 20,
    "1-25s (Titan)": 25
}

def generate_q(op, lvl, sec):
    if op == "Multiplication (×)":
        if sec <= 4: n1, n2 = random.randint(2, 5), random.randint(2, 5)
        elif sec <= 8: n1, n2 = random.randint(3, 9), random.randint(3, 9)
        elif sec <= 15: n1, n2 = random.randint(6, 12), random.randint(6, 12)
        else: n1, n2 = random.randint(11, 20), random.randint(6, 15)
        ans = n1 * n2
        sym = "×"
    elif op == "Addition (+)":
        if sec <= 4: n1, n2 = random.randint(5, 20), random.randint(5, 20)
        elif sec <= 8: n1, n2 = random.randint(20, 60), random.randint(15, 50)
        else: n1, n2 = random.randint(50, 150), random.randint(40, 100)
        ans = n1 + n2
        sym = "+"
    elif op == "Subtraction (−)":
        if sec <= 4: n1 = random.randint(10, 25); n2 = random.randint(2, n1 - 1)
        else: n1 = random.randint(30, 80); n2 = random.randint(10, n1 - 1)
        ans = n1 - n2
        sym = "−"
    else:
        ans = random.randint(2, 10)
        n2 = random.randint(2, 6)
        n1 = ans * n2
        sym = "÷"

    opts = {ans}
    while len(opts) < 4:
        delta = random.choice([-10, -5, -2, -1, 1, 2, 3, 5, 10])
        candidate = ans + delta
        if candidate >= 0 and candidate != ans:
            opts.add(candidate)
    opt_list = list(opts)
    random.shuffle(opt_list)
    return n1, n2, sym, ans, opt_list

def set_new_question():
    sec = TIMER_MAP.get(st.session_state.timer_choice, 8)
    n1, n2, sym, a, opts = generate_q(st.session_state.operation, st.session_state.level, sec)
    st.session_state.num1 = n1
    st.session_state.num2 = n2
    st.session_state.symbol = sym
    st.session_state.ans = a
    st.session_state.options = opts
    st.session_state.q_start = time.time()
    st.session_state.q_id += 1

# State Management
if "game_started" not in st.session_state: st.session_state.game_started = False
if "level" not in st.session_state: st.session_state.level = 0
if "score" not in st.session_state: st.session_state.score = 0
if "streak" not in st.session_state: st.session_state.streak = 0
if "player_hp" not in st.session_state or st.session_state.player_hp <= 0: st.session_state.player_hp = 100
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
if "last_msg" not in st.session_state: st.session_state.last_msg = None
if "play_sound" not in st.session_state: st.session_state.play_sound = None

curr_sec = TIMER_MAP.get(st.session_state.timer_choice, 8)
safe_level = min(max(0, st.session_state.level), len(MONSTERS) - 1)
curr_mon = MONSTERS[safe_level]
hero = CHARACTERS.get(st.session_state.equipped_costume, CHARACTERS["Sean O'Malley"])
gun = FF_GUNS.get(st.session_state.equipped_gun, FF_GUNS["G18 Pistol"])

if "mon_hp" not in st.session_state or st.session_state.mon_hp <= 0:
    st.session_state.mon_hp = curr_mon["max_hp"]

if "num1" not in st.session_state or "options" not in st.session_state:
    set_new_question()

if st.session_state.play_sound:
    trigger_sound(st.session_state.play_sound)
    st.session_state.play_sound = None

# ==========================================
# SIDEBAR: LEADERBOARD, UFC ROSTER & ARMORY
# ==========================================
with st.sidebar:
    st.title("🏆 Leaderboard")
    current_board = load_leaderboard()
    if current_board:
        for idx, entry in enumerate(current_board):
            medal = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else f"#{idx+1}"
            st.write(f"{medal} **{entry['name']}** — {entry['score']} pts (Round {entry.get('level', 1)})")
    else:
        st.caption("No records yet. Be the first!")

    if st.button("🗑 Reset Leaderboard"):
        reset_leaderboard()
        st.success("Leaderboard cleared!")
        st.rerun()

    st.markdown("---")
    st.title("🥋 UFC Fighters (12 Superstars)")
    st.write(f"💰 Available Coins: **{st.session_state.score}**")
    for c_name, c_info in CHARACTERS.items():
        c1, c2 = st.columns([2, 1])
        c1.write(f"{c_info['icon']} **{c_name}**")
        c1.caption(f"{c_info['title']} • {c_info['price']} 🪙")
        with c2:
            if c_name in st.session_state.costumes_owned:
                if st.session_state.equipped_costume == c_name:
                    st.write("🥊 Ready")
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
                        st.error("No coins!")

    st.markdown("---")
    st.title("🔫 Armory & Weapons")
    for g_name, g_info in FF_GUNS.items():
        c1, c2 = st.columns([2, 1])
        c1.write(f"{g_info['icon']} **{g_name}** (+{g_info['bonus']} Dmg)")
        c1.caption(f"_{g_info['desc']}_")
        with c2:
            if g_name in st.session_state.guns_owned:
                if st.session_state.equipped_gun == g_name:
                    st.write("✅ Armed")
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
                        st.error("No coins!")

    st.markdown("---")
    t_choice = st.selectbox(
        "⏱ Attack Timer:", 
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

# ==========================================
# SCREEN 1: LOBBY / HOME SCREEN
# ==========================================
if not st.session_state.game_started:
    st.markdown("<h1 style='text-align: center; color: #ff3333;'>🥊 QUESTMATH: UFC ARENA ⚔️</h1>", unsafe_allow_html=True)
    st.info("""
    ### 🎯 Road To World Championship:
    * **Round 1:** Grumble Goblin *(100 HP)*
    * **Round 2:** Shadow Dragon *(180 HP)*
    * **Round 3:** Titan Mecha *(World Championship - 260 HP)*
    """)
    st.write(f"🥋 **Selected Fighter:** {hero['icon']} **{st.session_state.equipped_costume}**")
    st.write(f"🔫 **Equipped Weapon:** {gun['icon']} **{st.session_state.equipped_gun}**")
    st.write(f"⭐ **Available Coins:** {st.session_state.score} 🪙")
    st.caption("👈 Use sidebar menu on top-left to equip/buy fighters and weapons!")

    if st.button("🚀 ENTER THE OCTAGON (START FIGHT)", use_container_width=True):
        st.session_state.game_started = True
        st.session_state.player_hp = 100
        st.session_state.level = 0
        st.session_state.mon_hp = MONSTERS[0]["max_hp"]
        st.session_state.last_msg = None
        set_new_question()
        st.rerun()

# ==========================================
# SCREEN 2: FIGHT OCTAGON ARENA
# ==========================================
else:
    current_round_num = st.session_state.level + 1
    total_rounds = len(MONSTERS)

    top1, top2 = st.columns([3, 1])
    top1.markdown(f"#### 🥊 Level {current_round_num}/{total_rounds}: {curr_mon['stage']}")
    if top2.button("🚪 Exit"):
        st.session_state.game_started = False
        st.rerun()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("⭐ Coins", st.session_state.score)
    m2.metric("🔥 Streak", f"{st.session_state.streak}x")
    m3.metric("❤️ You", f"{st.session_state.player_hp}")
    m4.metric("👾 Monster", f"{st.session_state.mon_hp}")

    # KNOCKED OUT
    if st.session_state.player_hp <= 0:
        st.error(f"💀 KNOCKED OUT! Round reached: {current_round_num} | Final Score: {st.session_state.score}")
        with st.form("save_form"):
            p_name = st.text_input("Fighter Name for Leaderboard:", max_chars=14, placeholder="Enter name...")
            if st.form_submit_button("💾 Save Score"):
                if p_name.strip():
                    save_score(p_name.strip(), st.session_state.score, current_round_num)
                    st.success("Registered in Hall of Fame! 🏆")
                    st.rerun()
        if st.button("Rematch 🔄", use_container_width=True):
            st.session_state.player_hp = 100
            st.session_state.score = 0
            st.session_state.level = 0
            st.session_state.mon_hp = MONSTERS[0]["max_hp"]
            st.session_state.last_msg = None
            set_new_question()
            st.rerun()

    # ROUND WON / TITLE WON
    elif st.session_state.mon_hp <= 0:
        trigger_sound("win")
        st.balloons()
        if st.session_state.level >= total_rounds - 1:
            st.success("🏆👑 UNDISPUTED UFC WORLD CHAMPION! All 3 Rounds Complete!")
            with st.form("champ_form"):
                p_name = st.text_input("Champion Name for Leaderboard:", max_chars=14, placeholder="Enter name...")
                if st.form_submit_button("💾 Register Championship"):
                    if p_name.strip():
                        save_score(p_name.strip(), st.session_state.score + 100, 3)
                        st.success("Champion registered! 🏆")
                        st.rerun()
            if st.button("Play Again from Round 1 🔄", use_container_width=True):
                st.session_state.level = 0
                st.session_state.mon_hp = MONSTERS[0]["max_hp"]
                st.session_state.player_hp = 100
                st.session_state.game_started = False
                st.session_state.last_msg = None
                set_new_question()
                st.rerun()
        else:
            st.success(f"🎉 TKO! {curr_mon['name']} defeated!")
            if st.button(f"Next Fight: Round {current_round_num + 1} ➡️", use_container_width=True):
                st.session_state.level += 1
                st.session_state.mon_hp = MONSTERS[st.session_state.level]['max_hp']
                st.session_state.score += 50
                st.session_state.last_msg = None
                set_new_question()
                st.rerun()

    # ACTIVE COMBAT
    else:
        # Side-by-side fighter and monster images
        img_c1, img_c2 = st.columns(2)
        with img_c1:
            st.caption(f"{hero['icon']} {st.session_state.equipped_costume}")
            st.image(hero["img"], width=120)
            st.caption(f"HP: {st.session_state.player_hp}/100")
        with img_c2:
            st.caption(f"👾 {curr_mon['name']}")
            st.image(curr_mon["img"], width=120)
            st.caption(f"HP: {st.session_state.mon_hp}/{curr_mon['max_hp']}")

        st.progress(float(max(0, min(100, int(st.session_state.mon_hp * 100 / curr_mon['max_hp'])))) / 100.0)

        # Dynamic Shrinking Timer (Resets on every question via unique key)
        timer_code = f"""
        <div style="width: 100%; height: 12px; background: #374151; border-radius: 6px; overflow: hidden; margin-top: 5px;">
            <div id="tbar_{st.session_state.q_id}" style="height: 100%; width: 100%; background: #22c55e; transition: width {curr_sec}s linear, background-color {curr_sec}s linear;"></div>
        </div>
        <script>
            setTimeout(function() {{
                var el = document.getElementById("tbar_{st.session_state.q_id}");
                if (el) {{
                    el.style.width = "0%";
                    el.style.backgroundColor = "#ef4444";
                }}
            }}, 50);
        </script>
        """
        st.components.v1.html(timer_code, height=22)
        st.caption(f"⏱️ Attack Window: **{curr_sec} Seconds**")

        if st.session_state.last_msg:
            m_type, m_txt = st.session_state.last_msg
            if m_type == "hit":
                st.success(m_txt)
            else:
                st.error(m_txt)

        st.info(f"### 🔥 What is: **{st.session_state.num1} {st.session_state.symbol} {st.session_state.num2}** ?")

        # 4 Tap-to-Strike Buttons
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
                st.session_state.play_sound = "miss"
                st.session_state.last_msg = ("timeout", "⏰ TIME UP! Opponent hit back for -20 HP!")
            elif selected_ans == st.session_state.ans:
                st.session_state.play_sound = gun["type"]
                streak_bonus = st.session_state.streak * 5
                dmg = 30 + streak_bonus + gun["bonus"]
                st.session_state.mon_hp = max(0, st.session_state.mon_hp - dmg)
                st.session_state.score += 20
                st.session_state.streak += 1
                st.session_state.last_msg = ("hit", f"💥 HIT! Dealt -{dmg} Damage with {st.session_state.equipped_gun}!")
            else:
                st.session_state.streak = 0
                st.session_state.player_hp = max(0, st.session_state.player_hp - 10)
                st.session_state.play_sound = "miss"
                st.session_state.last_msg = ("wrong", f"❌ Wrong! Correct answer: {st.session_state.ans}. Countered for -10 HP!")

            set_new_question()
            st.rerun()
