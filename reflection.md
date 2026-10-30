# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
  The UML Design will include Owner, Tasks, Pets, and Scheduler. The Owner class will contain information about the owner and corresponding pets. The Task class will contain information from specific activities, title duration, etc. The Pet class will contain information regarding the pet and tasks assigned to pets. Lasty the Scheduler tasks will manage all tasks keeping track of the times

3 core actions use should perform: Adding pets, creating and managing tasks, generate daily plan possibly

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes. I changed it by adding prefernces attribute so it can consider the owner's preferinces for budiling a plan. Additionally, I also added sort_tasks(), detect_conflicts(), and generate_daily_plan(). Mostly kept the same structure for the four classes.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers time, priortity, and prefernces in the system.
The constraints that matter the most for me was the time and duration of tasks. If two tasks overlap in starting, then we will have conflicting times. We may have a task that starts at 9:00am with duration fo 30 minutes and another task starting at 9:00am with duration of 40 minutes. These two tasks will conflict.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

My system finds any mactching date and time to detect conflicts. Although, this is very easy to understand, there is a tradeoff. If task overlaps during a time duration, it won't detect it. If one task starts at 8:00 am and another starts at same time, the two tasks conflict

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI to help brainstorming my UML digaram and building the different classes in the UML to actual code. Addiontionally, I used AI to help refactor some functions and improve the readibility of code.

Some helpful prompts/ questions:
How should I organize my UML diagram and what factors should I consider before buidling?
Give me the skeleton code for the classes from the UML diagram
How can I improve my code to increase readibility?
What went wrong here for my function?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I denied AI suggestion when it started suggesting more complex features for my system that seemed a bit too much for the project.

For AI genearted code, I tested the code by manualy running the code and also used pytest and made some tests to see if the code was running as expected.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

There wre several behaviors I tested such as sorting of schudle time, adding tasks, adding pets, checks for confilcting times of tasks, and much more.

These tests are importnant because we want the app to be functional and we do not want conflicting times for tasks. We cannot perform tasks at the same time.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I think my schdueler works as intended as I manually ran the application and made tests using pytest to check different behaviors.

If I had more time I would add other test edge cases, such as tasks exceeding time limit, invalid durations of the tasks, amd other edge cases.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am satisfied with the application being to able to sucessfully add pets and tasks. We can modify the tasks to different names and categories as desired. Additionally, I am happy with the scheudle geneartion as well, which lets users see all tasks.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would further improve conflict detection to handle more scanerios. For example, if two tasks overlap in duration. For example, one task can start at 8:00am and have a duration of 30 mins and another task may start at 8:15am with a duration of 30 minutes. These two tasks will overlap and conflict

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

It is always importanat to plan and brainstorm the project. Start off with the basics and skeleton code. Then gradually build up and use AI to my advantage when stuck. Overall, this project really helped me learn how to use AI.
