# ========== IMPORTS ==========  
import streamlit as st  
import plotly.express as px  

# ========== PAGE CONFIG ==========  
st.set_page_config(  
    page_title="Ultimate Converter",  
    page_icon="📊",  
    layout="wide"  
)  

# ========== PREMIUM CSS ==========  
st.markdown("""  
<style>  
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');  

    :root {  
        --primary: linear-gradient(135deg, #6366f1 0%, #3b82f6 100%);  
        --background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);  
        --card-bg: rgba(255, 255, 255, 0.9);  
        --text: #1e293b;  
        --shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);  
    }  

    [data-theme="dark"] {  
        --primary: linear-gradient(135deg, #818cf8 0%, #60a5fa 100%);  
        --background: linear-gradient(145deg, #0f172a 0%, #1e293b 100%);  
        --card-bg: rgba(30, 41, 59, 0.9);  
        --text: #f8fafc;  
        --shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);  
    }  

    * {  
        font-family: 'Poppins', sans-serif !important;  
    }  

    .stApp {  
        background-image: var(--background);  
        color: var(--text);  
        min-height: 100vh;  
    }  

    .custom-card {  
        background: var(--card-bg) !important;  
        border-radius: 15px;  
        padding: 2rem;  
        margin: 1.5rem 0;  
        box-shadow: var(--shadow);  
        backdrop-filter: blur(10px);  
        border: 1px solid rgba(255, 255, 255, 0.1);  
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);  
    }  

    .custom-card:hover {  
        transform: translateY(-5px);  
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);  
    }  

    .stButton>button {  
        background-image: var(--primary) !important;  
        color: white !important;  
        border-radius: 12px !important;  
        padding: 0.75rem 2rem !important;  
        border: none !important;  
        font-weight: 500 !important;  
        transition: all 0.3s ease !important;  
    }  

    .stButton>button:hover {  
        opacity: 0.9;  
        transform: scale(1.05);  
        box-shadow: var(--shadow);  
    }  

    .stSelectbox>div>div {  
        background: var(--card-bg) !important;  
        border: 1px solid rgba(255, 255, 255, 0.1) !important;  
        border-radius: 12px !important;  
    }  

    .stNumberInput>div>div {  
        background: var(--card-bg) !important;  
        border-radius: 12px !important;  
    }  

    .stSuccess {  
        background: rgba(16, 185, 129, 0.1) !important;  
        border-left: 4px solid #10b981 !important;  
        border-radius: 8px !important;  
    }  

    ::-webkit-scrollbar {  
        width: 8px;  
    }  
    ::-webkit-scrollbar-track {  
        background: var(--card-bg);  
    }  
    ::-webkit-scrollbar-thumb {  
        background: var(--text);  
        border-radius: 4px;  
    }  
</style>  
""", unsafe_allow_html=True)  

# ========== UNIT DATABASE ==========  
UNIT_DB = {  
    # Length  
    "Meters": 1,  
    "Centimeters": 0.01,  
    "Millimeters": 0.001,  
    "Kilometers": 1000,  
    "Feet": 0.3048,  
    "Inches": 0.0254,  
    "Miles": 1609.34,  

    # Temperature  
    "Celsius": {"to_f": lambda c: (c * 9/5) + 32},  
    "Fahrenheit": {"to_c": lambda f: (f - 32) * 5/9},  

    # Digital Storage  
    "Bytes": 1,  
    "KB": 1024,  
    "MB": 1024**2,  
    "GB": 1024**3,  

    # Weight  
    "Kilograms": 1,  
    "Grams": 0.001,  
    "Pounds": 0.453592  
}  

# ========== CORE FUNCTIONS ==========  
def convert_units(value, from_unit, to_unit):  
    try:  
        if from_unit == "Celsius" and to_unit == "Fahrenheit":  
            return UNIT_DB["Celsius"]["to_f"](value)  
        elif from_unit == "Fahrenheit" and to_unit == "Celsius":  
            return UNIT_DB["Fahrenheit"]["to_c"](value)  
        return value * (UNIT_DB[from_unit] / UNIT_DB[to_unit])  
    except KeyError:  
        st.error("❌ Invalid unit selection!")  
        return None  

# ========== APP STATE MANAGEMENT ==========  
if "history" not in st.session_state:  
    st.session_state.history = []  

# ========== MAIN INTERFACE ==========  
st.title("📐 Ultimate Unit Converter")  

# Theme Selector  
theme = st.selectbox("🌓 Theme", ["Light ☀️", "Dark 🌙"], index=0)  

# Conversion Panel  
with st.container():  
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)  
    
    cols = st.columns([3,3,3,1])  
    with cols[0]:  
        value = st.number_input("📏 Value", min_value=0.0)  
    with cols[1]:  
        from_unit = st.selectbox("🔁 From", list(UNIT_DB.keys()))  
    with cols[2]:  
        to_unit = st.selectbox("🎯 To", list(UNIT_DB.keys()))  
    with cols[3]:  
        if st.button("🔄 Swap", help="Swap units"):  
            from_unit, to_unit = to_unit, from_unit  
    
    if st.button("✨ Convert Now", type="primary"):  
        result = convert_units(value, from_unit, to_unit)  
        if result:  
            st.success(f"""  
            **✅ Conversion Successful!**  
            {value} {from_unit} = **{result:.4f} {to_unit}**  
            """)  
            st.session_state.history.append(f"{value} {from_unit} → {result:.2f} {to_unit}")  
            
            # Interactive Visualization  
            fig = px.bar(  
                x=[from_unit, to_unit],  
                y=[value, result],  
                title="📈 Conversion Comparison",  
                labels={"x": "Unit", "y": "Value"},  
                color=[from_unit, to_unit],  
                template="plotly_dark" if "Dark" in theme else "plotly_white"  
            )  
            fig.update_layout(  
                plot_bgcolor='rgba(0,0,0,0)',  
                paper_bgcolor='rgba(0,0,0,0)',  
                font_color='white' if "Dark" in theme else 'black'  
            )  
            st.plotly_chart(fig, use_container_width=True)  
    
    st.markdown('</div>', unsafe_allow_html=True)  

# History Section  
st.subheader("📜 Conversion History")  
if not st.session_state.history:  
    st.info("🌟 No conversions yet! Convert something to see history.")  
else:  
    for entry in reversed(st.session_state.history[-5:]):  
        st.markdown(f"""  
        <div class="custom-card">  
            📌 {entry}  
        </div>  
        """, unsafe_allow_html=True)  

# Footer  
st.markdown("---")  
st.markdown("🚀 Made with ❤️ by Areeshaa Tanoli | [GitHub](https://github.com)")  