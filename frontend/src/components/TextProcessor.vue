<template>
  <div class="text-processor">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <h2>{{ mode === 'rewrite' ? 'AI文本降重' : 'AI文本人性化' }}</h2>
        </div>
      </template>
      
      <el-form>
        <el-form-item label="输入文本">
          <el-input
            v-model="inputText"
            type="textarea"
            :rows="6"
            :maxlength="2000"
            :show-word-limit="true"
            resize="vertical"
            :placeholder="inputPlaceholder"
            @input="handleInput"
            @clear="handleClear"
            clearable
          >
            <template #prefix v-if="inputText">
              <el-icon @click="handleClear"><Close /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item label="输出语言">
          <el-select v-model="selectedLanguage" placeholder="请选择输出语言">
            <el-option
              v-for="lang in languages"
              :key="lang.value"
              :label="lang.label"
              :value="lang.value"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="模型选择">
          <el-select v-model="selectedModel" placeholder="请选择模型">
            <el-option
              v-for="model in models"
              :key="model.value"
              :label="model.label"
              :value="model.value"
            />
          </el-select>
        </el-form-item>

        <el-form-item>
          <div class="mode-selection">
            <el-checkbox v-model="useAdvanced">使用高级模式</el-checkbox>
            <el-tooltip
              class="advanced-tooltip"
              effect="light"
              placement="top-start"
              :content="advancedModeDescription"
              :show-after="100"
            >
              <el-icon class="help-icon"><QuestionFilled /></el-icon>
            </el-tooltip>
          </div>
          <div class="strength-control">
            <el-slider
              v-model="strength"
              :min="0"
              :max="100"
              :step="10"
              :format-tooltip="(val) => val + '%'"
              style="width: 200px;"
            />
            <el-tooltip
              class="strength-tooltip"
              effect="light"
              placement="top-start"
              :content="strengthDescription"
              :show-after="100"
            >
              <el-icon class="help-icon"><QuestionFilled /></el-icon>
            </el-tooltip>
          </div>
        </el-form-item>

        <el-form-item v-if="mode === 'humanize'" label="输出风格">
          <el-select v-model="selectedStyle" placeholder="请选择输出风格">
            <el-option
              v-for="style in styles"
              :key="style.value"
              :label="style.label"
              :value="style.value"
            />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="processText" :loading="loading">
            开始处理
          </el-button>
        </el-form-item>

        <el-form-item v-if="result" label="处理结果">
          <el-input
            v-model="result"
            type="textarea"
            :rows="6"
            :maxlength="3000"
            :show-word-limit="true"
            resize="vertical"
            readonly
          />
          <div class="result-actions">
            <el-button type="primary" link @click="copyResult">
              <el-icon><Document /></el-icon>
              复制结果
            </el-button>
            <el-button type="danger" link @click="clearResult">
              <el-icon><Delete /></el-icon>
              清空结果
            </el-button>
          </div>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Close, Document, Delete, QuestionFilled } from '@element-plus/icons-vue'
import axios from 'axios'

const props = defineProps({
  mode: {
    type: String,
    default: 'rewrite'
  }
})

// 响应式数据
const inputText = ref('')
const result = ref('')
const loading = ref(false)
const useAdvanced = ref(false)
const strength = ref(50)
const selectedModel = ref('gpt-3.5-turbo')
const selectedLanguage = ref('zh')
const selectedStyle = ref('casual')

// 计算属性
const inputPlaceholder = computed(() => {
  return props.mode === 'rewrite' 
    ? '请输入需要降重的文本...'
    : '请输入需要人性化处理的AI文本...'
})

// 高级模式说明
const advancedModeDescription = computed(() => {
  if (props.mode === 'rewrite') {
    return `高级模式功能：
• 更复杂的句式重组
• 主被动语态转换
• 智能添加过渡词
• 更灵活的语气调整
• 适当扩充细节
• 保持文章连贯性`
  } else {
    return `高级模式功能：
• 更自然的语言变化
• 添加个人观点和反应
• 加入情感表达
• 使用更多习语
• 添加场景和背景
• 加入生动的例子`
  }
})

// 添加进度条说明
const strengthDescription = computed(() => {
  if (props.mode === 'rewrite') {
    return `降重程度说明：
• 0-30%：轻度改写
  - 主要进行同义词替换
  - 保持原文结构基本不变
  - 适合轻微调整

• 30-70%：中度改写
  - 句式结构适度调整
  - 增加过渡词和连接词
  - 部分段落重组
  - 适合一般降重需求

• 70-100%：深度改写
  - 大幅度的结构重组
  - 更换表达方式
  - 扩充细节和例证
  - 适合高要求的降重`
  } else {
    return `人性化程度说明：
• 0-30%：轻度调整
  - 基础的语气词添加
  - 简单的表达变化
  - 保持原文风格为主

• 30-70%：中度优化
  - 增加对话和互动元素
  - 适度加入个人观点
  - 调整语言节奏
  - 添加生活化例子

• 70-100%：深度人性化
  - 完全的口语化改写
  - 丰富的情感表达
  - 大量个性化元素
  - 更自然的行文逻辑`
  }
})

