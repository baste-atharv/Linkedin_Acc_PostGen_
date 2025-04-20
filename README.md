### Project: LinkedIn Post Generator from accounts

#### Project Description
This project is a Generative AI (GenAI) application designed to automatically create engaging LinkedIn posts from public linkedin accounts posts. It leverages a language model (LLM) to generate concise, professional, and engaging LinkedIn content that highlights that analyses tone, writing style, engagement metrics, comments of the posts, making it ideal for content creators, marketers, and social media managers.

#### Project Workflow
1. **Content Scraping**:Challenge: LinkedIn API is restrictive and doesn't allow access to user content without special permissions. 
Solution:
Wrote a custom Selenium script that logged into LinkedIn using session cookies
2. **Tag Generation**: Parsed the raw Markdown content,Analyzed the article to generate relevant tags that enhance post visibility and engagement on LinkedIn.
3. **Post Creation with LLM**: Assistant Agent Creation
Agent 1: Content Tagger
Parses individual posts, Assigns tags: content_type, tone, structure, intent
Returns output in clean JSON format.

Agent 2: Post Writer
Takes text and tags from Agent 1
Generates variations per post
Follows structure rules (12-15 word paragraphs, 5-10 hashtags)
Also user can incorporate his feedback.

#### Key Learnings and Concepts

- **Structured Output**: 2 differnet agents were necessary for a structured flow and to avoid hallucination. Also for scalability(not done in this project due to API credit constraints and time deadline), each new linkedin account to be analysed should be a differnt agent.
- **Tag Relevancy and Optimization**: Using NLP techniques to ensure the tags are relevant and increase the post’s reach.
- **Prompt Engineering**: Crafting prompts that help the LLM accurately capture and convey the main ideas of the article in a LinkedIn-friendly format.
- **MCP**: MCP allows agents to build memory beyond single-thread interactions, enabling real-time updates to preferences and better continuity. Can be done using MCP but ready frameworks not available at the time and time deadlines.

#### Future Improvements

-Implementing persistent memory via OpenAI's retrieval + file search tools or MCP
-Creating a Streamlit UI for feedback collection and post selection



