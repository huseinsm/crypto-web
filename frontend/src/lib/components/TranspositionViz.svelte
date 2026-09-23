<script>
  let { data, step = -1 } = $props()
  const order = $derived(data.col_order ?? [])
  const active = $derived(order.length ? (step < 0 ? order.length - 1 : Math.min(step, order.length - 1)) : -1)

  // huruf kunci + ranking
  const keyChars = $derived((data.key.key ?? '').split(''))
  // kolom yang sudah dibaca
  const readCols = $derived(order.slice(0, active + 1))
</script>

<div class="space-y-4">
  <div class="text-xs uppercase tracking-widest text-cyan-400/80">
    {data.mode === 'encrypt' ? 'Enkripsi' : 'Dekripsi'} · kunci: {data.key.key} ·
    {data.ncol} kolom × {data.nrow} baris
  </div>

  <!-- kepala kolom -->
  <div class="overflow-x-auto">
    <div class="inline-block">
      <div class="flex gap-1 mb-1">
        {#each keyChars as kc, c}
          <div class="w-9 text-center">
            <div class="text-[10px] text-slate-500">kolom {c}</div>
            <div class="w-9 h-9 grid place-items-center rounded font-mono font-bold border
              border-violet-400/50 bg-violet-500/15 text-violet-200">{kc}</div>
            <div class="text-[10px] text-slate-500">rank {data.key_rank[c]}</div>
          </div>
        {/each}
      </div>
      <!-- matriks -->
      {#each data.grid as row, r}
        <div class="flex gap-1 mb-1">
          {#each row as cell, c}
            <div class="w-9 h-9 grid place-items-center rounded font-mono text-sm border
              {readCols.includes(c) ? 'bg-amber-500/15 border-amber-400/50 text-amber-200' : 'bg-slate-800/50 border-slate-700 text-slate-400'}">
              {cell}
            </div>
          {/each}
        </div>
      {/each}
    </div>
  </div>

  <!-- urutan baca kolom -->
  <div>
    <div class="text-xs uppercase tracking-widest text-slate-400 mb-2">Urutan kolom dibaca</div>
    <div class="flex flex-wrap gap-2">
      {#each order as c, i}
        <div class="px-3 py-1.5 rounded font-mono text-sm border
          {i <= active ? 'bg-cyan-500/15 border-cyan-400/50 text-cyan-200' : 'bg-slate-800/50 border-slate-700 text-slate-500'}
          {i === active ? 'pop' : ''}">
          #{i + 1} → kolom {c} ({keyChars[c]})
        </div>
      {/each}
    </div>
  </div>

  {#if data.note}
    <div class="text-xs text-slate-400 border-l-2 border-cyan-500/40 pl-3">{data.note}</div>
  {/if}
</div>
