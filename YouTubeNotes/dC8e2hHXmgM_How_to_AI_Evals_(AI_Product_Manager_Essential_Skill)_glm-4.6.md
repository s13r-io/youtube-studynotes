<!-- 
Source: https://www.youtube.com/watch?v=dC8e2hHXmgM
Channel: LiftoffPM
Duration: 12:26
Generated: 2025-12-06 12:46:45
Provider: Z.AI GLM-4.6
Transcript Words: ~2,250
-->

**Estimated Read Time:** 7 min


### AI Evals: The PM's Guide to Testing Gen AI Products

**Hashtags:** #AI #ProductManagement #GenAI #AIEvals #LLM #TechSkills #OpenAI #Anthropic

### 1. THE HOOK
Traditional tests fail for AI. This skill, praised by leaders at OpenAI and Anthropic as a core PM competency, is how you'll define and measure success for unpredictable AI products. Mastering evals transforms you from a feature shipper into a quality architect for the AI era.

### 2. CORE CONCEPT — The WHAT and WHY
Imagine you're a film critic. You don't just check if a movie has a beginning, middle, and end (correctness); you judge the acting, cinematography, and pacing (quality, style). **AI Evals** (AI evaluations) are your detailed rubric for grading a generative AI system. Unlike traditional software, which is **deterministic** (the same input always produces the same output), Gen AI is **non-deterministic**—asking the same question twice can yield different answers. This variability makes simple unit tests useless for measuring quality. Evals allow you to assess subjective dimensions like tone, creativity, safety, and brand alignment. They are the essential bridge between the fuzzy, creative nature of AI and the concrete requirements of a product. So how do you build a consistent quality standard for a system that's inherently inconsistent? You create a system of evals.

### 3. HOW IT WORKS — The HOW
Building a robust eval system is a four-step process that turns subjective quality into a measurable metric. This framework allows your team to iterate on AI models with confidence and speed.

`Step 1: Create Goldens → Step 2: Generate Synthetic Data → Step 3: Grade Outputs → Step 4: Build an Auto-rator`

**Step 1: Create Goldens**
"Goldens" are perfect, human-curated examples of ideal input-output pairs. As the PM, you lead the charge in defining these. They cover not just happy paths but also critical edge cases and failure scenarios. For a customer service bot, goldens would include:
*   **Input:** "I need a refund for order #12345." → **Output:** "Happy to help. Let me start the refund process. Was there anything wrong with your order?"
*   **Input:** "You guys are the worst, I can't believe I'm talking to a bot!" → **Output:** "I'm sorry to hear you're frustrated. Let me connect you to a human agent. What's the best number to reach you?"
This upfront work is intensive—a real team might write hundreds—but it creates the foundation for your entire quality standard.

**Step 2: Generate Synthetic Data**
A few hundred goldens aren't enough to test at scale. You use a separate LLM to generate thousands of variations of your goldens. This "synthetic data" expands test coverage for common cases, rare edge cases, and even adversarial attacks. A huge bonus is that you avoid using real user data, protecting privacy and PII (Personally Identifiable Information).

**Step 3: Grade the Outputs**
Now, you and your team act as the first judges. You grade the synthetic data on the dimensions you care about, creating a "source of truth." For the bot, this might be a binary pass/fail for accuracy and a 1-5 scale for tone. For a more creative product, like a 10-minute bedtime story generator, the criteria might be more complex: story coherence (1-5), image style match (1-5), etc. This human-graded data is the gold standard your AI will learn from.

**Step 4: Build an Auto-rator**
Human grading is expensive and slow. The final step is to train an AI model—your "auto-rator"—to mimic your human graders. You prompt it with instructions like: "You are an expert evaluator for a children's story app. Grade these new stories on a scale of 1-5 for coherence and style, using these examples of good and bad stories as your guide." You validate its performance by comparing its grades to the human grades (aiming for ~95% agreement). Once trusted, this auto-rator lets you test new model changes in minutes, not days, telling you instantly if you've improved, maintained, or degraded quality.

### 4. THREE PERSPECTIVES
**Perspective 1: Real-World Application**
Leaders at Anthropic have stated that writing evals is a core part of their PM interview process. Candidates are given a "crappy eval" and asked to improve it, demonstrating their ability to think about AI quality. Companies like Intercom and Zendesk building AI support agents use this exact methodology to ensure their bots are helpful, on-brand, and safe before they ever interact with a customer.

