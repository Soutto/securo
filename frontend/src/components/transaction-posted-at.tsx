import { transactionPostedAtParts } from '@/lib/format'
import { cn } from '@/lib/utils'

export function TransactionPostedAt({
  date,
  occurredAt,
  locale,
  stacked = false,
  className,
}: {
  date: string
  occurredAt?: string | null
  locale?: string
  stacked?: boolean
  className?: string
}) {
  const { dateLabel, timeLabel } = transactionPostedAtParts(date, occurredAt, locale)
  if (!timeLabel) {
    return <span className={cn('tabular-nums', className)}>{dateLabel}</span>
  }
  if (stacked) {
    return (
      <span className={cn('flex flex-col gap-0.5 leading-tight tabular-nums', className)}>
        <span>{dateLabel}</span>
        <span className="text-[11px] opacity-80">{timeLabel}</span>
      </span>
    )
  }
  return (
    <span className={cn('tabular-nums', className)}>
      {dateLabel} {timeLabel}
    </span>
  )
}
