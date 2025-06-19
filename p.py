import streamlit as st


class ENTConsultationSystem:
    def __init__(self):
        self.symptoms = ["眩暈", "鼻部症狀", "耳部症狀", "喉部症狀"]
        self.question_flows = {
            "眩暈": self.dizziness_questions,
            "鼻部症狀": self.nasal_questions,
            "耳部症狀": self.ear_questions,
            "喉部症狀": self.throat_questions
        }
        self.diagnosis = []  # 儲存可能的診斷結果

    def start(self):
        st.title("🌟 耳鼻喉科問診系統")
        st.markdown(
            "<h3 style='text-align: center; color: #4CAF50;'>快速且專業地了解您的症狀</h3>",
            unsafe_allow_html=True,
        )
        # 初始化Session State
        if "current_symptom" not in st.session_state:
            st.session_state.current_symptom = None
            st.session_state.question_index = 0
            st.session_state.diagnosis = []

        # 如果沒有選擇症狀，顯示選擇頁面
        if st.session_state.current_symptom is None:
            st.markdown("<h4 style='color: #FF5733;'>請選擇需要詢問的症狀類別：</h4>", unsafe_allow_html=True)
            selected_symptom = st.selectbox("選擇症狀類別：", self.symptoms)
            if st.button("開始問診 🚀"):
                st.session_state.current_symptom = selected_symptom
                st.session_state.question_index = 0
                st.session_state.diagnosis = []
        else:
            self.question_flows[st.session_state.current_symptom]()

    def dizziness_questions(self):
        questions = [
            {
                "問題": "您的職業是什麼？",
                "選項": ["油漆工", "加油工", "飛機引擎技工", "其他"],
                "診斷": "可能與有機溶劑暴露相關"
            },
            {
                "問題": "您是否有家族病史（如美尼爾氏症或偏頭痛）？",
                "選項": ["是", "否"],
                "診斷": "美尼爾氏症"
            },
            {
                "問題": "您的眩暈發作時間有多長？",
                "選項": ["幾秒", "幾小時", "幾天"],
                "診斷": ["良性陣發性頭位眩暈症（BPPV）", "美尼爾氏症", "前庭神經炎"]
            }
        ]
        self.single_question(questions, "眩暈")

    def nasal_questions(self):
        questions = [
            {
                "問題": "您是否有流鼻水？若有，鼻水顏色是什麼？",
                "選項": ["透明", "黃色", "其他"],
                "診斷": ["過敏性鼻炎", "急性鼻竇炎", None]
            },
            {
                "問題": "您是否經常感到鼻塞？",
                "選項": ["是", "否"],
                "診斷": "鼻中隔彎曲或鼻炎"
            }
        ]
        self.single_question(questions, "鼻部症狀")

    def ear_questions(self):
        questions = [
            {
                "問題": "您是否有耳痛？",
                "選項": ["是", "否"],
                "診斷": "外耳炎或急性中耳炎"
            }
        ]
        self.single_question(questions, "耳部症狀")

    def throat_questions(self):
        questions = [
            {
                "問題": "您是否有喉嚨疼痛？",
                "選項": ["是", "否"],
                "診斷": "急性咽炎或扁桃腺炎"
            }
        ]
        self.single_question(questions, "喉部症狀")

    def single_question(self, questions, symptom_category):
        question_index = st.session_state.question_index
        question = questions[question_index]

        # 顯示問題和選項
        st.subheader(f"👉 {symptom_category}問診")
        answer = st.radio(question["問題"], question["選項"])

        if st.button("下一題 ➡️"):
            # 根據回答保存診斷
            if isinstance(question["診斷"], list):
                diagnosis = question["診斷"][question["選項"].index(answer)]
                if diagnosis:
                    st.session_state.diagnosis.append(diagnosis)
            elif answer == "是":
                st.session_state.diagnosis.append(question["診斷"])

            # 移動到下一題或結束
            st.session_state.question_index += 1
            if st.session_state.question_index >= len(questions):
                st.session_state.current_symptom = None  # 重置症狀
                st.session_state.show_diagnosis = True  # 顯示診斷結果

    def display_diagnosis(self):
        st.title("🩺 診斷結果")
        st.markdown(
            "<h3 style='text-align: center; color: #6A1B9A;'>以下是根據問診結果的診斷：</h3>",
            unsafe_allow_html=True,
        )
        if st.session_state.diagnosis:
            for d in st.session_state.diagnosis:
                st.success(f"- {d}")
        else:
            st.warning("未發現任何相關疾病。")

        if st.button("重新開始問診 🔄"):
            st.session_state.current_symptom = None
            st.session_state.show_diagnosis = False


if __name__ == "__main__":
    if "show_diagnosis" not in st.session_state:
        st.session_state.show_diagnosis = False

    system = ENTConsultationSystem()
    if st.session_state.show_diagnosis:
        system.display_diagnosis()
    else:
        system.start()
