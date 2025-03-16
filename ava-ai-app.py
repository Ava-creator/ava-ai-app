import streamlit as st
from groq import Groq

# Initialize the Groq client
@st.cache_resource
def init_groq_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

# Function to generate a story using the Groq API
def generate_story(client, prompt):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Replace with the desired model
        messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}, {"role": "assistant", "content": ""}],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    return completion

# Main app logic
def main():
    st.title("Tell Me a Story!")
    
    # Input for the story prompt
    prompt = st.text_input("Enter a prompt for the story (e.g., 'Once upon a time...')")

    # Button to generate and display the story
    if st.button("Generate Story") and prompt.strip():
        st.markdown("---")
        st.subheader("Your Story:")
        
        # Initialize the Groq client
        client = init_groq_client()
        
        # Generate the story
        completion = generate_story(client, prompt)
        
        # Display the story as it streams
        story = ""
        for chunk in completion:
            delta_content = chunk.choices[0].delta.content
            if delta_content:
                story += delta_content
                st.write(delta_content, end="", unsafe_allow_html=True)
        
        # Ensure the final story is displayed
        st.write("\n---\nStory generation complete!")

if __name__ == "__main__":
    main()