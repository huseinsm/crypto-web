<script>
  let { data, step = -1 } = $props()
  const order = $derived(data.col_order ?? [])
  const active = $derived(order.length ? (step < 0 ? order.length - 1 : Math.min(step, order.length - 1)) : -1)
  const keyChars = $derived((data.key.key ?? '').split(''))
  const readCols = $derived(order.slice(0, active + 1))
</script>

<div class="space-y-4">
  <div class="text-xs uppercase tracking-[0.14em] text-brand font-semibold">
    {data.mode === 'encrypt' ? 'Enkripsi' : 'Dekripsi'} · kunci: {data.key.key} ·
    {data.ncol} kolom × {data.nrow} baris
  </div>

  <!-- kepala kolom -->
  <div class="overflow-x-auto">
    <div class="inline-block">
      <div class="flex gap-1 mb-1">
        {#each keyChars as kc, c}
          <div class="w-9 text-center">
            <div class="text-[10px] text-ink-3">kolom {c}</div>
            <div class="w-9 h-9 grid place-items-center rounded font-mono font-semibold border border-stone-300 bg-stone-100 text-stone-600">{kc}</div>
            <div class="text-[10px] text-ink-3">rank {data.key_rank[c]}</div>
          </div>
        {/each}
      </div>
      <!-- matriks -->
      {#each data.grid as row, r}
        <div class="flex gap-1 mb-1">
          {#each row as cell, c}
            <div class="w-9 h-9 grid place-items-center rounded font-mono text-sm border
              {readCols.includes(c) ? 'bg-gold-soft border-gold/40 text-gold' : 'bg-paper border-line text-ink-2'}">
              {cell}
            </div>
          {/each}
        </div>
      {/each}
    </div>
  </div>

  <!-- urutan baca kolom -->
  <div>
    <div class="text-xs uppercase tracking-[0.14em] text-ink-3 font-semibold mb-2">Urutan kolom dibaca</div>
    <div class="flex flex-wrap gap-2">
      {#each order as c, i}
        <div class="px-3 py-1.5 rounded font-mono text-sm border
          {i <= active ? 'bg-brand-soft border-brand/40 text-brand-deep' : 'bg-paper border-line text-ink-3'}">
          #{i + 1} → kolom {c} ({keyChars[c]})
        </div>
      {/each}
    </div>
  </div>

  {#if data.note}
    <div class="text-xs text-ink-2 border-l-2 border-brand/40 pl-3">{data.note}</div>
  {/if}
</div>
