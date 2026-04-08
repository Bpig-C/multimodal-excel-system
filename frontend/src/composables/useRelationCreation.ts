/**
 * 关系创建Composable
 * 提供关系创建的交互逻辑（点击两个实体创建关系）
 */

import { ref } from 'vue'

export interface RelationCreationState {
  isActive: boolean
  sourceEntityId: number | null
  targetEntityId: number | null
  step: 'idle' | 'selecting-source' | 'selecting-target'
}

export function useRelationCreation() {
  const state = ref<RelationCreationState>({
    isActive: false,
    sourceEntityId: null,
    targetEntityId: null,
    step: 'idle'
  })

  /**
   * 开始创建关系
   */
  const startCreation = () => {
    state.value = {
      isActive: true,
      sourceEntityId: null,
      targetEntityId: null,
      step: 'selecting-source'
    }
  }

  /**
   * 选择实体
   * @param entityId 实体ID
   * @returns 是否完成选择（选择了两个实体）
   */
  const selectEntity = (entityId: number): boolean => {
    if (!state.value.isActive) {
      return false
    }

    if (state.value.step === 'selecting-source') {
      // 选择源实体
      state.value.sourceEntityId = entityId
      state.value.step = 'selecting-target'
      return false
    } else if (state.value.step === 'selecting-target') {
      // 选择目标实体
      if (entityId === state.value.sourceEntityId) {
        // 不能选择同一个实体
        return false
      }
      state.value.targetEntityId = entityId
      return true // 完成选择
    }

    return false
  }

  /**
   * 取消创建
   */
  const cancelCreation = () => {
    state.value = {
      isActive: false,
      sourceEntityId: null,
      targetEntityId: null,
      step: 'idle'
    }
  }

  /**
   * 重置状态（创建完成后）
   */
  const reset = () => {
    cancelCreation()
  }

  /**
   * 获取当前选择的实体ID
   */
  const getSelectedEntities = () => {
    return {
      sourceEntityId: state.value.sourceEntityId,
      targetEntityId: state.value.targetEntityId
    }
  }

  /**
   * 判断实体是否被选中
   */
  const isEntitySelected = (entityId: number): 'source' | 'target' | null => {
    if (entityId === state.value.sourceEntityId) {
      return 'source'
    }
    if (entityId === state.value.targetEntityId) {
      return 'target'
    }
    return null
  }

  /**
   * 获取提示信息
   */
  const getHintMessage = (): string => {
    switch (state.value.step) {
      case 'selecting-source':
        return '请点击源实体'
      case 'selecting-target':
        return '请点击目标实体'
      default:
        return ''
    }
  }

  return {
    state,
    startCreation,
    selectEntity,
    cancelCreation,
    reset,
    getSelectedEntities,
    isEntitySelected,
    getHintMessage
  }
}
