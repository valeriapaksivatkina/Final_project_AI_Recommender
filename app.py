import pandas as pd
import streamlit as st
import openai
from fpdf import FPDF  # Import FPDF for PDF generation

@st.cache_data()
def load_data():
    df = pd.read_csv('./df_sampled_category_usability.csv').sample(700)
    return df

openai.api_key = ***

def recommend_tools(user_input, data):
    keywords = user_input.lower().split()  # Divide la entrada del usuario en palabras clave y las convierte a minúsculas
    matched_tools = []  # Lista vacía donde se almacenarán las herramientas coincidentes
    
    # Itera sobre cada fila (herramienta) en el conjunto de datos proporcionado
    for idx, row in data.iterrows():
        useable_for = row['Useable For'].lower()  # Obtiene el caso de uso de la herramienta en minúsculas
        description = row['Description'].lower()  # Obtiene la descripción de la herramienta en minúsculas
        
        # Verifica primero si alguna palabra clave está presente en el caso de uso de la herramienta
        if any(keyword in useable_for for keyword in keywords):
            # Si hay coincidencias en el caso de uso, agrega la herramienta a la lista de herramientas coincidentes
            matched_tools.append({
                'name': row['AI Tool Name'],         # Nombre de la herramienta de IA
                'description': row['Description'],   # Descripción de la herramienta
                'use_case': row['Useable For'],      # Caso de uso de la herramienta
                'link': row['Tool Link'],            # Enlace de la herramienta
                'free_paid': row['Free/Paid'],       # Gratis o de pago
                'charges': row['Charges'],           # Costos asociados
                'reviews': row['Review'] if 'Review' in data.columns else None  # Reseñas de la herramienta (si están disponibles)
            })
        elif any(keyword in description for keyword in keywords):
            # Si no hay coincidencias en el caso de uso pero sí en la descripción, agrega la herramienta igualmente
            matched_tools.append({
                'name': row['AI Tool Name'],         # Nombre de la herramienta de IA
                'description': row['Description'],   # Descripción de la herramienta
                'use_case': row['Useable For'],      # Caso de uso de la herramienta
                'link': row['Tool Link'],            # Enlace de la herramienta
                'free_paid': row['Free/Paid'],       # Gratis o de pago
                'charges': row['Charges'],           # Costos asociados
                'reviews': row['Review'] if 'Review' in data.columns else None  # Reseñas de la herramienta (si están disponibles)
            })
    
    # Si no se encontraron herramientas coincidentes, devuelve un mensaje indicando que no se encontraron herramientas
    if not matched_tools:
        return "We couldn't understand your question or no tools matching your interests were found. Please try a different query."
    
    prompt = f"Recommend AI tools for a user interested in {user_input}. Based on the tools found in the data:"
    max_tools_in_prompt = 5  # Limita el número de herramientas en el prompt
    for tool in matched_tools[:max_tools_in_prompt]:
        prompt += f"\n- {tool['name']} [More info]({tool['link']})"

    # Llama a OpenAI para completar el texto generado basado en el prompt
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",   # Modelo de OpenAI a utilizar
        prompt=prompt,                    # Prompt inicial
        max_tokens=150,                   # Máximo de tokens para la respuesta generada
        n=1,                              # Número de respuestas a generar
        stop=None,                        # Condición de parada opcional
        temperature=0.7                   # Temperatura para el muestreo de tokens
    )

    # Extrae y formatea la respuesta generada por OpenAI
    generated_text = response['choices'][0]['text'].strip()
    
    
    # Devuelve las herramientas coincidentes y el texto generado
    return matched_tools, generated_text



