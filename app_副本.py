import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="🎨 Art Gallery Dashboard",
    page_icon="🖼️",
    layout="wide"
)

# -------------------------------
# Custom Styling
# -------------------------------
st.markdown("""
    <style>
        .main {
            background-color: #f9f7f3;
        }
        .stApp {
            background: linear-gradient(135deg, #fff8f0, #fdfdfd);
        }
        h1, h2, h3 {
            color: #5a3e36;
        }
        .stSidebar {
            background-color: #fff3e6;
        }
        .css-1d391kg {
            background-color: #fff3e6;
        }
        .block-container {
            padding-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Sample Data
# -------------------------------
sample_data = pd.DataFrame({
    "Title": [
        "Mona Lisa",
        "Starry Night",
        "The Persistence of Memory",
        "Girl with a Pearl Earring",
        "The Scream"
    ],
    "Artist": [
        "Leonardo da Vinci",
        "Vincent van Gogh",
        "Salvador Dalí",
        "Johannes Vermeer",
        "Edvard Munch"
    ],
    "Year": [1503, 1889, 1931, 1665, 1893],
    "Medium": [
        "Oil on poplar",
        "Oil on canvas",
        "Oil on canvas",
        "Oil on canvas",
        "Oil, tempera, pastel on cardboard"
    ],
    "Price": [850, 700, 620, 580, 670],  # in millions USD
    "Period": [
        "Renaissance",
        "Post-Impressionism",
        "Surrealism",
        "Baroque",
        "Expressionism"
    ]
})

# -------------------------------
# Session State
# -------------------------------
if "artworks" not in st.session_state:
    st.session_state.artworks = sample_data.copy()

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.header("🎨 Add New Artwork")

with st.sidebar.form("add_artwork_form"):
    title = st.text_input("🖼️ Artwork Title")
    artist = st.text_input("👩‍🎨 Artist")
    year = st.number_input("📅 Year", min_value=1000, max_value=2100, step=1)
    medium = st.text_input("🖌️ Medium")
    price = st.number_input("💰 Price (in millions USD)", min_value=0.0, step=1.0)
    period = st.selectbox(
        "🏛️ Art Period",
        ["Renaissance", "Baroque", "Romanticism", "Impressionism",
         "Post-Impressionism", "Expressionism", "Surrealism", "Modernism", "Contemporary"]
    )
    submitted = st.form_submit_button("✨ Add Artwork")

    if submitted:
        if title and artist and medium:
            new_row = pd.DataFrame([{
                "Title": title,
                "Artist": artist,
                "Year": year,
                "Medium": medium,
                "Price": price,
                "Period": period
            }])
            st.session_state.artworks = pd.concat(
                [st.session_state.artworks, new_row],
                ignore_index=True
            )
            st.sidebar.success(f"🎉 '{title}' added successfully!")
        else:
            st.sidebar.warning("⚠️ Please fill in all fields!")

# -------------------------------
# Main Title
# -------------------------------
st.title("🖼️ Art Gallery Dashboard")
st.markdown("### Discover masterpieces, track values, and curate your dream gallery ✨")

# -------------------------------
# Search Filter
# -------------------------------
search_artist = st.text_input("🔍 Search by Artist Name")

filtered_df = st.session_state.artworks[
    st.session_state.artworks["Artist"].str.contains(search_artist, case=False, na=False)
]

# -------------------------------
# Data Table
# -------------------------------
st.subheader("📋 Gallery Collection")
st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

# -------------------------------
# Charts
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Artwork Prices")
    bar_fig = px.bar(
        filtered_df,
        x="Title",
        y="Price",
        color="Artist",
        text="Price",
        template="plotly_white"
    )
    bar_fig.update_traces(textposition="outside")
    bar_fig.update_layout(
        xaxis_title="Artwork",
        yaxis_title="Price (Millions USD)",
        showlegend=False
    )
    st.plotly_chart(bar_fig, use_container_width=True)

with col2:
    st.subheader("🎭 Art Period Distribution")
    pie_fig = px.pie(
        filtered_df,
        names="Period",
        hole=0.45,
        template="plotly_white"
    )
    pie_fig.update_traces(textinfo="percent+label")
    st.plotly_chart(pie_fig, use_container_width=True)

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown("🌟 *Art is not what you see, but what you make others see.* — Edgar Degas")
