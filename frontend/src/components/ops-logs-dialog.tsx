import { useTranslation } from 'react-i18next'
import {
  AlertTriangle,
  CheckCircle2,
  HardDriveDownload,
  RefreshCw,
  ScrollText,
  XCircle,
} from 'lucide-react'
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { useOpsLogs } from '@/hooks/use-ops-logs'
import { cn } from '@/lib/utils'

interface OpsLogsDialogProps {
  open: boolean
  onClose: () => void
}

export function OpsLogsDialog({ open, onClose }: OpsLogsDialogProps) {
  const { t, i18n } = useTranslation()
  const { data, isFetching } = useOpsLogs()
  const items = data?.items ?? []
  const hasFailure = data?.has_failure ?? false

  return (
    <Dialog open={open} onOpenChange={(v) => !v && onClose()}>
      <DialogContent className="sm:max-w-lg">
        <DialogHeader>
          <div className="flex items-center justify-between gap-3 pr-6">
            <DialogTitle>{t('opsLogs.title')}</DialogTitle>
            <span className="inline-flex items-center gap-1.5 rounded-full border bg-muted/60 px-2.5 py-1 text-[11px] font-medium text-muted-foreground">
              <ScrollText size={12} />
              <span>{t('opsLogs.subtitle')}</span>
            </span>
          </div>
        </DialogHeader>

        <div className="space-y-4">
          {hasFailure ? (
            <div className="flex items-start gap-2.5 rounded-lg border border-rose-500/30 bg-rose-500/10 px-3.5 py-3 text-sm font-medium text-rose-700 dark:text-rose-400">
              <AlertTriangle size={18} className="shrink-0 mt-0.5" />
              <span>{t('opsLogs.failureBanner')}</span>
            </div>
          ) : items.length > 0 ? (
            <div className="flex items-center gap-2.5 rounded-lg border border-emerald-500/30 bg-emerald-500/10 px-3.5 py-3 text-sm font-medium text-emerald-700 dark:text-emerald-400">
              <CheckCircle2 size={18} className="shrink-0" />
              <span>{t('opsLogs.okBanner')}</span>
            </div>
          ) : null}

          {isFetching && items.length === 0 ? (
            <div className="rounded-lg border bg-muted/40 px-3.5 py-3 text-sm text-muted-foreground">
              {t('opsLogs.loading')}
            </div>
          ) : items.length === 0 ? (
            <div className="rounded-lg border bg-muted/40 px-3.5 py-3 text-sm text-muted-foreground">
              {t('opsLogs.empty')}
            </div>
          ) : (
            <ul className="space-y-2">
              {items.map((item) => {
                const KindIcon = item.kind === 'backup' ? HardDriveDownload : RefreshCw
                return (
                  <li
                    key={item.id}
                    className={cn(
                      'flex items-start gap-2.5 rounded-lg border px-3.5 py-2.5',
                      item.success
                        ? 'bg-muted/30'
                        : 'border-rose-500/30 bg-rose-500/5',
                    )}
                  >
                    {item.success ? (
                      <CheckCircle2
                        size={16}
                        className="shrink-0 mt-0.5 text-emerald-600 dark:text-emerald-400"
                      />
                    ) : (
                      <XCircle
                        size={16}
                        className="shrink-0 mt-0.5 text-rose-600 dark:text-rose-400"
                      />
                    )}
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-1.5 text-sm font-medium">
                        <KindIcon size={13} className="text-muted-foreground" />
                        <span>
                          {item.kind === 'backup'
                            ? t('opsLogs.kindBackup')
                            : t('opsLogs.kindUpdate')}
                        </span>
                        <span className="text-[11px] font-normal text-muted-foreground tabular-nums">
                          {new Date(item.created_at).toLocaleString(i18n.language, {
                            dateStyle: 'short',
                            timeStyle: 'short',
                          })}
                        </span>
                      </div>
                      {item.message && (
                        <p className="mt-0.5 text-xs text-muted-foreground break-words">
                          {item.message}
                        </p>
                      )}
                    </div>
                  </li>
                )
              })}
            </ul>
          )}
        </div>

        <DialogFooter>
          <Button type="button" variant="outline" onClick={onClose}>
            {t('common.close')}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
