def sec(id, title, body):
    return dict(id=id, title=title, short={'claims':'Demo or product?'}.get(id,title), raw=f'<section id="{id}" class="b4 topic">\n  <h2><span class="n">@@CODE@@</span>{title}</h2>\n{body}\n</section>\n\n')

P = '<span class="chip ok">production</span>'
R = '<span class="chip res">research</span>'
D = '<span class="chip warn">demo</span>'
C = '<span class="chip claim">claim</span>'
RP = '<span class="chip claim">reported</span>'

TOPICS = [
sec('labs', 'AI labs and model families', f'''  <p class="what">Last updated <b>14 Oct 2026</b>. This page changes faster than any other; check the source before relying on a row. "Reported" means only press or third-party sources were found.</p>
  <div class="tbl"><table>
    <tr><th>Lab</th><th>Flagship models</th><th>Known for (vendor's own words)</th><th>Weights</th><th>Status</th></tr>
    <tr><td>Anthropic</td><td>Claude Fable 5.1; Opus 5.5, Sonnet 5.5, Haiku 5.5</td><td>Coding, knowledge work, agents; Haiku for cheap high-volume work</td><td>Closed</td><td>{P}</td></tr>
    <tr><td>OpenAI</td><td>GPT-6 family: Astra, Sol, Luna, Instant</td><td>Computer use, coding, science</td><td>Closed</td><td>{P} {RP} dates</td></tr>
    <tr><td>Google DeepMind</td><td>Gemini 4 Argon</td><td>Long-horizon coding, enterprise work</td><td>Closed</td><td>{P}</td></tr>
    <tr><td>Meta</td><td>Muse Spark 1.1</td><td>Agents, computer use, 1M context</td><td>Not stated</td><td>{P} in app; API preview</td></tr>
    <tr><td>xAI</td><td>Grok 4.7</td><td>Coding, multi-hour tasks</td><td>Closed</td><td>{P}</td></tr>
    <tr><td>Mistral</td><td>Mistral Large 4</td><td>Multilingual, enterprise</td><td>Open, weights promised</td><td>API preview; weights {C}</td></tr>
    <tr><td>DeepSeek</td><td>V4-Pro, V4-Flash</td><td>Low cost, long context</td><td>Open</td><td>{P} preview</td></tr>
    <tr><td>Alibaba</td><td>Qwen3.8</td><td>Multimodal input, 1M context</td><td>Open (some sizes)</td><td>{RP}</td></tr>
    <tr><td>Moonshot</td><td>Kimi K3</td><td>Long-horizon coding and agents</td><td>Open</td><td>{RP}</td></tr>
    <tr><td>Zhipu (Z.ai)</td><td>GLM-5.x</td><td>Coding, tool use</td><td>Open</td><td>{RP}</td></tr>
    <tr><td>Cohere</td><td>Command A+</td><td>Enterprise agents, citations, 48 languages</td><td>Open (Apache 2.0)</td><td>{P}</td></tr>
    <tr><td>AI21</td><td>Jamba2</td><td>Hybrid Mamba-transformer, 256K context</td><td>Open (Apache 2.0)</td><td>{P}</td></tr>
    <tr><td>Microsoft AI</td><td>MAI-Thinking-1 and other MAI models</td><td>Low-cost reasoning, voice, image</td><td>Closed</td><td>Private preview</td></tr>
    <tr><td>Amazon</td><td>Nova 2 (Lite, Pro, Sonic, Omni)</td><td>Cost, speech-to-speech, multimodal</td><td>Closed</td><td>{P}</td></tr>
  </table></div>'''),

sec('hw-cos', 'Hardware companies', f'''  <div class="tbl"><table>
    <tr><th>Company</th><th>Key products</th><th>Role</th><th>Status</th></tr>
    <tr><td>NVIDIA</td><td>Blackwell Ultra (GB300); Vera Rubin with HBM4</td><td>Main supplier of training and inference compute</td><td>GB300 {P}; Rubin ramping</td></tr>
    <tr><td>AMD</td><td>Instinct MI355X; MI450/MI455X, Helios rack</td><td>Second GPU source</td><td>MI355X {P}; MI455X {C}</td></tr>
    <tr><td>Google</td><td>TPU7x Ironwood; TPU 8t / 8i</td><td>In-house chips, also rented on Google Cloud</td><td>Ironwood {P}; TPU 8 {D}</td></tr>
    <tr><td>AWS</td><td>Trainium3; Trainium4 announced</td><td>Cheaper in-house training and inference</td><td>{P} / {C}</td></tr>
    <tr><td>Intel</td><td>Gaudi 3; Crescent Island inference GPU</td><td>Inference-focused data-centre GPUs</td><td>{C}</td></tr>
    <tr><td>Cerebras</td><td>Wafer-scale CS-3</td><td>Very fast inference cloud</td><td>{P}</td></tr>
    <tr><td>Groq</td><td>LPU (licensed to NVIDIA)</td><td>Low-latency inference</td><td>{P}</td></tr>
    <tr><td>TSMC</td><td>N2 and A16 process nodes; CoWoS packaging</td><td>Makes nearly all leading AI chips</td><td>{P}</td></tr>
    <tr><td>SK hynix, Samsung, Micron</td><td>HBM3e, HBM4</td><td>Memory stacked beside every accelerator</td><td>{P} {RP} for HBM4</td></tr>
    <tr><td>Apple</td><td>Foundation Models framework, M-series and A-series NPUs</td><td>Free on-device models for apps</td><td>{P}</td></tr>
    <tr><td>Qualcomm</td><td>Snapdragon NPUs</td><td>On-device AI in phones and laptops</td><td>{C}</td></tr>
  </table></div>'''),

sec('oss', 'Open-source communities', f'''  <div class="tbl"><table>
    <tr><th>Project</th><th>Role</th><th>Status</th></tr>
    <tr><td>Hugging Face</td><td>The main hub for open models and datasets; the Transformers library. The llama.cpp team joined in Feb 2026.</td><td>{P}</td></tr>
    <tr><td>PyTorch (Linux Foundation)</td><td>The default training framework; hosts vLLM</td><td>{P}</td></tr>
    <tr><td>vLLM</td><td>High-throughput model serving on NVIDIA, AMD, Intel and TPU</td><td>{P}</td></tr>
    <tr><td>llama.cpp and Ollama</td><td>Running quantised models locally on laptops and phones</td><td>{P}</td></tr>
    <tr><td>LangChain, LangGraph, LlamaIndex</td><td>App and agent frameworks; LlamaIndex focuses on RAG</td><td>{P}</td></tr>
    <tr><td>ROS 2</td><td>Standard robot middleware</td><td>{P}</td></tr>
    <tr><td>Agentic AI Foundation (Linux Foundation)</td><td>Neutral home for MCP, AGENTS.md and Google's A2A agent protocol</td><td>{P}</td></tr>
  </table></div>'''),

sec('advances', "What's new in 2025-26", f'''  <div class="tbl"><table>
    <tr><th>Area</th><th>Recent developments</th></tr>
    <tr><td><b>Frontier models and reasoning</b></td><td>Every lab now ships thinking or effort controls {P}. Vendors report near-saturated scores on hard maths and puzzle benchmarks {C}.</td></tr>
    <tr><td><b>Coding agents</b></td><td>Agents that edit, run and test code in real repositories; new models launch inside Cursor and GitHub Copilot on day one {P}. Benchmark gains are vendor-reported {C}.</td></tr>
    <tr><td><b>Computer-use agents</b></td><td>Models operating browsers and desktop apps (forms, CRMs, calendars) are a headline feature for Anthropic, OpenAI and Meta {P}; the best scores are vendor-reported {C}.</td></tr>
    <tr><td><b>Multimodal</b></td><td>Real-time speech-to-speech agents from Google and OpenAI {P}; Apple's on-device model takes image input {P}.</td></tr>
    <tr><td><b>Open-weight and local AI</b></td><td>Open models close to closed ones: DeepSeek V4, Qwen3.8, Kimi K3, Command A+ {P}/{RP}. Mistral Large 4 weights promised {C}.</td></tr>
    <tr><td><b>Long context, memory, orchestration</b></td><td>1M-token windows are standard on flagships {P}. MCP (tools) and A2A (agent to agent) both sit in the Agentic AI Foundation {P}.</td></tr>
    <tr><td><b>Generated video, music, worlds</b></td><td>Google's Gemini Omni Flash video and Project Genie world model {P}. OpenAI shut down Sora (app April 2026, API Sept 2026) {P}.</td></tr>
    <tr><td><b>Scientific AI</b></td><td>AlphaProof methods published in <i>Nature</i> (Nov 2025) {R}; Gemini Deep Think officially graded gold at IMO 2025 {R}; AlphaFold 3 code open for academic use {P}.</td></tr>
    <tr><td><b>Humanoid robotics</b></td><td>Gemini Robotics ER 2 (July 2026) {P}; π0.7 generalist robot model {R}. Factory humanoid deployments {RP}.</td></tr>
    <tr><td><b>Chips and efficiency</b></td><td>NVIDIA adding Groq LPU racks to Vera Rubin deployments {P}; Google splitting TPU 8 into training and inference chips {D}; diffusion LLMs near 1,000 tokens/s {C}.</td></tr>
  </table></div>'''),

sec('claims', 'Demo, research, product or marketing?', f'''  <p class="what">AI news mixes four very different kinds of claim. Learn to tell them apart before relaying anything.</p>
  <div class="tbl"><table>
    <tr><th>Type</th><th>Signals</th></tr>
    <tr><td>{P}</td><td>A public model ID or product, a price page, docs, a changelog. You can call it yourself today. Generally available, not preview or waitlist.</td></tr>
    <tr><td>{R}</td><td>A paper or preprint with method, data and limits. Maybe code or weights. No price, no service guarantee. Results come from one fixed setup.</td></tr>
    <tr><td>{D}</td><td>A video, keynote or blog with chosen examples. "Rolling out soon", waitlists, trusted testers. No API, no price, no failure rates.</td></tr>
    <tr><td>{C}</td><td>Superlatives, the vendor's own benchmark with no outside re-run, new benchmark names, "up to N× faster" without a baseline.</td></tr>
  </table></div>
  <h3>Five quick checks</h3>
  <ol class="steps">
    <li><div>Can I call it with a public ID right now?</div></li>
    <li><div>Has anyone outside the company re-run the number?</div></li>
    <li><div>Is there a date and a version?</div></li>
    <li><div>Does it say "preview", "trusted access" or "coming weeks"?</div></li>
    <li><div>Do sources disagree? Then treat it as unverified.</div></li>
  </ol>
  <div class="qa"><h3>QA perspective</h3><ul class="plain"><li>Before testing anything a vendor announced, confirm it is actually available in your account and region.</li><li>Re-run vendor benchmarks on your own tasks before trusting them.</li><li>Record the model ID and date with every result, because names stay the same while models change.</li></ul></div>'''),
]
