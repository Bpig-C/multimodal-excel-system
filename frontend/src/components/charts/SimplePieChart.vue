<template>
  <div class="pie-chart">
    <div v-if="slices.length > 0" class="chart-wrap">
      <svg :viewBox="`0 0 ${size} ${size}`" class="chart-svg" role="img" aria-label="pie chart">
        <template v-if="slices.length === 1">
          <circle
            :cx="center"
            :cy="center"
            :r="radius"
            :fill="slices[0].color"
          />
        </template>
        <template v-else>
          <path
            v-for="slice in slices"
            :key="slice.name"
            :d="slice.path"
            :fill="slice.color"
          />
        </template>
        <circle
          :cx="center"
          :cy="center"
          :r="innerRadius"
          fill="#fff"
        />
        <text :x="center" :y="center - 6" text-anchor="middle" class="total-label">总计</text>
        <text :x="center" :y="center + 14" text-anchor="middle" class="total-value">{{ total }}</text>
      </svg>

      <div class="legend">
        <div
          v-for="slice in slices"
          :key="`${slice.name}-${slice.count}`"
          class="legend-item"
        >
          <span class="dot" :style="{ backgroundColor: slice.color }" />
          <span class="name" :title="slice.name">{{ slice.name }}</span>
          <span class="value">{{ slice.count }} ({{ formatPercent(slice.percent) }})</span>
        </div>
      </div>
    </div>

    <el-empty v-else description="暂无数据" :image-size="100" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface PieItem {
  name: string
  count: number
}

const props = withDefaults(defineProps<{
  data: PieItem[]
  size?: number
  maxItems?: number
}>(), {
  size: 240,
  maxItems: 10
})

const colors = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc', '#2f4554']

const normalized = computed(() => {
  return (props.data || [])
    .filter((item) => item && Number(item.count) > 0)
    .slice(0, props.maxItems)
    .map((item) => ({
      name: String(item.name ?? ''),
      count: Number(item.count)
    }))
})

const total = computed(() => normalized.value.reduce((sum, item) => sum + item.count, 0))
const size = computed(() => props.size)
const center = computed(() => size.value / 2)
const radius = computed(() => Math.max(20, size.value * 0.42))
const innerRadius = computed(() => Math.max(12, radius.value * 0.55))

const slices = computed(() => {
  if (!normalized.value.length || total.value <= 0) return []

  let start = -Math.PI / 2
  return normalized.value.map((item, idx) => {
    const percent = item.count / total.value
    const end = start + percent * Math.PI * 2
    const path = buildSectorPath(center.value, center.value, radius.value, start, end)
    const slice = {
      ...item,
      percent,
      color: colors[idx % colors.length],
      path
    }
    start = end
    return slice
  })
})

function polarToCartesian(cx: number, cy: number, r: number, angle: number) {
  return {
    x: cx + r * Math.cos(angle),
    y: cy + r * Math.sin(angle)
  }
}

function buildSectorPath(cx: number, cy: number, r: number, start: number, end: number) {
  const diff = end - start
  if (diff >= Math.PI * 2 - 1e-6) {
    return `M ${cx} ${cy - r} A ${r} ${r} 0 1 1 ${cx - 0.01} ${cy - r} Z`
  }

  const startPoint = polarToCartesian(cx, cy, r, start)
  const endPoint = polarToCartesian(cx, cy, r, end)
  const largeArcFlag = diff > Math.PI ? 1 : 0

  return [
    `M ${cx} ${cy}`,
    `L ${startPoint.x} ${startPoint.y}`,
    `A ${r} ${r} 0 ${largeArcFlag} 1 ${endPoint.x} ${endPoint.y}`,
    'Z'
  ].join(' ')
}

function formatPercent(value: number) {
  return `${(value * 100).toFixed(1)}%`
}
</script>

<style scoped lang="scss">
.pie-chart {
  width: 100%;

  .chart-wrap {
    display: flex;
    gap: 16px;
    align-items: center;
  }

  .chart-svg {
    width: 240px;
    height: 240px;
    flex-shrink: 0;
  }

  .total-label {
    fill: #909399;
    font-size: 12px;
  }

  .total-value {
    fill: #303133;
    font-size: 18px;
    font-weight: 600;
  }

  .legend {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    min-width: 0;
  }

  .dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .name {
    color: #303133;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    max-width: 220px;
  }

  .value {
    color: #606266;
    margin-left: auto;
    white-space: nowrap;
  }
}
</style>
