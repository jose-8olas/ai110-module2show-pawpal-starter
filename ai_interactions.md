# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

The agent helped develop a function method that would find the earliest avaiable time for a new task. Howevre, it must not overlap with existing tasks.

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

It reviewed the existing Scheduler class in the pawpal_system.py
Then suggested implemnetation and explained how it worked
Then it suggested testing it and created tests so I could run them

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

I reviewed the implementation and explanation of it. Also, reviewed the test cases generated.
I ran the pytest to check and I saw that all test cases passed.

<!-- Describe anything the agent got wrong or that required human review -->

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

|                       | Option A                                                            | Option B |
| --------------------- | ------------------------------------------------------------------- | -------- |
| **Model / tool used** | Chatgpt 6                                                           | Claude   |
| **Prompt**            | I am developing a Python pet care scheduling system called PawPal+. |

I need to implement a weekly recurring task rescheduling feature.

Requirements:

1. When a weekly task is completed, mark the original task as completed.
2. Create a new task scheduled exactly 7 days after the original task's due date.
3. Preserve the original task's title, task type, duration, priority, time, and frequency.
4. The new task must have completed=False.
5. The original completed task must remain in the system.
6. Avoid modifying the original task when creating the next occurrence.

Provide a Python implementation using a dataclass Task and explain how the logic works. Also identify possible edge cases and testing scenarios. | same as chatgpt |
| **Response summary** | Provided implemenatation of the Scheduler class, task class | Provided implementation and all test cases |
| **What was useful** | Provided implemenataion | Provided implemenatation and test cases. These test cases are useful to see if the code works as intended |
| **Problems noticed** | The implementation would need to be adjusted to my current code | The implementation would need to be adjusted to my current code |
| **Decision** | Useful for foundation of skeleton code | Useful for test cases implemenatation |

**Which approach did you use in your final implementation and why?**

I used combination of both. Both offered very good solutions. Claude offered test cases and chatgpt provided implementation.

<!-- Your conclusion -->
