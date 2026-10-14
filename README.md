# How AI Works

An AI and emerging-technology handbook for QA engineers: 58 topics, each in the same template (what it is, how it works, key terms, uses, current state, limitations, QA perspective, what's next, further learning).

Open `index.html` in a browser. It is one self-contained file.

| Part | Covers |
|---|---|
| 1 AI Foundations | Machine learning, neural networks, LLMs, transformers, training, prompting, hallucinations and evals |
| 2 Modern AI Systems | RAG, agents, MCP, vision, speech, NLP, multimodal, recommenders, self-driving, AI engineering, decision models, data engineering, MLOps |
| 3 Hardware and Robotics | Chips, memory, quantisation, data centres, chip manufacturing, robotics, ROS 2, vision-language-action models, simulation, robot safety |
| 4 Future Intelligence | AGI, capabilities and gaps, predictions, society, bias and copyright, AI security, alignment, regulation, economics, research, careers |
| Landscape | Labs, chips, open source and recent advances, dated 14 Oct 2026 |

Fast-moving facts are tagged **production**, **research**, **demo**, **claim** or **reported**, and dated. They will go out of date; check the linked sources.

## Source

`src/` holds the topic data (`p1.py` to `p4.py`, `landscape.py`) and the generator (`gen.py`) that builds the page. The generator currently reads its page shell and font from local paths set at the top of `gen.py`; adjust those to rebuild.

Diagrams use [rough.js](https://roughjs.com) and the Virgil font from [Excalidraw](https://github.com/excalidraw/excalidraw) (SIL Open Font License).
