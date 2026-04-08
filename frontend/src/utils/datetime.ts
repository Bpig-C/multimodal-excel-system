/**
 * 日期时间工具函数
 *
 * 背景：后端使用 datetime.utcnow() 存储 UTC 时间，但序列化时通过
 * .isoformat() 输出的字符串不带时区后缀（如 "2026-03-04T05:52:59"）。
 * 浏览器解析无时区后缀的字符串时，会将其当作本地时间而非 UTC，导致
 * 在 UTC+8 环境下时间显示比实际早 8 小时。
 *
 * 解决方案：解析前统一追加 "Z"，告知浏览器这是 UTC 时间，浏览器会
 * 自动转换为本地时间显示。
 */

import { format, formatDistanceToNow } from 'date-fns'
import { zhCN } from 'date-fns/locale'

/**
 * 将后端返回的 UTC 时间字符串解析为 Date 对象（自动补 Z 后缀）
 */
export function parseUTCDate(dateString: string): Date {
  if (!dateString) return new Date(NaN)
  // 若已有时区信息（Z 或 +XX:XX），直接解析；否则追加 Z 表示 UTC
  const normalized =
    dateString.endsWith('Z') || /[+-]\d{2}:\d{2}$/.test(dateString)
      ? dateString
      : dateString + 'Z'
  return new Date(normalized)
}

/**
 * 格式化为 "yyyy-MM-dd HH:mm:ss" 本地时间字符串
 */
export function formatDateTime(dateString: string | null | undefined): string {
  if (!dateString) return '-'
  try {
    return format(parseUTCDate(dateString), 'yyyy-MM-dd HH:mm:ss')
  } catch {
    return dateString
  }
}

/**
 * 格式化为 "yyyy-MM-dd HH:mm" 本地时间字符串
 */
export function formatDateTimeShort(dateString: string | null | undefined): string {
  if (!dateString) return '-'
  try {
    return format(parseUTCDate(dateString), 'yyyy-MM-dd HH:mm')
  } catch {
    return dateString as string
  }
}

/**
 * 格式化为相对时间（如 "3 分钟前"）
 */
export function formatDateRelative(dateString: string | null | undefined): string {
  if (!dateString) return '-'
  try {
    return formatDistanceToNow(parseUTCDate(dateString), {
      addSuffix: true,
      locale: zhCN
    })
  } catch {
    return dateString as string
  }
}
