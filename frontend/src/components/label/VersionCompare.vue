<template>
  <el-dialog
    v-model="dialogVisible"
    title="版本比较"
    width="1200px"
  >
    <div v-if="version1 && version2" class="version-compare">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="版本1">{{ version1.version_name }}</el-descriptions-item>
        <el-descriptions-item label="版本2">{{ version2.version_name }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ version1.created_at }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ version2.created_at }}</el-descriptions-item>
      </el-descriptions>

      <div v-if="compareResult" class="compare-result">
        <el-divider>实体类型变更</el-divider>
        
        <el-collapse v-model="activeNames">
          <el-collapse-item title="新增实体类型" name="added-entities" v-if="compareResult.added_entities.length > 0">
            <el-table :data="compareResult.added_entities">
              <el-table-column prop="type_name" label="类型名称" width="150" />
              <el-table-column prop="type_name_zh" label="中文名称" width="150" />
              <el-table-column prop="description" label="描述" show-overflow-tooltip />
            </el-table>
          </el-collapse-item>

          <el-collapse-item title="删除实体类型" name="removed-entities" v-if="compareResult.removed_entities.length > 0">
            <el-table :data="compareResult.removed_entities">
              <el-table-column prop="type_name" label="类型名称" width="150" />
              <el-table-column prop="type_name_zh" label="中文名称" width="150" />
              <el-table-column prop="description" label="描述" show-overflow-tooltip />
            </el-table>
          </el-collapse-item>

          <el-collapse-item title="修改实体类型" name="modified-entities" v-if="compareResult.modified_entities.length > 0">
            <el-table :data="compareResult.modified_entities">
              <el-table-column prop="old.type_name" label="类型名称" width="150" />
              <el-table-column label="变更内容">
                <template #default="{ row }">
                  <div class="diff-content">
                    <div v-if="row.old.type_name_zh !== row.new.type_name_zh">
                      <span class="diff-label">中文名称:</span>
                      <span class="diff-old">{{ row.old.type_name_zh }}</span>
                      <span class="diff-arrow">→</span>
                      <span class="diff-new">{{ row.new.type_name_zh }}</span>
                    </div>
                    <div v-if="row.old.color !== row.new.color">
                      <span class="diff-label">颜色:</span>
                      <el-tag :color="row.old.color" :style="{ backgroundColor: row.old.color, color: '#fff' }">旧</el-tag>
                      <span class="diff-arrow">→</span>
                      <el-tag :color="row.new.color" :style="{ backgroundColor: row.new.color, color: '#fff' }">新</el-tag>
                    </div>
                    <div v-if="row.old.description !== row.new.description">
                      <span class="diff-label">描述:</span>
                      <span class="diff-old">{{ row.old.description }}</span>
                      <span class="diff-arrow">→</span>
                      <span class="diff-new">{{ row.new.description }}</span>
                    </div>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </el-collapse-item>
        </el-collapse>

        <el-divider>关系类型变更</el-divider>
        
        <el-collapse v-model="activeNames">
          <el-collapse-item title="新增关系类型" name="added-relations" v-if="compareResult.added_relations.length > 0">
            <el-table :data="compareResult.added_relations">
              <el-table-column prop="type_name" label="类型名称" width="150" />
              <el-table-column prop="type_name_zh" label="中文名称" width="150" />
              <el-table-column prop="description" label="描述" show-overflow-tooltip />
            </el-table>
          </el-collapse-item>

          <el-collapse-item title="删除关系类型" name="removed-relations" v-if="compareResult.removed_relations.length > 0">
            <el-table :data="compareResult.removed_relations">
              <el-table-column prop="type_name" label="类型名称" width="150" />
              <el-table-column prop="type_name_zh" label="中文名称" width="150" />
              <el-table-column prop="description" label="描述" show-overflow-tooltip />
            </el-table>
          </el-collapse-item>

          <el-collapse-item title="修改关系类型" name="modified-relations" v-if="compareResult.modified_relations.length > 0">
            <el-table :data="compareResult.modified_relations">
              <el-table-column prop="old.type_name" label="类型名称" width="150" />
              <el-table-column label="变更内容">
                <template #default="{ row }">
                  <div class="diff-content">
                    <div v-if="row.old.type_name_zh !== row.new.type_name_zh">
                      <span class="diff-label">中文名称:</span>
                      <span class="diff-old">{{ row.old.type_name_zh }}</span>
                      <span class="diff-arrow">→</span>
                      <span class="diff-new">{{ row.new.type_name_zh }}</span>
                    </div>
                    <div v-if="row.old.color !== row.new.color">
                      <span class="diff-label">颜色:</span>
                      <el-tag :color="row.old.color" :style="{ backgroundColor: row.old.color, color: '#fff' }">旧</el-tag>
                      <span class="diff-arrow">→</span>
                      <el-tag :color="row.new.color" :style="{ backgroundColor: row.new.color, color: '#fff' }">新</el-tag>
                    </div>
                    <div v-if="row.old.description !== row.new.description">
                      <span class="diff-label">描述:</span>
                      <span class="diff-old">{{ row.old.description }}</span>
                      <span class="diff-arrow">→</span>
                      <span class="diff-new">{{ row.new.description }}</span>
                    </div>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </el-collapse-item>
        </el-collapse>
      </div>

      <el-empty v-else description="暂无差异" />
    </div>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useLabelStore } from '@/stores/label'
import type { LabelSchemaVersion } from '@/api/label'

interface Props {
  visible: boolean
  version1?: LabelSchemaVersion
  version2?: LabelSchemaVersion
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:visible': [value: boolean]
}>()

const labelStore = useLabelStore()
const activeNames = ref(['added-entities', 'removed-entities', 'modified-entities', 'added-relations', 'removed-relations', 'modified-relations'])
const compareResult = ref<any>(null)

const dialogVisible = computed({
  get: () => props.visible,
  set: (value) => emit('update:visible', value)
})

watch(() => props.visible, async (visible) => {
  if (visible && props.version1 && props.version2) {
    try {
      compareResult.value = await labelStore.compareVersions(
        props.version1.version_id,
        props.version2.version_id
      )
    } catch (error) {
      ElMessage.error('比较失败')
    }
  }
})
</script>

<style scoped>
.version-compare {
  padding: 20px 0;
}

.compare-result {
  margin-top: 20px;
}

.diff-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.diff-label {
  font-weight: 500;
  margin-right: 8px;
}

.diff-old {
  color: #f56c6c;
  text-decoration: line-through;
}

.diff-new {
  color: #67c23a;
  font-weight: 500;
}

.diff-arrow {
  margin: 0 8px;
  color: #909399;
}
</style>
