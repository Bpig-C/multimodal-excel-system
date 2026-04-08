<template>
  <span
    class="entity-highlight"
    :class="{ selected: isSelected, hovered: isHovered }"
    :style="highlightStyle"
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
    @click="handleClick"
  >
    <slot />
    <span v-if="showLabel" class="entity-label">{{ label }}</span>
  </span>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Props {
  color: string
  label?: string
  isSelected?: boolean
  showLabel?: boolean
}

interface Emits {
  (e: 'click'): void
}

const props = withDefaults(defineProps<Props>(), {
  isSelected: false,
  showLabel: false
})

const emit = defineEmits<Emits>()

const isHovered = ref(false)

const highlightStyle = computed(() => {
  const baseColor = props.color || '#2196f3'
  
  return {
    '--entity-color': baseColor,
    '--entity-bg': `${baseColor}20`, // 20% opacity
    '--entity-border': baseColor,
    '--entity-hover-bg': `${baseColor}40`, // 40% opacity
    '--entity-selected-bg': '#ffeb3b40' // Yellow with 40% opacity
  }
})

const handleClick = () => {
  emit('click')
}
</script>

<style scoped>
.entity-highlight {
  position: relative;
  background-color: var(--entity-bg);
  border-bottom: 2px solid var(--entity-border);
  cursor: pointer;
  transition: all 0.2s;
  padding: 2px 0;
}

.entity-highlight:hover {
  background-color: var(--entity-hover-bg);
}

.entity-highlight.selected {
  background-color: var(--entity-selected-bg);
  border-bottom-color: #fbc02d;
}

.entity-label {
  position: absolute;
  top: -20px;
  left: 0;
  font-size: 11px;
  padding: 2px 6px;
  background-color: var(--entity-color);
  color: white;
  border-radius: 3px;
  white-space: nowrap;
  z-index: 10;
  opacity: 0;
  transition: opacity 0.2s;
}

.entity-highlight:hover .entity-label {
  opacity: 1;
}
</style>
