import sys, json

prompt = sys.argv[1].lower()

if "pr" in prompt and "review" in prompt:
    stage = "PR_REVIEW"
elif "test" in prompt:
    stage = "TESTS"
elif "build" in prompt:
    stage = "BUILD"
elif "deploy" in prompt:
    stage = "DEPLOY"
elif "slack" in prompt:
    stage = "SLACK_NOTIFY"
else:
    stage = "FULL"

print(json.dumps({"stage": stage}))
