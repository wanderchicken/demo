import openai
import os
import sys
import requests

# Set up your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# GitHub token (add it to GitHub secrets)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Function to post a comment on the PR
def post_pr_comment(pr_url, feedback):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    comment_url = f"{pr_url}/comments"
    payload = {
        "body": f"### AI Code Review Feedback\n\n{feedback}"
    }
    
    response = requests.post(comment_url, json=payload, headers=headers)
    if response.status_code == 201:
        print("Successfully posted the comment!")
    else:
        print(f"Failed to post comment: {response.status_code}, {response.text}")

def review_code(pr_diff_file):
    with open(pr_diff_file, 'r') as file:
        code_diff = file.read()

    try:
        # Send the code diff to OpenAI Codex to analyze and generate suggestions
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" for more advanced feedback
            messages=[
                {"role": "system", "content": "You are a helpful code review assistant."},
                {"role": "user", "content": f"Review the following code changes and provide suggestions or improvements:\n\n{code_diff}"}
            ],
            max_tokens=500,  # Limit the response size
            temperature=0.5,  # Creativity level (adjust as needed)
        )
        
        # Extract feedback from the AI response
        ai_feedback = response['choices'][0]['message']['content'].strip()
        return ai_feedback

    except Exception as e:
        return f"Error during AI review: {str(e)}"

if __name__ == "__main__":
    pr_diff_file = sys.argv[1]
    pr_url = sys.argv[2]  # Get the PR URL as an argument
    
    feedback = review_code(pr_diff_file)
    print("AI Review Feedback:\n", feedback)
    
    # Post feedback as a comment on the PR
    post_pr_comment(pr_url, feedback)
