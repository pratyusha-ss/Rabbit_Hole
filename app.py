import os
import streamlit as st

from ai_engine import generate_answer, get_surprise


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="The Rabbit Hole",
    page_icon="🐇",
    layout="wide",
)


# =========================================================
# CSS ONLY
# =========================================================

st.markdown(
    """
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700;800'
        '&family=Space+Grotesk:wght@500;600;700'
        '&display=swap'
    );

    .stApp {
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(145, 80, 255, 0.25),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(0, 190, 255, 0.20),
                transparent 30%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(255, 70, 170, 0.14),
                transparent 35%
            ),
            #080914;

        color: #ffffff;
    }

    header[data-testid="stHeader"] {
        background: #0d0d1c !important;
        height: 58px !important;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }

    header[data-testid="stHeader"]::before {
        content: "🐇  THE RABBIT HOLE";
        position: absolute;
        left: 28px;
        top: 14px;
        color: #ffffff !important;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 17px;
        font-weight: 800;
        letter-spacing: 1.2px;
    }

    header[data-testid="stHeader"] button {
        color: #ffffff !important;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 1.5rem;
        padding-bottom: 5rem;
    }

    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #ffffff !important;
    }

    p, label {
        font-family: 'DM Sans', sans-serif !important;
    }

    /* HERO */

    .hero {
        text-align: center;
        padding: 2rem 0 1rem;
    }

    .rabbit {
        font-size: 4.5rem;
        filter: drop-shadow(
            0 0 25px rgba(180, 100, 255, 0.7)
        );
    }

    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 4.7rem;
        font-weight: 800;
        letter-spacing: -0.07em;

        background: linear-gradient(
            90deg,
            #ffffff,
            #d8b4ff,
            #7de8ff,
            #ffffff
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-text {
        color: #d2d0df !important;
        font-size: 1.05rem;
        line-height: 1.7;
        max-width: 620px;
        margin: auto;
    }

    .eyebrow {
        color: #b89cff !important;
        font-size: 0.7rem;
        font-weight: 800;
        letter-spacing: 0.2em;
        text-transform: uppercase;
    }

    /* ANSWER */

    .answer-box {
        background:
            linear-gradient(
                135deg,
                rgba(126, 87, 194, 0.18),
                rgba(50, 150, 220, 0.10)
            );

        border: 1px solid rgba(180, 140, 255, 0.25);
        border-radius: 25px;
        padding: 2rem;
        margin: 1.5rem 0;

        box-shadow:
            0 20px 60px rgba(0,0,0,0.25);
    }

    .answer-label {
        color: #cdb6ff !important;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.16em;
    }

    /* CHOICES */

    .choice-card {
        border-radius: 22px;
        padding: 1.4rem;
        min-height: 175px;
        margin-bottom: 0.7rem;

        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.075),
                rgba(255,255,255,0.025)
            );

        border: 1px solid rgba(255,255,255,0.10);

        box-shadow:
            0 15px 45px rgba(0,0,0,0.18);
    }

    .choice-category {
        font-size: 0.68rem;
        letter-spacing: 0.15em;
        font-weight: 800;
        color: #b5a5ff !important;
    }

    .choice-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: #ffffff !important;
        margin-top: 0.5rem;
        line-height: 1.35;
    }

    .choice-description {
        color: #c6c4d2 !important;
        line-height: 1.6;
        margin-top: 0.5rem;
    }

    /* BUTTONS */

    .stButton > button {
        border-radius: 14px !important;
        border: 1px solid rgba(190,160,255,0.22) !important;
        background: rgba(255,255,255,0.055) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        min-height: 45px;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        background:
            linear-gradient(
                90deg,
                rgba(140,80,255,0.3),
                rgba(40,190,255,0.2)
            ) !important;

        border-color: rgba(200,170,255,0.6) !important;
        transform: translateY(-2px);
        color: #ffffff !important;
    }

    /* INPUT */

    .stTextInput input {
        background: #151526 !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        caret-color: #ffffff !important;

        border: 1px solid rgba(190,160,255,0.35) !important;
        border-radius: 16px !important;

        min-height: 50px;

        font-size: 1rem !important;
        font-weight: 600 !important;

        opacity: 1 !important;
    }

    .stTextInput input::placeholder {
        color: #9290a8 !important;
        -webkit-text-fill-color: #9290a8 !important;
        opacity: 1 !important;
    }

    .stTextInput input:focus {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border-color: #a57aff !important;

        box-shadow:
            0 0 20px rgba(140,90,255,0.25) !important;
    }

    /* METRICS */

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 18px;
        padding: 1rem;
    }

    div[data-testid="stMetricValue"] {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
        opacity: 1 !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #d4c7ff !important;
        font-weight: 800 !important;
        opacity: 1 !important;
    }

    /* CAPTIONS */

    .stCaption,
    [data-testid="stCaptionContainer"] {
        color: #aaa8bb !important;
    }

    /* ALERTS */

    div[data-testid="stAlert"] {
        background: rgba(126, 87, 194, 0.12) !important;
        border: 1px solid rgba(180,140,255,0.20) !important;
        color: #ffffff !important;
    }

    div[data-testid="stAlert"] p {
        color: #ffffff !important;
    }

    hr {
        border-color: rgba(255,255,255,0.08) !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "started": False,
    "topic": "",
    "answer": None,
    "path": [],
    "depth": 0,
    "xp": 0,
    "surprise": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# RESET
# =========================================================

def reset_game():
    for key, value in defaults.items():
        st.session_state[key] = value


# =========================================================
# START
# =========================================================

def start(topic):

    topic = topic.strip()

    if not topic:
        return

    with st.spinner("🐇 Opening the rabbit hole..."):

        result = generate_answer(
            topic,
            [topic]
        )

    st.session_state.started = True
    st.session_state.topic = topic
    st.session_state.answer = result
    st.session_state.path = [topic]
    st.session_state.depth = 1
    st.session_state.xp = 10
    st.session_state.surprise = None


# =========================================================
# EXPLORE
# =========================================================

def explore(choice):

    question = choice.get("title", "").strip()

    if not question:
        return

    new_path = st.session_state.path + [question]

    with st.spinner("🕳️ Falling deeper..."):

        result = generate_answer(
            question,
            new_path
        )

    st.session_state.topic = question
    st.session_state.answer = result
    st.session_state.path = new_path
    st.session_state.depth += 1
    st.session_state.xp += 15

    if st.session_state.depth % 2 == 0:

        st.session_state.surprise = get_surprise(
            st.session_state.depth
        )

    else:

        st.session_state.surprise = None


# =========================================================
# LEVEL
# =========================================================

def get_level(xp):

    if xp < 30:
        return "🌱 CURIOUS"

    if xp < 70:
        return "🔮 EXPLORER"

    if xp < 120:
        return "🧭 DEEP DIVER"

    return "🌌 RABBIT HOLE LEGEND"


# =========================================================
# TOP BAR
# =========================================================

st.caption("🐇  THE RABBIT HOLE")


# =========================================================
# LANDING PAGE
# =========================================================

if not st.session_state.started:

    st.markdown(
        '<div class="hero">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="rabbit">🐇</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-title">The Rabbit Hole</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-text">
        A game where every question has a deeper question hiding behind it.
        <br><br>
        Get the answer. Find the weird connection. Keep falling.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.caption("✦ ASK SOMETHING")

    topic = st.text_input(
        "Your question",
        placeholder="Why is space dark?",
        label_visibility="collapsed"
    )

    if st.button(
        "🐇 FALL INTO THE RABBIT HOLE",
        use_container_width=True
    ):

        if topic.strip():

            try:

                start(topic)
                st.rerun()

            except Exception as error:

                st.error(
                    f"🐇 The rabbit hole couldn't open:\n\n{error}"
                )

        else:

            st.warning("Ask a question first.")


    st.markdown("<br>", unsafe_allow_html=True)

    st.caption("TRY ONE OF THESE")

    examples = [
        "🌌 Why is space dark?",
        "💭 Why do we dream?",
        "🎵 How does music affect us?",
        "🌊 Why is the ocean blue?",
        "💻 How does a computer work?",
    ]

    cols = st.columns(5)

    for i, example in enumerate(examples):

        with cols[i]:

            if st.button(
                example,
                key=f"example_{i}",
                use_container_width=True
            ):

                try:

                    actual_question = example.split(
                        " ",
                        1
                    )[1]

                    start(actual_question)

                    st.rerun()

                except Exception as error:

                    st.error(
                        f"🐇 The rabbit hole couldn't open:\n\n{error}"
                    )


# =========================================================
# GAME
# =========================================================

else:

    answer = st.session_state.answer

    # -----------------------------------------------------
    # SAFETY CHECK
    # -----------------------------------------------------

    if answer is None:

        st.error(
            "The rabbit hole lost the current answer. "
            "Start a new question."
        )

        if st.button(
            "↩ Start again",
            use_container_width=True
        ):

            reset_game()
            st.rerun()

        st.stop()


    # -----------------------------------------------------
    # HEADER
    # -----------------------------------------------------

    left, right = st.columns([4, 1])

    with left:

        st.caption("🐇 YOUR RABBIT HOLE")

        st.title(
            st.session_state.topic
        )

    with right:

        st.metric(
            "XP",
            st.session_state.xp
        )


    st.caption(
        f"{get_level(st.session_state.xp)}  •  "
        f"Depth {st.session_state.depth}"
    )

    st.divider()


    # -----------------------------------------------------
    # ANSWER
    # -----------------------------------------------------

    st.markdown(
        '<div class="answer-box">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="answer-label">'
        '💡 HERE\'S THE ANSWER'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    # Native Streamlit text OUTSIDE the HTML card.
    # This prevents the text from ever appearing as raw HTML.

    st.write(
        answer.get(
            "answer",
            "No answer was returned."
        )
    )


    # -----------------------------------------------------
    # HOOK
    # -----------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="hook-box">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hook-title">'
        '👀 WAIT… THERE\'S MORE'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    st.write(
        answer.get(
            "hook",
            "There is more hiding underneath this."
        )
    )


    # -----------------------------------------------------
    # SURPRISE
    # -----------------------------------------------------

    if st.session_state.surprise:

        surprise = st.session_state.surprise

        st.info(
            f"✨ **Unexpected connection**\n\n"
            f"{surprise['from']} → {surprise['to']}\n\n"
            f"{surprise['connection']}"
        )


    # -----------------------------------------------------
    # CHOICES
    # -----------------------------------------------------

    st.divider()

    st.header("🕳️ Choose your next fall")

    st.caption(
        "Don't choose the 'best' answer. "
        "Choose the one you're most curious about."
    )

    choices = answer.get("choices", [])

    choices = [
        choice
        for choice in choices
        if isinstance(choice, dict)
        and choice.get("title")
    ][:3]


    if len(choices) < 3:

        st.warning(
            "The rabbit hole didn't find three paths. "
            "Try asking this question again."
        )

    else:

        cols = st.columns(3)

        for i, choice in enumerate(choices):

            with cols[i]:

                category = str(
                    choice.get(
                        "category",
                        "RABBIT HOLE"
                    )
                )

                title = str(
                    choice.get(
                        "title",
                        "Explore this connection?"
                    )
                )

                description = str(
                    choice.get(
                        "description",
                        "Follow this connection deeper."
                    )
                )


                # CARD

                st.markdown(
                    '<div class="choice-card">',
                    unsafe_allow_html=True
                )

                st.caption(category)

                st.markdown(
                    f"**{title}**"
                )

                st.write(
                    description
                )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


                # BUTTON

                if st.button(
                    "Explore this →",
                    key=f"choice_{st.session_state.depth}_{i}",
                    use_container_width=True
                ):

                    try:

                        explore(choice)

                        st.rerun()

                    except Exception as error:

                        st.error(
                            "🐇 Something went wrong while "
                            f"falling deeper:\n\n{error}"
                        )


    # -----------------------------------------------------
    # JOURNEY
    # -----------------------------------------------------

    st.divider()

    st.header("🗺️ Your Journey")

    for i, question in enumerate(
        st.session_state.path
    ):

        st.write(
            f"**{i + 1}.** {question}"
        )


    # -----------------------------------------------------
    # NEW GAME
    # -----------------------------------------------------

    st.divider()

    if st.button(
        "↩ Start a completely new question",
        use_container_width=True
    ):

        reset_game()
        st.rerun()