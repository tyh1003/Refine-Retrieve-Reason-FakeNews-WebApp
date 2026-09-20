<template>
  <div class="app-shell">
    <main class="app-main">
      <div class="language-toolbar">
        <button
          type="button"
          class="language-button"
          :class="{ active: locale === 'en' }"
          @click="setLocale('en')"
        >
          English
        </button>

        <button
          type="button"
          class="language-button"
          :class="{ active: locale === 'zh' }"
          @click="setLocale('zh')"
        >
          中文
        </button>
      </div>
      <section v-if="currentPage === 1" class="page-stack">
        <header class="page-header">
          <div class="eyebrow">AI Fake News Detection</div>
          <h1 class="project-title">
            <span>{{ t("projectLine1") }}</span>
            <span>{{ t("projectLine2") }}</span>
          </h1>
        </header>

        <section class="card upload-card">
          <div class="card-heading">
            <div>
              <h2>{{ t("uploadVideo") }}</h2>
              <p>{{ translateStatus(uploadMessage) }}</p>
            </div>
            <span class="soft-badge">Upload</span>
          </div>

          <input
            ref="fileInput"
            id="video-upload"
            type="file"
            accept="video/*"
            class="visually-hidden"
            @change="handleFileUpload"
          />

          <label for="video-upload" class="button primary-button">
            {{ t("chooseVideo") }}
          </label>

          
          <p v-if="uploadError" class="error-text">{{ uploadError }}</p>

          <div v-if="videoUrl" class="video-frame">
            <video :src="videoUrl" controls></video>
          </div>

        </section>

        <section v-if="videoUrl" class="card vote-card">
          <div class="card-heading">
            <div>
              <h2>{{ t("yourPrediction") }}</h2>
              <p>
                {{ t("currentVideo") }}：
                {{ uploadedVideoId || t("noVideoName") }}
              </p>
            </div>
            <span class="soft-badge">Vote</span>
          </div>

          <div class="vote-grid">
            <button
              v-for="option in voteOptions"
              :key="option.value"
              type="button"
              class="vote-button"
              :class="selectedVote === option.value ? `vote-active-${option.value}` : ''"
              @click="selectVote(option.value)"

            >
              <strong>{{ voteText(option.value) }}</strong>
              <span>{{ option.shortLabel }}</span>
            </button>
          </div>

        <div v-if="selectedVote === 'false'" class="reason-block">
          <p>{{ t("reason") }}</p>
            <div class="reason-list">
              <button

                v-for="reason in reasonOptions"

                :key="reason"

                type="button"

                class="reason-button"

                :class="{ 'reason-active': selectedReason === reason }"

                @click="selectedReason = reason"

              >

                {{ reasonText(reason) }}

              </button>

            </div>

          </div>



          <p v-if="voteError" class="error-text">{{ voteError }}</p>



          <button

            type="button"

            class="button primary-button submit-button"

            :disabled="!selectedVote || voteSubmitting"

            @click="submitVote"

          >

            {{ voteSubmitting ? t("submitting") : t("submit") }}

          </button>

        </section>



        <section v-if="showVoteStats" class="card stats-card">

          <div class="card-heading">

            <div>

              <h2>{{ t("voteStatistics") }}</h2>
              <p>{{ t("totalVotes", { n: voteStats.total }) }}</p>

            </div>

            <span class="soft-badge">Statistics</span>

          </div>



          <div class="stats-list">

            <div v-for="item in statisticsRows" :key="item.key" class="stats-row">

              <div class="stats-label">

                <span>{{ item.label }}</span>

                <strong>{{ item.percent }}%</strong>

              </div>

              <div class="meter">

                <span

                  :class="`meter-fill meter-${item.key}`"

                  :style="{ width: `${item.percent}%` }"

                ></span>

              </div>

            </div>

          </div>



          <button type="button" class="button secondary-button" @click="nextPage">

            {{ t("viewAI") }}

          </button>

        </section>

      </section>



      <section v-else class="page-stack">

        <header class="page-header compact">

          <div class="eyebrow">AI Reasoning Chain</div>

            <h1>{{ t("analysisPipeline") }}</h1>
            <p>{{ translateStatus(processStatus) }}</p>

        </header>



        <section class="flow-grid">

          <article class="card flow-card preprocess-card">

            <div class="flow-title">

              <span class="step-index">1</span>

              <div>

                <h2>{{ t("preprocessing") }}</h2>

                <p>{{ translateStatus(preprocessStatusText) }}</p>

              </div>

            </div>



            <ol class="step-list">

              <li

                v-for="(step, index) in preprocessDisplaySteps"

                :key="step"

                :class="stepStateClass(index)"

              >

                <span></span>

                {{ pipelineStepLabel(step) }}

              </li>

            </ol>

          </article>



          <article class="card flow-card retrieve-card">

            <div class="flow-title">

              <span class="step-index">2</span>

              <div>

                <h2>Retrieve</h2>

                <p>{{ translateStatus(retrieveStatusText) }}</p>

              </div>

            </div>



            <div class="field-list">

              <InfoBlock label="Rc" :value="translatedRetrieveDisplayFields.Rc" />
              <InfoBlock label="Rv" :value="translatedRetrieveDisplayFields.Rv" />
              <InfoBlock label="K_int" :value="translatedRetrieveDisplayFields.K_int" />
              <InfoBlock label="K_ext" :value="translatedRetrieveDisplayFields.K_ext" />
            </div>



            <div class="link-section">

              <span class="info-label">{{ t("externalSources") }}</span>
              <div v-if="retrieveLinks.length" class="source-link-grid">

                <a

                  v-for="(link, index) in retrieveLinks"

                  :key="`${link}-${index}`"

                  class="source-link-card"

                  :href="link"

                  target="_blank"

                  rel="noreferrer"

                >

                  <strong>{{ t("source") }} {{ index + 1 }}</strong>

                  <span>{{ link }}</span>

                </a>

              </div>

              <p v-else class="empty-text">{{ translateStatus(retrieveEmptyText) }}</p>

            </div>

          </article>



          <article class="card flow-card student-card">

            <div class="flow-title">

              <span class="step-index">3</span>

              <div>

                <h2>{{ t("studentModel") }}</h2>
                <p>{{ translateStatus(studentStatusText) }}</p>

              </div>

            </div>



            <div class="field-list">

              <InfoBlock label="system prompt" :value="studentPromptDisplayFields.system_prompt" />

              <InfoBlock label="user prompt" :value="studentPromptDisplayFields.user_prompt" />

              <InfoBlock label="Rc" :value="studentPromptDisplayFields.Rc" />

              <InfoBlock label="Rv" :value="studentPromptDisplayFields.Rv" />

              <InfoBlock label="K_int" :value="studentPromptDisplayFields.K_int" />

              <InfoBlock label="K_ext" :value="studentPromptDisplayFields.K_ext" />

            </div>

          </article>

        </section>



        <section class="card result-card">

          <div class="card-heading">

            <div>

              <h2>{{ t("finalResult") }}</h2>
              <p>{{ translateStatus(studentStatusText) }}</p>

            </div>

            <span class="soft-badge result-badge">Result</span>

          </div>



          <div class="result-grid">

            <div class="result-item">
              <span>{{ t("humanPrediction") }}</span>
              <strong>{{ voteText(selectedVote) }}</strong>
            </div>

            <div class="result-item">
              <span>{{ t("aiPrediction") }}</span>
              <strong>
                {{ studentReady ? voteText(aiVote) : translateStatus(studentStatusText) }}
              </strong>
            </div>

            <div class="result-item">
              <span>{{ t("groundTruth") }}</span>
              <strong>{{ voteText(systemAnswer) }}</strong>
            </div>

            <div class="result-item winner-item">
              <span>{{ t("comparison") }}</span>
              <strong>{{ winnerText }}</strong>
            </div>

          </div>



        <div class="reason-result">
          <h3>{{ t("aiExplanation") }}</h3>
          <p>
            {{
              locale === "en"
                ? (translatedContent.explanation ||
                  studentResult?.reason ||
                  translateStatus(studentResultEmptyText))
                : (studentResult?.reason ||
                  translateStatus(studentResultEmptyText))
            }}
          </p>
        </div>



          <div class="link-section result-source-section">

            <span class="info-label">{{ t("externalSources") }}</span>

            <div v-if="retrieveLinks.length" class="source-link-grid">

              <a

                v-for="(link, index) in retrieveLinks"

                :key="`result-${link}-${index}`"

                class="source-link-card"

                :href="link"

                target="_blank"

                rel="noreferrer"

              >

                <strong>{{ t("source") }} {{ index + 1 }}</strong>

                <span>{{ link }}</span>

              </a>

            </div>

            <p v-else class="empty-text">{{ translateStatus(retrieveEmptyText) }}</p>

          </div>



          <div class="button-row">

            <button type="button" class="button secondary-button" @click="refreshOutputs">

              {{ t("refresh") }}

            </button>

            <button type="button" class="button ghost-button" @click="resetGame">

              {{ t("restart") }}

            </button>

          </div>

        </section>

      </section>

    </main>

  </div>

