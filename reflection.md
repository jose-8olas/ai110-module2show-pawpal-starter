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

Yes. I chnaged it by adding prefernces attribute so it can consider the owner's preferinces for budiling a plan. Additionally, I also added sort_tasks(), detect_conflicts(), and generate_daily_plan(). Mostly kept the same structure for four classes.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

My system finds any mactching date and time to detect conflicts. Although, this is very easy to understand, there is a tradeoff. If task overlaps during a time duration, it won't detect it. If one task starts at 8:00 am and another starts at 8:15 and each of their durations are approxiamtely 30 minutes, these two tasks conflict.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
