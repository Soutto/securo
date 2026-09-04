import { useQuery } from '@tanstack/react-query'
import { opsLogs } from '@/lib/api'

export function useOpsLogs() {
  return useQuery({
    queryKey: ['ops-logs'],
    queryFn: opsLogs.list,
    staleTime: 30_000,
    refetchOnWindowFocus: true,
  })
}