</template>



<script setup>

import { computed, defineComponent, h, onBeforeUnmount, onMounted, reactive, ref } from "vue"



const API_BASE = (
  import.meta.env.VITE_API_BASE_URL?.trim() ||
  (import.meta.env.DEV ? "http://127.0.0.1:5000" : "/api")
).replace(/\/+$/, "")

const RUNNING_TEXT = "執行中..."

const DONE_TEXT = "已完成"

const NOT_FOUND_TEXT = "未查到"

const locale = ref("en")

// ============================================================
// Language
// ============================================================


function toggleLocale() {
  locale.value = locale.value === "zh" ? "en" : "zh"
}
async function setLocale(lang) {
  locale.value = lang

  if (lang === "en") {
    await translateDynamicContent()
  }
}


// ============================================================
// UI Translations
// ============================================================

const translations = {
  zh: {
    projectLine1: "秒懂真偽：以低成本證據鏈驅動的多模態",
    projectLine2: "Refine–Retrieve–Reason 短影音假訊息偵測",

    uploadVideo: "上傳影片",
    chooseVideo: "選擇影片",
    yourPrediction: "你的判斷",
    currentVideo: "目前影片",
    noVideoName: "尚未取得影片名稱",

    reason: "原因",
    imageTextMismatch: "圖文不符",
    knowledgeError: "知識有誤",
    other: "其他",

    submit: "送出判斷",
    submitting: "送出中...",

    voteStatistics: "目前投票比例",
    totalVotes: "目前共有 {n} 人投票",

    viewAI: "查看 AI 分析",
    analysisPipeline: "分析流程",

    preprocessing: "前處理",
    running: "執行中...",
    completed: "已完成",
    notFound: "未查到",

    extractAudioFrames: "抽取音訊與影格",
    speechVLM: "語音轉文字與 VLM 分析",
    dataMerge: "Data Merge",

    retrieve: "Retrieve",
    studentAnalysis: "小模型分析",
    analysisComplete: "分析完成",

    externalSources: "查到的資料",
    source: "資料",

    studentModel: "小模型",
    systemPromptTitle: "System Prompt",
    userPromptTitle: "User Prompt",

    rc: "文字內容（Rc）",
    rv: "影像內容（Rv）",
    internalKnowledge: "內部背景知識（K_int）",
    externalKnowledge: "外部背景知識（K_ext）",

    finalResult: "最後結果",
    humanPrediction: "使用者判斷",
    aiPrediction: "AI 判斷",
    groundTruth: "正確答案",
    comparison: "Human–AI Comparison",
    aiExplanation: "AI Explanation",

    refresh: "更新分析結果",
    restart: "重新開始",

    real: "真",
    fake: "假",
    notSelected: "尚未選擇",
    analyzing: "分析中",
    unableCompare: "無法比對",

    humanWins: "使用者勝利",
    aiWins: "AI 勝利",
    bothCorrect: "平手，雙方都答對",
    bothWrong: "平手，雙方都未答對",

    waitingUpload: "等待上傳影片...",
    notStarted: "尚未開始",
    uploading: "上傳中...",
    uploadedReady: "影片已上傳，準備分析...",
    uploadedAnalyzing: "影片已上傳，分析中",
    uploadFailed: "上傳失敗",

    noAnswer: "找不到對應答案",
    noVideoSelected: "尚未選擇影片",
    backendUnavailable: "無法連接後端，請確認 Flask backend 已啟動",
    selectPredictionFirst: "請先選擇判斷結果",
    missingVideoId: "尚未取得影片 ID",
    voteFailed: "投票送出失敗",

    processingMedia: "正在進行音訊、影格與視覺內容分析...",
    transcribingAudio: "正在進行語音轉文字...",
    retrievingEvidence: "正在進行知識檢索與外部證據搜尋...",
    studentModelAnalysis: "正在進行 Student Model 分析...",

  },

  en: {
    projectLine1: "Understand Authenticity at a Glance: Multimodal",
    projectLine2: "Refine–Retrieve–Reason Short-Video Misinformation Detection",

    uploadVideo: "Upload Video",
    chooseVideo: "Choose Video",
    yourPrediction: "Human Prediction",
    currentVideo: "Current Video",
    noVideoName: "Video name unavailable",

    reason: "Reason",
    imageTextMismatch: "Visual–Text Mismatch",
    knowledgeError: "Incorrect Knowledge",
    other: "Other",

    submit: "Submit Prediction",
    submitting: "Submitting...",

    voteStatistics: "Vote Statistics",
    totalVotes: "{n} votes in total",

    viewAI: "View AI Analysis",
    analysisPipeline: "Analysis Pipeline",

    preprocessing: "Preprocessing",
    running: "Running...",
    completed: "Completed",
    notFound: "Not Found",
    uploadedReady: "Video Uploaded — Ready for Analysis",

    extractAudioFrames: "Extract Audio & Frames",
    speechVLM: "Speech-to-Text & VLM Analysis",
    dataMerge: "Data Merge",

    retrieve: "Retrieve",
    studentAnalysis: "Student Model Analysis",
    analysisComplete: "Analysis Complete",

    externalSources: "External Sources",
    source: "Source",

    studentModel: "Student Model",
    systemPromptTitle: "System Prompt",
    userPromptTitle: "User Prompt",

    rc: "Textual Content (Rc)",
    rv: "Visual Content (Rv)",
    internalKnowledge: "Internal Background Knowledge (K_int)",
    externalKnowledge: "External Background Knowledge (K_ext)",

    finalResult: "Final Result",
    humanPrediction: "Human Prediction",
    aiPrediction: "AI Prediction",
    groundTruth: "Ground Truth",
    comparison: "Human–AI Comparison",
    aiExplanation: "AI Explanation",

    refresh: "Refresh Analysis Results",
    restart: "Restart",

    real: "Real",
    fake: "Fake",
    notSelected: "Not Selected",
    analyzing: "Analyzing",
    unableCompare: "Unable to Compare",

    humanWins: "Human Wins",
    aiWins: "AI Wins",
    bothCorrect: "Tie — Both Correct",
    bothWrong: "Tie — Both Incorrect",

    waitingUpload: "Waiting for Video Upload...",
    notStarted: "Not Started",
    uploading: "Uploading...",
    uploadedAnalyzing: "Video Uploaded — Analysis in Progress",
    uploadFailed: "Upload Failed",

    noAnswer: "No Corresponding Answer Found",
    noVideoSelected: "No Video Selected",
    backendUnavailable:
      "Unable to connect to the backend. Please make sure the Flask backend is running.",
    selectPredictionFirst: "Please select a prediction first.",
    missingVideoId: "Video ID is unavailable.",
    voteFailed: "Failed to submit prediction.",

    processingMedia: "Analyzing audio, frames, and visual content...",
    transcribingAudio: "Transcribing audio...",
    retrievingEvidence:
      "Retrieving evidence and searching external knowledge...",
    studentModelAnalysis: "Running Student Model analysis...",
  },
}