# Function to generate PDF from recommendations
def generate_pdf(matched_tools, user_input):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"Recommendations for AI tools based on your interest in '{user_input}':", ln=True, align='C')

    for i, tool in enumerate(matched_tools, start=1):
        pdf.cell(200, 10, txt=f"\n{i}. {tool['name']}:", ln=True)
        pdf.multi_cell(0, 10, txt=f"- Description: {tool['description']}\n  Use Case: {tool['use_case']}\n  Link: {tool['link']}\n  Reviews: {tool['reviews']}\n  Type: {tool['free_paid']}\n  Charges: {tool['charges']}\n", align='L')

    pdf_output = f"recommendations_{user_input.replace(' ', '_')}.pdf"
    pdf.output(name=pdf_output)

    return pdf_output

# Load data
data = load_data()

# Category descriptions 
category_descriptions = {
    'social media assistant': 'AI is used in social media management to schedule posts, analyze metrics, and generate engaging content, helping to optimize online presence.',
    'research': 'AI assists in research by analyzing large volumes of data, identifying patterns, and facilitating the discovery of new insights.',
    'e-commerce': 'In e-commerce, AI enhances customer experience through personalized recommendations, customer service chatbots, and inventory optimization.',
    'dating': 'AI in dating apps is used to match users based on compatibility, analyze behavioral patterns, and improve overall user experience.',
    'video generator': 'AI video generation tools create visual content automatically, personalize videos from data, and simplify video editing.',
    'code assistant': 'AI code assistants suggest lines of code, detect errors, and optimize software development, improving programmer efficiency.',
    'copywriting': 'AI in copywriting generates compelling ad copy, creates SEO content, and personalizes messages for different audiences.',
    'life assistant': 'AI personal assistants manage daily tasks, set reminders, handle calendars, and answer common questions to ease everyday life.',
    'text to speech': 'Text-to-speech technology converts written text into natural-sounding speech, used in accessibility applications and virtual assistants.',
    'general writing': 'AI general writing tools help draft, review, and improve texts, ensuring clarity and grammatical correctness.',
    'video editing': 'AI in video editing automates processes like cutting, editing, and adding special effects, saving time and effort for editors.',
    'music': 'AI in music composes original pieces, suggests chords and melodies, and personalizes playlists according to user preferences.',
    'low-code': 'AI-powered low-code platforms enable the creation of applications with minimal coding, accelerating development and reducing reliance on expert programmers.',
    'education assistant': 'AI education assistants personalize learning, provide automated tutoring, and assess student progress to improve educational outcomes.',
    'personalized videos': 'AI generates personalized videos by adjusting visual and audio content based on user data, enhancing engagement and content relevance.',
    'no-code': 'AI-powered no-code platforms allow users with no programming knowledge to develop applications and automations, democratizing technology.',
    'memory': 'AI memory tools help store, organize, and retrieve information efficiently, improving productivity and knowledge management.',
    'productivity': 'AI productivity applications optimize time management, automate repetitive tasks, and provide analytics to improve work efficiency.',
    'legal assistant': 'AI legal assistants analyze legal documents, conduct legal research, and assist in case preparation, streamlining legal processes.',
    'avatars': 'AI creates realistic and personalized digital avatars for use in video games, virtual reality, and social media applications.',
    'fashion': 'In fashion, AI predicts trends, personalizes clothing recommendations, and optimizes supply chains, improving efficiency and customer satisfaction.',
    'gift ideas': 'AI tools generate personalized gift ideas based on the recipient’s interests and preferences, making gift selection easier.',
    'summarizer': 'AI-generated summaries condense long texts into shorter, clearer versions, saving time in reading and understanding documents.',
    'fun tools': 'AI entertainment tools create interactive games, generate fun content, and personalize playful experiences for users.',
    'spreadsheets': 'AI in spreadsheets automates data analysis, generates visualizations, and performs complex calculations, improving productivity in data management.',
    'prompts': 'AI tools generate content suggestions and questions to inspire creativity and guide writing in various contexts.',
    '3D': 'AI in 3D design facilitates the creation of three-dimensional models, optimizes rendering processes, and personalizes augmented and virtual reality experiences.',
    'logo generator': 'AI tools generate personalized logos using algorithms that analyze design trends and user preferences.',
    'search engine': 'AI-powered search engines improve the relevance of results, personalize searches, and analyze large volumes of information quickly.',
    'presentations': 'AI presentation tools automatically create slides, suggest designs and content, and optimize information visualization.',
    'healthcare': 'AI in healthcare diagnoses diseases, personalizes treatments, and improves patient management by analyzing medical data.',
    'religion': 'AI in religion provides tools for studying sacred texts, generating religious content, and facilitating connections within faith communities.',
    'image editing': 'AI image editing tools enhance photos, remove imperfections, and apply special effects automatically.',
    'transcriber': 'AI transcription tools convert audio into written text, facilitating record creation and accessibility.',
    'email assistant': 'AI email assistants manage inboxes, suggest responses, and classify messages to improve communication efficiency.',
    'art': 'AI in art creates original works, suggests styles and techniques, and personalizes pieces according to user preferences.',
    'SQL': 'AI tools for SQL optimize queries, generate scripts, and analyze databases, improving data management efficiency.',
    'customer support': 'AI in customer support automates responses, analyzes queries, and provides personalized assistance, improving customer satisfaction.',
    'resources': 'AI resource tools manage information, optimize material usage, and provide analytics for strategic decision-making.',
    'real estate': 'AI in real estate evaluates properties, predicts market trends, and personalizes purchase or rental recommendations.',
    'developer tools': 'AI development tools automate testing, suggest code improvements, and optimize the software development lifecycle.',
    'design assistant': 'AI design assistants suggest layouts, color combinations, and styles, and generate personalized graphics.',
    'startup tools': 'AI tools for startups provide market analysis, optimize business strategies, and automate administrative processes.',
    'gaming': 'AI in gaming creates intelligent characters, personalizes gaming experiences, and optimizes game performance.',
    'travel': 'AI travel tools personalize itineraries, suggest destinations, and optimize bookings to enhance traveler experiences.',
    'story teller': 'AI storytelling tools generate original stories, suggest plots and characters, and personalize narrative content.',
    'paraphraser': 'AI paraphrasing tools rephrase texts to improve clarity, avoid plagiarism, and adapt content for different audiences.',
    'human resources': 'AI in human resources automates recruitment processes, analyzes employee performance, and suggests professional development plans.',
    'experiments': 'AI tools for experiments facilitate the design, execution, and analysis of scientific tests, optimizing research.',
    'fitness': 'AI in fitness personalizes workout routines, analyzes physical performance, and suggests improvements in health and well-being.',
    'image generator': 'AI image generation tools create original graphics, personalize visual content, and optimize creative processes.',
    'finance': 'AI in finance analyzes economic data, predicts market trends, and optimizes investment management.',
    'audio editing': 'AI audio editing tools enhance sound quality, remove noise, and apply special effects.',
    'SEO': 'AI in SEO optimizes web content, suggests keywords, and analyzes page performance to improve search engine ranking.',
    'sales': 'AI sales tools analyze customer data, optimize sales strategies, and personalize product recommendations.'
}

