# ui/app.py

import json
from pathlib import Path
from typing import Any

import requests
import streamlit as st

from feedback import save_feedback

# --------------------------------------------------
# PATHS AND CONFIGURATION
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]

RECORDS_CANDIDATES = [
    ROOT / "9" / "data" / "records.json",
    ROOT / "day9" / "data" / "records.json",
    ROOT / "data" / "records.json",
]

DEFAULT_API = "http://127.0.0.1:8000"

# --------------------------------------------------
# STREAMLIT PAGE
# --------------------------------------------------

st.set_page_config(
    page_title="GSTSaral",
    page_icon="🧾",
    layout="centered",
)

st.title("🧾 GSTSaral")
st.caption(
    "GST Assistant | RAG + Agent | Checkpoint 2"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .warning-strip {
        background-color: #fff3cd;
        color: #664d03;
        border: 1px solid #ffecb5;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }

    .signature {
        text-align: center;
        color: gray;
        font-size: 14px;
        margin-top: 30px;
        padding: 15px;
        border-top: 1px solid #ddd;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("Settings")

    api_base = st.text_input(
        "Backend URL",
        value=DEFAULT_API,
    ).strip().rstrip("/")

    mode = st.radio(
        "Select chatbot mode",
        [
            "RAG (/ask)",
            "Agent (/agent)",
        ],
    )

    top_k = st.slider(
        "Number of retrieved records",
        min_value=1,
        max_value=10,
        value=3,
    )

    config = st.selectbox(
        "Retrieval configuration",
        ["A", "B"],
    )

    use_graph = True

    if mode == "Agent (/agent)":

        use_graph = st.checkbox(
            "Use LangGraph workflow",
            value=True,
        )

    if st.button("Clear conversation"):

        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.caption(
        "GSTSaral Checkpoint 2"
    )

# --------------------------------------------------
# LOAD GST RECORDS
# --------------------------------------------------

@st.cache_data
def load_records():

    for file_path in RECORDS_CANDIDATES:

        if file_path.exists():

            try:

                with open(
                    file_path,
                    "r",
                    encoding="utf-8",
                ) as file:

                    return json.load(file)

            except Exception:

                continue

    return []

records = load_records()

# --------------------------------------------------
# FIND RECORD FROM CITATION
# --------------------------------------------------

def record_for_citation(citation):

    record_id = citation.get(
        "record_id",
        "",
    )

    # Day 9 uses record IDs based on
    # the original record index.

    try:

        index = int(record_id) - 1

        if 0 <= index < len(records):

            return records[index]

    except (ValueError, TypeError):

        pass

    # Fallback matching using topic/title.

    title = str(
        citation.get("title", "")
    ).lower()

    for record in records:

        topic = str(
            record.get("item_or_topic", "")
        ).lower()

        if topic and topic in title:

            return record

    return None

# --------------------------------------------------
# OLD VS CURRENT RULE WARNING
# --------------------------------------------------

def show_old_current_warning(citations):

    if not citations:

        return

    already_shown = set()

    for citation in citations:

        record = record_for_citation(
            citation
        )

        if not record:

            continue

        old_rule = record.get(
            "old_rule"
        )

        new_rule = record.get(
            "new_rule"
        )

        topic = record.get(
            "item_or_topic",
            citation.get("title", "GST topic"),
        )

        effective_date = record.get(
            "effective_from"
        )

        faq_date = (
            record.get("faq_date")
            or record.get("publication_date")
            or record.get("date")
        )

        if not old_rule or not new_rule:

            continue

        if old_rule == new_rule:

            continue

        if topic in already_shown:

            continue

        already_shown.add(topic)

        # Yellow warning strip.

        st.markdown(
            f"""
            <div class="warning-strip">

            ⚠️ <b>Old vs Current Rule</b><br><br>

            <b>Topic:</b> {topic}<br>

            <b>Older rule:</b> {old_rule}<br>

            <b>Newer rule:</b> {new_rule}<br>

            <b>Effective date:</b>
            {effective_date or "Not specified"}

            </div>
            """,
            unsafe_allow_html=True,
        )

        # Historical FAQ date.

        if faq_date:

            st.info(
                f"This FAQ is from {faq_date}. "
                f"A newer rule is available."
            )

        else:

            st.caption(
                "Historical FAQ publication date "
                "is not available in the dataset."
            )

        # Older source citation.

        old_url = (
            record.get("old_source_url")
            or citation.get("source_url")
        )

        # Newer source citation.

        new_url = record.get(
            "source_url"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                "**Older rule source**"
            )

            if old_url:

                st.markdown(
                    f"[View older source]({old_url})"
                )

            else:

                st.caption(
                    "Older source URL not available."
                )

        with col2:

            st.markdown(
                "**Newer rule source**"
            )

            if new_url:

                st.markdown(
                    f"[View current source]({new_url})"
                )

            else:

                st.caption(
                    "Newer source URL not available."
                )

# --------------------------------------------------
# CITATIONS
# --------------------------------------------------

def show_citations(citations):

    if not citations:

        st.caption(
            "No citations available."
        )

        return

    with st.expander(
        "📚 Sources and citations",
        expanded=True,
    ):

        for number, citation in enumerate(
            citations,
            start=1,
        ):

            title = citation.get(
                "title",
                "GST Record",
            )

            source = citation.get(
                "source",
                "Unknown source",
            )

            page = citation.get(
                "page",
                "Not specified",
            )

            record_id = citation.get(
                "record_id",
                "Unknown",
            )

            source_url = citation.get(
                "source_url",
                "",
            )

            st.markdown(
                f"**[{number}] {title}**"
            )

            st.caption(
                f"Source: {source} | "
                f"Page: {page} | "
                f"Record ID: {record_id}"
            )

            if source_url:

                st.markdown(
                    f"[Open source document]({source_url})"
                )

            st.divider()

# --------------------------------------------------
# API REQUEST
# --------------------------------------------------

def ask_backend(question):

    if mode == "RAG (/ask)":

        endpoint = "/ask"

        payload = {
            "question": question,
            "top_k": top_k,
            "config": config,
        }

    else:

        endpoint = "/agent"

        payload = {
            "question": question,
            "top_k": top_k,
            "config": config,
            "use_graph": use_graph,
        }

    response = requests.post(
        api_base + endpoint,
        json=payload,
        timeout=120,
    )

    response.raise_for_status()

    return response.json()

# --------------------------------------------------
# EXTRACT ANSWER AND CITATIONS
# --------------------------------------------------

def extract_response(data):

    answer = data.get(
        "answer",
        "No answer returned.",
    )

    citations = data.get(
        "citations",
        [],
    )

    # Agent may return RAG data inside answer.

    if isinstance(answer, dict):

        nested_answer = answer.get(
            "answer",
            answer,
        )

        nested_citations = answer.get(
            "citations",
            [],
        )

        if nested_citations:

            citations = nested_citations

        answer = nested_answer

    if isinstance(answer, dict):

        answer = json.dumps(
            answer,
            ensure_ascii=False,
            indent=2,
        )

    return str(answer), citations

# --------------------------------------------------
# CHAT HISTORY
# --------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []

# Display previous messages.

for index, message in enumerate(
    st.session_state.messages
):

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        if message.get("citations"):

            show_citations(
                message["citations"]
            )

            show_old_current_warning(
                message["citations"]
            )

        # Feedback buttons.

        if (
            message["role"] == "assistant"
            and message.get("question")
        ):

            if message.get(
                "feedback_saved"
            ):

                st.caption(
                    "✅ Feedback saved"
                )

            else:

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "👍 Helpful",
                        key=f"up_{index}",
                    ):

                        save_feedback(
                            message["question"],
                            message["content"],
                            "up",
                            mode,
                        )

                        message[
                            "feedback_saved"
                        ] = True

                        st.rerun()

                with col2:

                    if st.button(
                        "👎 Not helpful",
                        key=f"down_{index}",
                    ):

                        save_feedback(
                            message["question"],
                            message["content"],
                            "down",
                            mode,
                        )

                        message[
                            "feedback_saved"
                        ] = True

                        st.rerun()

# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

question = st.chat_input(
    "Ask your GST question here..."
)

if question:

    # Save user question.

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    # Generate assistant answer.

    with st.chat_message("assistant"):

        with st.spinner(
            "Searching GST records..."
        ):

            try:

                data = ask_backend(
                    question
                )

                answer, citations = (
                    extract_response(data)
                )

                st.markdown(answer)

                if citations:

                    show_citations(
                        citations
                    )

                    show_old_current_warning(
                        citations
                    )

                # Save response.

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "question": question,
                        "citations": citations,
                        "feedback_saved": False,
                    }
                )

            except requests.exceptions.ConnectionError:

                error_message = (
                    "❌ Cannot connect to GSTSaral backend. "
                    "Please start the Day 9 API first."
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                        "question": question,
                    }
                )

            except requests.exceptions.HTTPError as error:

                error_message = (
                    f"Backend HTTP error: {error}"
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                        "question": question,
                    }
                )

            except Exception as error:

                error_message = (
                    f"Error: {error}"
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                        "question": question,
                    }
                )

# --------------------------------------------------
# SIGNATURE
# --------------------------------------------------

st.markdown(
    """
    <div class="signature">

    GSTSaral · Sanjivani SJ-36<br>

    Checkpoint 2 | RAG + Agent + Feedback

    </div>
    """,
    unsafe_allow_html=True,
)