// ============================================================
// Translation helper
// ============================================================

function t(key, params = {}) {
  let text = translations[locale.value]?.[key] ?? key

  Object.entries(params).forEach(([name, value]) => {
    text = text.replaceAll(`{${name}}`, String(value))
  })

  return text
}


// ============================================================
// System Prompt — display only
// 不影響 Backend 實際送給 Student Model 的 Prompt
// ============================================================

const systemPromptZh = `你是一位專業的多模態事實查核專家，專精於辨識短影音中的假訊息、敘事操縱以及「脫離上下文」的誤導資訊。你的任務是嚴格根據提供的「內部背景知識」以及「外部背景知識」來驗證「文字內容」與「影像內容」描述的短影音之真實性。

在分析過程中，請特別警覺以下高階欺騙手段：

1. 脫離上下文：影像本身可能是真實的，但被賦予了錯誤的時間、地點或事件描述。
2. 地理政治重新映射：將事件發生的地點竄改為其他地區以達到特定目的。
3. 具體細節陷阱：在敘事中加入極其具體的細節（如精確的時間、人名）來增加可信度，但整體結論與事實不符。
4. 上下文劫持：利用真實的視覺證據來支持一個完全不相關且虛假的敘事結論。
5. 違背物理常識的內容：影像或文字描述中包含明顯違反物理定律或常識的元素。
6. 影像內容與文字描述的矛盾：影像中顯示的事件、人物或環境與文字描述的內容存在明顯不一致。

請採取以下思考步驟進行分析：

1. 文字分析：解析「文字內容」中的核心主張、時間、地點及關鍵事件。
2. 影像分析：分析「影像內容」的視覺描述，確認影像內容是否支持「文字內容」的主張。
3. 知識比對：將「文字內容」與「影像內容」共同與「內部背景知識」及「外部背景知識」進行交叉比對，檢查是否存在矛盾或資訊缺失。
   - 重要：需要共同參考「內部背景知識」與「外部背景知識」，避免過度依賴單一知識來源。
   - 重要：比對過程中，若外部背景知識無明確資訊能驗證短影音的內容，先檢查是否存在上述的高階欺騙手段，若無則可僅依據內部背景知識進行判斷。
   - 重要：若影片內容中沒有提供完整之日期與時間，不要預設其他時間欄位的內容。
4. 綜合判定：基於上述比對，評估該短影音內容的真實程度。

請嚴格依照以下 JSON 格式回傳：

{
  "pred_label": 0,
  "reason": "Provide a concise and objective explanation of the judgment in English without unnecessary description."
}

欄位輸出限制：
- pred_label：只能輸出 0 或 1。0 代表完全真實，1 代表存在誤導或矛盾。
- reason：使用英文提供簡潔且明確的判定理由。
- 所有輸出皆為純文字。
- reason 必須以英文輸出。`


const systemPromptEn = `You are a professional multimodal fact-checking expert specializing in identifying misinformation, narrative manipulation, and out-of-context misleading information in short-form videos. Your task is to strictly verify the authenticity of the short-form video described by the Textual Content and Visual Content based on the provided Internal Background Knowledge and External Background Knowledge.

During the analysis, pay particular attention to the following advanced deception techniques:

1. Out-of-context manipulation: The visual content itself may be authentic but associated with an incorrect time, location, or event description.
2. Geopolitical remapping: The actual location of an event may be altered and reassigned to another region for a specific purpose.
3. Specific-detail traps: Highly specific details, such as exact times or names, may be inserted into a narrative to increase credibility even when the overall conclusion is inconsistent with the facts.
4. Context hijacking: Authentic visual evidence may be used to support an unrelated or false narrative.
5. Violations of physical common sense: The visual or textual content may contain elements that clearly violate physical laws or common sense.
6. Contradictions between visual and textual content: The events, individuals, or environments shown in the video may be inconsistent with the textual description.

Follow these reasoning steps:

1. Text Analysis: Identify the core claims, time, location, and key events in the Textual Content.
2. Visual Analysis: Analyze the Visual Content and determine whether it supports the claims made in the Textual Content.
3. Knowledge Verification: Cross-check the Textual Content and Visual Content against both the Internal Background Knowledge and External Background Knowledge to identify contradictions or missing information.
   - Important: Both internal and external background knowledge should be considered to avoid over-reliance on a single source.
   - Important: If the external background knowledge does not provide sufficient information for verification, first examine whether any of the advanced deception techniques described above are present. If none are identified, the judgment may be based on the internal background knowledge.
   - Important: If the video does not provide a complete date and time, do not infer unspecified temporal information.
4. Final Assessment: Based on the above comparisons, evaluate the authenticity of the short-form video.

Return the result strictly in the following JSON format:

{
  "pred_label": 0,
  "reason": "Provide a concise and objective explanation of the judgment in English without unnecessary description."
}

Output constraints:
- pred_label: The authenticity classification label. It must be either 0 or 1. 0 represents authentic content, while 1 represents content containing misleading information or contradictions.
- reason: Provide a concise and explicit explanation in English.
- All outputs must be plain text.`


// 根據目前 UI 語言決定展示哪一版
const systemPromptDisplay = computed(() =>
  locale.value === "en" ? systemPromptEn : systemPromptZh
)


// ============================================================
// User Prompt — display only
// ============================================================

const userPromptDisplay = computed(() => {
  const rc = result.value?.Rc ?? ""
  const rv = result.value?.Rv ?? ""
  const kInt = result.value?.K_int ?? ""
  const kExt = result.value?.K_ext ?? ""

  if (locale.value === "en") {
    return `Determine the authenticity of the short-form video strictly based on the provided background knowledge and provide the reasoning for the judgment.

- Textual Content (Rc): ${rc}
- Visual Content (Rv): ${rv}
- Internal Background Knowledge (K_int): ${kInt}
- External Background Knowledge (K_ext): ${kExt}`
  }

  return `你需要嚴格根據背景知識來判斷短影音真偽並輸出判斷依據。

- 文字內容：${rc}
- 影像內容：${rv}
- 內部背景知識：${kInt}
- 外部背景知識：${kExt}`
})


// ============================================================
// InfoBlock
// ============================================================

const InfoBlock = defineComponent({
  props: {
    label: {
      type: String,
      required: true,
    },

    value: {
      type: [String, Number, Array, Object, Boolean],
      default: null,
    },
  },

  setup(props) {
    const formattedValue = computed(() => formatValue(props.value))

    return () =>
      h("div", { class: "info-block" }, [
        h("span", { class: "info-label" }, props.label),
        h("div", { class: "info-value" }, formattedValue.value),
      ])
  },
})

function voteText(vote) {
  if (vote === "true") return t("real")
  if (vote === "false") return t("fake")

  return t("notSelected")
}

function reasonText(reason) {
  const map = {
    "圖文不符": "imageTextMismatch",
    "知識有誤": "knowledgeError",
    "其他": "other",
  }

  return map[reason] ? t(map[reason]) : reason
}