# Category emoticons 
category_emoticons = {
    'social media assistant': '📱',
    'research': '🔍',
    'e-commerce': '🛒',
    'dating': '💑',
    'video generator': '🎥',
    'code assistant': '💻',
    'copywriting': '✍️',
    'life assistant': '🧑‍💼',
    'text to speech': '🗣️',
    'general writing': '📝',
    'video editing': '✂️',
    'music': '🎵',
    'low-code': '🧩',
    'education assistant': '🎓',
    'personalized videos': '📹',
    'no-code': '🔧',
    'memory': '🧠',
    'productivity': '📈',
    'legal assistant': '⚖️',
    'avatars': '👤',
    'fashion': '👗',
    'gift ideas': '🎁',
    'summarizer': '🔖',
    'fun tools': '🎉',
    'spreadsheets': '📊',
    'prompts': '💡',
    '3D': '🧱',
    'logo generator': '🏷️',
    'search engine': '🌐',
    'presentations': '📽️',
    'healthcare': '🏥',
    'religion': '⛪',
    'image editing': '🖼️',
    'transcriber': '✍️',
    'email assistant': '📧',
    'art': '🎨',
    'SQL': '🗃️',
    'customer support': '💬',
    'resources': '📚',
    'real estate': '🏠',
    'developer tools': '🛠️',
    'design assistant': '🖌️',
    'startup tools': '🚀',
    'gaming': '🎮',
    'travel': '✈️',
    'story teller': '📚',
    'paraphraser': '🔄',
    'human resources': '👥',
    'experiments': '🧪',
    'fitness': '🏋️‍♂️',
    'image generator': '🌄',
    'finance': '💹',
    'audio editing': '🎧',
    'SEO': '🔎',
    'sales': '💼'
}

