/**
 * 复核管理Store
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { reviewApi } from '@/api'
import type { ReviewTask, ReviewStatistics } from '@/types'

export const useReviewStore = defineStore('review', () => {
  // State
  const reviewList = ref<ReviewTask[]>([])
  const currentReview = ref<ReviewTask | null>(null)
  const statistics = ref<ReviewStatistics | null>(null)
  const total = ref(0)
  const loading = ref(false)

  // Actions
  const fetchList = async (params?: {
    page?: number
    page_size?: number
    status?: string
    reviewer_id?: number
  }) => {
    loading.value = true
    try {
      const response = await reviewApi.list(params)
      reviewList.value = response.items
      total.value = response.total
      return response
    } finally {
      loading.value = false
    }
  }

  const fetchDetail = async (reviewId: string) => {
    loading.value = true
    try {
      const review = await reviewApi.get(reviewId)
      currentReview.value = review
      return review
    } finally {
      loading.value = false
    }
  }

  const submit = async (taskId: string) => {
    loading.value = true
    try {
      const result = await reviewApi.submit(taskId)
      return result
    } finally {
      loading.value = false
    }
  }

  const approve = async (reviewId: string, data?: {
    comment?: string
  }) => {
    loading.value = true
    try {
      await reviewApi.approve(reviewId, data)
      // 更新列表中的状态
      const review = reviewList.value.find(r => r.review_id === reviewId)
      if (review) {
        review.status = 'approved'
      }
      if (currentReview.value?.review_id === reviewId) {
        currentReview.value.status = 'approved'
      }
    } finally {
      loading.value = false
    }
  }

  const reject = async (reviewId: string, data: {
    comment: string
    suggestions?: string
  }) => {
    loading.value = true
    try {
      await reviewApi.reject(reviewId, data)
      // 更新列表中的状态
      const review = reviewList.value.find(r => r.review_id === reviewId)
      if (review) {
        review.status = 'rejected'
      }
      if (currentReview.value?.review_id === reviewId) {
        currentReview.value.status = 'rejected'
      }
    } finally {
      loading.value = false
    }
  }

  const fetchStatistics = async (datasetId: number) => {
    loading.value = true
    try {
      const stats = await reviewApi.getStatistics(datasetId)
      statistics.value = stats
      return stats
    } finally {
      loading.value = false
    }
  }

  const fetchSummary = async (datasetId: number) => {
    loading.value = true
    try {
      return await reviewApi.getSummary(datasetId)
    } finally {
      loading.value = false
    }
  }

  const reset = () => {
    reviewList.value = []
    currentReview.value = null
    statistics.value = null
    total.value = 0
    loading.value = false
  }

  return {
    reviewList,
    currentReview,
    statistics,
    total,
    loading,
    fetchList,
    fetchDetail,
    submit,
    approve,
    reject,
    fetchStatistics,
    fetchSummary,
    reset
  }
})
