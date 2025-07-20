import io
from time import sleep
from _common import ivcap, pp
from ivcap_client.job import Job

crew = """
{
  "$schema": "urn:sd-core:schema.crewai.request.1",
  "name": "Simple Test Crew",
  "inputs": {},
  "crew": {
    "agents": [
      {
        "name": "researcher",
        "role": "Senior Research Analyst",
        "goal": "Uncover cutting-edge developments in AI and data science",
        "backstory": "You work at a leading tech think tank. Your expertise lies in identifying emerging trends. You have a knack for dissecting complex data and presenting actionable insights",
        "tools": [
          {
            "id": "urn:sd-core:crewai.builtin.websiteSearchTool",
            "opts": {
              "safesearch": "off"
            }
          },
          {
            "id": "urn:sd-core:crewai.builtin.serperDevTool"
          }
        ],
        "allow_delegation": false
      },
      {
        "name": "writer",
        "role": "Tech Content Strategist",
        "goal": "Craft compelling content on tech advancements",
        "backstory": "You are a renowned Content Strategist, known for your insightful and engaging articles. You transform complex concepts into compelling narratives.",
        "allow_delegation": true
      }
    ],
    "tasks": [
      {
        "description": "Conduct a comprehensive analysis of the latest advancements in AI in 2024. Identify key trends, breakthrough technologies, and potential industry impacts.",
        "expected_output": "Full analysis report in bullet points.",
        "agent": "researcher"
      },
      {
        "description": "Using the insights provided, develop an engaging blog post that highlights the most significant AI advancements. Your post should be informative yet accessible, catering to a tech-savvy audience. Make it sound cool, avoid complex words so it doesn't sound like AI.",
        "expected_output": "Full blog post of at least 4 paragraphs",
        "agent": "writer"
      }
    ],
    "verbose": true,
    "process": "sequential"
  }
}"""

service = ivcap.get_service_by_name("crewia-agent-runner")
pp.pprint(service)

# job = Job(ivcap, id="urn:ivcap:job:b2823888-e0ca-4e01-8b34-a4f4bceacc78", service=service)
# job.status(refresh=True)
# pp.pprint(job)

count = 5
jobs = []
for _ in range(count):
    job = service.request_job(io.StringIO(crew), timeout=0)
    jobs.append(job)

running_jobs = set(jobs)
while running_jobs:
    print(f".. checking on {len(running_jobs)}")
    job = running_jobs.pop()
    status = job.status(refresh=True)
    if status == "succeeded":
        print(f"Job {job} done")
    elif status == "error":
        print(f"Job {job} failed")
    else:
        running_jobs.add(job) # not done yet, add back
    sleep(5)  # wait a bit before trying again

print("All jobs finished")
# if job.status_code == 202:
#     pp.pprint(job.json())
# else:
#     pp.pprint(job)
