import streamlit as st
from hasura import read_by_subject
import pandas as pd
from openai import OpenAI
import unicodedata

client = OpenAI()

st.set_page_config(
    page_title="学習指導要領コード", layout="wide", initial_sidebar_state="expanded"
)

st.title("学習指導要領コードそれっぽく割り当てツール")

st.sidebar.title("ラベル対象条件")

school = st.sidebar.selectbox(
    "学校？",
    ("2", "3", "4"),
    format_func=lambda x: ["小学校", "中学校", "高等学校"][int(x) - 2],
    index=1,
    placeholder="学校を選択してください",
)

subject = st.sidebar.selectbox(
    "どの教科？",
    ("0", "1", "2", "3", "4", "5", "6", "7", "8"),
    format_func=lambda x: [
        "総則",
        "国語",
        "社会",
        "地理歴史",
        "公民",
        "算数・数学",
        "理科",
        "生活",
        "音楽",
    ][int(x)],
    index=5,
    placeholder="教科を選択してください",
)

goal = st.sidebar.multiselect(
    "目標区分",
    ["0", "1", "2", "3", "4", "5"],
    format_func=lambda x: [
        "その他",
        "目標（大項目）",
        "目標及び内容（大項目）",
        "指導計画の作成と内容の取り扱い（大項目）",
        "内容（大項目）",
        "各科目",
    ][int(x)],
    default=["4", "5"],
)

limit = st.sidebar.number_input("最大ラベル数", min_value=1, max_value=10, value=3)

data = read_by_subject(school=school, subject=subject, goal=goal, limit=None)
st.sidebar.write(f"{len(data['data']['codes'])} 件のラベルが対象")

model = st.sidebar.selectbox(
    "モデル選択", ("gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"), index=0
)


def make_instruction(_input, _labels, limit):
    instruction = """Classify this content to non deplicated suitable {limit} labels under the content:
    {_input}
    ----
    {_labels}
    ----
    Answer format is JSON {reliability:0~1, output:[{code: , text: }]}. Even if you are not sure, qualify the reliability and recommend a proper category.
    """
    return (
        instruction.replace("{_input}", str(_input))
        .replace("{_labels}", str(_labels))
        .replace("{limit}", str(limit))
    )


def on_submit():
    data = read_by_subject(school=school, subject=subject, goal=goal, limit=None)
    labels = data["data"]["codes"]
    instruction = make_instruction(input_txt, labels, limit)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a JSON answer bot. Don't answer other words.",
            },
            {
                "role": "user",
                "content": instruction,
            },
        ],
    )

    raw_result = unicodedata.normalize("NFKC", completion.choices[0].message.content)
    result = eval(raw_result)
    if "reliability" not in result:
        st.error("エラーが発生しました {result}")
        return
    reliability = result["reliability"]
    output = result["output"]
    try:
        df = pd.DataFrame(output)
        with container:
            st.table(df)
            if reliability >= 0.9:
                st.success(f"信頼度：{reliability}", icon="✅")
            elif reliability >= 0.6:
                st.info(f"信頼度：{reliability}", icon="🤔")
            else:
                st.warning(f"信頼度：{reliability}", icon="❌")
    except Exception as e:
        st.error(f"エラーが発生しました：{e}")


with st.form(key="input_form"):
    input_txt = st.text_area(
        "問題文を入力してください",
        "-4+7を計算しなさい",
    )

    st.form_submit_button(
        label="GPTに聞く👂",
        help=None,
        on_click=on_submit,
        type="secondary",
        disabled=False,
        use_container_width=False,
    )

container = st.container(height=300, border=None)
