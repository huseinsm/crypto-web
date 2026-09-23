<script>
  let { data, step = -1 } = $props()
  const steps = $derived(data.steps ?? [])
  const active = $derived(steps.length ? (step < 0 ? steps.length - 1 : Math.min(step, steps.length - 1)) : -1)
  const cur = $derived(active >= 0 ? steps[active] : null)

  // kumpulkan sel yang disorot pada langkah aktif
  const hl = $derived.by(() => {
    if (!cur) return []
    const p = cur.pos.map(o => `${o.r}-${o.c}`)
    const e = [cur.cipher[0], cur.cipher[1]]
    return p
  })
  const outCells = $derived.by(() => {
    if (!cur) return []
    return [cur.cipher[0], cur.cipher[1]]
  })
</script>

<div class="space-y-4">
  <div class="text-xs uppercase tracking-widest text-cyan-400/80">
    {data.mode === 'encrypt' ? 'Enkripsi' : 'Dekripsi'} · kunci: {data.key.key} · J digabung ke I
  </div>

  <div class="grid lg:grid-cols-2 gap-6">
    <!-- MATRIKS 5x5 -->
    <div>
      <div class="text-xs uppercase tracking-widest text-slate-400 mb-2">Matriks 5×5</div>
      <div class="inline-grid grid-cols-5 gap-1.5">
        {#each data.matrix as row, r}
          {#each row as cell, c}
            {@const key = `${r}-${c}`}
            <div class="w-11 h-11 grid place-items-center rounded-lg font-mono text-lg border transition
              {hl.includes(key) ? 'bg-cyan-500/25 border-cyan-400 text-cyan-100 glow' : ''}
              {outCells.includes(cell) && !hl.includes(key) ? 'bg-amber-500/20 border-amber-400/60 text-amber-200' : ''}
              {!hl.includes(key) && !(outCells.includes(cell) && !hl.includes(key)) ? 'bg-slate-800/50 border-slate-700 text-slate-300' : ''}">
              {cell}
            </div>
          {/each}
        {/each}
      </div>
      <div class="mt-3 flex gap-4 text-[11px] text-slate-400">
        <span class="flex items-center gap-1"><span class="w-3 h-3 rounded bg-cyan-500/40 border border-cyan-400"></span> huruf asal</span>
        <span class="flex items-center gap-1"><span class="w-3 h-3 rounded bg-amber-500/40 border border-amber-400"></span> hasil</span>
      </div>
    </div>

    <!-- LANGKAH PER PASANGAN -->
    <div>
      <div class="text-xs uppercase tracking-widest text-slate-400 mb-2">Langkah per pasangan</div>
      <div class="space-y-1.5 max-h-72 overflow-auto pr-1">
        {#each steps as s, i}
          <div class="flex items-center gap-3 px-3 py-2 rounded-lg border font-mono text-sm
            {i === active ? 'border-cyan-400/60 bg-cyan-500/10' : 'border-slate-800 bg-slate-900/40'}">
            <span class="text-slate-400 w-14">{s.pair}</span>
            <span class="text-slate-500 text-xs flex-1">{s.rule}</span>
            <span class="text-amber-300 font-bold">{i <= active ? s.cipher : '?'}</span>
          </div>
        {/each}
      </div>
    </div>
  </div>

  {#if cur}
    <div class="text-sm text-slate-300 font-mono border-l-2 border-cyan-500/40 pl-3">
      {cur.pair[0]} di ({cur.pos[0].r},{cur.pos[0].c}) · {cur.pair[1]} di ({cur.pos[1].r},{cur.pos[1].c})
      — <span class="text-cyan-300">{cur.rule}</span> → <span class="text-amber-300">{cur.cipher}</span>
    </div>
  {/if}

  <div class="text-xs text-slate-400 font-mono">
    Teks disiapkan: <span class="text-slate-200">{data.prepared}</span>
    {#if data.input_clean !== data.prepared}
      <span class="text-slate-500">(disisipkan X untuk huruf kembar / ganjil)</span>
    {/if}
  </div>
</div>