function pipelineStepLabel(step) {
  const map = {
    "抽取音訊與影格": "extractAudioFrames",
    "語音轉文字與 VLM 分析": "speechVLM",
    "Data Merge": "dataMerge",
    "Retrieve": "retrieve",
    "小模型分析": "studentAnalysis",
    "分析完成": "analysisComplete",
  }

  return map[step] ? t(map[step]) : step
}

function translateStatus(text) {
  const map = {
    "等待上傳影片...": "waitingUpload",
    "尚未開始": "notStarted",
    "執行中...": "running",
    "已完成": "completed",
    "未查到": "notFound",
    "上傳中...": "uploading",
    "影片已上傳，分析中": "uploadedAnalyzing",
    "上傳失敗": "uploadFailed",
    "找不到對應答案": "noAnswer",
    "尚未選擇影片": "noVideoSelected",
    "正在進行音訊、影格與視覺內容分析...": "processingMedia",
    "正在進行語音轉文字...": "transcribingAudio",
    "正在進行知識檢索與外部證據搜尋...": "retrievingEvidence",
    "正在進行 Student Model 分析...": "studentModelAnalysis",
    "分析完成": "analysisComplete",
  }

  return map[text] ? t(map[text]) : text
}

const voteOptions = [

  { value: "true", label: "真", shortLabel: "TRUE" },

  { value: "false", label: "假", shortLabel: "FALSE" },

]



const reasonOptions = ["圖文不符", "知識有誤", "其他"]

const pipelineSteps = [
  "抽取音訊與影格",
  "語音轉文字與 VLM 分析",
  "Data Merge",
  "Retrieve",
  "小模型分析",
  "分析完成",
]



const preprocessDisplaySteps = computed(() => pipelineSteps.slice(0, 3))



const currentPage = ref(1)

const videoUrl = ref(null)

const uploadedVideoId = ref("")

const selectedVote = ref(null)

const selectedReason = ref("")

const showVoteStats = ref(false)

const voteSubmitting = ref(false)

const voteError = ref("")

const uploadMessage = ref("尚未選擇影片")

const uploadError = ref("")

const processStatus = ref("等待上傳影片...")

const pipelineStep = ref("尚未開始")

const currentStage = ref("idle")

const retrieveResult = ref(null)

const studentResult = ref(null)

const statusStudentPrompt = ref(null)

const systemAnswer = ref(null)

const correctAnswerText = ref("找不到對應答案")

const fileInput = ref(null)

const translatedContent = ref({
  Rc: "",
  Rv: "",
  K_int: "",
  K_ext: "",
  userPrompt: "",
  explanation: "",
})

const translationLoading = ref(false)
const lastTranslationKey = ref("")



const voteStats = reactive({

  total: 0,

  true_count: 0,

  false_count: 0,

  true_percent: 0,

  false_percent: 0,

})



let pollTimer = null

let uploadAbortController = null

let uploadRequestSeq = 0

const uploadInProgress = ref(false)



const statisticsRows = computed(() => [
  { key: "true", label: t("real"), percent: voteStats.true_percent },
  { key: "false", label: t("fake"), percent: voteStats.false_percent },
])



const retrieveFields = computed(() => retrieveResult.value || {})

const retrieveReady = computed(() => hasMeaningfulData(retrieveFields.value))

const retrieveLinks = computed(() => collectRetrieveLinks(retrieveFields.value))

const studentReady = computed(() => Boolean(studentResult.value))

const retrieveNoResult = computed(() => {

  if (retrieveFields.value.not_found) return true

  if (currentStage.value === "error" && pipelineStep.value === "Retrieve") return true



  return ["student", "done"].includes(currentStage.value) && !retrieveReady.value

})

const retrieveStarted = computed(

  () =>

    currentStage.value === "retrieve" ||

    ["student", "done"].includes(currentStage.value) ||

    retrieveReady.value ||

    retrieveNoResult.value

)

const studentStarted = computed(

  () =>

    currentStage.value === "student" ||

    currentStage.value === "done" ||

    studentReady.value ||

    (currentStage.value === "error" && pipelineStep.value === "小模型分析")

)



const preprocessStatusText = computed(() => {

  if (["retrieve", "student", "done"].includes(currentStage.value)) return DONE_TEXT

  if (currentStage.value === "preprocess") return RUNNING_TEXT



  return ""

})



const retrieveStatusText = computed(() => {

  if (!retrieveStarted.value) return ""

  if (currentStage.value === "retrieve") return RUNNING_TEXT

  if (retrieveNoResult.value) return NOT_FOUND_TEXT

  if (["student", "done"].includes(currentStage.value) && retrieveReady.value) return DONE_TEXT



  return ""

})



const studentStatusText = computed(() => {

  if (!studentStarted.value) return ""

  if (currentStage.value === "student") return RUNNING_TEXT

  if (currentStage.value === "done" && studentReady.value) return DONE_TEXT

  if (currentStage.value === "done" || currentStage.value === "error") return NOT_FOUND_TEXT



  return ""

})



const retrieveDisplayFields = computed(() => {

  if (!retrieveStarted.value) return blankRetrieveFields()

  if (currentStage.value === "retrieve") return fillRetrieveFields(RUNNING_TEXT)

  if (retrieveNoResult.value) return fillRetrieveFields(NOT_FOUND_TEXT)



  return retrieveFields.value

})

const translatedRetrieveDisplayFields = computed(() => {
  const original = retrieveDisplayFields.value

  // 中文介面：直接顯示原始中文
  if (locale.value !== "en") {
    return original
  }

  // 英文介面：如果 API 已翻譯完成就顯示英文
  return {
    Rc: translatedContent.value.Rc || original.Rc,
    Rv: translatedContent.value.Rv || original.Rv,
    K_int: translatedContent.value.K_int || original.K_int,
    K_ext: translatedContent.value.K_ext || original.K_ext,
  }
})

const retrieveEmptyText = computed(() => {

  if (!retrieveStarted.value) return ""

  if (currentStage.value === "retrieve") return RUNNING_TEXT

  if (retrieveNoResult.value) return NOT_FOUND_TEXT



  return ""

})

const studentResultEmptyText = computed(() => {

  if (!studentStarted.value) return ""

  if (currentStage.value === "student") return RUNNING_TEXT

  if (currentStage.value === "done" || currentStage.value === "error") return NOT_FOUND_TEXT



  return ""

})



const studentPromptFields = computed(() => {

  const prompt = statusStudentPrompt.value || {}

  const retrieve = retrieveFields.value



  return {

    system_prompt: prompt.system_prompt || "",

    user_prompt: prompt.user_prompt || buildStudentUserPrompt(retrieve),

    Rc: prompt.Rc ?? retrieve.Rc,

    Rv: prompt.Rv ?? retrieve.Rv,

    K_int: prompt.K_int ?? retrieve.K_int,

    K_ext: prompt.K_ext ?? retrieve.K_ext,

  }

})

const studentPromptDisplayFields = computed(() => {
  if (!studentStarted.value) {
    return blankStudentPromptFields()
  }

  if (
    currentStage.value === "student" &&
    !hasMeaningfulData(studentPromptFields.value)
  ) {
    return fillStudentPromptFields(RUNNING_TEXT)
  }

  if (
    (currentStage.value === "done" || currentStage.value === "error") &&
    !studentReady.value
  ) {
    return fillStudentPromptFields(NOT_FOUND_TEXT)
  }

  const original = studentPromptFields.value

  // 中文 UI：維持原始中文內容
  if (locale.value !== "en") {
    return {
      ...original,
      system_prompt: systemPromptZh,
      user_prompt: buildDisplayUserPrompt("zh"),
    }
  }

  // 英文 UI
  return {
    ...original,
    system_prompt: systemPromptEn,
    user_prompt: buildDisplayUserPrompt("en"),

    Rc: translatedContent.value.Rc || original.Rc,
    Rv: translatedContent.value.Rv || original.Rv,
    K_int: translatedContent.value.K_int || original.K_int,
    K_ext: translatedContent.value.K_ext || original.K_ext,
  }
})



