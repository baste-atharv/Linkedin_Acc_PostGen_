### 🚀 Project: LinkedIn Post Generator from Accounts

---

#### 📌 Project Description

This is a Generative AI (GenAI) application that automatically creates engaging LinkedIn posts by analyzing public LinkedIn content. It leverages a large language model (LLM) to generate concise, professional, and high-engagement posts. The model analyzes tone, writing style, engagement metrics, and comments to craft content that resonates—making it an ideal tool for content creators, marketers, and social media managers.

---

#### 🔄 Project Workflow

1. **Content Scraping**
   - **Challenge**: LinkedIn’s API is highly restrictive and does not allow access to user content without special permissions.
   - **Solution**: Built a custom Selenium script that logs into LinkedIn using session cookies to extract post data.

2. **Tag Generation**
   - Parsed raw Markdown content.
   - Analyzed the post to generate relevant tags (e.g., content type, tone, structure, intent) that boost visibility and engagement.

3. **Post Creation with LLM**
   - **Agent 1: Content Tagger**
     - Parses individual posts.
     - Assigns structured tags: `content_type`, `tone`, `structure`, `intent`.
     - Returns output in clean JSON format.
   - **Agent 2: Post Writer**
     - Takes text and tags from Agent 1.
     - Generates multiple post variations.
     - Adheres to structure rules (e.g., 12–15 word paragraphs, 5–10 hashtags).
     - Incorporates user feedback for iterative improvement.

---

#### 📚 Key Learnings & Concepts

- **Structured Output**  
  Introduced two agents to ensure a clean and scalable workflow while minimizing hallucinations. Ideally, each new LinkedIn account should have a dedicated agent for scalability (not implemented due to API credit limits and time constraints).

- **Tag Relevancy & Optimization**  
  Used NLP techniques to ensure tags are relevant and boost post reach.

- **Prompt Engineering**  
  Crafted prompts to help the LLM extract and articulate key ideas in a LinkedIn-friendly tone.

- **MCP (Model Context Protocol)**  
  Explored using MCP to allow agents to retain memory across interactions for preference updates and content continuity. Ready-to-use frameworks were unavailable during development due to tight deadlines.

---

#### 🔮 Future Improvements

- Integrate persistent memory using OpenAI's **Retrieval + File Search** or **MCP**.
- Build a **Streamlit UI** for:
  - Collecting user feedback.
  - Previewing and selecting post variations.
  - Saving or scheduling posts for publishing.
