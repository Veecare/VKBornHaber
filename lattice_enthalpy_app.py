import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random

# Page configuration
st.set_page_config(page_title="Lattice Enthalpy Learning Tool", layout="wide")

# Initialize session state
if 'current_section' not in st.session_state:
    st.session_state.current_section = 0
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}
if 'born_haber_step' not in st.session_state:
    st.session_state.born_haber_step = 0

# Main title
st.title("🔬 Lattice Enthalpy: Interactive Learning Tool")
st.markdown("---")

# Sidebar navigation
sections = [
    "📚 Theory & Concepts",
    "🧮 Born-Haber Cycle",
    "📊 Data Analysis",
    "🎯 Interactive Exercises",
    "🧪 Compound Examples",
    "❓ Conceptual Questions"
]

selected_section = st.sidebar.selectbox("Navigate to:", sections, index=st.session_state.current_section)
st.session_state.current_section = sections.index(selected_section)

# Compound data
compound_data = {
    'Compound': ['LiCl', 'NaCl', 'Na₂O', 'K₂O', 'MgS', 'CaCl₂', 'AlCl₃'],
    'Lattice_Enthalpy_kJ_mol': [853, 786, 2478, 2238, 3406, 2255, 5492],
    'Cation_Charge': [1, 1, 1, 1, 2, 2, 3],
    'Anion_Charge': [1, 1, 2, 2, 2, 1, 1],
    'Cation_Radius_pm': [76, 102, 102, 138, 72, 100, 54],
    'Anion_Radius_pm': [181, 181, 140, 140, 184, 181, 181]
}

df = pd.DataFrame(compound_data)

# Section 1: Theory & Concepts
if st.session_state.current_section == 0:
    st.header("📚 Lattice Enthalpy: Theory & Concepts")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("What is Lattice Enthalpy?")
        st.markdown("""
        **Lattice Enthalpy** is the energy required to completely separate one mole of an ionic solid 
        into gaseous ions, or the energy released when gaseous ions combine to form one mole of ionic solid.
        
        **Mathematical Expression:**
        """)
        st.latex(r"MX_{(s)} \rightarrow M^{n+}_{(g)} + X^{n-}_{(g)} \quad \Delta H_{lattice}")
        
        st.subheader("Factors Affecting Lattice Enthalpy")
        
        with st.expander("1. Charge on Ions"):
            st.markdown("""
            - **Higher charges** → **Higher lattice enthalpy**
            - Lattice enthalpy ∝ (q₁ × q₂)
            - Example: MgO (charges: 2+, 2-) has much higher lattice enthalpy than NaCl (charges: 1+, 1-)
            """)
        
        with st.expander("2. Size of Ions"):
            st.markdown("""
            - **Smaller ions** → **Higher lattice enthalpy**
            - Lattice enthalpy ∝ 1/r₀ (where r₀ is the distance between ion centers)
            - Example: LiF has higher lattice enthalpy than CsI
            """)
        
        with st.expander("3. Crystal Structure"):
            st.markdown("""
            - Different crystal structures have different coordination numbers
            - Higher coordination number generally leads to higher lattice enthalpy
            - Common structures: Rock salt (NaCl), Cesium chloride (CsCl), Fluorite (CaF₂)
            """)
    
    with col2:
        st.subheader("Born-Landé Equation")
        st.latex(r"U = -\frac{NAMz^+z^-e^2}{4\pi\epsilon_0r_0}\left(1-\frac{1}{n}\right)")
        
        st.markdown("""
        Where:
        - **N_A**: Avogadro's number
        - **M**: Madelung constant
        - **z⁺, z⁻**: Charges on cation and anion
        - **e**: Elementary charge
        - **ε₀**: Permittivity of free space
        - **r₀**: Nearest neighbor distance
        - **n**: Born exponent
        """)
        
        st.info("💡 **Key Insight**: Lattice enthalpy is proportional to (charge₁ × charge₂)/distance")

