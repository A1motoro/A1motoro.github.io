# 第二小时：使用 AI 进行数据分析 - 正确的方法

## 🎯 学习目标
到课程结束时，您将能够：
- 理解分析任何数据集的系统方法
- 使用 AI 指导您完成正确的数据分析工作流程
- 提出关于数据质量和结构的正确问题
- 培养数据探索的分析思维能力
- 使用 AI 辅助创建全面的数据分析计划

## 🚀 数据分析思维

**在我们开始编码之前，让我们理解数据分析的正确方法：**

数据分析就像当侦探一样 - 您需要：
1. **勘察犯罪现场**（理解您的数据）
2. **寻找线索**（识别模式和问题）
3. **追踪证据**（分析关系）
4. **得出结论**（解释发现）

**黄金法则**：永远不要在不首先理解您正在处理什么的情况下开始分析数据！

## 📊 第一部分：数据理解与评估
### **步骤 1：了解您的数据**

#### **数据概览的 AI 提示：**
> "我有一个名为 'UM_C19_2021.csv' 的新数据集。在我分析它之前，帮助我理解我正在处理什么。我应该首先问这个数据什么问题？"

**AI 应该帮助您思考的内容：**
- 这个数据集代表什么？
- 我们有多少条记录和列？
- 列名是什么，它们意味着什么？
- 这个数据涵盖什么时间段？
- 这个数据集的主要目的是什么？

**学生行动**：逐一询问 AI 这些问题来建立您的理解。

#### **AI Prompt for Data Structure:**
> "Now that I know what this dataset is about, help me examine its structure. What should I look for to understand how the data is organized?"

**What the AI should guide you to discover:**
- Data types of each column (numbers, text, dates)
- Whether there are missing values
- If the data looks complete and consistent
- Any obvious patterns or anomalies

### **Step 2: Data Quality Assessment**

#### **AI Prompt for Missing Data:**
> "I want to check if my data has any quality issues. How should I approach looking for missing values, duplicates, or other problems?"

