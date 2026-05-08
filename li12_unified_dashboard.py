"""Li-12 unified dashboard entrypoint.

Rebecca's Bridge page uses only actual cached project records and renders today's
relationship weather without exposing backend metadata.
"""
from __future__ import annotations

from dashboard_components import (
    EMPTY_TODAY_MESSAGE,
    render_today_evidence,
    render_today_inputs,
    render_today_rating_card,
    render_today_signals,
)
from dashboard_data_loader import (
    DASHBOARD_TIMEZONE,
    filter_records_for_today,
    get_record_inventory,
    get_today_bounds,
    load_cached_normalized_records,
)
from dashboard_insights import build_today_bridge_summary, build_today_relationship_rating


def render_bridge_page(timezone_name: str = DASHBOARD_TIMEZONE) -> None:
    import streamlit as st

    st.title("Rebecca Bridge")
    records = load_cached_normalized_records()
    today_records = filter_records_for_today(records, timezone_name)
    if not today_records:
        st.info(EMPTY_TODAY_MESSAGE)
        return

    rating = build_today_relationship_rating(today_records)
    render_today_rating_card(rating)
    st.markdown("### Short Summary")
    st.write(build_today_bridge_summary(today_records, rating))
    render_today_inputs(today_records)
    render_today_signals(today_records, rating)
    render_today_evidence(today_records, rating)


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
    for directory in inventory.get('actual_source_directories_scanned', []):
        print(f"- {directory}")
    print("top candidate files:")
    for path in inventory.get('top_candidate_files', []):
        print(f"- {path}")


def main() -> None:
    import streamlit as st

    st.set_page_config(page_title="Li-12 Unified Dashboard", layout="wide")
    page = st.sidebar.radio("Page", ["Bridge"], index=0)
    if page == "Bridge":
        render_bridge_page()


if __name__ == "__main__":
    main()