// 添加 clearAll 函数
const clearAll = () => {
  inputText.value = ''
  result.value = ''
  useAdvanced.value = false
  strength.value = 50
  selectedModel.value = 'gpt-3.5-turbo'
  selectedLanguage.value = 'zh'
  selectedStyle.value = 'casual'
}

// 监听模式变化
watch(() => props.mode, (newMode) => {
  // 切换模式时清空内容
  clearAll()
})

// 输入处理
const handleInput = (value) => {
  // 可以在这里添加输入验证或其他处理
  if (value.length >= 1900) {
    ElMessage.warning('接近字数限制')
  }
}

// 清空处理
const handleClear = () => {
  inputText.value = ''
}

const clearResult = () => {
  result.value = ''
}

// 复制结果
const copyResult = () => {
  navigator.clipboard.writeText(result.value)
    .then(() => {
      ElMessage({
        message: '复制成功',
        type: 'success',
        icon: Document
      })
    })
    .catch(() => {
      ElMessage({
        message: '复制失败',
        type: 'error'
      })
    })
}

// 处理文本
const processText = async () => {
  if (!inputText.value.trim()) {
    ElMessage({
      message: '请输入需要处理的文本',
      type: 'warning'
    })
    return
  }

  if (inputText.value.length > 2000) {
    ElMessage({
      message: '文本长度超出限制',
      type: 'warning'
    })
    return
  }

  loading.value = true
  try {
    const response = await axios.post('/api/generate/', {
      text: inputText.value,
      strength: strength.value / 100,
      advanced: useAdvanced.value,
      model: selectedModel.value,
      mode: props.mode,
      language: selectedLanguage.value,
      style: selectedStyle.value
    })
    result.value = response.data.processed
    ElMessage({
      message: '处理成功',
      type: 'success'
    })
  } catch (error) {
    console.error('错误详情:', error)
    ElMessage({
      message: error.response?.data?.error || '处理失败',
      type: 'error'
    })
  } finally {
    loading.value = false
  }
}

// 可选模型列表
const models = [
  { label: 'GPT-3.5 Turbo（推荐）', value: 'gpt-3.5-turbo' },
  { label: 'GPT-3.5 Turbo 16K（长文本）', value: 'gpt-3.5-turbo-16k' },
  { label: 'GPT-4（更强但更贵）', value: 'gpt-4' },
  { label: 'GPT-4 Turbo（最新版本）', value: 'gpt-4-turbo-preview' }
]

// 添加语言选择
const languages = [
  { label: '中文', value: 'zh' },
  { label: 'English', value: 'en' }
]

// 风格选项列表
const styles = [
  { label: '学术专业', value: 'academic' },
  { label: '商务正式', value: 'business' },
  { label: '日常口语', value: 'casual' },
  { label: '风趣幽默', value: 'humorous' },
  { label: '故事叙述', value: 'narrative' },
  { label: '新闻报道', value: 'journalistic' },
  { label: '博客随笔', value: 'blog' },
  { label: '社交媒体', value: 'social' }
]
</script>

<style scoped>
.text-processor {
  max-width: 800px;
  margin: 20px auto;
  padding: 0 20px;
}

.card-header {
  text-align: center;
}

.el-form-item {
  margin-bottom: 20px;
}

.result-actions {
  margin-top: 10px;
  display: flex;
  gap: 15px;
}

:deep(.el-input__wrapper) {
  padding: 8px 12px;
}

:deep(.el-textarea__inner) {
  min-height: 120px !important;
  font-size: 14px;
  line-height: 1.6;
}

:deep(.el-input__count) {
  background: transparent;
  font-size: 12px;
  color: #909399;
}

.mode-selection {
  display: flex;
  align-items: center;
  gap: 8px;
}

.help-icon {
  color: #909399;
  font-size: 16px;
  cursor: pointer;
  transition: color 0.3s;
}

.help-icon:hover {
  color: #409EFF;
}

:deep(.el-tooltip__trigger) {
  outline: none;
}

:deep(.el-tooltip__popper) {
  max-width: 300px;
  line-height: 1.6;
  white-space: pre-line;
}

.strength-control {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 20px;
}
</style> 