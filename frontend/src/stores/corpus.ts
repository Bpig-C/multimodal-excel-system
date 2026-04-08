/**
 * 语料管理Store
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { corpusApi } from '@/api'
import type { Corpus, PaginatedResponse } from '@/types'

export const useCorpusStore = defineStore('corpus', () => {
  // State
  const corpusList = ref<Corpus[]>([])
  const currentCorpus = ref<Corpus | null>(null)
  const total = ref(0)
  const loading = ref(false)

  // Actions
  const fetchList = async (params?: {
    page?: number
    page_size?: number
    source_file?: string
    source_field?: string  // 修改为 source_field 以匹配后端
    has_images?: boolean
  }) => {
    loading.value = true
    try {
      const response = await corpusApi.list(params)
      corpusList.value = response.items
      total.value = response.total
      return response
    } finally {
      loading.value = false
    }
  }

  const fetchDetail = async (id: number) => {
    loading.value = true
    try {
      const corpus = await corpusApi.get(id)
      currentCorpus.value = corpus
      return corpus
    } finally {
      loading.value = false
    }
  }

  const upload = async (file: File) => {
    loading.value = true
    try {
      const result = await corpusApi.upload(file)
      // 上传成功后刷新列表
      await fetchList()
      return result
    } finally {
      loading.value = false
    }
  }

  const deleteCorpus = async (textId: string) => {
    loading.value = true
    try {
      await corpusApi.delete(textId)
      // 删除成功后从列表中移除
      corpusList.value = corpusList.value.filter(c => c.text_id !== textId)
      total.value--
    } finally {
      loading.value = false
    }
  }

  const reset = () => {
    corpusList.value = []
    currentCorpus.value = null
    total.value = 0
    loading.value = false
  }

  return {
    corpusList,
    currentCorpus,
    total,
    loading,
    fetchList,
    fetchDetail,
    upload,
    deleteCorpus,
    reset
  }
})
