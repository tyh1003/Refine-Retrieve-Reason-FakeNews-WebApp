<template>
  <div class="app-shell">
    <main class="app-main">
      <section v-if="currentPage === 1" class="page-stack">
        <header class="page-header">
          <div class="eyebrow">AI Fake News Detection</div>
          <h1 class="project-title">
            <span>秒懂真偽：以低成本證據鏈驅動的多模態</span>
            <span>Refine–Retrieve–Reason短影音假訊息偵測</span>
          </h1>
        </header>

        <section class="card upload-card">
          <div class="card-heading">
            <div>
              <h2>上傳影片</h2>
              <p>{{ uploadMessage }}</p>
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

          <label for="video-upload" class="button primary-button">選擇影片</label>
          <p v-if="uploadError" class="error-text">{{ uploadError }}</p>

          <div v-if="videoUrl" class="video-frame">
            <video :src="videoUrl" controls></video>
          </div>

        </section>

        <section v-if="videoUrl" class="card vote-card">
          <div class="card-heading">
            <div>
              <h2>你的判斷</h2>
              <p>目前影片：{{ uploadedVideoId || "尚未取得影片名稱" }}</p>
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
              <strong>{{ option.label }}</strong>
              <span>{{ option.shortLabel }}</span>
            </button>
          </div>

          <div v-if="selectedVote === 'false'" class="reason-block">
            <p>原因</p>
            <div class="reason-list">
              <button

                v-for="reason in reasonOptions"

                :key="reason"

                type="button"

                class="reason-button"

                :class="{ 'reason-active': selectedReason === reason }"

                @click="selectedReason = reason"

              >

                {{ reason }}

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

            {{ voteSubmitting ? "送出中..." : "送出判斷" }}

          </button>

        </section>



        <section v-if="showVoteStats" class="card stats-card">

          <div class="card-heading">

            <div>

              <h2>目前投票比例</h2>

              <p>目前共有 {{ voteStats.total }} 人投票</p>

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

            查看 AI 分析

          </button>

        </section>

      </section>



      <section v-else class="page-stack">

        <header class="page-header compact">

          <div class="eyebrow">AI Reasoning Chain</div>

          <h1>分析流程</h1>

          <p>{{ processStatus }}</p>

        </header>



        <section class="flow-grid">

          <article class="card flow-card preprocess-card">

            <div class="flow-title">

              <span class="step-index">1</span>

              <div>

                <h2>前處理</h2>

                <p>{{ preprocessStatusText }}</p>

              </div>

            </div>



            <ol class="step-list">

              <li

                v-for="(step, index) in preprocessDisplaySteps"

                :key="step"

                :class="stepStateClass(index)"

              >

                <span></span>

                {{ step }}

              </li>

            </ol>

          </article>



          <article class="card flow-card retrieve-card">

            <div class="flow-title">

              <span class="step-index">2</span>

              <div>

                <h2>Retrieve</h2>

                <p>{{ retrieveStatusText }}</p>

              </div>

            </div>



            <div class="field-list">

              <InfoBlock label="Rc" :value="retrieveDisplayFields.Rc" />

              <InfoBlock label="Rv" :value="retrieveDisplayFields.Rv" />

              <InfoBlock label="K_int" :value="retrieveDisplayFields.K_int" />

              <InfoBlock label="K_ext" :value="retrieveDisplayFields.K_ext" />

            </div>



            <div class="link-section">

              <span class="info-label">查到的資料</span>

              <div v-if="retrieveLinks.length" class="source-link-grid">

                <a

                  v-for="(link, index) in retrieveLinks"

                  :key="`${link}-${index}`"

                  class="source-link-card"

                  :href="link"

                  target="_blank"

                  rel="noreferrer"

                >

                  <strong>資料 {{ index + 1 }}</strong>

                  <span>{{ link }}</span>

                </a>

              </div>

              <p v-else class="empty-text">{{ retrieveEmptyText }}</p>

            </div>

          </article>



          <article class="card flow-card student-card">

            <div class="flow-title">

              <span class="step-index">3</span>

              <div>

                <h2>小模型</h2>

                <p>{{ studentStatusText }}</p>

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

              <h2>最後結果</h2>

              <p>{{ studentStatusText }}</p>

            </div>

            <span class="soft-badge result-badge">Result</span>

          </div>



          <div class="result-grid">

            <div class="result-item">

              <span>使用者判斷</span>

              <strong>{{ voteLabel(selectedVote) }}</strong>

            </div>

            <div class="result-item">

              <span>AI 判斷</span>

              <strong>{{ studentReady ? voteLabel(aiVote) : studentStatusText }}</strong>

            </div>

            <div class="result-item">

              <span>正確答案</span>

              <strong>{{ correctAnswerText }}</strong>

            </div>

            <div class="result-item winner-item">

              <span>勝負</span>

              <strong>{{ winnerText }}</strong>

            </div>

          </div>



          <div class="reason-result">

            <h3>AI reason</h3>

            <p>{{ studentResult?.reason || studentResultEmptyText }}</p>

          </div>



          <div class="link-section result-source-section">

            <span class="info-label">查到的資料</span>

            <div v-if="retrieveLinks.length" class="source-link-grid">

              <a

                v-for="(link, index) in retrieveLinks"

                :key="`result-${link}-${index}`"

                class="source-link-card"

                :href="link"

                target="_blank"

                rel="noreferrer"

              >

                <strong>資料 {{ index + 1 }}</strong>

                <span>{{ link }}</span>

              </a>

            </div>

            <p v-else class="empty-text">{{ retrieveEmptyText }}</p>

          </div>



          <div class="button-row">

            <button type="button" class="button secondary-button" @click="refreshOutputs">

              更新分析結果

            </button>

            <button type="button" class="button ghost-button" @click="resetGame">

              重新開始

            </button>

          </div>

        </section>

      </section>

    </main>

  </div>

