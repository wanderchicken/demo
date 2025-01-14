import openai
import os
import sys
import requests

# Ensure OpenAI API key is set correctly
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("The OpenAI API key is not set in the environment variables.")

# GitHub token (automatically passed from GitHub Actions)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Function to post a line-based review comment on the PR
def post_pr_review_comment(pr_url, feedback, commit_id, path, line):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    review_comment_url = f"{pr_url}/comments"

    payload = {
        "body": f"### AI Code Review Feedback\n\n{feedback}",
        "commit_id": commit_id,
        "path": path,
        "line": line,
    }

    response = requests.post(review_comment_url, json=payload, headers=headers)
    if response.status_code == 201:
        print("Successfully posted the review comment!")
    else:
        print(f"Failed to post comment: {response.status_code}, {response.text}")

def review_code(pr_diff_file):
    with open(pr_diff_file, 'r') as file:
        code_diff = file.read()

    try:
        # Send the code diff to OpenAI for analysis (using gpt-3.5-turbo or gpt-4)
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
        ai_feedback = response.choices[0].message.content
        return ai_feedback

    except Exception as e:
        return f"Error during AI review: {str(e)}"

if __name__ == "__main__":
    pr_diff_file = sys.argv[1]
    pr_url = sys.argv[2]  # Get the PR URL as an argument
    commit_id = sys.argv[3]  # Get the commit ID from the arguments
    path = 'test.py'  # Get the file path (relative to the repository)
    line = 1

    feedback = review_code(pr_diff_file)
    print("AI Review Feedback:\n", feedback)

    # Post feedback as a review comment on the PR
    post_pr_review_comment(pr_url, feedback, commit_id, path, line)
