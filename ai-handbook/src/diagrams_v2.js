
// F1 nested map
draw('d-nest', 1000, 420, [
  {t:'ellipse', cx:500, cy:212, w:960, h:400, tone:'gray', label:''},
  {t:'ellipse', cx:560, cy:240, w:740, h:320, tone:'blue', label:''},
  {t:'ellipse', cx:620, cy:268, w:520, h:240, tone:'violet', label:''},
  {t:'ellipse', cx:680, cy:292, w:280, h:150, tone:'yellow', label:''},
  {t:'text', x:500, y:44, s:'Artificial intelligence', cls:'hd'},
  {t:'text', x:560, y:126, s:'Machine learning: learns from data', cls:'hd'},
  {t:'text', x:620, y:198, s:'Deep learning: deep neural nets', cls:'hd'},
  {t:'text', x:680, y:286, s:'LLMs', cls:'lb'},
  {t:'text', x:680, y:312, s:'predict the next token', cls:'sb'}
]);
// F2 tokens
var tk = [['Un',70,'4882'],['believ',110,'7019'],['able',80,'481'],[' results',120,'3135'],['!',50,'0']];
var tok = [
  {t:'box', x:20, y:30, w:290, h:64, tone:'yellow', label:'"Unbelievable results!"'},
  {t:'arrow', p:[[312,62],[396,62]], cls:'acc', label:'tokenizer', lx:354, ly:50, lc:'acc'},
  {t:'text', x:20, y:150, s:'token IDs (illustrative)', cls:'sb', a:'start'},
  {t:'text', x:500, y:240, s:'The model reads only the IDs. About 4 characters per token in English.', cls:'sb'}
];
var x = 400;
tk.forEach(function(t){
  tok.push({t:'box', x:x, y:34, w:t[1], h:56, tone:'blue', label:t[0]});
  tok.push({t:'arrow', p:[[x + t[1]/2, 92],[x + t[1]/2, 136]], cls:'mut'});
  tok.push({t:'box', x:x, y:140, w:t[1], h:44, tone:'violet', label:t[2]});
  x += t[1] + 14;
});
draw('d-tok', 1000, 260, tok);
// F3 generation loop
draw('d-gen', 1000, 320, [
  {t:'box', x:20, y:100, w:230, h:80, tone:'yellow', label:'"The cat sat', sub:'on the"'},
  {t:'box', x:320, y:90, w:170, h:100, tone:'violet', label:'LLM', sub:'one forward pass'},
  {t:'box', x:560, y:40, w:230, h:200, tone:'blue', label:''},
  {t:'text', x:580, y:66, s:'next-token probabilities', cls:'sb', a:'start'},
  {t:'text', x:580, y:104, s:'mat', cls:'tx', a:'start'}, {t:'box', x:650, y:90, w:62, h:20, tone:'violet', label:''}, {t:'text', x:770, y:104, s:'0.62', cls:'sb', a:'end'},
  {t:'text', x:580, y:144, s:'floor', cls:'tx', a:'start'}, {t:'box', x:650, y:130, w:21, h:20, tone:'violet', label:''}, {t:'text', x:770, y:144, s:'0.21', cls:'sb', a:'end'},
  {t:'text', x:580, y:184, s:'sofa', cls:'tx', a:'start'}, {t:'box', x:650, y:170, w:9, h:20, tone:'violet', label:''}, {t:'text', x:770, y:184, s:'0.09', cls:'sb', a:'end'},
  {t:'text', x:580, y:222, s:'... 100,000+ more', cls:'sb', a:'start'},
  {t:'box', x:850, y:100, w:130, h:80, tone:'green', label:'"mat"', sub:'sampled'},
  {t:'arrow', p:[[252,140],[316,140]], cls:'acc', label:'token IDs', lx:284, ly:126, lc:'acc'},
  {t:'arrow', p:[[492,140],[556,140]], cls:'acc', label:'softmax', lx:524, ly:126, lc:'acc'},
  {t:'arrow', p:[[792,140],[846,140]], cls:'acc', label:'pick', lx:819, ly:126, lc:'acc'},
  {t:'arrow', p:[[915,182],[915,290],[135,290],[135,182]], dash:true, label:'append the token and repeat', lx:525, ly:278}
]);
// B1 attention
var words = ['The','animal',"didn't",'cross','because','it','was','tired'];
var at = [];
words.forEach(function(w, i){ at.push({t:'box', x:20 + i*122, y:30, w:108, h:50, tone:(w === 'it' ? 'red' : (w === 'animal' ? 'green' : 'gray')), red:(w === 'it'), label:w}); });
var itx = 20 + 5*122 + 54;
at.push({t:'curve', p:[[itx,82],[ (itx+142)/2, 230],[142,82]], cls:'acc', w:5});
at.push({t:'curve', p:[[itx,82],[ (itx+74)/2, 200],[74,82]], cls:'mut', w:1});
at.push({t:'curve', p:[[itx,82],[ (itx+386)/2, 150],[386,82]], cls:'mut', w:1});
at.push({t:'curve', p:[[itx,82],[ (itx+928)/2, 160],[928,82]], cls:'mut', w:1.5});
at.push({t:'text', x:430, y:250, s:'"it" attends most to "animal"', cls:'al acc'});
at.push({t:'text', x:500, y:300, s:'Attention(Q, K, V) = softmax(Q·Kᵀ / √dₖ) · V', cls:'hd'});
at.push({t:'text', x:500, y:332, s:'Q: what this token looks for   ·   K: what each token offers   ·   V: what it passes on', cls:'sb'});
draw('d-attn', 1000, 350, at);
// B2 training
draw('d-train', 1000, 300, [
  {t:'box', x:20, y:60, w:200, h:96, tone:'gray', label:'Pre-training', sub:'next token, huge text'},
  {t:'box', x:280, y:72, w:150, h:72, tone:'violet', label:'Base model'},
  {t:'box', x:490, y:60, w:190, h:96, tone:'blue', label:'Fine-tuning', sub:'SFT on demonstrations'},
  {t:'box', x:740, y:50, w:240, h:116, tone:'green', label:'Preference tuning', sub:'RLHF, DPO or RLAIF'},
  {t:'box', x:760, y:220, w:200, h:60, tone:'yellow', label:'Assistant model'},
  {t:'arrow', p:[[222,108],[276,108]], cls:'acc'},
  {t:'arrow', p:[[432,108],[486,108]], cls:'acc'},
  {t:'arrow', p:[[682,108],[736,108]], cls:'acc'},
  {t:'arrow', p:[[860,168],[860,216]], cls:'acc'},
  {t:'text', x:120, y:186, s:'most of the compute', cls:'sb'},
  {t:'text', x:585, y:186, s:'people write examples', cls:'sb'},
  {t:'text', x:860, y:196, s:'', cls:'sb'}
]);
// B3 embedding space
draw('d-embed', 1000, 380, [
  {t:'zone', x:20, y:16, w:580, h:350, label:'embedding space (2D sketch)'},
  {t:'dot', x:110, y:100, cls:'grn'}, {t:'text', x:126, y:105, s:'dog', cls:'tx', a:'start'},
  {t:'dot', x:170, y:130, cls:'grn'}, {t:'text', x:186, y:135, s:'puppy', cls:'tx', a:'start'},
  {t:'dot', x:110, y:165, cls:'grn'}, {t:'text', x:126, y:170, s:'cat', cls:'tx', a:'start'},
  {t:'dot', x:420, y:250, cls:'acc'}, {t:'text', x:436, y:255, s:'mortgage', cls:'tx', a:'start'},
  {t:'dot', x:470, y:300, cls:'acc'}, {t:'text', x:486, y:305, s:'interest rate', cls:'tx', a:'start'},
  {t:'dot', x:380, y:320, cls:'acc'}, {t:'text', x:396, y:325, s:'bank loan', cls:'tx', a:'start'},
  {t:'dot', x:330, y:200, cls:'red'}, {t:'text', x:150, y:215, s:'query: "how do I get\na home loan?"', cls:'al red', a:'start'},
  {t:'arrow', p:[[338,206],[410,244]], cls:'red', dash:true, label:'nearest', lx:400, ly:212, lc:'red'},
  {t:'text', x:650, y:90, s:'cosine similarity', cls:'hd', a:'start'},
  {t:'text', x:650, y:126, s:'cos(a,b) = a·b / (‖a‖‖b‖)', cls:'tx', a:'start'},
  {t:'text', x:650, y:176, s:'1  same direction: similar', cls:'tx', a:'start'},
  {t:'text', x:650, y:206, s:'0  unrelated', cls:'tx', a:'start'},
  {t:'text', x:650, y:256, s:'Real embeddings have', cls:'sb', a:'start'},
  {t:'text', x:650, y:278, s:'1,536 or 3,072 dimensions', cls:'sb', a:'start'}
]);
// B4 RAG
draw('d-rag', 1000, 470, [
  {t:'zone', x:10, y:10, w:980, h:170, label:'INDEXING: once per document'},
  {t:'box', x:40, y:70, w:150, h:72, tone:'gray', label:'Documents'},
  {t:'box', x:250, y:70, w:150, h:72, tone:'blue', label:'Chunk', sub:'~512 tokens'},
  {t:'box', x:460, y:70, w:150, h:72, tone:'violet', label:'Embed'},
  {t:'box', x:690, y:60, w:200, h:92, tone:'green', label:'Vector store', sub:'vectors + text'},
  {t:'arrow', p:[[192,106],[246,106]], cls:'acc'},
  {t:'arrow', p:[[402,106],[456,106]], cls:'acc'},
  {t:'arrow', p:[[612,106],[686,106]], cls:'acc'},
  {t:'zone', x:10, y:200, w:980, h:260, label:'QUERY TIME: every question'},
  {t:'box', x:40, y:270, w:150, h:72, tone:'yellow', label:'Question'},
  {t:'box', x:250, y:270, w:150, h:72, tone:'violet', label:'Embed'},
  {t:'box', x:460, y:270, w:160, h:72, tone:'blue', label:'Search', sub:'top-k chunks'},
  {t:'box', x:690, y:250, w:140, h:112, tone:'yellow', label:'Prompt', sub:'question + chunks'},
  {t:'box', x:870, y:270, w:110, h:72, tone:'violet', label:'LLM'},
  {t:'arrow', p:[[192,306],[246,306]], cls:'acc'},
  {t:'arrow', p:[[402,306],[456,306]], cls:'acc'},
  {t:'arrow', p:[[622,306],[686,306]], cls:'acc'},
  {t:'arrow', p:[[832,306],[866,306]], cls:'acc'},
  {t:'arrow', p:[[790,154],[790,200],[560,200],[560,266]], dash:true, cls:'mut', label:'nearest vectors', lx:676, ly:218},
  {t:'arrow', p:[[925,344],[925,400]], cls:'acc'},
  {t:'text', x:925, y:428, s:'answer + sources', cls:'al acc'}
]);
// B5 agent loop
draw('d-agent', 1000, 330, [
  {t:'box', x:20, y:110, w:150, h:72, tone:'yellow', label:'Goal'},
  {t:'box', x:260, y:40, w:200, h:92, tone:'violet', label:'LLM', sub:'think, pick a tool'},
  {t:'box', x:600, y:40, w:200, h:92, tone:'blue', label:'Your code', sub:'runs the tool'},
  {t:'box', x:600, y:210, w:200, h:80, tone:'green', label:'Result', sub:'added to the context'},
  {t:'box', x:20, y:240, w:170, h:66, tone:'gray', label:'Final answer'},
  {t:'arrow', p:[[172,140],[256,100]], cls:'acc'},
  {t:'arrow', p:[[462,86],[596,86]], cls:'acc', label:'tool_use', lx:529, ly:72, lc:'acc'},
  {t:'arrow', p:[[700,134],[700,206]], cls:'acc'},
  {t:'arrow', p:[[596,250],[360,250],[360,136]], dash:true, label:'tool_result', lx:478, ly:238},
  {t:'arrow', p:[[280,134],[140,236]], cls:'mut', label:'no more tools', lx:150, ly:200},
  {t:'text', x:830, y:180, s:'repeat until done', cls:'al acc', a:'start'}
]);
// X1 MoE
var moe = [
  {t:'box', x:20, y:150, w:120, h:60, tone:'yellow', label:'token'},
  {t:'box', x:200, y:130, w:160, h:100, tone:'red', label:'Router', sub:'scores 8 experts'},
  {t:'arrow', p:[[142,180],[196,180]], cls:'acc'}
];
for (var e = 0; e < 8; e++){
  var on = (e === 2 || e === 5), y = 14 + e*42;
  moe.push({t:'box', x:470, y:y, w:170, h:34, tone:(on ? 'green' : 'gray'), red:false, label:'expert ' + (e+1)});
}
moe.push({t:'arrow', p:[[362,170],[466,99]], cls:'acc', label:'0.7', lx:410, ly:122, lc:'acc'});
moe.push({t:'arrow', p:[[362,196],[466,227]], cls:'acc', label:'0.3', lx:418, ly:230, lc:'acc'});
moe.push({t:'box', x:740, y:140, w:150, h:80, tone:'violet', label:'Weighted sum'});
moe.push({t:'arrow', p:[[642,99],[736,165]], cls:'acc'});
moe.push({t:'arrow', p:[[642,227],[736,196]], cls:'acc'});
moe.push({t:'arrow', p:[[892,180],[960,180]], cls:'acc'});
moe.push({t:'text', x:555, y:362, s:'grey experts do not run for this token', cls:'sb'});
draw('d-moe', 1000, 380, moe);
// X2 thinking
draw('d-think', 1000, 300, [
  {t:'text', x:20, y:30, s:'Standard model', cls:'hd', a:'start'},
  {t:'box', x:20, y:46, w:170, h:64, tone:'yellow', label:'Question'},
  {t:'box', x:260, y:46, w:150, h:64, tone:'violet', label:'LLM'},
  {t:'box', x:800, y:46, w:180, h:64, tone:'green', label:'Answer'},
  {t:'arrow', p:[[192,78],[256,78]], cls:'acc'},
  {t:'arrow', p:[[412,78],[796,78]], cls:'acc'},
  {t:'text', x:20, y:170, s:'Reasoning model', cls:'hd', a:'start'},
  {t:'box', x:20, y:186, w:170, h:64, tone:'yellow', label:'Question'},
  {t:'box', x:260, y:186, w:150, h:64, tone:'violet', label:'LLM'},
  {t:'box', x:470, y:176, w:270, h:84, tone:'gray', label:'thinking tokens', sub:'break down, try, check, fix'},
  {t:'box', x:800, y:186, w:180, h:64, tone:'green', label:'Better answer'},
  {t:'arrow', p:[[192,218],[256,218]], cls:'acc'},
  {t:'arrow', p:[[412,218],[466,218]], cls:'acc'},
  {t:'arrow', p:[[742,218],[796,218]], cls:'acc'},
  {t:'text', x:605, y:284, s:'more test-time compute: slower and costlier, better on hard problems', cls:'al acc'}
]);
// X3 multimodal
var mm = [
  {t:'box', x:20, y:70, w:130, h:130, tone:'gray', label:''},
  {t:'text', x:85, y:228, s:'image', cls:'sb'}
];
[52,85,118].forEach(function(v){ mm.push({t:'line', x1:v, y1:70, x2:v, y2:200, cls:'mut'}); mm.push({t:'line', x1:20, y1:v+50, x2:150, y2:v+50, cls:'mut'}); });
mm = mm.concat([
  {t:'box', x:240, y:95, w:160, h:80, tone:'blue', label:'Vision encoder', sub:'ViT'},
  {t:'box', x:460, y:95, w:150, h:80, tone:'yellow', label:'Projection', sub:'into word space'},
  {t:'arrow', p:[[152,135],[236,135]], cls:'acc', label:'16×16\npatches', lx:194, ly:104, lc:'acc'},
  {t:'arrow', p:[[402,135],[456,135]], cls:'acc'},
  {t:'arrow', p:[[612,135],[656,135]], cls:'acc'}
]);
for (var v = 0; v < 3; v++) mm.push({t:'box', x:660 + v*40, y:117, w:34, h:36, tone:'blue', label:''});
for (var w2 = 0; w2 < 3; w2++) mm.push({t:'box', x:790 + w2*40, y:117, w:34, h:36, tone:'yellow', label:''});
mm.push({t:'text', x:719, y:186, s:'image tokens', cls:'sb'});
mm.push({t:'text', x:849, y:186, s:'text tokens', cls:'sb'});
mm.push({t:'arrow', p:[[780,195],[810,214]], cls:'acc'});
mm.push({t:'box', x:740, y:218, w:200, h:40, tone:'violet', label:'LLM'});
draw('d-mm', 1000, 270, mm);
// X4 Jev vs LLM
draw('d-jev', 1000, 400, [
  {t:'text', x:20, y:28, s:'With an LLM', cls:'hd', a:'start'},
  {t:'box', x:20, y:44, w:180, h:80, tone:'yellow', label:'Prompt', sub:'ticket + instructions'},
  {t:'box', x:260, y:44, w:130, h:80, tone:'violet', label:'LLM'},
  {t:'box', x:450, y:44, w:280, h:80, tone:'gray', label:'"This looks like a', sub:'billing issue, because..."'},
  {t:'box', x:790, y:44, w:190, h:80, tone:'blue', label:'Your code', sub:'parses the text'},
  {t:'arrow', p:[[202,84],[256,84]], cls:'acc'},
  {t:'arrow', p:[[392,84],[446,84]], cls:'acc', label:'token by token', lx:419, ly:142, lc:'acc'},
  {t:'arrow', p:[[732,84],[786,84]], cls:'acc'},
  {t:'text', x:885, y:146, s:'format can vary', cls:'al red'},
  {t:'text', x:20, y:200, s:'With Jev (a System One model)', cls:'hd', a:'start'},
  {t:'box', x:20, y:216, w:180, h:96, tone:'yellow', label:'state', sub:'+ named questions'},
  {t:'box', x:260, y:226, w:130, h:76, tone:'green', label:'Jev'},
  {t:'box', x:450, y:206, w:530, h:116, tone:'blue', label:''},
  {t:'text', x:470, y:236, s:'choice  →  billing   (billing 0.91 · bug 0.06 · other 0.03)', cls:'tx', a:'start'},
  {t:'text', x:470, y:266, s:'score   →  urgency 4 of 5   (per-level probabilities)', cls:'tx', a:'start'},
  {t:'text', x:470, y:296, s:'noul    →  0.12   (probability the customer will churn)', cls:'tx', a:'start'},
  {t:'arrow', p:[[202,264],[256,264]], cls:'acc'},
  {t:'arrow', p:[[392,264],[446,264]], cls:'acc', label:'one pass', lx:419, ly:340, lc:'acc'},
  {t:'text', x:715, y:360, s:'typed answers with probabilities, no text to parse', cls:'al acc'}
]);

