# 🏛️ Board Agent

A sophisticated AI-powered board review system that simulates a multi-expert advisory board to evaluate proposals across legal, ethical, financial, and technical dimensions. Built with LangGraph and Google's Gemini AI.

## 🌟 Features

- **Multi-Expert Review**: Simulates a board of advisors including:
  - Legal Advisor (Indian Penal Code compliance)
  - Ethics Expert (ethical concerns and fairness)
  - Financial Analyst (cost analysis and ROI)
  - Technical Analyst (feasibility and technical risks)
  - Final Verdict Generator (comprehensive decision)

- **Structured Workflow**: Uses LangGraph to orchestrate a sequential review process
- **Comprehensive Analysis**: Each expert provides detailed feedback with specific verdicts
- **Risk Assessment**: Final verdict includes overall risk level and deployment recommendations
- **Google Gemini Integration**: Powered by Google's advanced Gemini 2.0 Flash model

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google AI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Board-Agent.git
   cd Board-Agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Google AI API key**
   ```bash
   export GOOGLE_API_KEY="your_api_key_here"
   ```
   Or the system will prompt you to enter it when you run the application.

### Usage

#### Running the Main Application

```bash
python main.py
```

The application will run with a default proposal about AI surveillance in schools. You can modify the `user_input` variable in `main.py` to test different proposals.

#### Using the Jupyter Notebook

```bash
jupyter notebook Board_Agent.ipynb
```

The notebook provides an interactive environment to experiment with different proposals and see the step-by-step review process.

## 📋 Example Proposals

The system comes with several example proposals:

1. **AI Surveillance in Schools**: Exam monitoring system using webcam footage
2. **Smart Traffic Lights**: City-wide AI traffic management system
3. **Medical AI Assistant**: TB detection system for hospitals

## 🏗️ Architecture

The Board Agent uses a sequential workflow where each expert reviews the proposal and passes their analysis to the next expert:

```
Technical Analyst → Ethics Expert → Legal Advisor → Financial Analyst → Technical Analyst (2nd review) → Final Verdict
```

### State Management

The system uses a `ReviewState` TypedDict to manage the review process:

```python
class ReviewState(TypedDict):
    proposal: LastValue[str]
    legal_feedback: str
    ethics_feedback: str
    technical_feedback: str
    financial_feedback: str
    policy_feedback: str
    final_verdict: str
```

## 🔧 Configuration

### Model Settings

The system uses Google's Gemini 2.0 Flash model with the following configuration:

```python
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-thinking-exp-01-21",
    temperature=0.2
)
```

### Customizing Expert Prompts

Each expert has a structured prompt that can be customized in the respective functions:
- `legal_advisor()`: Focuses on Indian Penal Code compliance
- `ethics_expert()`: Evaluates ethical concerns and fairness
- `financial_analyst()`: Assesses costs, ROI, and sustainability
- `technical_analyst()`: Evaluates feasibility and technical risks

## 📊 Output Format

Each expert provides structured feedback including:

- **Issues/Risks**: Specific concerns identified
- **Suggestions**: Recommended modifications or mitigations
- **Verdict**: Clear recommendation (e.g., "Legal/Not Legal", "Ethical/Not Ethical")

The final verdict includes:
- **Overall Risk Level**: Low/Medium/High
- **Deployment Recommendation**: Yes/No with conditions
- **Rationale**: Concise explanation of the decision

## 🛠️ Development

### Project Structure

```
Board-Agent/
├── main.py                 # Main application script
├── Board_Agent.ipynb      # Jupyter notebook for interactive use
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore           # Git ignore rules
├── LICENSE              # MIT License
├── config.py            # Configuration settings
└── examples/            # Sample proposals
    ├── surveillance_proposal.txt
    ├── traffic_proposal.txt
    └── medical_proposal.txt
```

### Adding New Experts

To add a new expert to the board:

1. Create a new function following the pattern of existing experts
2. Add the expert to the StateGraph builder
3. Update the ReviewState TypedDict if needed
4. Connect the expert in the workflow

### Customizing the Workflow

The workflow can be modified by changing the edges in the StateGraph:

```python
builder.add_edge("expert1", "expert2")
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- Powered by [Google Gemini AI](https://ai.google.dev/)
- Uses [LangChain](https://github.com/langchain-ai/langchain) for LLM integration

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/Board-Agent/issues) page
2. Create a new issue with detailed information
3. For discussions, use the [Discussions](https://github.com/yourusername/Board-Agent/discussions) tab

## 🔮 Future Enhancements

- [ ] Web interface for proposal submission
- [ ] Support for multiple AI models
- [ ] Custom expert configurations
- [ ] Export reports in PDF format
- [ ] Integration with external APIs for real-time data
- [ ] Multi-language support
- [ ] Batch processing capabilities

---

**Made with ❤️ for better decision-making**