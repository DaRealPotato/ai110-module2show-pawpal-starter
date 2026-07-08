# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

Here, I have decided on 4 core classes: Owner, Pet, Tasks, Scheduler
A scheduler takes Owner info to see their availability and what needs to be done urgently based on pet's needs. Owner can write down how many pets they have, and for each pet, can write down the tasks that need to be done, as well as what time they should be completed by. from there, a schedule can be created so that owner can then look at and follow to make sure these tasks are done. 


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

I was at first thinking about schedule, however Claude reminded me that it might be better to separate the jobs: one should make the result list, while another is in charge of building it. I personally want to keep it separate, as it might end up being too much code in one file (For the sake of keeping things neat.)

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