// neural network
var nn = [];
var IN=[90,165,240], HID=[60,135,210,285], OUT=[165];
IN.forEach(function(y){ HID.forEach(function(h){ nn.push({t:'line', x1:110, y1:y, x2:280, y2:h}); }); });
HID.forEach(function(h){ nn.push({t:'line', x1:320, y1:h, x2:480, y2:165}); });
IN.forEach(function(y){ nn.push({t:'ellipse', cx:90, cy:y, w:44, h:44, tone:'yellow', label:''}); });
HID.forEach(function(y){ nn.push({t:'ellipse', cx:300, cy:y, w:44, h:44, tone:'blue', label:''}); });
nn.push({t:'ellipse', cx:500, cy:165, w:48, h:48, tone:'violet', label:''});
nn = nn.concat([
  {t:'text', x:90, y:28, s:'inputs', cls:'sb'}, {t:'text', x:300, y:28, s:'hidden layer', cls:'sb'}, {t:'text', x:500, y:28, s:'output', cls:'sb'},
  {t:'box', x:620, y:125, w:150, h:80, tone:'red', label:'Loss', sub:'how wrong?'},
  {t:'box', x:840, y:125, w:140, h:80, tone:'green', label:'Correct', sub:'answer'},
  {t:'arrow', p:[[526,165],[616,165]], cls:'acc', label:'prediction', lx:571, ly:152, lc:'acc'},
  {t:'arrow', p:[[838,165],[774,165]], cls:'mut'},
  {t:'arrow', p:[[695,207],[695,330],[300,330],[300,312]], cls:'red', dash:true, label:'backpropagation: nudge every weight to lower the loss', lx:500, ly:352, lc:'red'}
]);
draw('d-nn', 1000, 370, nn);
// data split
draw('d-split', 1000, 270, [
  {t:'box', x:20, y:40, w:630, h:70, tone:'blue', label:'Training  70%'},
  {t:'box', x:660, y:40, w:150, h:70, tone:'yellow', label:'Validation 15%'},
  {t:'box', x:820, y:40, w:160, h:70, tone:'green', label:'Test 15%'},
  {t:'text', x:335, y:140, s:'teaches the model', cls:'sb'},
  {t:'text', x:735, y:140, s:'tunes settings', cls:'sb'},
  {t:'text', x:900, y:140, s:'final score, once', cls:'sb'},
  {t:'arrow', p:[[900,150],[860,186]], cls:'acc'},
  {t:'box', x:560, y:190, w:420, h:60, tone:'violet', label:'Model in production: inference'}
]);
// gateway
draw('d-gateway', 1000, 300, [
  {t:'box', x:20, y:105, w:140, h:76, tone:'yellow', label:'Your app'},
  {t:'box', x:220, y:95, w:180, h:96, tone:'blue', label:'Gateway', sub:'keys, limits, logs'},
  {t:'box', x:460, y:95, w:170, h:96, tone:'violet', label:'Router', sub:'pick a model'},
  {t:'box', x:740, y:30, w:220, h:76, tone:'green', label:'Model A', sub:'primary'},
  {t:'box', x:740, y:190, w:220, h:76, tone:'gray', label:'Model B', sub:'fallback'},
  {t:'box', x:220, y:224, w:180, h:56, tone:'gray', label:'Cache'},
  {t:'arrow', p:[[162,143],[216,143]], cls:'acc'},
  {t:'arrow', p:[[402,143],[456,143]], cls:'acc'},
  {t:'arrow', p:[[632,125],[736,72]], cls:'acc'},
  {t:'arrow', p:[[632,165],[736,222]], cls:'red', dash:true, label:'on error or timeout', lx:690, ly:186, lc:'red'},
  {t:'arrow', p:[[310,193],[310,220]], both:true, cls:'mut'}
]);
// robot control loop
draw('d-robot', 1000, 300, [
  {t:'text', x:500, y:20, s:'goal', cls:'al acc'},
  {t:'arrow', p:[[500,28],[500,46]], cls:'acc'},
  {t:'box', x:60, y:50, w:200, h:80, tone:'blue', label:'Sensors', sub:'camera, lidar, encoders'},
  {t:'box', x:400, y:50, w:200, h:80, tone:'violet', label:'Controller', sub:'compare with goal'},
  {t:'box', x:740, y:50, w:200, h:80, tone:'yellow', label:'Actuators', sub:'motors'},
  {t:'box', x:400, y:200, w:200, h:80, tone:'green', label:'Robot and world'},
  {t:'arrow', p:[[262,90],[396,90]], cls:'acc', label:'measurement', lx:329, ly:78, lc:'acc'},
  {t:'arrow', p:[[602,90],[736,90]], cls:'acc', label:'command', lx:669, ly:78, lc:'acc'},
  {t:'arrow', p:[[840,132],[840,240],[604,240]], cls:'acc', label:'moves', lx:840, ly:190, lc:'acc'},
  {t:'arrow', p:[[396,240],[160,240],[160,134]], cls:'acc', label:'changes what is sensed', lx:278, ly:228, lc:'acc'}
]);