const activeStepIndex = computed(() => {

  const exactIndex = pipelineSteps.indexOf(pipelineStep.value)

  if (exactIndex >= 0) return exactIndex

  if (currentStage.value === "retrieve") return 3

  if (currentStage.value === "student") return 4

  if (currentStage.value === "done") return 5



  return -1

})



const aiVote = computed(() =>

  normalizeVote(studentResult.value?.ai_vote ?? studentResult.value?.pred_label)

)



const winnerText = computed(() => {
  if (!studentReady.value) return t("analyzing")

  const user = selectedVote.value
  const ai = aiVote.value
  const answer = systemAnswer.value

  if (!answer) return t("unableCompare")

  const userCorrect = user === answer
  const aiCorrect = ai === answer

  if (userCorrect && !aiCorrect) return t("humanWins")
  if (aiCorrect && !userCorrect) return t("aiWins")
  if (aiCorrect && userCorrect) return t("bothCorrect")

  return t("bothWrong")
})



onMounted(async () => {

  await refreshOutputs()



  pollTimer = window.setInterval(() => {

    refreshOutputs()

  }, 3000)

})



onBeforeUnmount(() => {

  if (pollTimer) {

    window.clearInterval(pollTimer)

  }



  cancelActiveUpload()

  revokeVideoUrl()

})



async function fetchJson(path, options = {}) {

  const response = await fetch(`${API_BASE}${path}`, options)

  let data = null



  try {

    data = await response.json()

  } catch {

    data = null

  }



  if (!response.ok) {

    const error = new Error(data?.error || `HTTP ${response.status}`)

    error.status = response.status

    throw error

  }



  return data

}

