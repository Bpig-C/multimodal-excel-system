/**
 * 文本选择Composable
 * 提供增强的文本选择功能，包括偏移量计算和验证
 */

export interface TextSelection {
  start: number
  end: number
  text: string
}

export function useTextSelection() {
  /**
   * 获取当前文本选择
   * @param container 文本容器元素
   * @returns 选择的文本范围和内容
   */
  const getSelection = (container: HTMLElement | undefined): TextSelection | null => {
    console.log('[useTextSelection] getSelection called, container:', container)
    
    if (!container) {
      console.log('[useTextSelection] No container')
      return null
    }

    const selection = window.getSelection()
    console.log('[useTextSelection] window.getSelection():', selection)
    
    if (!selection || selection.rangeCount === 0) {
      console.log('[useTextSelection] No selection or no ranges')
      return null
    }

    const range = selection.getRangeAt(0)
    console.log('[useTextSelection] range:', range)
    console.log('[useTextSelection] range.commonAncestorContainer:', range.commonAncestorContainer)
    
    // 确保选择在容器内
    if (!container.contains(range.commonAncestorContainer)) {
      console.log('[useTextSelection] Selection not in container')
      return null
    }

    // 计算偏移量
    const start = getOffsetInContainer(container, range.startContainer, range.startOffset)
    const end = getOffsetInContainer(container, range.endContainer, range.endOffset)
    
    console.log('[useTextSelection] Calculated offsets - start:', start, 'end:', end)

    if (start === -1 || end === -1) {
      console.log('[useTextSelection] Invalid offsets')
      return null
    }

    // 允许 start === end 的情况（光标位置），但检查选择的文本
    const selectedText = selection.toString()
    if (start === end && !selectedText) {
      console.log('[useTextSelection] Empty selection (no text selected)')
      return null
    }

    const result = {
      start: Math.min(start, end),
      end: Math.max(start, end),
      text: selectedText
    }
    
    console.log('[useTextSelection] Returning selection:', result)
    return result
  }

  /**
   * 计算节点在容器中的偏移量
   * @param container 容器元素
   * @param node 目标节点
   * @param offset 节点内偏移量
   * @returns 在容器中的绝对偏移量
   */
  const getOffsetInContainer = (
    container: HTMLElement,
    node: Node,
    offset: number
  ): number => {
    let currentOffset = 0
    const walker = document.createTreeWalker(
      container,
      NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT,
      null
    )

    let currentNode: Node | null = walker.nextNode()

    while (currentNode) {
      if (currentNode === node) {
        return currentOffset + offset
      }

      if (currentNode.nodeType === Node.TEXT_NODE) {
        currentOffset += currentNode.textContent?.length || 0
      } else if (currentNode.nodeType === Node.ELEMENT_NODE) {
        const element = currentNode as HTMLElement
        // 如果是span元素，检查data-offset属性
        if (element.tagName === 'SPAN' && element.hasAttribute('data-offset')) {
          const dataOffset = parseInt(element.getAttribute('data-offset') || '0', 10)
          if (currentNode === node) {
            return dataOffset + offset
          }
        }
      }

      currentNode = walker.nextNode()
    }

    return -1
  }

  /**
   * 验证偏移量是否有效
   * @param text 原始文本
   * @param start 起始偏移量
   * @param end 结束偏移量
   * @returns 是否有效
   */
  const validateOffset = (text: string, start: number, end: number): boolean => {
    if (start < 0 || end > text.length || start >= end) {
      return false
    }
    return true
  }

  /**
   * 修正偏移量（如果文本略有变化）
   * @param text 原始文本
   * @param entityText 实体文本
   * @param start 起始偏移量
   * @param end 结束偏移量
   * @returns 修正后的偏移量，如果无法修正则返回null
   */
  const correctOffset = (
    text: string,
    entityText: string,
    start: number,
    end: number
  ): { start: number; end: number } | null => {
    // 首先验证原始偏移量
    if (validateOffset(text, start, end) && text.substring(start, end) === entityText) {
      return { start, end }
    }

    // 尝试在附近查找匹配
    const searchRange = 50 // 搜索范围
    const searchStart = Math.max(0, start - searchRange)
    const searchEnd = Math.min(text.length, end + searchRange)
    const searchText = text.substring(searchStart, searchEnd)

    const index = searchText.indexOf(entityText)
    if (index !== -1) {
      const newStart = searchStart + index
      const newEnd = newStart + entityText.length
      return { start: newStart, end: newEnd }
    }

    // 无法修正
    return null
  }

  /**
   * 计算两个文本范围是否重叠
   * @param range1 范围1
   * @param range2 范围2
   * @returns 是否重叠
   */
  const hasOverlap = (
    range1: { start: number; end: number },
    range2: { start: number; end: number }
  ): boolean => {
    return !(range1.end <= range2.start || range1.start >= range2.end)
  }

  /**
   * 高亮显示文本范围
   * @param container 容器元素
   * @param start 起始偏移量
   * @param end 结束偏移量
   */
  const highlightRange = (container: HTMLElement, start: number, end: number) => {
    const spans = container.querySelectorAll('span[data-offset]')
    spans.forEach((span) => {
      const offset = parseInt(span.getAttribute('data-offset') || '0', 10)
      if (offset >= start && offset < end) {
        span.classList.add('highlighted')
      } else {
        span.classList.remove('highlighted')
      }
    })
  }

  /**
   * 清除所有高亮
   * @param container 容器元素
   */
  const clearHighlight = (container: HTMLElement) => {
    const spans = container.querySelectorAll('span.highlighted')
    spans.forEach((span) => {
      span.classList.remove('highlighted')
    })
  }

  return {
    getSelection,
    getOffsetInContainer,
    validateOffset,
    correctOffset,
    hasOverlap,
    highlightRange,
    clearHighlight
  }
}
