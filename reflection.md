# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
  System should be able to add pet owners and pets, connect owners to their pets. Be able to add/edit taks, mark tasks as completed when they are done. Take contraints like owner preference in time, priotity and types of task. Users should also be able to schedule a task and see today's task.

   Owner: The person a oet belongs to.
   Name
   Age
   Busy time

   Pet: Pet that the tasks needs to be done on by the owner.
   Name
   Age
   Type
   Breed

   Task: Individual tasks that needs to be done.
   Task title
   Duration
   Priority

   Scheduler: Holds all the tasks and keeps track of them.
   Today Task
   Task left
   Completed Task

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
  Yes, Now there will only be one shceduler per owner regardless of the quanity of the pets they own.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
  My scheduler uses a lightweight conflict check that only flags exact HH:MM matches instead of trying to detect overlapping task durations. That tradeoff keeps the code easy to read and fast enough for a small pet-care planner, even though it will miss some more complex time conflicts.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
  I used AI to break the project into phases, check the UML against the code, and refine the scheduler and tests. The most helpful prompts were specific ones about design choices, edge cases, and whether a change still fit the system goals.

   The most useful features were code exploration, refactoring help, and turning vague requirements into concrete classes and methods.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
  I rejected a suggestion to add full overlap detection because it would have made the scheduler harder to explain and test. I kept the simpler exact-time warning and verified it with tests and a demo run.

   I also kept one scheduler per owner instead of spreading scheduling across multiple objects.

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
  I learned that the lead architect still has to make the final design decisions. AI helps most when it supports the plan instead of replacing it.