</template>



<script setup>

import { computed, defineComponent, h, onBeforeUnmount, onMounted, reactive, ref } from "vue"



const API_BASE = "http://127.0.0.1:5000"

const RUNNING_TEXT = "執行中..."

const DONE_TEXT = "已完成"

const NOT_FOUND_TEXT = "未查到"



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
        /* 🛠️ 關鍵修改：將原本的 "pre" 改成 "div" */
        h("div", { class: "info-value" }, formattedValue.value),
      ])
  },
})



const voteOptions = [

  { value: "true", label: "真", shortLabel: "TRUE" },

  { value: "false", label: "假", shortLabel: "FALSE" },

]



const reasonOptions = ["圖文不符", "知識有誤", "其他"]

const pipelineSteps = [

  "抽取音訊與影格",

  "語音轉文字與影格壓縮",

  "OCR",

  "Data Merge",

  "Retrieve",

  "小模型分析",

  "分析完成",

]



const preprocessDisplaySteps = computed(() => pipelineSteps.slice(0, 4))



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

  { key: "true", label: "真", percent: voteStats.true_percent },

  { key: "false", label: "假", percent: voteStats.false_percent },

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

  if (!studentStarted.value) return blankStudentPromptFields()

  if (currentStage.value === "student" && !hasMeaningfulData(studentPromptFields.value)) {

    return fillStudentPromptFields(RUNNING_TEXT)

  }

  if ((currentStage.value === "done" || currentStage.value === "error") && !studentReady.value) {

    return fillStudentPromptFields(NOT_FOUND_TEXT)

  }



  return studentPromptFields.value

})



const activeStepIndex = computed(() => {

  const exactIndex = pipelineSteps.indexOf(pipelineStep.value)

  if (exactIndex >= 0) return exactIndex

  if (currentStage.value === "retrieve") return 4

  if (currentStage.value === "student") return 5

  if (currentStage.value === "done") return 6



  return -1

})



const aiVote = computed(() =>

  normalizeVote(studentResult.value?.ai_vote ?? studentResult.value?.pred_label)

)



const winnerText = computed(() => {

  if (!studentReady.value) return "分析中"



  const user = selectedVote.value

  const ai = aiVote.value

  const answer = systemAnswer.value

  if (!answer) return "無法比對"



  const userCorrect = user === answer

  const aiCorrect = ai === answer



  if (userCorrect && !aiCorrect) return "使用者勝利"

  if (aiCorrect && !userCorrect) return "AI 勝利"

  if (aiCorrect && userCorrect) return "平手，雙方都答對"



  return "平手，雙方都未答對"

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

  if (vote === "true") return "真"

  if (vote === "false") return "假"



  return "尚未選擇"

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

  background: linear-gradient(135deg, #eee8ff, #faf8ff);

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

  border-color: #a78bfa;

  background: #ddd2ff;

  color: #4c1d95;

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

  border-color: #e5aa63;

  background: #fff1df;

}



.retrieve-card {

  border-color: #9ec58f;

  background: #edf7e8;

}



.student-card {

  border-color: #8db4df;

  background: #eaf3ff;

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

  color: #8a4f00;

  background: #ffdcae;

}



.step-list .step-active span {

  border-color: #d97706;

  background: #d97706;

}



.step-list .step-done {

  color: #8a4f00;

  background: #ffead0;

}



.step-list .step-done span {

  border-color: #f59e0b;

  background: #f59e0b;

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

  border-color: #a78bfa;

  background: #d8c9ff;

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



.button-row {

  margin-top: 20px;

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