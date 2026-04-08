<template>
  <el-dialog
    v-model="dialogVisible"
    :title="isEntityType ? '审核实体类型定义' : '审核关系类型定义'"
    width="800px"
  >
    <el-form :model="formData" label-width="120px">
      <el-form-item label="类型名称">
        <el-input :value="typeName" disabled />
      </el-form-item>
      
      <el-form-item label="定义">
        <el-input
          v-model="formData.definition"
          type="textarea"
          :rows="4"
          placeholder="请输入或修改定义"
        />
      </el-form-item>

      <el-form-item label="方向规则" v-if="!isEntityType">
        <el-input
          v-model="formData.direction_rule"
          type="textarea"
          :rows="2"
          placeholder="请输入关系方向规则"
        />
      </el-form-item>

      <el-form-item label="示例">
        <el-tag
          v-for="(example, index) in formData.examples"
          :key="index"
          closable
          @close="removeExample(index)"
          style="margin-right: 8px; margin-bottom: 8px;"
        >
          {{ example }}
        </el-tag>
        <el-input
          v-model="newExample"
          placeholder="输入示例后按回车添加"
          @keyup.enter="addExample"
          style="width: 200px; margin-top: 8px;"
        />
      </el-form-item>

      <el-form-item label="消歧说明">
        <el-input
          v-model="formData.disambiguation"
          type="textarea"
          :rows="3"
          placeholder="请输入消歧说明"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="handleReject">驳回</el-button>
      <el-button type="primary" @click="handleApprove">批准</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useLabelStore } from '@/stores/label'
import type { EntityType, RelationType } from '@/api/label'

interface Props {
  visible: boolean
  entityType?: EntityType | null
  relationType?: RelationType | null
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:visible': [value: boolean]
  'success': []
}>()

const labelStore = useLabelStore()
const newExample = ref('')

const formData = ref({
  definition: '',
  direction_rule: '',
  examples: [] as string[],
  disambiguation: ''
})

const dialogVisible = computed({
  get: () => props.visible,
  set: (value) => emit('update:visible', value)
})

const isEntityType = computed(() => !!props.entityType)

const typeName = computed(() => {
  if (props.entityType) {
    return `${props.entityType.type_name_zh} (${props.entityType.type_name})`
  }
  if (props.relationType) {
    return `${props.relationType.type_name_zh} (${props.relationType.type_name})`
  }
  return ''
})

watch(() => props.visible, (visible) => {
  if (visible) {
    if (props.entityType) {
      formData.value = {
        definition: props.entityType.definition || '',
        direction_rule: '',
        examples: props.entityType.examples || [],
        disambiguation: props.entityType.disambiguation || ''
      }
    } else if (props.relationType) {
      formData.value = {
        definition: props.relationType.definition || '',
        direction_rule: props.relationType.direction_rule || '',
        examples: props.relationType.examples || [],
        disambiguation: props.relationType.disambiguation || ''
      }
    }
  }
})

const addExample = () => {
  if (newExample.value.trim()) {
    formData.value.examples.push(newExample.value.trim())
    newExample.value = ''
  }
}

const removeExample = (index: number) => {
  formData.value.examples.splice(index, 1)
}

const handleApprove = async () => {
  try {
    if (props.entityType) {
      await labelStore.reviewEntityType(props.entityType.id, {
        approved: true,
        definition: formData.value.definition,
        examples: formData.value.examples,
        disambiguation: formData.value.disambiguation
      })
    } else if (props.relationType) {
      await labelStore.reviewRelationType(props.relationType.id, {
        approved: true,
        definition: formData.value.definition,
        direction_rule: formData.value.direction_rule,
        examples: formData.value.examples,
        disambiguation: formData.value.disambiguation
      })
    }
    emit('success')
    dialogVisible.value = false
  } catch (error) {
    ElMessage.error('审核失败')
  }
}

const handleReject = async () => {
  try {
    if (props.entityType) {
      await labelStore.reviewEntityType(props.entityType.id, {
        approved: false
      })
    } else if (props.relationType) {
      await labelStore.reviewRelationType(props.relationType.id, {
        approved: false
      })
    }
    ElMessage.success('已驳回')
    emit('success')
    dialogVisible.value = false
  } catch (error) {
    ElMessage.error('操作失败')
  }
}
</script>