# Section 2: Born-Haber Cycle
elif st.session_state.current_section == 1:
    st.header("🧮 Born-Haber Cycle")
    
    # Born-Haber cycle steps for NaCl
    steps = [
        {"name": "Start", "description": "Na(s) + ½Cl₂(g)", "energy": 0, "process": "Starting materials"},
        {"name": "Sublimation", "description": "Na(g) + ½Cl₂(g)", "energy": 107, "process": "Sublimation of Na"},
        {"name": "Dissociation", "description": "Na(g) + Cl(g)", "energy": 107 + 122, "process": "Bond dissociation of Cl₂"},
        {"name": "Ionization", "description": "Na⁺(g) + Cl(g) + e⁻", "energy": 107 + 122 + 496, "process": "Ionization of Na"},
        {"name": "Electron Affinity", "description": "Na⁺(g) + Cl⁻(g)", "energy": 107 + 122 + 496 - 349, "process": "Electron affinity of Cl"},
        {"name": "Lattice Formation", "description": "NaCl(s)", "energy": 107 + 122 + 496 - 349 - 786, "process": "Lattice formation"}
    ]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Born-Haber Cycle for NaCl")
        
        # Create energy diagram
        fig = go.Figure()
        
        x_positions = list(range(len(steps)))
        energies = [step["energy"] for step in steps]
        
        # Add energy levels
        for i, (x, energy, step) in enumerate(zip(x_positions, energies, steps)):
            fig.add_trace(go.Scatter(
                x=[x], y=[energy], 
                mode='markers+text',
                marker=dict(size=12, color='red'),
                text=f"{step['name']}<br>{energy} kJ/mol",
                textposition="top center",
                name=step['process'],
                showlegend=False
            ))
            
            if i < len(steps) - 1:
                fig.add_trace(go.Scatter(
                    x=[x, x+1], y=[energy, energies[i+1]],
                    mode='lines',
                    line=dict(color='blue', width=2),
                    showlegend=False
                ))
        
        fig.update_layout(
            title="Energy Changes in Born-Haber Cycle",
            xaxis_title="Process Step",
            yaxis_title="Energy (kJ/mol)",
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Step-by-Step Navigation")
        
        if st.button("Next Step", key="born_haber_next"):
            if st.session_state.born_haber_step < len(steps) - 1:
                st.session_state.born_haber_step += 1
        
        if st.button("Previous Step", key="born_haber_prev"):
            if st.session_state.born_haber_step > 0:
                st.session_state.born_haber_step -= 1
        
        if st.button("Reset", key="born_haber_reset"):
            st.session_state.born_haber_step = 0
        
        current_step = steps[st.session_state.born_haber_step]
        
        st.markdown(f"### Step {st.session_state.born_haber_step + 1}: {current_step['name']}")
        st.markdown(f"**Process:** {current_step['process']}")
        st.markdown(f"**Formula:** {current_step['description']}")
        st.markdown(f"**Total Energy:** {current_step['energy']} kJ/mol")
        
        if st.session_state.born_haber_step == 0:
            st.info("Starting with solid sodium and gaseous chlorine")
        elif st.session_state.born_haber_step == 1:
            st.info("Energy input required to convert solid Na to gaseous Na atoms")
        elif st.session_state.born_haber_step == 2:
            st.info("Energy input to break Cl₂ bonds")
        elif st.session_state.born_haber_step == 3:
            st.info("Energy input to remove electron from Na")
        elif st.session_state.born_haber_step == 4:
            st.info("Energy released when Cl gains an electron")
        else:
            st.success("Final step: Lattice enthalpy - energy released when ionic solid forms!")

# Section 3: Data Analysis
elif st.session_state.current_section == 2:
    st.header("📊 Data Analysis")
    
    st.subheader("Compound Data Comparison")
    st.dataframe(df, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Lattice Enthalpy vs Charge Product")
        
        df['Charge_Product'] = df['Cation_Charge'] * df['Anion_Charge']
        
        fig = px.scatter(df, x='Charge_Product', y='Lattice_Enthalpy_kJ_mol', 
                        hover_data=['Compound'], 
                        title="Effect of Ionic Charges on Lattice Enthalpy")
        fig.update_traces(marker=dict(size=12))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Effect of Ionic Size")
        
        df['Sum_Radii'] = df['Cation_Radius_pm'] + df['Anion_Radius_pm']
        
        fig = px.scatter(df, x='Sum_Radii', y='Lattice_Enthalpy_kJ_mol',
                        hover_data=['Compound'],
                        title="Lattice Enthalpy vs Sum of Ionic Radii")
        fig.update_traces(marker=dict(size=12, color='green'))
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Comprehensive Analysis")
    
    # Create 3D plot
    fig = px.scatter_3d(df, x='Charge_Product', y='Sum_Radii', z='Lattice_Enthalpy_kJ_mol',
                       hover_data=['Compound'], 
                       title="3D Relationship: Charge, Size, and Lattice Enthalpy",
                       color='Lattice_Enthalpy_kJ_mol',
                       color_continuous_scale='viridis')
    
    st.plotly_chart(fig, use_container_width=True)

# Section 4: Interactive Exercises
elif st.session_state.current_section == 3:
    st.header("🎯 Interactive Exercises")
    
    exercise_type = st.selectbox("Choose Exercise Type:", 
                                ["Prediction Quiz", "Calculation Practice", "Ranking Exercise"])
    
    if exercise_type == "Prediction Quiz":
        st.subheader("Lattice Enthalpy Prediction Quiz")
        
        questions = [
            {
                "question": "Which compound has higher lattice enthalpy: MgO or NaCl?",
                "options": ["MgO", "NaCl", "Same"],
                "correct": 0,
                "explanation": "MgO has higher charges (Mg²⁺, O²⁻) compared to NaCl (Na⁺, Cl⁻), leading to much higher lattice enthalpy."
            },
            {
                "question": "Why does LiF have higher lattice enthalpy than CsI?",
                "options": ["Larger ions", "Smaller ions", "Different charges"],
                "correct": 1,
                "explanation": "Li⁺ and F⁻ are much smaller than Cs⁺ and I⁻, leading to stronger electrostatic attraction."
            }
        ]
        
        for i, q in enumerate(questions):
            st.markdown(f"**Question {i+1}:** {q['question']}")
            answer = st.radio(f"Select answer for Q{i+1}:", q['options'], key=f"q{i}")
            
            if st.button(f"Check Answer {i+1}", key=f"check{i}"):
                if q['options'].index(answer) == q['correct']:
                    st.success(f"✅ Correct! {q['explanation']}")
                else:
                    st.error(f"❌ Incorrect. {q['explanation']}")
    
    elif exercise_type == "Calculation Practice":
        st.subheader("Born-Haber Cycle Calculations")
        
        st.markdown("**Practice Problem:** Calculate the lattice enthalpy of NaCl using the following data:")
        
        data = {
            "Process": ["Sublimation of Na", "Dissociation of Cl₂", "Ionization of Na", "Electron affinity of Cl", "Formation of NaCl"],
            "Energy (kJ/mol)": ["+107", "+122", "+496", "-349", "-411"]
        }
        
        st.table(pd.DataFrame(data))
        
        user_answer = st.number_input("Enter the lattice enthalpy (kJ/mol):", value=0)
        
        if st.button("Check Calculation"):
            correct_answer = 107 + 122 + 496 - 349 - (-411)
            if abs(user_answer - correct_answer) < 10:
                st.success(f"✅ Correct! Lattice enthalpy = {correct_answer} kJ/mol")
            else:
                st.error(f"❌ Incorrect. The correct answer is {correct_answer} kJ/mol")
                st.markdown("**Solution:** ΔH_lattice = ΔH_sub + ΔH_diss + ΔH_ion + ΔH_ea - ΔH_form")
    
    else:  # Ranking Exercise
        st.subheader("Ranking Exercise")
        
        compounds_to_rank = ["LiF", "NaCl", "MgO", "CaCl₂"]
        st.markdown("**Task:** Rank these compounds from highest to lowest lattice enthalpy:")
        
        rankings = {}
        for i, compound in enumerate(compounds_to_rank):
            rankings[compound] = st.selectbox(f"Rank for {compound}:", [1, 2, 3, 4], key=f"rank_{compound}")
        
        if st.button("Check Ranking"):
            correct_order = ["MgO", "LiF", "CaCl₂", "NaCl"]  # Approximate correct order
            user_order = sorted(rankings.keys(), key=lambda x: rankings[x])
            
            st.markdown("**Your ranking (highest to lowest):**")
            for i, compound in enumerate(user_order):
                st.write(f"{i+1}. {compound}")
            
            st.markdown("**Correct ranking:**")
            for i, compound in enumerate(correct_order):
                st.write(f"{i+1}. {compound}")

# Section 5: Compound Examples
elif st.session_state.current_section == 4:
    st.header("🧪 Detailed Compound Examples")
    
    selected_compound = st.selectbox("Select a compound to analyze:", df['Compound'].tolist())
    
    compound_info = df[df['Compound'] == selected_compound].iloc[0]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Lattice Enthalpy", f"{compound_info['Lattice_Enthalpy_kJ_mol']} kJ/mol")
        st.metric("Cation Charge", f"+{compound_info['Cation_Charge']}")
        st.metric("Anion Charge", f"-{compound_info['Anion_Charge']}")
    
    with col2:
        st.metric("Cation Radius", f"{compound_info['Cation_Radius_pm']} pm")
        st.metric("Anion Radius", f"{compound_info['Anion_Radius_pm']} pm")
        st.metric("Charge Product", f"{compound_info['Cation_Charge'] * compound_info['Anion_Charge']}")
    
    with col3:
        # Create a simple ionic structure visualization
        fig, ax = plt.subplots(figsize=(4, 4))
        
        # Draw cation
        circle1 = plt.Circle((0.3, 0.5), 0.15, color='red', alpha=0.7, label='Cation')
        ax.add_patch(circle1)
        ax.text(0.3, 0.5, f"+{compound_info['Cation_Charge']}", ha='center', va='center', fontsize=12, fontweight='bold')
        
        # Draw anion
        circle2 = plt.Circle((0.7, 0.5), 0.2, color='blue', alpha=0.7, label='Anion')
        ax.add_patch(circle2)
        ax.text(0.7, 0.5, f"-{compound_info['Anion_Charge']}", ha='center', va='center', fontsize=12, fontweight='bold')
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.set_title(f"{selected_compound} Structure")
        ax.legend()
        ax.axis('off')
        
        st.pyplot(fig)
    
    st.subheader(f"Analysis of {selected_compound}")
    
    # Detailed analysis
    if selected_compound in ['LiCl', 'NaCl']:
        st.markdown(f"""
        **{selected_compound}** is an alkali metal halide with:
        - **Structure:** Rock salt (face-centered cubic)
        - **Coordination number:** 6:6
        - **Key features:** Typical ionic compound with moderate lattice enthalpy
        """)
    elif selected_compound in ['Na₂O', 'K₂O']:
        st.markdown(f"""
        **{selected_compound}** is an alkali metal oxide with:
        - **Structure:** Antifluorite
        - **Higher lattice enthalpy** due to doubly charged oxide ion
        - **Highly basic** and reacts vigorously with water
        """)
    elif selected_compound == 'MgS':
        st.markdown("""
        **MgS** is an alkaline earth metal sulfide with:
        - **Very high lattice enthalpy** due to both ions being doubly charged
        - **Structure:** Rock salt type
        - **Properties:** High melting point, good electrical insulator
        """)
    elif selected_compound == 'CaCl₂':
        st.markdown("""
        **CaCl₂** is an alkaline earth metal halide with:
        - **Structure:** Rutile or fluorite type
        - **Coordination:** Ca²⁺ surrounded by 8 Cl⁻ ions
        - **Applications:** De-icing agent, desiccant
        """)
    elif selected_compound == 'AlCl₃':
        st.markdown("""
        **AlCl₃** shows interesting behavior:
        - **High lattice enthalpy** due to Al³⁺ high charge
        - **Significant covalent character** due to high charge density of Al³⁺
        - **Dimeric in vapor phase:** Al₂Cl₆
        """)

# Section 6: Conceptual Questions
elif st.session_state.current_section == 5:
    st.header("❓ Conceptual Questions & Advanced Topics")
    
    topic = st.selectbox("Choose a topic:", 
                        ["Factors Affecting Lattice Enthalpy", 
                         "Covalent Character in Ionic Compounds",
                         "Polarization and Fajan's Rules",
                         "Crystal Structures and Lattice Energy"])
    
    if topic == "Factors Affecting Lattice Enthalpy":
        st.subheader("Factors Affecting Lattice Enthalpy")
        
        questions = [
            {
                "q": "Why does MgO have a much higher lattice enthalpy than NaCl?",
                "a": "MgO has doubly charged ions (Mg²⁺, O²⁻) compared to singly charged ions in NaCl (Na⁺, Cl⁻). Since lattice enthalpy is proportional to the product of charges, MgO has approximately 4 times higher lattice enthalpy."
            },
            {
                "q": "Explain why LiF has higher lattice enthalpy than CsI.",
                "a": "Li⁺ and F⁻ are much smaller ions than Cs⁺ and I⁻. The smaller size leads to shorter interionic distances and stronger electrostatic attractions, resulting in higher lattice enthalpy."
            },
            {
                "q": "How does crystal structure affect lattice enthalpy?",
                "a": "Different crystal structures have different coordination numbers and packing efficiencies. Higher coordination numbers generally lead to more favorable electrostatic interactions and higher lattice enthalpies."
            }
        ]
        
        for i, item in enumerate(questions):
            with st.expander(f"Question {i+1}: {item['q']}"):
                st.write(item['a'])
    
    elif topic == "Covalent Character in Ionic Compounds":
        st.subheader("Covalent Character in Ionic Compounds")
        
        st.markdown("""
        Even 'ionic' compounds can have significant covalent character. This depends on:
        
        **Fajan's Rules:**
        1. **Small, highly charged cation** increases covalent character
        2. **Large, highly charged anion** increases covalent character  
        3. **Electron configuration** of cation (pseudo-noble gas > noble gas)
        """)
        
        # Interactive polarization visualization
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Examples of increasing covalent character:**")
            covalent_data = {
                "Compound": ["NaCl", "MgCl₂", "AlCl₃", "SiCl₄"],
                "Cation": ["Na⁺", "Mg²⁺", "Al³⁺", "Si⁴⁺"],
                "Covalent Character": ["Low", "Medium", "High", "Very High"],
                "Evidence": ["Ionic solid", "Ionic solid", "Dimeric vapor", "Molecular liquid"]
            }
            st.table(pd.DataFrame(covalent_data))
        
        with col2:
            charge_density = st.slider("Cation Charge Density", 0.1, 2.0, 1.0)
            anion_polarizability = st.slider("Anion Polarizability", 0.1, 2.0, 1.0)
            
            covalent_character = (charge_density * anion_polarizability) * 50
            
            st.metric("Predicted Covalent Character (%)", f"{covalent_character:.1f}")
            
            if covalent_character < 20:
                st.success("Predominantly ionic")
            elif covalent_character < 50:
                st.warning("Mixed ionic-covalent")
            else:
                st.error("Predominantly covalent")
    
    elif topic == "Polarization and Fajan's Rules":
        st.subheader("Polarization Effects")
        
        st.markdown("""
        **Polarization** occurs when a cation distorts the electron cloud of an anion,
        leading to covalent character in supposedly ionic compounds.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Factors Increasing Polarization:**")
            st.markdown("""
            - High charge on cation
            - Small size of cation
            - Large size of anion
            - High charge on anion
            - Pseudo-noble gas configuration of cation
            """)
            
        with col2:
            st.markdown("**Examples:**")
            st.markdown("""
            - **BeF₂:** High polarization → covalent character
            - **AgCl:** Ag⁺ has pseudo-noble gas config → covalent character
            - **PbI₂:** Large I⁻ easily polarized → yellow color
            """)
        
        # Quiz on polarization
        st.subheader("Quick Quiz")
        q1 = st.radio("Which cation causes more polarization?", ["Li⁺", "Cs⁺"])
        if q1 == "Li⁺":
            st.success("✅ Correct! Li⁺ is smaller and has higher charge density.")
        else:
            st.error("❌ Li⁺ is smaller and causes more polarization.")
    
    else:  # Crystal Structures and Lattice Energy
        st.subheader("Crystal Structures and Their Effect on Lattice Energy")
        
        structures = {
            "Rock Salt (NaCl)": {
                "coordination": "6:6",
                "examples": ["NaCl", "MgO", "CaO"],
                "madelung": 1.748
            },
            "Cesium Chloride (CsCl)": {
                "coordination": "8:8", 
                "examples": ["CsCl", "CsBr"],
                "madelung": 1.763
            },
            "Fluorite (CaF₂)": {
                "coordination": "8:4",
                "examples": ["CaF₂", "UO₂"],
                "madelung": 2.519
            },
            "Zinc Blende (ZnS)": {
                "coordination": "4:4",
                "examples": ["ZnS", "CuCl"],
                "madelung": 1.638
            }
        }
        
        selected_structure = st.selectbox("Select crystal structure:", list(structures.keys()))
        
        info = structures[selected_structure]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Coordination Number:** {info['coordination']}")
            st.markdown(f"**Madelung Constant:** {info['madelung']}")
            st.markdown(f"**Examples:** {', '.join(info['examples'])}")
        
        with col2:
            st.markdown("**Key Points:**")
            if "Rock Salt" in selected_structure:
                st.markdown("- Most common structure for 1:1 compounds")
                st.markdown("- Face-centered cubic arrangement") 
                st.markdown("- High coordination leads to strong interactions")
            elif "Cesium Chloride" in selected_structure:
                st.markdown("- Body-centered cubic")
                st.markdown("- Highest coordination for 1:1 compounds")
                st.markdown("- Slightly higher Madelung constant")
            elif "Fluorite" in selected_structure:
                st.markdown("- Common for 1:2 compounds")
                st.markdown("- Anions in tetrahedral holes")
                st.markdown("- High Madelung constant due to charge arrangement")
            else:
                st.markdown("- Tetrahedral coordination")
                st.markdown("- Common when cation and anion similar sizes")
                st.markdown("- Lower coordination → lower lattice energy")

# Footer with navigation
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("← Previous Section") and st.session_state.current_section > 0:
        st.session_state.current_section -= 1
        st.rerun()

with col3:
    if st.button("Next Section →") and st.session_state.current_section < len(sections) - 1:
        st.session_state.current_section += 1
        st.rerun()

with col2:
    st.markdown(f"**Section {st.session_state.current_section + 1} of {len(sections)}**")

# Additional styling
st.markdown("""
<style>
.stAlert > div {
    padding: 1rem;
}
.metric-container {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)