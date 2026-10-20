import re
import streamlit as st

st.set_page_config(
    page_title="Read & Test | English Reading Quiz",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ───────────────────────── Content ─────────────────────────

MARKETS = [
    ("St. Lawrence Market", "Toronto, Canada"),
    ("Castries Market", "St. Lucia"),
    ("Kreta Ayer Wet Market", "Singapore"),
    ("La Vucciria Market", "Palermo, Italy"),
    ("Borough Market", "London, England"),
]

PASSAGE = [
    (
        "1  St Lawrence, Toronto, Canada",
        "St Lawrence food market, in Toronto, is 200 years old. "
        "There are a lot of shops with every kind of meat and seafood.",
    ),
    (
        "2  Castries Market, St Lucia",
        "Naturally, this island in the Caribbean has a market famous for fish and fruit. "
        "Try the local sauce – it's very hot and spicy!",
    ),
    (
        "3  Kreta Ayer Wet Market, Singapore",
        "There's a lot of different food here and there's also a great restaurant upstairs. "
        "Go at around 6 a.m. and have some tasty noodles for breakfast.",
    ),
    (
        "4  La Vucciria, Palermo, Italy",
        "There aren't many markets in the world with live music. "
        "But in Palermo, musicians play and sing as shoppers buy their sausages and fresh pasta.",
    ),
    (
        "5  Borough Market, London, England",
        "Borough Market is 1,000 years old and famous with food lovers. "
        "It's open every day, but try to go early – it's very popular, "
        "so there isn't much food left by the end of the day!",
    ),
]

QUESTIONS = [
    # ── True / False ──
    {"type": "tf", "q": "St Lawrence food market is in Toronto, Canada.", "answer": "True"},
    {"type": "tf", "q": "Castries Market is famous for meat and cheese.", "answer": "False"},
    {"type": "tf", "q": "The restaurant at Kreta Ayer Wet Market is downstairs.", "answer": "False"},
    {"type": "tf", "q": "Borough Market is open every day.", "answer": "True"},
    # ── Multiple choice (choose the correct answer) ──
    {
        "type": "mc",
        "q": "How old is St Lawrence market?",
        "options": ["50 years old", "100 years old", "200 years old", "1,000 years old"],
        "answer": "200 years old",
    },
    {
        "type": "mc",
        "q": "What is very hot and spicy in Castries Market?",
        "options": ["The fruit", "The local sauce", "The noodles", "The sausages"],
        "answer": "The local sauce",
    },
    {
        "type": "mc",
        "q": "What can you hear in La Vucciria?",
        "options": ["Church bells", "Traffic", "Live music", "Radio news"],
        "answer": "Live music",
    },
    # ── Short answer ──
    {
        "type": "short",
        "q": "Name one kind of food you can buy in St Lawrence market.",
        "answer": "Meat (or seafood)",
        "accepted": ["meat", "seafood", "sea food"],
    },
    {
        "type": "short",
        "q": "What tasty food can you have for breakfast at Kreta Ayer Wet Market?",
        "answer": "Noodles",
        "accepted": ["noodles", "noodle"],
    },
    {
        "type": "short",
        "q": "How old is Borough Market?",
        "answer": "1,000 years old",
        "accepted": ["1000", "1 000", "one thousand"],
    },
]

TYPE_LABEL = {"tf": "True or False", "mc": "Choose the correct answer", "short": "Short answer"}

# ───────────────────────── Styling ─────────────────────────

GREEN = "#1F4330"
GREEN_SOFT = "#2F5A40"
CREAM = "#FBEFDF"
SAND = "#EBDDC6"
WOOD = "#D9A066"
WOOD_DARK = "#8A5A2B"
INK = "#2A2A22"

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;700;800&family=Nunito:wght@400;600;700&display=swap');

html, body, [class*="css"], .stApp {{
    font-family: 'Nunito', sans-serif;
    color: {INK};
}}
.stApp {{ background: {CREAM}; }}
#MainMenu, footer, header, [data-testid="stSidebar"], [data-testid="collapsedControl"] {{ display: none; }}
.block-container {{ padding-top: 1.2rem; padding-bottom: 3rem; max-width: 1180px; }}

h1, h2, h3, .display {{ font-family: 'Baloo 2', sans-serif; color: {GREEN}; }}

/* Buttons */
div.stButton > button, div.stFormSubmitButton > button {{
    border-radius: 999px; font-family: 'Baloo 2', sans-serif; font-weight: 700;
    font-size: 1.05rem; padding: .55rem 1.2rem; border: 2px solid transparent;
    background: {SAND}; color: {GREEN}; width: 100%;
}}
div.stButton > button:hover, div.stFormSubmitButton > button:hover {{ border-color: {GREEN}; color: {GREEN}; }}
div.stButton > button[kind="primary"], div.stFormSubmitButton > button[kind="primary"],
button[data-testid="stBaseButton-primary"], button[data-testid="stBaseButton-primaryFormSubmit"] {{
    background: {GREEN}; color: #fff; border-color: {GREEN};
}}
div.stButton > button[kind="primary"]:hover, button[data-testid="stBaseButton-primary"]:hover,
button[data-testid="stBaseButton-primaryFormSubmit"]:hover {{
    background: {GREEN_SOFT}; color: #fff; border-color: #fff;
}}
div.stButton > button:focus-visible, div.stFormSubmitButton > button:focus-visible {{
    outline: 3px solid {WOOD}; outline-offset: 2px;
}}

/* Brand bar */
.brand {{ display:flex; align-items:center; gap:.7rem; }}
.brand .logo {{ font-size:2.2rem; }}
.brand .t1 {{ font-family:'Baloo 2'; font-weight:800; font-size:1.7rem; color:{GREEN}; line-height:1; }}
.brand .t2 {{ font-size:.95rem; color:{INK}; }}

/* Hero */
.hero {{
    border-radius: 28px; padding: 2rem 1.5rem 1rem; margin-top: .8rem;
    background:
      radial-gradient(1200px 300px at 50% -10%, rgba(255,255,255,.65), transparent 60%),
      linear-gradient(180deg, #CFE0E6 0%, #F2D9B5 45%, #E8C9A0 100%);
    position: relative; overflow: hidden;
}}
.signpost {{ display:flex; flex-direction:column; gap:.55rem; }}
.sign {{
    background: linear-gradient(180deg, #E3B67F, {WOOD}); color:{INK};
    padding:.55rem 1.4rem .55rem .9rem; font-size:.92rem; line-height:1.2;
    clip-path: polygon(0 0, 92% 0, 100% 50%, 92% 100%, 0 100%);
    box-shadow: 0 2px 0 {WOOD_DARK}; border-left: 6px solid {WOOD_DARK};
}}
.sign b {{ font-family:'Baloo 2'; font-size:1.02rem; display:block; }}
.sign:nth-child(odd) {{ transform: rotate(-1.5deg); }}
.sign:nth-child(even) {{ transform: rotate(1deg); margin-left:.4rem; }}

.board {{
    background: linear-gradient(180deg, #E8BE8A, {WOOD}); border: 4px solid {WOOD_DARK};
    border-radius: 34px 34px 20px 20px; padding: 1.4rem 1rem .8rem; text-align:center;
    box-shadow: 0 6px 0 rgba(138,90,43,.35);
}}
.board h1 {{
    font-size: clamp(2.2rem, 5.5vw, 3.9rem); line-height: .95; margin:0;
    font-weight: 800; color: {GREEN}; text-transform: uppercase; letter-spacing: .01em;
}}
.board .sub {{
    background: {CREAM}; border-radius: 22px; padding:.7rem 1rem; margin:1rem auto 0;
    max-width: 90%; font-size: 1.1rem; font-weight:600;
}}
.emoji-row {{ font-size:2.6rem; text-align:center; letter-spacing:.3rem; margin-top:1rem; }}
.chalk {{
    background:#2E3A33; color:#F3F0E6; border:5px solid {WOOD_DARK}; border-radius:10px;
    padding:1rem; text-align:center; font-family:'Baloo 2'; font-size:1.3rem; transform: rotate(2deg);
}}

/* Feature strip */
.strip {{
    display:grid; grid-template-columns: repeat(4, 1fr); gap:1rem; text-align:center; margin-top:1.6rem;
}}
.strip div {{ padding:.4rem; border-right:2px solid {WOOD}; }}
.strip div:last-child {{ border-right:none; }}
.strip .ic {{ font-size:2.2rem; }}
.strip .lb {{ font-family:'Baloo 2'; font-weight:600; font-size:1.05rem; color:{GREEN}; }}
@media (max-width: 700px) {{ .strip {{ grid-template-columns: repeat(2, 1fr); }} .strip div {{ border-right:none; }} }}

/* Cards */
.card {{
    background:#fff; border:2px solid {SAND}; border-radius:22px; padding:1.3rem 1.5rem; margin-bottom:1rem;
}}
.card h3 {{ margin:0 0 .4rem; font-size:1.35rem; }}
.card p {{ font-size:1.12rem; line-height:1.75; margin:0; max-width:70ch; }}
.qtag {{
    display:inline-block; background:{SAND}; color:{GREEN}; border-radius:999px;
    padding:.1rem .8rem; font-size:.85rem; font-weight:700; margin-bottom:.4rem;
}}
.qtext {{ font-size:1.12rem; font-weight:700; margin-bottom:.3rem; }}

/* Results */
.score-ring {{
    width: 190px; height: 190px; border-radius: 50%; margin: 0 auto;
    display:flex; align-items:center; justify-content:center; flex-direction:column;
}}
.score-ring .pct {{ font-family:'Baloo 2'; font-size:3rem; font-weight:800; color:{GREEN}; line-height:1; }}
.score-ring .of {{ font-size:1rem; font-weight:700; }}
.stat {{ text-align:center; background:#fff; border:2px solid {SAND}; border-radius:20px; padding:1rem; }}
.stat .n {{ font-family:'Baloo 2'; font-size:2.2rem; font-weight:800; line-height:1; }}
.cheer {{
    background:{GREEN}; color:#fff; border-radius:22px; padding:1.2rem 1.6rem;
    font-family:'Baloo 2'; font-size:1.35rem; text-align:center; margin:1.2rem 0;
}}
.res {{ border-radius:16px; padding:.9rem 1.2rem; margin-bottom:.7rem; font-size:1.05rem; }}
.res.ok {{ background:#E6F2E4; border:2px solid #9CC79A; }}
.res.bad {{ background:#FBE5DF; border:2px solid #E3A596; }}
.res .rq {{ font-weight:700; }}
</style>
""",
    unsafe_allow_html=True,
)

# ───────────────────────── State ─────────────────────────

ss = st.session_state
ss.setdefault("page", "Home")
ss.setdefault("submitted", False)
ss.setdefault("answers", {})
ss.setdefault("version", 0)  # changes on retake so the widgets reset


def go(page: str):
    ss.page = page


def normalize(text: str) -> str:
    text = re.sub(r"[^a-z0-9 ]", " ", (text or "").lower())
    return re.sub(r"\s+", " ", text).strip()


def is_correct(q: dict, given) -> bool:
    if given is None or str(given).strip() == "":
        return False
    if q["type"] in ("tf", "mc"):
        return given == q["answer"]
    g = f" {normalize(given)} "
    return any(f" {normalize(a)} " in g for a in q["accepted"])


def grade():
    results = []
    for i, q in enumerate(QUESTIONS):
        given = ss.answers.get(i)
        results.append({"q": q, "given": given, "ok": is_correct(q, given)})
    return results


def retake():
    ss.answers = {}
    ss.submitted = False
    ss.version += 1
    ss.page = "Quiz"


# ───────────────────────── Top bar ─────────────────────────

NAV = [("Home", "🏠"), ("Read", "📖"), ("Quiz", "📝"), ("Results", "🏆")]

brand, *navcols = st.columns([2.4, 1, 1, 1, 1])
with brand:
    st.markdown(
        '<div class="brand"><div class="logo">🛒</div><div>'
        '<div class="t1">Read &amp; Test</div><div class="t2">English Reading Quiz</div>'
        "</div></div>",
        unsafe_allow_html=True,
    )
for col, (name, icon) in zip(navcols, NAV):
    with col:
        st.button(
            f"{icon} {name}",
            key=f"nav_{name}",
            type="primary" if ss.page == name else "secondary",
            on_click=go,
            args=(name,),
        )

# ───────────────────────── Page 1: Home ─────────────────────────

if ss.page == "Home":
    signs = "".join(f'<div class="sign"><b>{n}</b>({c})</div>' for n, c in MARKETS)
    left, mid, right = st.columns([1.15, 1.9, 1.05], gap="medium")

    st.markdown('<div class="hero">', unsafe_allow_html=True)
    with left:
        st.markdown(f'<div class="signpost">{signs}</div>', unsafe_allow_html=True)
        st.markdown('<div class="emoji-row">🧺🍎🍊🍇</div>', unsafe_allow_html=True)
    with mid:
        st.markdown(
            '<div class="board"><h1>Welcome to<br>the Markets!</h1>'
            '<div class="sub">Explore five amazing food markets around the world.</div></div>',
            unsafe_allow_html=True,
        )
        st.write("")
        st.button("READ NOW  →", key="read_now", type="primary", on_click=go, args=("Read",))
        st.markdown('<div class="emoji-row">🛒🥬🍅</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="chalk">Fresh Food<br>Good Mood ♡</div>', unsafe_allow_html=True)
        st.markdown('<div class="emoji-row">👩‍🍳🥖</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="strip">'
        '<div><div class="ic">🌍</div><div class="lb">Discover<br>Global Markets</div></div>'
        '<div><div class="ic">📖</div><div class="lb">Read &amp; Learn</div></div>'
        '<div><div class="ic">✅</div><div class="lb">Test Your Knowledge</div></div>'
        '<div><div class="ic">🏆</div><div class="lb">See Your Results</div></div>'
        "</div>",
        unsafe_allow_html=True,
    )

# ───────────────────────── Page 2: Read ─────────────────────────

elif ss.page == "Read":
    st.markdown("## Top 5 | Food markets")
    st.caption("Food markets are great places to find interesting local food. Here are our top five markets from around the world.")
    for title, body in PASSAGE:
        st.markdown(f'<div class="card"><h3>{title}</h3><p>{body}</p></div>', unsafe_allow_html=True)
    _, c, _ = st.columns([1, 1, 1])
    with c:
        st.button("Go Quiz Now  →", key="go_quiz", type="primary", on_click=go, args=("Quiz",))

# ───────────────────────── Page 3: Quiz ─────────────────────────

elif ss.page == "Quiz":
    st.markdown("## Quiz Time")
    st.caption("10 questions: True or False, Choose the correct answer, and Short answer.")

    if ss.submitted:
        st.info("You already submitted this quiz. You can see your results or try again.")
        c1, c2 = st.columns(2)
        c1.button("See my results", type="primary", on_click=go, args=("Results",))
        c2.button("Try again", on_click=retake)
    else:
        with st.form("quiz_form"):
            collected = {}
            for i, q in enumerate(QUESTIONS):
                key = f"q{i}_{ss.version}"
                st.markdown(
                    f'<span class="qtag">Question {i + 1} · {TYPE_LABEL[q["type"]]}</span>'
                    f'<div class="qtext">{q["q"]}</div>',
                    unsafe_allow_html=True,
                )
                if q["type"] == "tf":
                    collected[i] = st.radio(
                        q["q"], ["True", "False"], index=None, key=key,
                        horizontal=True, label_visibility="collapsed",
                    )
                elif q["type"] == "mc":
                    collected[i] = st.radio(
                        q["q"], q["options"], index=None, key=key, label_visibility="collapsed",
                    )
                else:
                    collected[i] = st.text_input(
                        q["q"], key=key, placeholder="Type your answer here",
                        label_visibility="collapsed",
                    )
                st.divider()
            submitted = st.form_submit_button("Submit answers", type="primary")

        if submitted:
            ss.answers = collected
            ss.submitted = True
            ss.page = "Results"
            st.rerun()

# ───────────────────────── Page 4: Results ─────────────────────────

elif ss.page == "Results":
    st.markdown("## Your Results")

    if not ss.submitted:
        st.warning("You haven't finished the quiz yet. Take the quiz to see your results.")
        st.button("Go to the quiz", type="primary", on_click=go, args=("Quiz",))
    else:
        results = grade()
        total = len(results)
        right_n = sum(r["ok"] for r in results)
        wrong_n = total - right_n
        pct = round(right_n / total * 100)

        if pct == 100:
            msg = "🌟 Perfect score! You are a true market expert. Amazing work!"
        elif pct >= 80:
            msg = "🎉 Excellent work! You understood the text very well. Keep it up!"
        elif pct >= 60:
            msg = "👏 Good job! You are doing well. Read once more and you will get even higher."
        elif pct >= 40:
            msg = "💪 Nice try! Every attempt makes you better. Read the text again and try once more."
        else:
            msg = "🌱 Don't give up! Learning takes time. Read the text again slowly and you will improve."

        ring = f"background: conic-gradient({GREEN} {pct * 3.6}deg, {SAND} 0);"
        c1, c2, c3 = st.columns([1.2, 1, 1], vertical_alignment="center")
        with c1:
            st.markdown(
                f'<div class="score-ring" style="{ring}"><div style="background:{CREAM};'
                f'width:150px;height:150px;border-radius:50%;display:flex;align-items:center;'
                f'justify-content:center;flex-direction:column;">'
                f'<div class="pct">{pct}%</div><div class="of">{right_n} / {total}</div></div></div>',
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f'<div class="stat"><div class="n" style="color:#2E7D32">{right_n}</div>Correct answers</div>',
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                f'<div class="stat"><div class="n" style="color:#C0392B">{wrong_n}</div>Wrong answers</div>',
                unsafe_allow_html=True,
            )

        st.markdown(f'<div class="cheer">{msg}</div>', unsafe_allow_html=True)

        wrong = [(i, r) for i, r in enumerate(results, 1) if not r["ok"]]
        right = [(i, r) for i, r in enumerate(results, 1) if r["ok"]]

        st.markdown("### ❌ Wrong answers")
        if not wrong:
            st.success("No wrong answers. Great job!")
        for i, r in wrong:
            given = r["given"] if r["given"] not in (None, "") else "No answer"
            st.markdown(
                f'<div class="res bad"><div class="rq">{i}. {r["q"]}</div>'
                f'Your answer: <b>{given}</b><br>Correct answer: <b>{r["q"]["answer"]}</b></div>',
                unsafe_allow_html=True,
            )

        st.markdown("### ✅ Correct answers")
        if not right:
            st.info("No correct answers this time. Try again!")
        for i, r in right:
            st.markdown(
                f'<div class="res ok"><div class="rq">{i}. {r["q"]}</div>'
                f'Your answer: <b>{r["given"]}</b></div>',
                unsafe_allow_html=True,
            )

        b1, b2 = st.columns(2)
        b1.button("📖 Read again", on_click=go, args=("Read",))
        b2.button("🔁 Try the quiz again", type="primary", on_click=retake)