**What the AI should help you investigate:**
- Are there missing values in any columns?
- Do the missing values follow a pattern?
- Are there duplicate records?
- Do the data values make sense (e.g., negative numbers where they shouldn't be)?

#### **AI Prompt for Data Validation:**
> "Help me validate that my data makes sense. What should I check to ensure the data quality is good enough for analysis?"

**What the AI should guide you to verify:**
- Date ranges are logical
- Numbers are within expected ranges
- Categorical variables have reasonable values
- No obvious data entry errors

## 🧹 Part 2: Data Cleaning & Preprocessing 
### **Step 3: Handling Data Issues**

#### **AI Prompt for Missing Data Strategy:**
> "I found some missing values in my dataset. Help me think through the best approach to handle them. What questions should I consider?"

**What the AI should help you decide:**
- Why are values missing? (random vs. systematic)
- How many values are missing?
- Should I remove, fill, or investigate further?
- What impact will my decision have on the analysis?

#### **AI Prompt for Outlier Detection:**
> "I want to identify any unusual values in my data that might be outliers. How should I approach this systematically?"

**What the AI should guide you to consider:**
- What defines an "outlier" for your specific data?
- Are unusual values errors or legitimate data?
- How should you handle outliers once identified?
- What might outliers tell you about your data?

## 🔍 Part 3: Exploratory Data Analysis 
### **Step 4: Understanding Individual Variables**

#### **AI Prompt for Univariate Analysis:**
> "Now I want to understand each variable in my dataset individually. What should I look for when examining each column?"

**What the AI should help you explore:**
- What are the typical values for each variable?
- How are the values distributed?
- Are there any patterns or trends?
- What insights can you draw from single variables?

### **Step 5: Exploring Relationships**

#### **AI Prompt for Bivariate Analysis:**
> "I want to understand how different variables relate to each other. What relationships should I investigate first?"

**What the AI should guide you to examine:**
- How do positive and negative cases relate to time?
- Are there differences between residence types?
- What patterns emerge when you compare variables?
- Which relationships are most interesting or important?

### **Step 6: Time-Based Analysis**

#### **AI Prompt for Temporal Patterns:**
> "Since this is COVID-19 data over time, what time-based patterns should I look for? How should I approach analyzing trends?"

**What the AI should help you investigate:**
- Daily, weekly, and monthly patterns
- Peak periods and their characteristics
- Seasonal or cyclical trends
- Changes over time in different categories

## 📈 Part 4: Statistical Insights 
### **Step 7: Drawing Statistical Conclusions**

#### **AI Prompt for Statistical Summary:**
> "I want to create a comprehensive summary of my findings. What key statistics and insights should I focus on?"

**What the AI should help you identify:**
- Most important patterns in the data
- Key differences between groups
- Significant trends over time
- Surprising or unexpected findings

#### **AI Prompt for Business Insights:**
> "How can I translate my statistical findings into meaningful insights that someone could act on?"

**What the AI should guide you to consider:**
- What do the numbers actually mean?
- What actions could be taken based on these findings?
- What questions remain unanswered?
- What additional analysis might be needed?

## 🎨 Part 5: Visualization Strategy 
### **Step 8: Choosing the Right Charts**

#### **AI Prompt for Visualization Planning:**
> "I want to create visualizations that tell the story of my data. What types of charts would be most effective for showing my key findings?"

**What the AI should help you decide:**
- Which charts best show trends over time?
- How to compare different groups effectively?
- What visualizations highlight your main insights?
- How to create a coherent narrative with multiple charts?

### **Step 9: Creating Impactful Visualizations**

#### **AI Prompt for Chart Design:**
> "Help me think about how to make my visualizations clear and impactful. What design principles should I consider?"

**What the AI should guide you to focus on:**
- Clear titles and labels
- Appropriate color choices
- Chart types that match your data
- How to avoid misleading representations

## 🤖 AI Prompting Best Practices for Data Analysis

### **Effective Prompt Structure:**
1. **Start with Understanding**: "Help me understand what I'm looking at..."
2. **Ask for Guidance**: "What should I consider when..."
3. **Request Systematic Approach**: "How should I approach..."
4. **Seek Interpretation Help**: "What does this tell me about..."

### **Common AI Commands:**
- **`Ctrl + K`**: Open AI chat
- **`Ctrl + I`**: Inline AI suggestions
- **`Ctrl + Shift + I`**: Generate code from selection

### **Prompt Examples for Each Phase:**

#### **Data Understanding:**
```
"What questions should I ask about this dataset first?"
"How can I assess the quality of my data?"
"What should I look for when examining the structure?"
```

#### **Data Cleaning:**
```
"How should I approach handling missing values?"
"What's the best way to identify outliers?"
"How do I decide whether to remove or fix data issues?"
```

#### **Exploratory Analysis:**
```
"What patterns should I look for in this data?"
"How should I investigate relationships between variables?"
"What time-based analysis would be most valuable?"
```

#### **Statistical Insights:**
```
"What are the key findings from my analysis?"
"How can I interpret these statistical results?"
"What insights would be most actionable?"
```

#### **Visualization:**
```
"What charts would best show my key findings?"
"How should I design visualizations for clarity?"
"What story am I trying to tell with my data?"
```

## 🧪 Hands-On Practice

### **Exercise 1: Data Understanding**
1. Use AI to guide you through understanding your dataset
2. Ask systematic questions about data structure and quality
3. Document your findings before proceeding

### **Exercise 2: Quality Assessment**
1. Work with AI to identify data quality issues
2. Develop strategies for handling problems
3. Make informed decisions about data cleaning

### **Exercise 3: Systematic Exploration**
1. Use AI to guide your exploratory analysis
2. Focus on one aspect at a time
3. Build understanding step by step

### **Exercise 4: Insight Development**
1. Work with AI to interpret your findings
2. Develop actionable insights
3. Plan effective visualizations

## 🔍 Troubleshooting Common Issues

### **AI Not Understanding Your Data:**
- Provide more context about your dataset
- Ask specific questions about what you're trying to understand
- Break down complex questions into simpler parts

### **Getting Overwhelmed:**
- Focus on one phase at a time
- Ask AI to help you prioritize what to look at first
- Don't try to analyze everything at once

### **Unclear Results:**
- Ask AI to help you interpret what you're seeing
- Request simpler explanations
- Ask for help translating numbers into insights

## 📚 Key Takeaways

1. **Always start with understanding** - never jump into analysis
2. **Use AI to guide your thinking process**, not just generate code
3. **Follow a systematic workflow** - quality first, then exploration, then insights
4. **Ask the right questions** before seeking answers
5. **Build understanding step by step** - don't rush the process

## 🎯 Next Steps

Next, you'll learn to:
- Create comprehensive analysis reports using AI
- Develop data storytelling skills
- Apply your analytical thinking to different types of data
- Build confidence in making data-driven decisions

---

**Practice Tip**: Remember, you're not just learning to use AI - you're learning to think like a data analyst. The AI is your guide, but you're the detective! 🕵️‍♀️🚀

