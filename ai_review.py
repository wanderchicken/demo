import openai
import os
import sys

# Set up your OpenAI API key (this can also be stored in GitHub Secrets for security)
openai.api_key = os.getenv("OPENAI_API_KEY")

def review_code(pr_diff_file):
    with open(pr_diff_file, 'r') as file:
        code_diff = file.read()

    try:
        # Send the code diff to OpenAI Codex to analyze and generate suggestions
        response = openai.Completion.create(
            engine="code-davinci-002",  # Codex model for code-related tasks
            prompt=f"Review the following code changes and provide suggestions or improvements:\n\n{code_diff}",
            max_tokens=500,  # Limit the response size
            temperature=0.5,  # Creativity level, tweak based on your preference
            n=1  # Number of completions to generate
        )
        
        # Extract feedback from the AI response
        ai_feedback = response.choices[0].text.strip()
        
        return ai_feedback

    except Exception as e:
        return f"Error during AI review: {str(e)}"

if __name__ == "__main__":
    pr_diff_file = sys.argv[1]
    feedback = review_code(pr_diff_file)
    print("AI Review Feedback:\n", feedback)
    
    # Optionally, store the feedback in a file to output later or send it as a PR comment
    with open("ai_review_feedback.txt", "w") as f:
        f.write(feedback)
