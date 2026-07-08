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

The scheduler considers priority (tasks are sorted high -> medium -> low before anything else), available time (Owner.available_minutes caps the day, and each task checks fits_in(minutes_remaining) before being placed), preferred time (Task.time, used for sorting and conflict detection), and completion status (completed tasks are excluded entirely). I decided priority mattered most because a pet's schedule is really about urgency. A dog needing a walk matters more than optional playtime. Priority is the primary sort key and time/duration are secondary.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

Scheduler.generate() uses a first-fit greedy algorithm instead of an optimal one: it walks the priority-sorted list once and packs each task in if it fits in whatever time is left, without backtracking to check if skipping a task would let two smaller ones fit better. This is reasonable because a pet owner's task list is small (a handful of tasks per pet), so the greedy approach is easy to reason about and predict ("higher priority always gets scheduled first"), and the loss versus a perfectly optimal packing is negligible compared to the gain in simplicity and code I can actually trust and debug.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

Claude was used for debugging, testing, and design review. It checked my UML early on, added some additional sections that could give me help, which i ended up liking and decided to use, it helped resolve certain bugs with regards to app.py not wanting to open up, as well as discovering that there was a bug where owner data would be deleted and  not saved. "what edge cases matter for sorting and recurring tasks" was a great  prompt to use.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

when trying to open up streamlit, claude suggested that there was a bug with the code, however after digging through, it was just the way I was trying to run the file that made it not work. I didnt jump immediately to accept its answer, i looked for my answer first.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I focused tests on the three behaviors most likely to have subtle bugs: sorting correctness (Scheduler.sort_by_time() — chronological order, untimed tasks sorted last, stable ordering for ties), recurrence logic (Pet.complete_task() correctly queuing the next daily/weekly occurrence, and not doing so for non-recurring or duplicate-titled tasks), and conflict detection (Scheduler.detect_conflicts() flagging real overlaps while correctly treating back-to-back, non-overlapping tasks as conflict-free, i.e. 2 tasks at same time). These mattered because they're the parts of the scheduler with the most hidden logic; boundary conditions (exact adjacency, ties, missing values) are exactly where greedy/sorting algorithms can go wrong.




**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I'm confident (4/5) that the scheduler works correctly for the cases I tested, all 15 tests pass.

not sure about other tests, but I will think of new ones when i revisit this.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm happy with how I split the code into separate pieces, one class for the data (Task, Pet, Owner) and one for the scheduling logic (Scheduler). That made it a lot easier to test each part on its own instead of testing everything at once.


**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I'd test the recurring tasks and the schedule generator together, since right now I only tested them separately. Besides that, I don't know yet.



**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The biggest thing I learned is that my README and UML can say one thing while my code actually does something else, and I won't notice unless I go back and compare them. Checking my docs against my actual code helped me catch real bugs, like one that was deleting a user's pets by accident. Not only that, but the use of AI helps me catch onto bugs and solve them faster, helping me in the end to complete this project.