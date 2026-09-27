import streamlit as st
import random

# --------------------------------
# 기본 설정
# --------------------------------

st.set_page_config(
    page_title="Eco Life",
    page_icon="🌱",
    layout="wide"
)

# --------------------------------
# 게임 데이터
# --------------------------------

ACTIONS = {
    "🚲 자전거 타기": {
        "coin": 20,
        "exp": 15,
        "message": "자동차 대신 자전거를 이용했어요!"
    },
    "🥤 텀블러 사용": {
        "coin": 10,
        "exp": 10,
        "message": "일회용 컵을 줄였어요!"
    },
    "♻️ 분리배출": {
        "coin": 15,
        "exp": 12,
        "message": "쓰레기를 올바르게 분리배출했어요!"
    },
    "💡 전기 절약": {
        "coin": 10,
        "exp": 8,
        "message": "사용하지 않는 전등을 껐어요!"
    },
    "🌳 나무 심기": {
        "coin": 30,
        "exp": 25,
        "message": "나무를 심어 지구를 도왔어요!"
    }
}

ITEMS = {
    "🌳 나무 모자": {
        "price": 30,
        "type": "hat"
    },
    "🌸 꽃 장식": {
        "price": 20,
        "type": "accessory"
    },
    "🕶️ 환경 지킴이 선글라스": {
        "price": 50,
        "type": "accessory"
    },
    "👕 초록 티셔츠": {
        "price": 40,
        "type": "clothes"
    },
    "🌎 지구 망토": {
        "price": 100,
        "type": "cape"
    }
}

# --------------------------------
# 게임 상태 초기화
# --------------------------------

if "coin" not in st.session_state:
    st.session_state.coin = 0

if "exp" not in st.session_state:
    st.session_state.exp = 0

if "level" not in st.session_state:
    st.session_state.level = 1

if "owned_items" not in st.session_state:
    st.session_state.owned_items = []

if "equipped_items" not in st.session_state:
    st.session_state.equipped_items = []

if "history" not in st.session_state:
    st.session_state.history = []

# --------------------------------
# 레벨 계산
# --------------------------------

def check_level_up():

    required_exp = st.session_state.level * 100

    if st.session_state.exp >= required_exp:

        st.session_state.exp -= required_exp
        st.session_state.level += 1

        st.balloons()

        st.success(
            f"🎉 레벨 업! 이제 레벨 {st.session_state.level}입니다!"
        )


# --------------------------------
# 환경 행동 실행
# --------------------------------

def do_action(action_name):

    action = ACTIONS[action_name]

    st.session_state.coin += action["coin"]
    st.session_state.exp += action["exp"]

    st.session_state.history.append({
        "action": action_name,
        "coin": action["coin"],
        "exp": action["exp"]
    })

    check_level_up()

    st.success(
        f"{action['message']} "
        f"+{action['coin']} 🌱 코인!"
    )


# --------------------------------
# 아이템 구매
# --------------------------------

def buy_item(item_name):

    item = ITEMS[item_name]

    if item_name in st.session_state.owned_items:

        st.warning("이미 가지고 있는 아이템이에요!")

        return

    if st.session_state.coin < item["price"]:

        st.error("코인이 부족해요!")

        return

    st.session_state.coin -= item["price"]

    st.session_state.owned_items.append(item_name)

    st.success(
        f"{item_name} 구매 완료! 🎉"
    )


# --------------------------------
# 아이템 장착
# --------------------------------

def equip_item(item_name):

    if item_name not in st.session_state.owned_items:

        st.error("먼저 아이템을 구매해주세요.")

        return

    if item_name in st.session_state.equipped_items:

        st.session_state.equipped_items.remove(item_name)

        st.info(
            f"{item_name} 장착을 해제했어요."
        )

    else:

        st.session_state.equipped_items.append(item_name)

        st.success(
            f"{item_name} 장착 완료!"
        )


# --------------------------------
# 제목
# --------------------------------

st.title("🌱 Eco Life")
st.subheader("환경을 지키고, 나만의 캐릭터를 꾸며보세요!")

# --------------------------------
# 상태 표시
# --------------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "🌱 Eco Coin",
        st.session_state.coin
    )

with col2:

    st.metric(
        "⭐ Level",
        st.session_state.level
    )

with col3:

    st.metric(
        "✨ EXP",
        st.session_state.exp
    )

st.divider()

# --------------------------------
# 탭
# --------------------------------

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🌍 환경 행동",
        "🏪 상점",
        "🧑 캐릭터",
        "📊 나의 기록"
    ]
)

# =================================
# 환경 행동
# =================================

with tab1:

    st.header("🌍 오늘의 환경 행동")

    st.write(
        "실제로 실천한 환경보호 행동을 선택해보세요!"
    )

    for action_name, action_data in ACTIONS.items():

        col1, col2 = st.columns([4, 1])

        with col1:

            st.write(
                f"### {action_name}"
            )

            st.write(
                f"보상: +{action_data['coin']} 🌱 "
                f"+{action_data['exp']} EXP"
            )

        with col2:

            if st.button(
                "실천!",
                key=f"action_{action_name}"
            ):

                do_action(action_name)


# =================================
# 상점
# =================================

with tab2:

    st.header("🏪 Eco Shop")

    st.write(
        "모은 코인으로 캐릭터 아이템을 구매하세요!"
    )

    for item_name, item_data in ITEMS.items():

        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:

            st.write(
                f"### {item_name}"
            )

        with col2:

            st.write(
                f"{item_data['price']} 🌱"
            )

        with col3:

            if st.button(
                "구매",
                key=f"buy_{item_name}"
            ):

                buy_item(item_name)


# =================================
# 캐릭터
# =================================

with tab3:

    st.header("🧑 나의 캐릭터")

    st.markdown(
        """
        <div style="
            border: 2px solid #dddddd;
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            font-size: 80px;
        ">
        🧑
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    st.subheader("✨ 장착한 아이템")

    if len(st.session_state.equipped_items) == 0:

        st.info(
            "아직 장착한 아이템이 없어요."
        )

    else:

        for item in st.session_state.equipped_items:

            st.write(
                f"✨ {item}"
            )

    st.divider()

    st.subheader("🎒 보유 아이템")

    if len(st.session_state.owned_items) == 0:

        st.info(
            "아직 아이템이 없어요. "
            "환경 행동을 해서 코인을 모아보세요!"
        )

    else:

        for item in st.session_state.owned_items:

            col1, col2 = st.columns([3, 1])

            with col1:

                st.write(item)

            with col2:

                if st.button(
                    "장착/해제",
                    key=f"equip_{item}"
                ):

                    equip_item(item)


# =================================
# 기록
# =================================

with tab4:

    st.header("📊 나의 환경 실천 기록")

    if len(st.session_state.history) == 0:

        st.info(
            "아직 기록이 없습니다."
        )

    else:

        total_coin = sum(
            item["coin"]
            for item in st.session_state.history
        )

        total_actions = len(
            st.session_state.history
        )

        st.metric(
            "🌍 실천 횟수",
            total_actions
        )

        st.metric(
            "🌱 총 획득 코인",
            total_coin
        )

        st.subheader("최근 활동")

        for item in reversed(
            st.session_state.history
        ):

            st.write(
                f"{item['action']} "
                f"+{item['coin']} 🌱 "
                f"+{item['exp']} EXP"
)
