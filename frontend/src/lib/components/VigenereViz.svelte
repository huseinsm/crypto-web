<script>
  let { data, step = -1 } = $props()
  const steps = $derived(data.steps ?? [])
  const active = $derived(steps.length ? (step < 0 ? steps.length - 1 : Math.min(step, steps.length - 1)) : -1)
  const alphabet = $derived(data.alphabet)

  // sel Tabula Recta yang perlu disorot
  const marks = $derived(
    steps.slice(0, active + 1).map(s => `${s.p_index}-${s.k_index}`)
  )
  const cur = $derived(active >= 0 ? steps[active] : null)
</script>

<div class="space-y-4">
  <div class="text-xs uppercase tracking-widest text-cyan-400/80">
    {data.mode === 'encrypt' ? 'Enkripsi' : 'Dekripsi'} · kunci: {data.key.key} · panjang kunci {data.key.key.length}
  </div>

  <!-- baris pesan + baris kunci -->
  <div class="overflow-x-auto pb-2">
    <div class="flex gap-1.5">
      {#each steps as s, i}
        <div class="flex flex-col items-center gap-1 shrink-0">
          <div class="text-[10px] text-slate-500 font-mono">{i}</div>
          <div class="w-8 h-8 grid place-items-center rounded font-mono text-sm border
            {i <= active ? 'bg-cyan-500/15 border-cyan-400/50 text-cyan-200' : 'bg-slate-800/50 border-slate-700 text-slate-600'}
            {i === active ? 'glow' : ''}">{s.char}</div>
          <div class="w-8 h-8 grid place-items-center rounded font-mono text-xs border
            {i <= active ? 'bg-violet-500/15 border-violet-400/50 text-violet-200' : 'bg-slate-800/50 border-slate-700 text-slate-600'}">{s.key_char}</div>
          <div class="text-[10px] text-slate-600 font-mono">↓</div>
          <div class="w-8 h-8 grid place-items-center rounded font-mono text-sm border
            {i <= active ? 'bg-amber-500/15 border-amber-400/50 text-amber-200' : 'bg-slate-800/50 border-slate-700 text-slate-600'}
            {i === active ? 'pop' : ''}">{i <= active ? s.cipher : '?'}</div>
        </div>
      {/each}
    </div>
  </div>

  {#if cur}
    <div class="text-sm text-slate-300 font-mono">
      ({cur.p_index} + {cur.k_index}) mod 26 = <span class="text-amber-300 font-bold">{cur.new_index}</span>
      → <span class="text-amber-300">{cur.cipher}</span>
    </div>
  {/if}

  <!-- Tabula Recta -->
  <details class="group">
    <summary class="cursor-pointer text-xs uppercase tracking-widest text-slate-400 hover:text-cyan-300 select-none">
      Tabula Recta (tabel Vigenère 26×26) — baris = huruf pesan, kolom = huruf kunci
    </summary>
    <div class="mt-3 overflow-auto max-h-72 rounded-lg border border-slate-800">
      <table class="border-collapse text-[10px] font-mono">
        <thead>
          <tr>
            <th class="sticky left-0 top-0 bg-slate-900 p-1 border border-slate-800"></th>
            {#each alphabet as c}
              <th class="sticky top-0 bg-slate-900 p-1 border border-slate-800 text-violet-300">{c}</th>
            {/each}
          </tr>
        </thead>
        <tbody>
          {#each data.tabula_recta as row, r}
            <tr>
              <th class="sticky left-0 bg-slate-900 p-1 border border-slate-800 text-cyan-300">{alphabet[r]}</th>
              {#each row as cell, c}
                {@const key = `${r}-${c}`}
                <td class="p-1 border border-slate-800 text-center
                  {marks.includes(key) ? 'bg-amber-400/80 text-slate-900 font-bold' : 'text-slate-400'}">{cell}</td>
              {/each}
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </details>
</div>
