import streamlit as st
from groq import Groq

# Initialize the Groq client
@st.cache_resource
def init_groq_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

# Function to generate a story using the Groq API
def generate_story(client, prompt):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an excellent children story teller."},
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": ""}
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,  # Changed to False to get complete response
        stop=None,
    )
    return completion.choices[0].message.content

# Main app logic
def main():
    st.title("Ava's Google📔📔📔")
    
    # Input for the story prompt
    prompt = st.text_input("Enter a exam for the story (e.g., 'Once upon a time...')")

    # Button to generate and display the story
    if st.button("Generate Story") and prompt.strip():
        st.markdown("---")
        st.subheader("Your Answer:")
        
        try:
            # Initialize the Groq client
            client = init_groq_client()
            
            # Generate the story
            story = generate_story(client, prompt)
            
            # Display the complete story
            st.markdown(story)
            st.success("Answer generation complete!")
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()