**Perspective 2: Technical Deep-Dive**
Under the hood, auto-rators are typically fine-tuned or prompted LLMs (like GPT-4 or Claude 3). The human-graded dataset from Step 3 acts as the fine-tuning data or a few-shot prompt. For specific tasks, teams might also use standard evaluation metrics like ROUGE (for text summarization overlap) or FID (Fréchet Inception Distance for image quality/realism) as part of their grading rubric.

**Perspective 3: Common Pitfall**
Here's where people stumble: they build an auto-rator and think they can "set it and forget it." Human oversight is non-negotiable. You must continuously spot-check the auto-rator's grades, especially for nuanced dimensions like tone or creativity. More importantly, the world changes, and your "goldens" can become outdated. Humans must constantly refine the goldens and retrain the auto-rator to prevent "model drift" and ensure quality stays aligned with evolving user expectations and brand standards.

### 5. PRACTICAL CHEAT SHEET
- **When Relevant:** Anytime you are building a product feature that uses a Large Language Model (LLM) or other generative AI.
- **Watch Out For:** "Golden Rot"—your perfect examples becoming outdated as your product or user needs evolve. Schedule regular reviews of your goldens.
- **Quick Win:** For your next AI feature, write down 5-10 "golden" input-output examples that define the ideal behavior. This clarifies requirements for the entire team.
- **Common Confusion:** Thinking an auto-rator removes the need for human judgment. It only scales it; it doesn't replace it.
- **Limitations:** Evals struggle to measure truly novel or groundbreaking creativity. They are best at ensuring consistency and quality against a defined standard.

### 6. KEY TERMS GLOSSARY
**AI Evals:** The overall process of evaluating a non-deterministic AI system using structured tests and rubrics.
**Non-Deterministic:** A system where the same input can produce different outputs on different runs (like most Gen AI models).
**Goldens:** Human-curated, perfect input-output examples that serve as the benchmark for quality.
**Synthetic Data:** Artificially generated data (often by an LLM) that mimics real data, used to scale up testing.
**Auto-rator:** An AI model trained to automatically evaluate the outputs of another AI system against a set of criteria.
**Rubric:** A scoring guide or framework used to grade qualitative aspects like tone, style, or coherence.
**PII (Personally Identifiable Information):** Sensitive personal data that synthetic data helps avoid using in testing.

### 7. MEMORY ANCHORS
**One-Sentence Summary:** AI evals use human-defined "goldens" to train an AI grader, enabling fast, consistent testing of non-deterministic AI systems.

**The Analogy to Remember:** AI evals are like creating a master rubric and then training an expert teaching assistant to grade papers for you.

**5 Flashcard Q&A:**
**Q:** What is the core problem AI evals solve? | **A:** They provide a way to measure quality and consistency in non-deterministic Gen AI systems, where traditional unit tests fail.
**Q:** What is a "golden" in the context of AI evals? | **A:** A human-curated, perfect example of an input and its ideal output, used as a benchmark for quality.
**Q:** Why is synthetic data generation a key step? | **A:** It scales test coverage to thousands of scenarios without using real, potentially sensitive user data.
**Q:** What is the ultimate goal of building an auto-rator? | **A:** To automate the evaluation process, allowing product teams to iterate and test AI model changes much faster.
**Q:** Why can't you fully remove humans from the eval process? | **A:** Humans are needed to create the initial goldens, spot-check the auto-rator for nuance, and update the quality standard as the product evolves.

**3 Deeper Questions:**
1. What happens to your product's quality if your initial "goldens" contain hidden biases?
2. How would you explain the ROI (return on investment) of spending weeks building an eval system to a skeptical engineering manager?
3. When is a simple, deterministic unit test still a better choice than a complex AI eval system?

### 8. KEY MOMENTS
- [~1:30] The core problem explained: Deterministic vs. Non-deterministic systems.
- [~4:00] The 4-step process for setting up an eval system begins.
- [~12:30] A second, more creative example is introduced: a bedtime story generator for kids.
- [~16:30] The critical reminder that human oversight never goes away.