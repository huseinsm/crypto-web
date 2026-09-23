<script>
  let { data, step = -1 } = $props()
  const steps = $derived(data.steps ?? [])
  const active = $derived(steps.length ? (step < 0 ? steps.length - 1 : Math.min(step, steps.length - 1)) : -1)
  const alphabet = $derived(data.alphabet)

  const marks = $derived(steps.slice(0, active + 1).map(s => `${s.p_index}-${s.k_index}`))
  const cur = $derived(active >= 0 ? steps[active] : null)
</script>

<div class="space-y-4">
  <div class="text-xs uppercase tracking-[0.14em] text-brand font-semibold">
    {data.mode === 'encrypt' ? 'Enkripsi' : 'Dekripsi'} · kunci: {data.key.key}
  </div>

  <!-- baris pesan + baris kunci -->
  <div class="overflow-x-auto pb-2">
    <div class="flex gap-1.5">
      {#each steps as s, i}
        <div class="flex flex-col items-center gap-1 shrink-0">
          <div class="text-[10px] text-ink-3 font-mono">{i}</div>
          <div class="w-8 h-8 grid place-items-center rounded font-mono text-sm border
            {i <= active ? 'bg-brand-soft border-brand/40 text-brand-deep' : 'bg-paper border-line text-ink-3'}">{s.char}</div>
          <div class="w-8 h-8 grid place-items-center rounded font-mono text-xs border
            {i <= active ? 'bg-stone-100 border-stone-300 text-stone-600' : 'bg-paper border-line text-ink-3'}">{s.key_char}</div>
          <div class="text-[10px] text-ink-3 font-mono">↓</div>
          <div class="w-8 h-8 grid place-items-center rounded font-mono text-sm border
            {i <= active ? 'bg-gold-soft border-gold/40 text-gold' : 'bg-paper border-line text-ink-3'}">{i <= active ? s.cipher : '?'}</div>
        </div>
      {/each}
    </div>
  </div>

  {#if cur}
    <div class="text-sm text-ink-2 font-mono">
      ({cur.p_index} + {cur.k_index}) mod 26 = <span class="text-gold font-semibold">{cur.new_index}</span>
      → <span class="text-gold">{cur.cipher}</span>
    </div>
  {/if}

  <!-- Tabula Recta -->
  <details class="group">
    <summary class="cursor-pointer text-xs uppercase tracking-[0.14em] text-ink-3 hover:text-brand font-semibold select-none">
      Tabula Recta (tabel Vigenère 26×26)
    </summary>
    <div class="mt-3 overflow-auto max-h-72 rounded-lg border border-line">
      <table class="border-collapse text-[10px] font-mono">
        <thead>
          <tr>
            <th class="sticky left-0 top-0 bg-surface p-1 border border-line"></th>
            {#each alphabet as c}
              <th class="sticky top-0 bg-surface p-1 border border-line text-stone-500">{c}</th>
            {/each}
          </tr>
        </thead>
        <tbody>
          {#each data.tabula_recta as row, r}
            <tr>
              <th class="sticky left-0 bg-surface p-1 border border-line text-brand">{alphabet[r]}</th>
              {#each row as cell, c}
                {@const key = `${r}-${c}`}
                <td class="p-1 border border-line text-center
                  {marks.includes(key) ? 'bg-gold text-white font-semibold' : 'text-ink-3'}">{cell}</td>
              {/each}
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </details>
</div>
