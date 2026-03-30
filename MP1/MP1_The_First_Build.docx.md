**MINI-PROJECT 1**

**The First Build**

*AI-Directed Engineering with Goal & Direction*

| Type | Individual |
| :---- | :---- |
| **Points** | 100 points (Part A: 50 pts | Part B: 50 pts) |
| **Due Date** | Monday, April 13, 2026 at 11:59 PM (both Part A and Part B) |
| **Primary Pillar** | Goal & Direction ★★★ |
| **Tools** | GitHub Codespaces, GitHub Copilot Pro, Frontier AI (Claude, ChatGPT, Gemini, etc.) |

# **Overview**

This project has two parts that introduce you to both the foundations of machine learning and the practice of AI-directed engineering.

**Part A** is a guided Jupyter notebook that gives you a visual tour of how machine learning works under the hood — data as vectors, training through gradient descent, classification boundaries, overfitting, and real embeddings. This is the lab companion to our “How AI Thinks” sessions.

**Part B** is a real engineering design problem. You’ve received a design brief from your manager at ACME Robotics (see the attached brief document). Your job: collaborate with AI to design the gear train and linkage for the MiniClaw gripper. The emphasis is on **Goal & Direction**: how well you define the problem, direct the AI, catch its mistakes, and evaluate the results.

# **Part A: Under the Hood**

*Due: Monday, April 13 at 11:59 PM  |  50 points  |  \~60–90 minutes*

Open the provided Jupyter notebook in your GitHub Codespace and work through six sections: Setup, Data as Vectors (2D→3D→nD), Regression and Gradient Descent, Classification and Overfitting, Real Word Embeddings, and Reflection. Most code is pre-written — look for the YOUR TURN cells where you experiment and the Reflection cells where you write.

### **Submit:**

* Completed notebook pushed to your course repository (all cells run, outputs visible)

* YOUR TURN cells showing meaningful experimentation

* Three reflection responses (2–3 thoughtful sentences each)

# **Part B: MiniClaw Gear Train Design**

*Due: Monday, April 13 at 11:59 PM  |  50 points*

Read the attached design brief from Jordan Chen carefully. Then, using AI as your engineering partner, design the gear train and linkage for the MiniClaw gripper.

## **Deliverables**

1. **Goal Statement (half page):** Your engineering requirements, success criteria, and key unknowns — written before you start designing. This is a mini PRD.

2. **Design Iteration Log:** Minimum 3 documented iterations showing how your design evolved through AI collaboration. Each: your prompt → AI response → your engineering assessment → what changed.

3. **Final Design Package:** A Python script or notebook (built with Copilot) that outputs your gear parameters, verifies constraints, and includes a diagram or sketch of the arrangement.

4. **Trust Assessment (one paragraph):** Where did AI help most? Where did it mislead you? What needs verification before prototyping?

# **Grading Rubric**

Every mini-project is evaluated across all five pillars. The weight shifts based on the project’s primary emphasis. Part A and Part B are weighted equally.

## **Part A: Under the Hood (50 points)**

| Component | Points | What We Are Looking For |
| :---- | ----- | :---- |
| **Completion & Experimentation** | **30** | All cells run. YOUR TURN cells show genuine experimentation (changed values, tried different inputs, explored beyond the minimum). Not just running the defaults. |
| **Reflections** | **20** | Three thoughtful reflections that demonstrate observation, connection to course concepts, and curiosity. Generic responses (“I learned a lot”) earn minimal credit. |

## **Part B: MiniClaw Design (50 points)**

| Pillar | Points | What We Are Looking For |
| :---- | ----- | :---- |
| **Goal & Direction ★★★** | **20** | Clear requirements with specific success criteria. Evidence the problem was framed before jumping to solutions. Goal statement demonstrates engineering judgment. |
| **Context Management ★** | **3** | Gave the AI appropriate technical context: constraints, equations, material properties, and the design brief requirements. |
| **Tools & Integration ★** | **2** | Used the right tool for each sub-task. Copilot for code, LLM for reasoning, hand calcs for verification. |
| **Centaur Engineering ★★** | **13** | Iteration log shows genuine back-and-forth. Engineering judgment applied to AI outputs. Dead ends documented honestly. |
| **Evaluation & Trust ★★** | **12** | Final design verified against constraints. Trust assessment is specific. Student can articulate what needs checking before fabrication. |
| **Total** | **50** | *Part B subtotal (+ 50 pts Part A \= 100 pts for MP1)* |

# **Reference: Key Gear Equations**

You are expected to use AI to help with these, but you should recognize them and understand what they mean.

| Relationship | Formula / Description |
| :---- | :---- |
| **Pitch Diameter** | d \= m × z   (module × tooth count) |
| **Center Distance** | a \= m × (z₁ \+ z₂) / 2 |
| **Gear Ratio** | i \= z₂ / z₁ \= T₂ / T₁ |
| **Output Torque** | T₂ \= T₁ × i × η   (η ≈ 0.95 per spur stage) |
| **Lewis Bending Stress** | σ \= F\_t / (b × m × Y)   (tangential force, face width, module, form factor) |
| **PLA Strength** | \~50 MPa bulk; use 25–30 MPa for printed parts (layer adhesion) |

| Remember: Be an Engineer The AI is a tool you direct, not a teammate who does the work for you. If you cannot explain what your submission does and why, that is a problem regardless of how polished the output appears. The goal is not a perfect gear train — it’s demonstrating that you can direct AI toward an engineering outcome, evaluate the results, and know what you trust. |
| :---- |