# Cargar imagen del logo desde el archivo en tu ordenador
logo_path = './logo.webp'


# Mostrar el logo en el sidebar
st.sidebar.image(logo_path, use_column_width=True)

# Estilo CSS para el cuadro con sombra
css = """
<style>
    .description-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .description-title {
        text-align: center;
        font-size: 24px;
    }
    .description-content {
        text-align: justify;
        font-size: 16px;
    }
</style>
"""

# Texto de la descripción de la app en formato Markdown
app_description = """
<div class="description-box">
    <div class="description-content">
        This app combines recommendation and aggregation features to provide personalized artificial intelligence tools for each user. It acts as recommender that analyzes individual needs and functions as a data aggregator, gathering detailed information from a wide range of available AI tools.
    </div>
</div>
"""

# Mostrar el estilo CSS
st.markdown(css, unsafe_allow_html=True)

# Mostrar la descripción de la app en el sidebar
st.sidebar.markdown(app_description, unsafe_allow_html=True)

# Sidebar with category filters
st.sidebar.title("AI Tool Category")
categories = ['all'] + list(data['Useable For'].unique())

# Emoticon for "All" category
all_emoticon = '🌟'

selected_category = st.sidebar.radio(
    "Select categories:",
    options=categories,
    format_func=lambda x: f"{all_emoticon} All" if x == 'all' else f"{category_emoticons.get(x, '')} {x}"
)

# Check if "All" category is selected
if selected_category == 'all':
    st.title("AI Tool Recommender")

    # Display an image after the title
    st.image("./ai-drive-product.jpeg", use_column_width=True)
    
    # User input for recommendations
    user_input = st.text_area("Tell us the areas you're interested in:")

    # Generate recommendations on button click
    if st.button("Generate Recommendations"):
        st.info("Generating recommendations...")
        results = recommend_tools(user_input, data)

        if isinstance(results, str):
            st.write(results)
        else:
            matched_tools, recommendations = results

            st.subheader("AI Tool Recommendations:")

            # Divide la pantalla en dos columnas
            col1, col2 = st.columns(2)
            for i, tool in enumerate(matched_tools):
                column = col1 if i % 2 == 0 else col2
                with column:
                    st.markdown(f"""
                        <div style="border: 1px solid #e0e0e0; border-radius: 10px; padding: 10px; margin: 10px 0;">
                            <h3>{tool['name']}</h3>
                            <p><strong>Description:</strong> {tool['description']}</p>
                            <p><strong>Use Case:</strong> {tool['use_case']}</p>
                            <p><strong>Link:</strong> <a href="{tool['link']}" target="_blank">{tool['link']}</a></p>
                            <p><strong>Reviews:</strong> {tool['reviews']}</p>
                            <p><strong>Type:</strong> {tool['free_paid']}</p>
                            <p><strong>Charges:</strong> {tool['charges']}</p>
                        </div>
                """, unsafe_allow_html=True)

            # Download recommendations as PDF
            pdf_file = generate_pdf(matched_tools, user_input)
            st.success(f"PDF generated successfully!")
            st.markdown(f"Download [recommendations PDF]({pdf_file})")

    # Evaluation and Review section
    st.subheader("App Evaluation and Review")
    rating = st.slider("Rate this app (1 = worst, 5 = best)", min_value=1, max_value=5, step=1)
    review = st.text_area("Write a review about your experience with this app")

    if st.button("Submit Review"):
        # Process review submission (can be saved to database, etc.)
        st.success("Thank you for your review!")