async function translateDynamicContent() {
  // 中文介面不需要翻譯
  if (locale.value !== "en") return

  const texts = {
    Rc: retrieveResult.value?.Rc || "",
    Rv: retrieveResult.value?.Rv || "",
    K_int: retrieveResult.value?.K_int || "",
    K_ext: retrieveResult.value?.K_ext || "",
    explanation: studentResult.value?.reason || "",
  }

  // 避免還沒有資料時呼叫 API
  const hasContent = Object.values(texts).some(
    value => typeof value === "string" && value.trim()
  )

  if (!hasContent) return

  // 建立目前內容的 fingerprint
  // 相同內容就不重複呼叫翻譯 API
  const currentKey = JSON.stringify(texts)

  if (currentKey === lastTranslationKey.value) {
    return
  }

  translationLoading.value = true

  try {
    const response = await fetch(`${API_BASE}/translate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        texts,
      }),
    })

    if (!response.ok) {
      throw new Error(`Translation failed: ${response.status}`)
    }

    const data = await response.json()

    if (!data.success) {
      throw new Error(data.error || "Translation failed")
    }

    translatedContent.value = {
      ...translatedContent.value,
      ...data.translations,
    }

    // 只有成功才記錄 cache key
    lastTranslationKey.value = currentKey
  } catch (error) {
    console.error("Translation error:", error)
  } finally {
    translationLoading.value = false
  }
}

async function refreshOutputs() {
  const status = await fetchStatus()

  if (!statusBelongsToCurrentVideo(status) || uploadInProgress.value) {
    return
  }

  const tasks = []

  if (shouldFetchRetrieveResult()) tasks.push(fetchRetrieveResult())
  if (shouldFetchStudentResult()) tasks.push(fetchStudentResult())

  if (tasks.length) {
    await Promise.allSettled(tasks)
  }

  if (locale.value === "en") {
    await translateDynamicContent()
  }
}



async function fetchStatus() {

  try {

    const data = await fetchJson("/status")

    if (!statusBelongsToCurrentVideo(data) || uploadInProgress.value) {

      return data

    }



    processStatus.value = data.status || "等待上傳影片..."

    pipelineStep.value = data.pipeline_step || "尚未開始"

    currentStage.value = data.current_stage || "idle"



    if (hasMeaningfulData(data.retrieve_input)) {

      retrieveResult.value = data.retrieve_input

    }



    if (hasMeaningfulData(data.student_prompt)) {

      statusStudentPrompt.value = data.student_prompt

    }



    if (data.student_result) {

      studentResult.value = normalizeStudentResult(data.student_result)

    }



    applyCorrectAnswerFields(data)

    return data

  } catch (error) {

    if (!isPendingFetchError(error)) {

      console.error("failed to load status", error)

    }



    return null

  }

}



async function fetchRetrieveResult() {

  try {

    const data = await fetchJson("/result")

    if (resultBelongsToCurrentVideo(data)) {

      retrieveResult.value = data

    }

  } catch (error) {

    if (!isPendingFetchError(error)) {

      console.error("failed to load retrieve result", error)

    }

  }

}



async function fetchStudentResult() {

  try {

    const data = await fetchJson("/student_result")

    if (resultBelongsToCurrentVideo(data)) {

      studentResult.value = normalizeStudentResult(data)

    }

  } catch (error) {

    if (!isPendingFetchError(error)) {

      console.error("failed to load student result", error)

    }

  }

}



async function fetchVoteStatistics(videoId = uploadedVideoId.value) {

  if (!videoId) {

    resetVoteStats()

    return

  }



  try {

    const params = new URLSearchParams({ video_id: videoId })

    const data = await fetchJson(`/vote/statistics?${params.toString()}`)

    if (videoId === uploadedVideoId.value) {

      updateVoteStats(data)

    }

  } catch (error) {

    if (!isPendingFetchError(error)) {

      console.error("failed to load vote statistics", error)

    }

  }

}



async function handleFileUpload(event) {

  const file = event.target.files?.[0]

  if (!file) return



  event.target.value = ""

  cancelActiveUpload()

  const requestSeq = ++uploadRequestSeq

  uploadAbortController = new AbortController()

  uploadInProgress.value = true



  revokeVideoUrl()

  resetAnalysisState()

  selectedVote.value = null

  selectedReason.value = ""



  videoUrl.value = URL.createObjectURL(file)

  uploadedVideoId.value = file.name

  resetCorrectAnswer()

  uploadMessage.value = "上傳中..."

  uploadError.value = ""



  await fetchVoteStatistics(file.name)

  if (requestSeq !== uploadRequestSeq) return



  const formData = new FormData()

  formData.append("video", file)



  try {

    const data = await fetchJson("/upload", {

      method: "POST",

      body: formData,

      signal: uploadAbortController.signal,

    })



    if (requestSeq !== uploadRequestSeq) return



    uploadedVideoId.value = data.filename || file.name

    applyCorrectAnswerFields(data)

    await fetchVoteStatistics(uploadedVideoId.value)

    uploadMessage.value = "影片已上傳，分析中"

  } catch (error) {

    if (requestSeq !== uploadRequestSeq || error?.name === "AbortError") return



    uploadError.value =

      error.message === "Failed to fetch"

        ? "無法連接後端，請確認 Flask backend 已啟動"

        : error.message || "上傳失敗"

    uploadMessage.value = "上傳失敗"

  } finally {

    if (requestSeq === uploadRequestSeq) {

      uploadAbortController = null

      uploadInProgress.value = false

    }

  }

}



function selectVote(vote) {

  selectedVote.value = vote

  voteError.value = ""



  if (vote !== "false") {

    selectedReason.value = ""

  }

}



async function submitVote() {

  if (!selectedVote.value) {

    voteError.value = "請先選擇判斷結果"

    return

  }



  if (!uploadedVideoId.value) {

    voteError.value = "尚未取得影片 ID"

    return

  }



  voteSubmitting.value = true

  voteError.value = ""



  try {

    const data = await fetchJson("/vote", {

      method: "POST",

      headers: {

        "Content-Type": "application/json",

      },

      body: JSON.stringify({

        video_id: uploadedVideoId.value,

        vote: selectedVote.value,

      }),

    })



    updateVoteStats(data.statistics)

    showVoteStats.value = true

  } catch (error) {

    voteError.value = error.message || "投票送出失敗"

  } finally {

    voteSubmitting.value = false

  }

}



function updateVoteStats(data) {

  if (!data) return



  Object.assign(voteStats, {

    total: data.total ?? 0,

    true_count: data.true_count ?? 0,

    false_count: data.false_count ?? 0,

    true_percent: data.true_percent ?? 0,

    false_percent: data.false_percent ?? 0,

  })

}



function resetVoteStats() {

  updateVoteStats({

    total: 0,

    true_count: 0,

    false_count: 0,

    true_percent: 0,

    false_percent: 0,

  })

}



function blankRetrieveFields() {

  return {

    Rc: "",

    Rv: "",

    K_int: "",

    K_ext: "",

  }

}



function fillRetrieveFields(value) {

  return {

    Rc: value,

    Rv: value,

    K_int: value,

    K_ext: value,

  }

}



function blankStudentPromptFields() {

  return {

    system_prompt: "",

    user_prompt: "",

    Rc: "",

    Rv: "",

    K_int: "",

    K_ext: "",

  }

}



function fillStudentPromptFields(value) {

  return {

    system_prompt: value,

    user_prompt: value,

    Rc: value,

    Rv: value,

    K_int: value,

    K_ext: value,

  }

}



function shouldFetchRetrieveResult() {

  return ["student", "done"].includes(currentStage.value) && !retrieveReady.value

}



function shouldFetchStudentResult() {

  return currentStage.value === "done" && !studentReady.value

}



function normalizeVideoId(value) {

  const filename = String(value || "")

    .split(/[\\/]/)

    .pop()

    .trim()



  return filename.replace(/\.[^.]+$/, "")

}



function statusBelongsToCurrentVideo(data) {

  if (!data || !uploadedVideoId.value || !data.filename) return false



  return normalizeVideoId(data.filename) === normalizeVideoId(uploadedVideoId.value)

}



function resultBelongsToCurrentVideo(data) {

  if (!data || !uploadedVideoId.value || !data.vid) return false



  return normalizeVideoId(data.vid) === normalizeVideoId(uploadedVideoId.value)

}



function cancelActiveUpload() {

  uploadRequestSeq += 1



  if (uploadAbortController) {

    uploadAbortController.abort()

    uploadAbortController = null

  }



  uploadInProgress.value = false

}



function nextPage() {

  currentPage.value = 2

  refreshOutputs()

}



function resetGame() {

  cancelActiveUpload()

  revokeVideoUrl()

  resetAnalysisState()

  selectedVote.value = null

  selectedReason.value = ""

  uploadedVideoId.value = ""

  uploadMessage.value = "尚未選擇影片"

  uploadError.value = ""

  currentPage.value = 1



  if (fileInput.value) {

    fileInput.value.value = ""

  }

}



function resetAnalysisState() {

  showVoteStats.value = false

  resetVoteStats()

  retrieveResult.value = null

  studentResult.value = null

  statusStudentPrompt.value = null

  processStatus.value = "等待上傳影片..."

  pipelineStep.value = "尚未開始"

  currentStage.value = "idle"

  resetCorrectAnswer()

}



function revokeVideoUrl() {

  if (videoUrl.value) {

    URL.revokeObjectURL(videoUrl.value)

    videoUrl.value = null

  }

}



function stepStateClass(index) {

  if (activeStepIndex.value > index) return "step-done"

  if (activeStepIndex.value === index) return "step-active"



  return ""

}



function voteLabel(vote) {
  return voteText(vote)
}



function normalizeVote(value) {

  if (value === true) return "true"

  if (value === false) return "false"

  if (typeof value === "number") {

    if (value === 0) return "true"

    if (value === 1) return "false"

    return null

  }



  const normalized = String(value ?? "").trim().toLowerCase()

  if (["true", "real", "genuine", "0", "真"].includes(normalized)) return "true"

  if (["false", "fake", "1", "假"].includes(normalized)) return "false"



  return null

}



function normalizeStudentResult(data) {

  if (!data) return null



  const result = { ...data }

  result.ai_vote = normalizeVote(result.ai_vote ?? result.pred_label ?? result.label)



  if (typeof result.confidence === "undefined") {

    result.confidence = result.conf

  }



  return result

}

function buildDisplayUserPrompt(lang) {
  const original = studentPromptFields.value

  const rc =
    lang === "en"
      ? translatedContent.value.Rc || original.Rc || ""
      : original.Rc || ""

  const rv =
    lang === "en"
      ? translatedContent.value.Rv || original.Rv || ""
      : original.Rv || ""

  const kInt =
    lang === "en"
      ? translatedContent.value.K_int || original.K_int || ""
      : original.K_int || ""

  const kExt =
    lang === "en"
      ? translatedContent.value.K_ext || original.K_ext || ""
      : original.K_ext || ""

  if (lang === "en") {
    return [
      "Determine whether the video content is real or fake based on the following information, and output pred_label and reason.",
      "",
      "Rc:",
      formatValue(rc),
      "",
      "Rv:",
      formatValue(rv),
      "",
      "K_int:",
      formatValue(kInt),
      "",
      "K_ext:",
      formatValue(kExt),
    ].join("\n")
  }

  return [
    "請根據以下資料判斷影片內容為真或假，並輸出 pred_label 與 reason。",
    "",
    "Rc:",
    formatValue(rc),
    "",
    "Rv:",
    formatValue(rv),
    "",
    "K_int:",
    formatValue(kInt),
    "",
    "K_ext:",
    formatValue(kExt),
  ].join("\n")
}

function buildStudentUserPrompt(retrieve) {

  if (!hasMeaningfulData(retrieve)) return ""



  return [

    "請根據以下資料判斷影片內容為真或假，並輸出 pred_label 與 reason。",

    "",

    "Rc:",

    formatValue(retrieve.Rc),

    "",

    "Rv:",

    formatValue(retrieve.Rv),

    "",

    "K_int:",

    formatValue(retrieve.K_int),

    "",

    "K_ext:",

    formatValue(retrieve.K_ext),

  ].join("\n")

}



function applyCorrectAnswerFields(data) {

  if (!data || !Object.prototype.hasOwnProperty.call(data, "correct_answer")) {

    return

  }



  systemAnswer.value = data.correct_answer_vote || null

  correctAnswerText.value = data.correct_answer || "找不到對應答案"

}



function resetCorrectAnswer() {

  systemAnswer.value = null

  correctAnswerText.value = "找不到對應答案"

}



function hasMeaningfulData(value) {

  if (!value) return false

  if (Array.isArray(value)) return value.length > 0

  if (typeof value !== "object") return Boolean(value)



  return Object.values(value).some((item) => {

    if (Array.isArray(item)) return item.length > 0

    if (typeof item === "boolean") return item

    return item !== null && typeof item !== "undefined" && item !== ""

  })

}



function collectRetrieveLinks(data) {

  if (!data || typeof data !== "object") return []



  const links = []

  const linkKeys = [

    "uri",

    "uris",

    "url",

    "urls",

    "link",

    "links",

    "source",

    "sources",

    "source_url",

    "source_urls",

  ]



  linkKeys.forEach((key) => appendLinks(data[key], links))



  return Array.from(new Set(links)).slice(0, 12)

}



function appendLinks(value, links) {

  if (!value) return



  if (Array.isArray(value)) {

    value.forEach((item) => appendLinks(item, links))

    return

  }



  if (typeof value === "object") {

    Object.values(value).forEach((item) => appendLinks(item, links))

    return

  }



  const matches = String(value).match(/https?:\/\/[^\s"'<>]+/g) || []

  matches.forEach((match) => {

    const cleaned = match.replace(/[),.;\]]+$/, "")

    if (cleaned) links.push(cleaned)

  })

}



function isPendingFetchError(error) {

  const message = String(error?.message || error || "")

  return (

    error?.status === 404 ||

    message.includes("Failed to fetch") ||

    message.includes("NetworkError") ||

    message.includes("Load failed")

  )

}



function formatValue(value) {

  if (value === null || typeof value === "undefined" || value === "") {

    return ""

  }



  if (Array.isArray(value)) {

    return value.length ? value.map((item) => `- ${item}`).join("\n") : ""

  }



  if (typeof value === "object") {

    return JSON.stringify(value, null, 2)

  }



  return String(value)

}

</script>



<style scoped>

:global(*) {

  box-sizing: border-box;

}



.app-shell {

  min-height: 100vh;

  overflow-x: hidden;

  background:

    radial-gradient(circle at top left, rgba(255, 224, 221, 0.75), transparent 32%),

    radial-gradient(circle at bottom right, rgba(207, 238, 244, 0.9), transparent 34%),

    #fffdf8;

  color: #24232c;

}



.app-main {

  width: min(1080px, calc(100% - 28px));

  margin: 0 auto;

  padding: 40px 0 56px;

}



.page-stack,

.flow-grid,

.field-list,

.stats-list {

  display: grid;

}



.page-stack {

  gap: 24px;

}



.flow-grid {
  display: grid;
  gap: 18px;
  min-width: 0 !important;
  width: 100% !important;
  /* 加上這行，確保 Grid 的欄位不會被內容撐開 */
  grid-template-columns: minmax(0, 1fr) !important; 
}



.card, .field-list {
  min-width: 0 !important;
  width: 100% !important;
}



.stats-list {

  gap: 16px;

}



.page-header {

  display: grid;

  gap: 10px;

  text-align: center;

}



.page-header.compact {

  gap: 8px;

}



.eyebrow {

  justify-self: center;

  width: fit-content;

  padding: 7px 13px;

  border: 1px solid #b9a7ff;

  border-radius: 999px;

  background: #f3edff;

  color: #5b21b6;

  font-size: 12px;

  font-weight: 900;

  letter-spacing: 0.1em;

  text-transform: uppercase;

}



h1,

h2,

h3,

p,

pre {

  margin: 0;

}



h1 {

  font-size: clamp(32px, 5vw, 56px);

  line-height: 1.15;

  letter-spacing: 0;

}



.project-title {

  font-size: clamp(24px, 3.3vw, 40px);

  line-height: 1.25;

}



.project-title span {

  display: block;

  white-space: nowrap;

}



h2 {

  font-size: 24px;

  line-height: 1.25;

}



h3 {

  font-size: 14px;

  letter-spacing: 0.08em;

  text-transform: uppercase;

}



.page-header p,

.card-heading p,

.flow-title p {

  color: #55515e;

  line-height: 1.65;

}



.card {

  min-width: 0;

  border: 1px solid rgba(59, 55, 70, 0.16);

  border-radius: 8px;

  background: rgba(255, 255, 255, 0.9);

  box-shadow: 0 14px 30px rgba(72, 50, 112, 0.07);

}



.upload-card,

.vote-card,

.stats-card,

.result-card {

  padding: clamp(20px, 3vw, 34px);

}



.result-card {

  border-color: #b9a7ff;

  background: #dae8fc;

}



.card-heading {

  display: flex;

  align-items: flex-start;

  justify-content: space-between;

  gap: 16px;

  margin-bottom: 18px;

}



.soft-badge {

  flex: 0 0 auto;

  border: 1px solid rgba(94, 77, 142, 0.25);

  border-radius: 999px;

  padding: 6px 10px;

  background: rgba(255, 255, 255, 0.78);

  color: #4c3a72;

  font-size: 12px;

  font-weight: 900;

}



.result-badge {
  border-color: #8FB1E8;  /* 外框 */
  background: #DDEBFF;    /* 底色 */
  color: #345B91;         /* Result 文字 */
}



.visually-hidden {

  position: absolute;

  width: 1px;

  height: 1px;

  padding: 0;

  overflow: hidden;

  clip: rect(0, 0, 0, 0);

  white-space: nowrap;

  border: 0;

}



.button {

  display: inline-flex;

  min-height: 44px;

  max-width: 100%;

  align-items: center;

  justify-content: center;

  border: 1px solid transparent;

  border-radius: 8px;

  padding: 0 18px;

  font-weight: 900;

  text-align: center;

  cursor: pointer;

  transition: transform 160ms ease, opacity 160ms ease;

}



.button:hover {

  transform: translateY(-1px);

}



.button:disabled {

  cursor: not-allowed;

  opacity: 0.5;

  transform: none;

}



.primary-button {

  background: #7657d6;

  color: #ffffff;

}



.secondary-button {

  background: #287f70;

  color: #ffffff;

}



.ghost-button {

  border-color: #7657d6;

  background: #ffffff;

  color: #5b21b6;

}



.video-frame {

  width: 100%;

  max-width: 100%;

  margin-top: 20px;

  overflow: hidden;

  border: 1px solid rgba(47, 44, 69, 0.28);

  border-radius: 8px;

  background: #15151f;

}



.video-frame video {

  display: block;

  width: 100%;

  max-width: 100%;

  aspect-ratio: 16 / 9;

}



.vote-grid {

  display: grid;

  grid-template-columns: repeat(2, minmax(0, 1fr));

  gap: 14px;

}



.vote-button {

  min-width: 0;

  min-height: 112px;

  border: 1px solid rgba(47, 44, 69, 0.2);

  border-radius: 8px;

  background: rgba(255, 255, 255, 0.78);

  color: #25223b;

  cursor: pointer;

  transition: transform 160ms ease, border-color 160ms ease, background 160ms ease;

}



.vote-button:hover {

  transform: translateY(-1px);

  border-color: #7657d6;

}



.vote-button strong,

.vote-button span {

  display: block;

}



.vote-button strong {

  font-size: 30px;

  line-height: 1.2;

}



.vote-button span {

  margin-top: 5px;

  color: #666073;

  font-size: 11px;

  font-weight: 900;

  letter-spacing: 0.08em;

}



.vote-active-true {

  border-color: #478a40;

  background: #dff5d1;

}



.vote-active-false {

  border-color: #b44a44;

  background: #ffd2cf;

}



.reason-block {

  display: grid;

  gap: 10px;

  margin-top: 20px;

}



.reason-block p {

  color: #3d3656;

  font-weight: 900;

}



.reason-list,

.button-row {

  display: flex;

  flex-wrap: wrap;

  gap: 10px;

}



.reason-button {

  min-height: 38px;

  border: 1px solid #bca8ff;

  border-radius: 999px;

  padding: 0 14px;

  background: #ffffff;

  color: #4c3a72;

  font-weight: 800;

  cursor: pointer;

}



.reason-active {

  background: #ede7ff;

  color: #5b21b6;

}



.submit-button,

.stats-card .secondary-button {

  margin-top: 20px;

}



.error-text {

  margin-top: 12px;

  color: #a51e1e;

  font-weight: 800;

  line-height: 1.5;

  overflow-wrap: anywhere;

}



.stats-row {

  display: grid;

  gap: 8px;

}



.stats-label {

  display: flex;

  align-items: center;

  justify-content: space-between;

  gap: 12px;

  color: #334155;

  font-weight: 900;

}



.meter {

  height: 12px;

  overflow: hidden;

  border-radius: 999px;

  background: #eeeaf2;

}



.meter-fill {

  display: block;

  height: 100%;

  border-radius: inherit;

}



.meter-true {

  background: #5faa58;

}



.meter-false {

  background: #e36b65;

}



.flow-card {

  padding: 20px;

}



.preprocess-card {
  border-color: #D99A9A;
  background: #E7C2C0;
}



.retrieve-card {

  border-color: #afb17e;

  background: #fef1cc;

}



.student-card {

  border-color: #72b17a;

  background: #d5e8d4;

}



.flow-title {

  display: flex;

  gap: 14px;

  align-items: flex-start;

  margin-bottom: 18px;

}



.step-index {

  display: inline-grid;

  width: 38px;

  height: 38px;

  flex: 0 0 38px;

  place-items: center;

  border-radius: 8px;

  background: #7657d6;

  color: #ffffff;

  font-weight: 900;

}



.step-list {

  display: grid;

  gap: 10px;

  padding: 0;

  margin: 0;

  list-style: none;

}



.step-list li {

  display: flex;

  align-items: center;

  gap: 10px;

  min-height: 34px;

  border-radius: 8px;

  padding: 8px 10px;

  background: rgba(255, 255, 255, 0.65);

  color: #585b66;

  font-weight: 800;

  overflow-wrap: anywhere;

}



.step-list li span {

  width: 10px;

  height: 10px;

  flex: 0 0 10px;

  border: 2px solid #aca6b8;

  border-radius: 999px;

}



.step-list .step-active {
  color: #7A3030;
  background: #F1C6C3;
}

.step-list .step-active span {
  border-color: #B94F4F;
  background: #B94F4F;
}



.step-list .step-done {
  color: #8B4545;
  background: #F8E2E0;
}

.step-list .step-done span {
  border-color: #C96B6B;
  background: #C96B6B;
}



.info-block {
  display: grid;
  gap: 8px;
  min-width: 0 !important;
  width: 100% !important;
  padding: 12px;
  border: 1px solid rgba(59, 55, 70, 0.14);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.72);
  /* 讓卡片本身隱藏多餘部分，但這主要是防禦性設定 */
  overflow: hidden !important; 
}



.info-label {

  color: #4a435b;

  font-size: 12px;

  font-weight: 900;

  letter-spacing: 0.06em;

  text-transform: uppercase;

}



/* 尋找並修改成以下設定 */

.info-value {
  display: block;
  width: 100%;
  
  /* 徹底解放高度，有多少字就撐多高 */
  max-height: none !important; 
  
  /* 完美折行黃金組合 */
  white-space: pre-wrap;       /* 保留文字原本的換行符號（\n），同時自動折行 */
  word-break: break-all;       /* 遇到卡片邊界，管你是網址、中英文、特殊符號一律強制斷行 */
  overflow-wrap: anywhere;     /* 現代瀏覽器全面適用 */

  /* 基礎視覺樣式 */
  color: #2f2d36;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 13px;
  line-height: 1.6;
}



.link-section {

  display: grid;

  gap: 10px;

  min-width: 0;

  margin-top: 16px;

}



.source-link-grid {

  display: grid;

  grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));

  gap: 10px;

  min-width: 0;

}



.source-link-card {

  display: grid;

  gap: 7px;

  min-width: 0;

  padding: 13px;

  border: 1px solid #9bbdd4;

  border-radius: 8px;

  background: rgba(255, 255, 255, 0.78);

  color: #253f5c;

  text-decoration: none;

  transition: border-color 160ms ease, background 160ms ease;

}



.source-link-card:hover {

  border-color: #4d83b5;

  background: #ffffff;

}



.source-link-card strong {

  color: #214f7a;

  font-size: 13px;

}



.source-link-card span {

  color: #32465b;

  font-size: 12px;

  line-height: 1.5;

  overflow-wrap: anywhere;

}



.retrieve-card .source-link-card {

  border-color: #9ec58f;

  background: rgba(255, 255, 255, 0.74);

  color: #315b35;

}



.retrieve-card .source-link-card:hover {

  border-color: #5c9258;

  background: #ffffff;

}



.retrieve-card .source-link-card strong {

  color: #2f6a35;

}



.retrieve-card .source-link-card span {

  color: #3f5f42;

}



.empty-text {

  color: #6b7280;

  font-weight: 800;

}



.result-grid {

  display: grid;

  grid-template-columns: repeat(4, minmax(0, 1fr));

  gap: 12px;

}



.result-item {

  display: grid;

  gap: 8px;

  min-height: 112px;

  padding: 14px;

  border: 1px solid #c4b5fd;

  border-radius: 8px;

  background: #e7deff;

}



.result-item span {

  color: #4c3a72;

  font-size: 13px;

  font-weight: 900;

}



.result-item strong {

  color: #342159;

  font-size: 22px;

  line-height: 1.3;

  overflow-wrap: anywhere;

}



.result-item small {

  color: #5f4b83;

  font-weight: 800;

  overflow-wrap: anywhere;

}



.winner-item {
  border-color: #8FB1E8;
  background: #BDD3F8;
}



.reason-result {

  display: grid;

  gap: 10px;

  margin-top: 16px;

  padding: 14px;

  border: 1px solid #c4b5fd;

  border-radius: 8px;

  background: rgba(255, 255, 255, 0.65);

}



.reason-result p {

  color: #323545;

  line-height: 1.75;

  overflow-wrap: anywhere;

}



.result-source-section {

  padding: 14px;

  border: 1px solid #c4b5fd;

  border-radius: 8px;

  background: rgba(255, 255, 255, 0.65);

}



.result-source-section .source-link-card {

  border-color: #c4b5fd;

  color: #4c3a72;

}



.result-source-section .source-link-card strong {

  color: #4c1d95;

}

.prompt-text {
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.6;
}


.button-row {

  margin-top: 20px;

}

/* 1. 使用者判斷－最淡藍 */
.result-item:nth-child(1) {
  background: #EAF3FF;
}

/* 2. AI 判斷－淡藍 */
.result-item:nth-child(2) {
  background: #EAF3FF;
}

/* 3. 正確答案－稍深藍 */
.result-item:nth-child(3) {
  background: #EAF3FF;
}

/* 4. 勝負－最深藍 */
.result-item:nth-child(4) {
  background: #bbc6dc;
}

/* 5. AI REASON－非常淡的藍 */
.reason-result {
  background: #F2F7FF;
}

.language-toolbar {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-bottom: 18px;
}

.language-button {
  min-height: 36px;
  border: 1px solid #b9a7ff;
  border-radius: 999px;
  padding: 0 14px;
  background: rgba(255, 255, 255, 0.86);
  color: #4c3a72;
  font-weight: 900;
  cursor: pointer;
}

.language-button.active {
  background: #7657d6;
  color: #ffffff;
}

@media (max-width: 820px) {

  .app-main {

    width: min(100% - 20px, 1080px);

    padding: 24px 0 40px;

  }



  .card-heading {

    display: grid;

  }



  .vote-grid,

  .result-grid {

    grid-template-columns: 1fr;

  }



  .vote-button {

    min-height: 88px;

  }



  .project-title span {

    white-space: normal;

  }

}

</style>
