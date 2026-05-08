"""Li-12 Unified Dashboard entrypoint with role-aware Rebecca/Admin pages."""
from __future__ import annotations

import os

from dashboard_components import (
    EMPTY_TODAY_MESSAGE,
    render_behavior_correlation_widget,
    render_daily_emotions_report,
    render_learning_page,
    render_relationship_widgets,
    render_today_evidence,
    render_today_inputs,
    render_today_signals,
    render_word_count_widget,
)
from dashboard_data_loader import DASHBOARD_TIMEZONE, filter_records_for_today, get_record_inventory, load_cached_normalized_records
from dashboard_insights import build_daily_emotions_report, build_today_relationship_rating

APP_NAME = "Unified Dashboard"
REBECCA_PAGES = ["Overview", "Chats", "Journals", "Memories", "User Input", "Insights", "Bridge", "Learning"]
ADMIN_PAGES = REBECCA_PAGES + ["Letters", "Evidence", "Data Quality", "System Logs", "Admin Tools"]
ROLE_PASSWORD_ENV = {
    "Rebecca": "LI12_DASHBOARD_REBECCA_PASSWORD",
    "Admin": "LI12_DASHBOARD_ADMIN_PASSWORD",
}


def _records_by_type(records: list[dict[str, object]], record_type: str) -> list[dict[str, object]]:
    return [record for record in records if str(record.get("record_type", "")).lower() == record_type]


def _require_login() -> str | None:
    import streamlit as st

    if st.session_state.get("li12_role") in {"Rebecca", "Admin"}:
        return str(st.session_state["li12_role"])
    st.title(APP_NAME)
    role = st.radio("Role", ["Rebecca", "Admin"], horizontal=True)
    password = st.text_input("Password", type="password")
    if st.button("Log in"):
        expected = os.environ.get(ROLE_PASSWORD_ENV[role], "")
        if expected and password == expected:
            st.session_state["li12_role"] = role
            st.rerun()
        else:
            st.error("Invalid login.")
    return None


def render_overview_page(records: list[dict[str, object]], role: str) -> None:
    report = build_daily_emotions_report(records, role)
    render_daily_emotions_report(report, role)
    render_word_count_widget(records)
    today_records = report.get("today_records", [])
    if isinstance(today_records, list):
        render_relationship_widgets(today_records)


def render_chats_page(records: list[dict[str, object]]) -> None:
    import streamlit as st

    chats = _records_by_type(records, "chat")
    tabs = st.tabs(["Recent Chats", "Word Count"])
    with tabs[0]:
        if chats:
            for record in chats[:50]:
                st.markdown(f"**{record.get('timestamp', '')} · {record.get('profile', '')}**")
                st.write(record.get("excerpt", ""))
    with tabs[1]:
        render_word_count_widget(records)


def render_simple_record_page(records: list[dict[str, object]], record_type: str, title: str) -> None:
    import streamlit as st

    page_records = _records_by_type(records, record_type)
    st.title(title)
    tabs = st.tabs(["Recent", "Signals"])
    with tabs[0]:
        if page_records:
            for record in page_records[:50]:
                st.markdown(f"**{record.get('timestamp', '')} · {record.get('profile', '')}**")
                st.write(record.get("excerpt", ""))
    with tabs[1]:
        today_records = filter_records_for_today(page_records)
        if today_records:
            rating = build_today_relationship_rating(today_records)
            render_today_signals(today_records, rating)


def render_insights_page(records: list[dict[str, object]]) -> None:
    import streamlit as st

    st.title("Insights")
    tabs = st.tabs(["Signals", "Behavior Correlation"])
    with tabs[0]:
        today_records = filter_records_for_today(records)
        if today_records:
            rating = build_today_relationship_rating(today_records)
            render_today_signals(today_records, rating)
    with tabs[1]:
        render_behavior_correlation_widget(records)


def render_bridge_page(records: list[dict[str, object]], role: str, timezone_name: str = DASHBOARD_TIMEZONE) -> None:
    import streamlit as st

    st.title("Bridge")
    tabs = st.tabs(["Today", "Correlations", "Evidence"])
    today_records = filter_records_for_today(records, timezone_name)
    with tabs[0]:
        if not today_records:
            st.info(EMPTY_TODAY_MESSAGE)
            return
        report = build_daily_emotions_report(records, role)
        render_daily_emotions_report(report, role)
        render_today_inputs(today_records)
        render_relationship_widgets(today_records)
    with tabs[1]:
        render_behavior_correlation_widget(records)
    with tabs[2]:
        if today_records:
            rating = build_today_relationship_rating(today_records)
            render_today_evidence(today_records, rating)


def render_admin_page(page: str, records: list[dict[str, object]]) -> None:
    import streamlit as st

    st.title(page)
    if page == "Evidence":
        today_records = filter_records_for_today(records)
        if today_records:
            rating = build_today_relationship_rating(today_records)
            render_today_evidence(today_records, rating)
    elif page == "Data Quality":
        debug_print_record_inventory()
        st.json(get_record_inventory())
    elif page in {"System Logs", "Admin Tools", "Letters"}:
        st.caption("Admin-only area. No Rebecca-visible content is rendered here.")


def render_page(page: str, records: list[dict[str, object]], role: str) -> None:
    if page == "Overview":
        render_overview_page(records, role)
    elif page == "Chats":
        render_chats_page(records)
    elif page == "Journals":
        render_simple_record_page(records, "journal", "Journals")
    elif page == "Memories":
        render_simple_record_page(records, "memory", "Memories")
    elif page == "User Input":
        render_learning_page(role)
    elif page == "Insights":
        render_insights_page(records)
    elif page == "Bridge":
        render_bridge_page(records, role)
    elif page == "Learning":
        render_learning_page(role)
    elif role == "Admin":
        render_admin_page(page, records)


def debug_print_record_inventory() -> None:
    """Print safe loader counts for CLI debugging without exposing raw records."""
    inventory = get_record_inventory()
    print(f"candidate source files scanned: {inventory.get('candidate_source_files_scanned', 0)}")
    print(f"rejected system/project files count: {inventory.get('rejected_system_project_files_count', 0)}")
    print(f"normalized records total: {inventory.get('normalized_records_total', 0)}")
    print(f"records by type: {inventory.get('records_by_type', {})}")
    print(f"records by profile: {inventory.get('records_by_profile', {})}")
    print(f"chat records count: {inventory.get('chat_records_count', 0)}")
    print(f"journal records count: {inventory.get('journal_records_count', 0)}")
    print(f"memory records count: {inventory.get('memory_records_count', 0)}")
    print("actual source directories scanned:")
    for directory in inventory.get("actual_source_directories_scanned", []):
        print(f"- {directory}")
    print("top candidate files:")
    for path in inventory.get("top_candidate_files", []):
        print(f"- {path}")


def main() -> None:
    import streamlit as st

    st.set_page_config(page_title=APP_NAME, layout="wide")
    role = _require_login()
    if not role:
        return
    st.title(APP_NAME)
    pages = ADMIN_PAGES if role == "Admin" else REBECCA_PAGES
    page = st.sidebar.radio("Page", pages, index=0)
    if st.sidebar.button("Log out"):
        st.session_state.pop("li12_role", None)
        st.rerun()
    records = load_cached_normalized_records()
    render_page(page, records, role)


if __name__ == "__main__":
    main()
