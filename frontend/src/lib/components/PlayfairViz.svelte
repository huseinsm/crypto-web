<script>
  let { data, step = -1 } = $props()
  const steps = $derived(data.steps ?? [])
  const active = $derived(steps.length ? (step < 0 ? steps.length - 1 : Math.min(step, steps.length - 1)) : -1)
  const cur = $derived(active >= 0 ? steps[active] : null)

  // posisi huruf asal (pasangan) yang disorot
  const hl = $derived(cur ? cur.pos.map(o => `${o.r}-${o.c}`) : [])
  // huruf hasil (cipher) yang disorot di matriks
  const outCells = $derived(cur ? [cur.cipher[0], cur.cipher[1]] : [])
</script>

<div class="space-y-4">
  <div class="text-xs uppercase tracking-[0.14em] text-brand font-semibold">
    {data.mode === 'encrypt' ? 'Enkripsi' : 'Dekripsi'} · kunci: {data.key.key} · J digabung ke I
  </div>

  <div class="grid lg:grid-cols-2 gap-6">
    <!-- MATRIKS 5x5 -->
    <div>
      <div class="text-xs uppercase tracking-[0.14em] text-ink-3 font-semibold mb-2">Matriks 5×5</div>
      <div class="inline-grid grid-cols-5 gap-1.5">
        {#each data.matrix as row, r}
          {#each row as cell, c}
            {@const key = `${r}-${c}`}
            {@const isHL = hl.includes(key)}
            {@const isOut = !isHL && outCells.includes(cell)}
            <div class="w-11 h-11 grid place-items-center rounded-md font-mono text-lg border transition
              {isHL ? 'bg-brand text-white border-brand' : ''}
              {isOut ? 'bg-gold-soft border-gold/50 text-gold' : ''}
              {!isHL && !isOut ? 'bg-paper border-line text-ink-2' : ''}">
              {cell}
            </div>
          {/each}
        {/each}
      </div>
      <div class="mt-3 flex gap-4 text-[11px] text-ink-2">
        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded bg-brand"></span> huruf asal</span>
        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded bg-gold-soft border border-gold/50"></span> hasil</span>
      </div>
    </div>

    <!-- LANGKAH PER PASANGAN -->
    <div>
      <div class="text-xs uppercase tracking-[0.14em] text-ink-3 font-semibold mb-2">Langkah per pasangan</div>
      <div class="space-y-1.5 max-h-72 overflow-auto pr-1">
        {#each steps as s, i}
          <div class="flex items-center gap-3 px-3 py-2 rounded-lg border font-mono text-sm
            {i === active ? 'border-brand/40 bg-brand-soft' : 'border-line bg-paper'}">
            <span class="text-ink-2 w-14">{s.pair}</span>
            <span class="text-ink-3 text-xs flex-1">{s.rule}</span>
            <span class="text-gold font-semibold">{i <= active ? s.cipher : '?'}</span>
          </div>
        {/each}
      </div>
    </div>
  </div>

  {#if cur}
    <div class="text-sm text-ink-2 font-mono border-l-2 border-brand/40 pl-3">
      {cur.pair[0]} di ({cur.pos[0].r},{cur.pos[0].c}) · {cur.pair[1]} di ({cur.pos[1].r},{cur.pos[1].c})
      — <span class="text-brand">{cur.rule}</span> → <span class="text-gold">{cur.cipher}</span>
    </div>
  {/if}

  <div class="text-xs text-ink-3 font-mono">
    Teks disiapkan: <span class="text-ink">{data.prepared}</span>
    {#if data.input_clean !== data.prepared}
      <span class="text-ink-3">(disisipkan X untuk huruf kembar / ganjil)</span>
    {/if}
  </div>
</div>