else:
    # Display category description
    st.markdown(f"<h2 style='font-weight: bold;'>AI Tool Category: {category_emoticons.get(selected_category, '')} {selected_category}</h2>", unsafe_allow_html=True)
    if selected_category in category_descriptions:
        st.write(category_descriptions[selected_category])

    # Filter data based on selected categories
    filtered_data = data[data['Useable For'] == selected_category]

    # Filter options for 'free' and 'paid' as tabs
    tab_free, tab_paid, tab_freemium = st.tabs(["🆓 Free", "💰 Paid", "🔄 Freemium"])

    # Display tools as cards based on the selected tab
    with tab_free:
        free_tools = filtered_data[filtered_data['Free/Paid'].str.lower() == 'free']
        for idx, row in free_tools.iterrows():
            st.markdown(f"""
                <div style="border: 1px solid #e0e0e0; border-radius: 10px; padding: 10px; margin: 10px 0;
                            box-shadow: 0 4px 8px rgba(0,0,0,0.1); background-color: #f9f9f9;">
                    <h3>{row['AI Tool Name']}</h3>
                    <p><strong>Description:</strong> {row['Description']}</p>
                    <p><strong>Link:</strong> <a href="{row['Tool Link']}" target="_blank">{row['Tool Link']}</a></p>
                    <p><strong>Reviews:</strong> {row['Review']}</p>
                    <div style="clear: both;"></div>
                </div>
            """, unsafe_allow_html=True)

    with tab_paid:
        paid_tools = filtered_data[filtered_data['Free/Paid'].str.lower() == 'paid']
        for idx, row in paid_tools.iterrows():
            st.markdown(f"""
                <div style="border: 1px solid #e0e0e0; border-radius: 10px; padding: 10px; margin: 10px 0;
                            box-shadow: 0 4px 8px rgba(0,0,0,0.1); background-color: #f9f9f9;">
                    <h3>{row['AI Tool Name']}</h3>
                    <p><strong>Description:</strong> {row['Description']}</p>
                    <p><strong>Link:</strong> <a href="{row['Tool Link']}" target="_blank">{row['Tool Link']}</a></p>
                    <p><strong>Reviews:</strong> {row['Review']}</p>
                    <p><strong>Type:</strong> {row['Free/Paid']}</p>
                    <p><strong>Charges:</strong> {row['Charges']}</p>
                    <div style="clear: both;"></div>
                </div>
            """, unsafe_allow_html=True)
    with tab_freemium:
        paid_tools = filtered_data[filtered_data['Free/Paid'].str.lower() == 'freemium']
        for idx, row in paid_tools.iterrows():
            st.markdown(f"""
                <div style="border: 1px solid #e0e0e0; border-radius: 10px; padding: 10px; margin: 10px 0;
                            box-shadow: 0 4px 8px rgba(0,0,0,0.1); background-color: #f9f9f9;">
                    <h3>{row['AI Tool Name']}</h3>
                    <p><strong>Description:</strong> {row['Description']}</p>
                    <p><strong>Link:</strong> <a href="{row['Tool Link']}" target="_blank">{row['Tool Link']}</a></p>
                    <p><strong>Reviews:</strong> {row['Review']}</p>
                    <p><strong>Type:</strong> {row['Free/Paid']}</p>
                    <p><strong>Charges:</strong> {row['Charges']}</p>
                    <div style="clear: both;"></div>
                </div>
            """, unsafe_allow_html=True)        
