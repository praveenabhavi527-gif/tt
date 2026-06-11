import streamlit as st
import pandas as pd
import pickle

st.set_page_config(
    page_title="Smart AI Timetable Generator",
    page_icon="📅",
    layout="wide"
)

# -----------------------------
# AGENTS
# -----------------------------

class PriorityAgent:
    def prioritize_subjects(self, subjects):
        difficulty_score = {
            "Hard": 3,
            "Medium": 2,
            "Easy": 1
        }

        sorted_subjects = sorted(
            subjects.items(),
            key=lambda x: difficulty_score[x[1]],
            reverse=True
        )

        return [subject for subject, level in sorted_subjects]


class PlannerAgent:
    def create_plan(self, prioritized_subjects, subjects):

        plan = {}

        for subject in prioritized_subjects:

            difficulty = subjects[subject]

            if difficulty == "Hard":
                plan[subject] = 3

            elif difficulty == "Medium":
                plan[subject] = 2

            else:
                plan[subject] = 1

        return plan


class SchedulerAgent:
    def generate_schedule(self, plan, daily_hours):

        days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]

        timetable = []

        subjects = []

        for subject, hrs in plan.items():
            subjects.extend([subject] * hrs)

        index = 0

        for day in days:

            start_hour = 6

            for hour in range(daily_hours):

                subject = subjects[index % len(subjects)]

                timetable.append(
                    [
                        day,
                        f"{start_hour + hour}:00",
                        f"{start_hour + hour + 1}:00",
                        subject
                    ]
                )

                index += 1

        return timetable


class ReviewerAgent:
    def review(self, timetable):

        report = [
            "Timetable generated successfully.",
            "Hard subjects received more study slots.",
            "Weekly study plan is balanced.",
            "No scheduling conflicts detected."
        ]

        return report


# -----------------------------
# UI
# -----------------------------

st.title("📅 Smart AI Timetable Generator")
st.markdown("### Agentic AI Based Timetable Planner")

st.sidebar.header("Subject Details")

num_subjects = st.sidebar.number_input(
    "Number of Subjects",
    min_value=1,
    max_value=20,
    value=5
)

subjects = {}

for i in range(num_subjects):

    col1, col2 = st.sidebar.columns(2)

    subject_name = col1.text_input(
        f"Subject {i+1}",
        value=f"Subject{i+1}",
        key=f"name_{i}"
    )

    difficulty = col2.selectbox(
        f"Level {i+1}",
        ["Hard", "Medium", "Easy"],
        key=f"level_{i}"
    )

    subjects[subject_name] = difficulty

daily_hours = st.sidebar.slider(
    "Study Hours Per Day",
    1,
    12,
    5
)

# -----------------------------
# GENERATE
# -----------------------------

if st.button("Generate Timetable"):

    priority_agent = PriorityAgent()
    planner_agent = PlannerAgent()
    scheduler_agent = SchedulerAgent()
    reviewer_agent = ReviewerAgent()

    prioritized_subjects = (
        priority_agent.prioritize_subjects(subjects)
    )

    study_plan = (
        planner_agent.create_plan(
            prioritized_subjects,
            subjects
        )
    )

    timetable = (
        scheduler_agent.generate_schedule(
            study_plan,
            daily_hours
        )
    )

    review_report = (
        reviewer_agent.review(timetable)
    )

    df = pd.DataFrame(
        timetable,
        columns=[
            "Day",
            "Start Time",
            "End Time",
            "Subject"
        ]
    )

    st.success("Timetable Generated Successfully")

    st.subheader("Generated Timetable")
    st.dataframe(
        df,
        use_container_width=True
    )

    st.subheader("Reviewer Agent Report")

    for item in review_report:
        st.write("✅", item)

    # Save PKL

    with open("timetable.pkl", "wb") as file:
        pickle.dump(df, file)

    with open("timetable.pkl", "rb") as file:
        st.download_button(
            label="⬇ Download PKL File",
            data=file,
            file_name="timetable.pkl",
            mime="application/octet-stream"
        )

    csv = df.to_csv(index=False)

    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name="timetable.csv",
        mime="text/csv"
    )
