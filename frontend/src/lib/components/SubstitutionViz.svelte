<script>
  let { data, step = -1 } = $props()
  const steps = $derived(data.steps ?? [])
  const active = $derived(steps.length ? (step < 0 ? steps.length - 1 : Math.min(step, steps.length - 1)) : -1)
  const cur = $derived(active >= 0 ? steps[active] : null)

  const plain = $derived(data.plain_alphabet.split(''))
  const cipher = $derived(data.cipher_alphabet.split(''))
  const hiPlain = $derived(cur ? cur.char : null)
</script>

<div class="space-y-5">
  <div class="text-xs uppercase tracking-widest text-cyan-400/80">
    {data.mode === 'encrypt' ? 'Enkripsi' : 'Dekripsi'} · kata kunci: {data.key.key}
  </div>

  <!-- tabel substitusi 26 kolom -->
  <div class="overflow-x-auto">
    <div class="inline-block">
      <div class="text-[10px] uppercase tracking-widest text-cyan-300 mb-1">Alfabet asli (plain)</div>
      <div class="flex gap-1 mb-2">
        {#each plain as ch, i}
          <div class="w-8 h-8 grid place-items-center rounded font-mono text-sm border
            {ch === hiPlain ? 'bg-cyan-500/25 border-cyan-400 text-cyan-100 glow' : 'bg-slate-800/50 border-slate-700 text-slate-300'}">
            {ch}
          </div>
        {/each}
      </div>
      <div class="text-center text-slate-600 text-xs mb-1">↓ substitusi ↓</div>
      <div class="text-[10px] uppercase tracking-widest text-amber-300 mb-1">Alfabet cipher</div>
      <div class="flex gap-1">
        {#each cipher as ch, i}
          <div class="w-8 h-8 grid place-items-center rounded font-mono text-sm border
            {cur && cur.cipher === ch ? 'bg-amber-500/25 border-amber-400 text-amber-100 pop' : 'bg-slate-800/50 border-slate-700 text-amber-200/70'}">
            {ch}
          </div>
        {/each}
      </div>
    </div>
  </div>

  <!-- peta A->Z dll -->
  <details>
    <summary class="cursor-pointer text-xs uppercase tracking-widest text-slate-400 hover:text-cyan-300 select-none">
      Lihat tabel pemetaan lengkap
    </summary>
    <div class="mt-3 grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-1.5 font-mono text-xs">
      {#each plain as ch, i}
        <div class="px-2 py-1 rounded border border-slate-800 bg-slate-900/50">
          <span class="text-cyan-300">{ch}</span>
          <span class="text-slate-600 mx-1">→</span>
          <span class="text-amber-300">{cipher[i]}</span>
        </div>
      {/each}
    </div>
  </details>

  <!-- langkah huruf -->
  {#if cur}
    <div class="text-sm text-slate-300 font-mono border-l-2 border-cyan-500/40 pl-3">
      huruf ke-{cur.i}: <span class="text-cyan-300">{cur.char}</span>
      → <span class="text-amber-300 font-bold">{cur.cipher}</span>
    </div>
  {/if}
  <div class="text-sm font-mono text-slate-400">
    Hasil: <span class="text-amber-200">{data.result}</span>
  </div>
</div>
